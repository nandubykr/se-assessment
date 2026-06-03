#!/usr/bin/env python3
"""
API Exploration Script
- Discovers available endpoints
- Tests authentication
- Checks rate limits
- Probes for data structure
- Tracks remaining time
"""

import requests
import json
import hashlib
from datetime import datetime
from config import BASE_URL, get_auth_headers, ENDPOINTS_TO_EXPLORE

# Session for connection pooling
session = requests.Session()


def print_response(title, response):
    """Pretty print response details."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    print(f"URL: {response.url}")
    
    # Print relevant headers
    relevant_headers = [
        'content-type',
        'content-length',
        'ratelimit-limit',
        'ratelimit-remaining',
        'ratelimit-reset',
        'retry-after',
        'x-clock-started',
    ]
    print("\nHeaders:")
    for header in relevant_headers:
        if header in response.headers:
            print(f"  {header}: {response.headers[header]}")
    
    # Print body
    print("\nBody:")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except json.JSONDecodeError:
        print(response.text[:500])


def get_remaining_time():
    """Check remaining time in assessment window."""
    headers = get_auth_headers()
    endpoint = f"{BASE_URL}/api/v1/time"
    
    try:
        response = session.get(endpoint, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            remaining = data.get('remaining_seconds', 'unknown')
            print(f"⏱ Remaining Time: {remaining} seconds")
            return remaining
        else:
            print(f"Could not fetch remaining time: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching time: {e}")
        return None


def probe_endpoint(endpoint_path, method="GET", data=None):
    """Probe a single endpoint."""
    url = f"{BASE_URL}{endpoint_path}"
    headers = get_auth_headers()
    
    try:
        if method == "GET":
            response = session.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = session.post(url, headers=headers, json=data, timeout=10)
        
        print_response(f"Endpoint: {endpoint_path}", response)
        
        # Check for rate limit headers
        if 'ratelimit-remaining' in response.headers:
            remaining = response.headers.get('ratelimit-remaining')
            limit = response.headers.get('ratelimit-limit')
            print(f"\nRate Limit: {remaining}/{limit}")
        
        return response
    
    except requests.exceptions.RequestException as e:
        print(f"Error probing {endpoint_path}: {e}")
        return None


def explore_main_endpoints():
    """Explore main known endpoints."""
    print(f"\n[{datetime.now().isoformat()}] Starting API Exploration")
    print("=" * 60)
    
    print("\n1. Checking remaining assessment time...")
    get_remaining_time()
    
    print("\n2. Probing standard endpoints...")
    for endpoint in ENDPOINTS_TO_EXPLORE:
        print(f"\n→ Probing {endpoint}")
        probe_endpoint(endpoint)
        
        # Check time after each probe
        time_left = get_remaining_time()
        if time_left and isinstance(time_left, int) and time_left < 300:
            print("\n⚠ WARNING: Less than 5 minutes remaining!")
            break


def probe_submission_endpoint():
    """Test the submission endpoint to understand format."""
    print(f"\n\n3. Testing submission endpoint format...")
    
    # Try an invalid submission to see the error format
    headers = get_auth_headers()
    url = f"{BASE_URL}/api/v1/submit"
    
    payload = {
        "type": "test",
        "value": "test_value",
        "notes": "Testing submission format"
    }
    
    try:
        response = session.post(url, headers=headers, json=payload, timeout=10)
        print_response("Submission Endpoint Test", response)
        
        # Parse error to understand valid types
        if response.status_code >= 400:
            data = response.json()
            print(f"\nError indicates valid submission types...")
            if 'valid_types' in data:
                print(f"Valid types: {data['valid_types']}")
    
    except Exception as e:
        print(f"Error: {e}")


def save_exploration_results(filename="exploration_results.json"):
    """Save exploration results for later reference."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "base_url": BASE_URL,
        "endpoints_probed": ENDPOINTS_TO_EXPLORE,
        "status": "exploration_in_progress",
    }
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to {filename}")


if __name__ == "__main__":
    try:
        explore_main_endpoints()
        probe_submission_endpoint()
        save_exploration_results()
        
        print(f"\n\n{'='*60}")
        print("Exploration Complete!")
        print(f"{'='*60}")
    
    except KeyboardInterrupt:
        print("\n\nExploration interrupted by user.")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
