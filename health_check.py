#!/usr/bin/env python3
"""
Health Check Script
- Verifies API connectivity
- Does NOT start the 3-hour clock (unauthenticated)
- Safe to run multiple times
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://ca-seassessment-api-dev.happywater-190f264d.northcentralus.azurecontainerapps.io"
HEALTH_ENDPOINT = f"{BASE_URL}/api/v1/health"


def check_health():
    """Check API health without authentication."""
    print(f"[{datetime.now().isoformat()}] Checking API health...")
    print(f"URL: {HEALTH_ENDPOINT}\n")

    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}\n")

        try:
            data = response.json()
            print(f"Response Body:\n{json.dumps(data, indent=2)}")
        except json.JSONDecodeError:
            print(f"Response Body (raw):\n{response.text}")

        if response.status_code == 200:
            print("\n✓ API is healthy and reachable!")
            return True
        else:
            print(f"\n✗ Unexpected status code: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"✗ Error connecting to API: {e}")
        return False


if __name__ == "__main__":
    success = check_health()
    exit(0 if success else 1)
