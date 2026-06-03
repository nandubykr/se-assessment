#!/usr/bin/env python3
"""
Layer 1 - Data Integrity
- Fetch the full dataset efficiently
- Prove byte-level integrity (likely via hash/checksum)
- Submit Layer 1 answer
"""

import requests
import json
import hashlib
from datetime import datetime
from config import BASE_URL, get_auth_headers

session = requests.Session()


def fetch_dataset():
    """Fetch the complete dataset from the API."""
    print(f"\n[{datetime.now().isoformat()}] Fetching dataset...")
    
    headers = get_auth_headers()
    
    # Try common dataset endpoints
    endpoints_to_try = [
        "/api/v1/dataset",
        "/api/v1/data",
        "/api/v1/records",
    ]
    
    for endpoint in endpoints_to_try:
        url = f"{BASE_URL}{endpoint}"
        print(f"\nTrying: {endpoint}")
        
        try:
            response = session.get(url, headers=headers, timeout=30)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f" Successfully fetched from {endpoint}")
                return response.content, endpoint
            
            elif response.status_code == 404:
                print(f"Endpoint not found")
            
            else:
                print(f"Status: {response.status_code}")
                try:
                    print(f"Response: {response.json()}")
                except:
                    print(f"Response: {response.text[:200]}")
        
        except Exception as e:
            print(f"Error: {e}")
    
    return None, None


def calculate_integrity_hash(data):
    """Calculate cryptographic hash of data for integrity verification."""
    hashes = {
        'sha256': hashlib.sha256(data).hexdigest(),
        'sha1': hashlib.sha1(data).hexdigest(),
        'md5': hashlib.md5(data).hexdigest(),
    }
    
    return hashes


def analyze_dataset(data):
    """Analyze the structure and content of the dataset."""
    print(f"\n[{datetime.now().isoformat()}] Analyzing dataset...")
    
    # Try to parse as JSON
    try:
        json_data = json.loads(data)
        print(f"✓ Valid JSON detected")
        print(f"  Type: {type(json_data)}")
        
        if isinstance(json_data, dict):
            print(f"  Keys: {list(json_data.keys())}")
        elif isinstance(json_data, list):
            print(f"  Length: {len(json_data)}")
            if len(json_data) > 0:
                print(f"  First item: {json_data[0]}")
        
        return json_data
    
    except json.JSONDecodeError:
        print(f"Not valid JSON, binary data")
        return None


def submit_layer1_answer(integrity_hash, dataset_endpoint):
    """Submit Layer 1 answer (integrity hash)."""
    print(f"\n[{datetime.now().isoformat()}] Submitting Layer 1 answer...")
    
    headers = get_auth_headers()
    url = f"{BASE_URL}/api/v1/submit"
    
    payload = {
        "type": "layer1",
        "value": integrity_hash,
        "notes": f"Dataset fetched from {dataset_endpoint}, SHA256 hash for integrity verification"
    }
    
    print(f"\nPayload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = session.post(url, headers=headers, json=payload, timeout=10)
        print(f"\nStatus: {response.status_code}")
        
        try:
            result = response.json()
            print(f"Response:\n{json.dumps(result, indent=2)}")
            
            if response.status_code in [200, 201]:
                print("Layer 1 submission accepted!")
                return True
            else:
                print(f"Submission rejected: {result.get('error')}")
                return False
        
        except json.JSONDecodeError:
            print(f"Response: {response.text}")
            return False
    
    except Exception as e:
        print(f"Error submitting: {e}")
        return False


def main():
    """Main Layer 1 workflow."""
    print("="*60)
    print("LAYER 1 - DATA INTEGRITY")
    print("="*60)
    
    # Fetch dataset
    data, endpoint = fetch_dataset()
    
    if data is None:
        print(" Failed to fetch dataset")
        return False
    
    print(f" Dataset size: {len(data)} bytes")
    
    # Calculate integrity hashes
    hashes = calculate_integrity_hash(data)
    print(f"\nIntegrity Hashes:")
    for algorithm, hash_value in hashes.items():
        print(f"  {algorithm}: {hash_value}")
    
    # Analyze dataset
    parsed_data = analyze_dataset(data)
    
    # Save dataset locally for reference
    with open("dataset.bin", "wb") as f:
        f.write(data)
    print(f" Dataset saved to dataset.bin")
    
    # Save hashes
    with open("dataset_hashes.json", "w") as f:
        json.dump(hashes, f, indent=2)
    print(f" Hashes saved to dataset_hashes.json")
    
    # Submit Layer 1 answer
    # Try SHA256 first (most common for integrity)
    success = submit_layer1_answer(hashes['sha256'], endpoint)
    
    return success


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
