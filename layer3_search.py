#!/usr/bin/env python3
"""
Layer 3 - Hidden Answer
- Find a short alphabetic answer hidden across decrypted records
- The answer is alphabetic (letters only)
- Search through decrypted dataset
- Submit Layer 3 answer
"""

import json
import re
from datetime import datetime
from config import BASE_URL, get_auth_headers
import requests

session = requests.Session()


def load_decrypted_data():
    """Load the decrypted dataset from Layer 2."""
    try:
        with open("decrypted_dataset.json", "r") as f:
            data = json.load(f)
        print(f"✓ Loaded decrypted dataset")
        return data
    
    except FileNotFoundError:
        print(f"✗ decrypted_dataset.json not found. Run layer2_decryption.py first.")
        return None


def extract_alphabetic_strings(data, min_length=3, max_length=50):
    """Extract all alphabetic strings from the data structure."""
    candidates = set()
    
    def traverse(obj):
        if isinstance(obj, str):
            # Extract sequences of alphabetic characters
            matches = re.findall(r'[A-Za-z]+', obj)
            for match in matches:
                if min_length <= len(match) <= max_length:
                    candidates.add(match)
        
        elif isinstance(obj, dict):
            for value in obj.values():
                traverse(value)
        
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)
    
    traverse(data)
    return sorted(candidates)


def search_for_patterns(data):
    """Search for hidden patterns in the data."""
    print(f"\n[{datetime.now().isoformat()}] Searching for patterns...")
    
    if isinstance(data, dict):
        print(f"\nDataset is a dictionary with keys:")
        for key, value in data.items():
            if isinstance(value, list):
                print(f"  {key}: list of {len(value)} items")
            elif isinstance(value, dict):
                print(f"  {key}: dictionary")
                print(f"    Sub-keys: {list(value.keys())}")
            else:
                print(f"  {key}: {type(value).__name__}")
    
    elif isinstance(data, list):
        print(f"\nDataset is a list with {len(data)} items")
        if len(data) > 0:
            print(f"First item: {json.dumps(data[0], indent=2)}")
    
    # Extract alphabetic candidates
    print(f"\nExtracting alphabetic strings...")
    candidates = extract_alphabetic_strings(data)
    
    print(f"\nFound {len(candidates)} unique alphabetic strings:")
    for i, candidate in enumerate(candidates[:50]):  # Show first 50
        print(f"  {i+1}. {candidate} (len={len(candidate)})")
    
    if len(candidates) > 50:
        print(f"  ... and {len(candidates) - 50} more")
    
    return candidates


def look_for_answer_structure(data):
    """
    Look for hints about answer structure.
    Layer 3 answer is described as 'short' and 'alphabetic'.
    """
    print(f"\n[{datetime.now().isoformat()}] Analyzing for answer hints...")
    
    # Look for specific fields that might contain the answer
    hint_fields = [
        'answer', 'hidden', 'secret', 'key', 'code', 'flag',
        'solution', 'message', 'value', 'name', 'id'
    ]
    
    def find_in_data(obj, path=""):
        results = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                if key.lower() in hint_fields:
                    results.append((new_path, value))
                results.extend(find_in_data(value, new_path))
        
        elif isinstance(obj, list):
            for i, item in enumerate(obj[:10]):  # Check first 10 items
                new_path = f"{path}[{i}]"
                results.extend(find_in_data(item, new_path))
        
        return results
    
    hints = find_in_data(data)
    if hints:
        print(f"\nPotential answer locations:")
        for path, value in hints:
            print(f"  {path}: {value}")
    
    return hints


def submit_layer3_answer(answer):
    """Submit Layer 3 answer."""
    print(f"\n[{datetime.now().isoformat()}] Submitting Layer 3 answer...")
    
    headers = get_auth_headers()
    url = f"{BASE_URL}/api/v1/submit"
    
    payload = {
        "type": "layer3",
        "value": answer,
        "notes": f"Hidden alphabetic answer found in decrypted records"
    }
    
    print(f"\nPayload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = session.post(url, headers=headers, json=payload, timeout=10)
        print(f"\nStatus: {response.status_code}")
        
        result = response.json()
        print(f"Response:\n{json.dumps(result, indent=2)}")
        
        if response.status_code in [200, 201]:
            print("\n✓ Layer 3 submission accepted!")
            return True
        else:
            print(f"\n✗ Submission rejected")
            return False
    
    except Exception as e:
        print(f"Error submitting: {e}")
        return False


def interactive_search(candidates):
    """Allow interactive searching through candidates."""
    print(f"\n[{datetime.now().isoformat()}] Interactive search mode")
    print(f"Total candidates: {len(candidates)}")
    print(f"Sorted by length:")
    
    by_length = {}
    for candidate in candidates:
        length = len(candidate)
        if length not in by_length:
            by_length[length] = []
        by_length[length].append(candidate)
    
    for length in sorted(by_length.keys()):
        words = by_length[length]
        print(f"\n  Length {length}: {len(words)} words")
        if length <= 10:  # Show words of length 10 or less
            print(f"    {', '.join(words[:20])}")
            if len(words) > 20:
                print(f"    ... and {len(words) - 20} more")


def main():
    """Main Layer 3 workflow."""
    print("="*60)
    print("LAYER 3 - HIDDEN ANSWER")
    print("="*60)
    
    # Load decrypted data
    data = load_decrypted_data()
    if data is None:
        return False
    
    # Search for patterns and candidates
    candidates = search_for_patterns(data)
    
    # Look for hints
    hints = look_for_answer_structure(data)
    
    # Interactive search
    interactive_search(candidates)
    
    print(f"\n{'='*60}")
    print("Layer 3 Search Complete")
    print(f"{'='*60}")
    print(f"\nTo submit an answer, modify this script to call:")
    print(f"  submit_layer3_answer('your_alphabetic_answer')")
    
    return True


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
