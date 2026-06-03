#!/usr/bin/env python3
"""
Layer 2 - Decryption
- Obtain decryption key from platform
- Decrypt the dataset
- Submit Layer 2 answer
"""

import requests
import json
import base64
from datetime import datetime
from cryptography.fernet import Fernet
from config import BASE_URL, get_auth_headers

session = requests.Session()


def fetch_decryption_key():
    """Obtain decryption key from the API."""
    print(f"\n[{datetime.now().isoformat()}] Fetching decryption key...")
    
    headers = get_auth_headers()
    
    # Try common key endpoints
    endpoints_to_try = [
        "/api/v1/key",
        "/api/v1/decrypt-key",
        "/api/v1/decryption-key",
    ]
    
    for endpoint in endpoints_to_try:
        url = f"{BASE_URL}{endpoint}"
        print(f"\nTrying: {endpoint}")
        
        try:
            response = session.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Successfully fetched key from {endpoint}")
                print(f"Response: {json.dumps(data, indent=2)}")
                return data, endpoint
            
            elif response.status_code == 404:
                print(f"  → Endpoint not found")
            
            else:
                print(f"  → Status: {response.status_code}")
        
        except Exception as e:
            print(f"  → Error: {e}")
    
    return None, None


def decrypt_dataset(encrypted_data, key_info):
    """Decrypt dataset using provided key."""
    print(f"\n[{datetime.now().isoformat()}] Decrypting dataset...")
    
    try:
        # Handle different key formats
        if isinstance(key_info, dict):
            if 'key' in key_info:
                key = key_info['key']
            elif 'encryption_key' in key_info:
                key = key_info['encryption_key']
            else:
                print(f"Unknown key format in response")
                return None
        else:
            key = key_info
        
        # Try Fernet decryption
        try:
            # Key might be base64 encoded
            if isinstance(key, str):
                key_bytes = key.encode('utf-8')
            else:
                key_bytes = key
            
            cipher = Fernet(key_bytes)
            decrypted = cipher.decrypt(encrypted_data)
            print(f"✓ Successfully decrypted using Fernet")
            return decrypted
        
        except Exception as e:
            print(f"Fernet decryption failed: {e}")
            print(f"Trying alternative decryption methods...")
            return None
    
    except Exception as e:
        print(f"Error during decryption: {e}")
        return None


def load_encrypted_dataset():
    """Load the encrypted dataset from Layer 1."""
    try:
        with open("dataset.bin", "rb") as f:
            data = f.read()
        print(f"✓ Loaded encrypted dataset ({len(data)} bytes)")
        return data
    
    except FileNotFoundError:
        print(f"✗ dataset.bin not found. Run layer1_integrity.py first.")
        return None


def analyze_decrypted_data(data):
    """Analyze the decrypted data."""
    print(f"\n[{datetime.now().isoformat()}] Analyzing decrypted data...")
    
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
                print(f"  First item: {json.dumps(json_data[0], indent=2)}")
        
        # Save decrypted data
        with open("decrypted_dataset.json", "w") as f:
            json.dump(json_data, f, indent=2)
        print(f"✓ Decrypted data saved to decrypted_dataset.json")
        
        return json_data
    
    except json.JSONDecodeError:
        print(f"  Not JSON, treating as binary/text")
        try:
            text = data.decode('utf-8', errors='ignore')
            print(f"  First 200 chars: {text[:200]}")
            return text
        except:
            return data


def submit_layer2_answer(decryption_confirmation):
    """Submit Layer 2 answer."""
    print(f"\n[{datetime.now().isoformat()}] Submitting Layer 2 answer...")
    
    headers = get_auth_headers()
    url = f"{BASE_URL}/api/v1/submit"
    
    payload = {
        "type": "layer2",
        "value": decryption_confirmation,
        "notes": "Successfully decrypted the dataset using platform-issued key"
    }
    
    print(f"\nPayload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = session.post(url, headers=headers, json=payload, timeout=10)
        print(f"\nStatus: {response.status_code}")
        
        result = response.json()
        print(f"Response:\n{json.dumps(result, indent=2)}")
        
        if response.status_code in [200, 201]:
            print("\n✓ Layer 2 submission accepted!")
            return True
        else:
            print(f"\n✗ Submission rejected")
            return False
    
    except Exception as e:
        print(f"Error submitting: {e}")
        return False


def main():
    """Main Layer 2 workflow."""
    print("="*60)
    print("LAYER 2 - DECRYPTION")
    print("="*60)
    
    # Load encrypted dataset from Layer 1
    encrypted_data = load_encrypted_dataset()
    if encrypted_data is None:
        return False
    
    # Fetch decryption key
    key_info, key_endpoint = fetch_decryption_key()
    if key_info is None:
        print("✗ Failed to fetch decryption key")
        return False
    
    # Decrypt dataset
    decrypted_data = decrypt_dataset(encrypted_data, key_info)
    if decrypted_data is None:
        print("✗ Failed to decrypt dataset")
        return False
    
    print(f"\n✓ Decrypted data size: {len(decrypted_data)} bytes")
    
    # Analyze decrypted data
    parsed_data = analyze_decrypted_data(decrypted_data)
    
    # Submit Layer 2 answer
    # For Layer 2, the answer might be a confirmation that decryption succeeded
    success = submit_layer2_answer("decryption_successful")
    
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
