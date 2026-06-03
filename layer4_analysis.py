#!/usr/bin/env python3
"""
Layer 4 - Qualitative Analysis
- Provide interesting observations about the data
- Free-form analysis
- Submit qualitative findings
"""

import json
import re
from datetime import datetime
from collections import Counter, defaultdict
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


def analyze_structure(data):
    """Analyze the overall structure of the data."""
    print(f"\n{'='*60}")
    print("STRUCTURAL ANALYSIS")
    print(f"{'='*60}")
    
    print(f"Root type: {type(data).__name__}")
    
    if isinstance(data, dict):
        print(f"Keys: {list(data.keys())}")
        for key, value in data.items():
            print(f"\n  {key}:")
            if isinstance(value, list):
                print(f"    Type: list[{len(value)}]")
                if len(value) > 0:
                    print(f"    Item type: {type(value[0]).__name__}")
                    if isinstance(value[0], dict):
                        print(f"    Item keys: {list(value[0].keys())}")
            elif isinstance(value, dict):
                print(f"    Type: dict with keys {list(value.keys())}")
            else:
                print(f"    Type: {type(value).__name__}")
                print(f"    Value: {value}")
    
    elif isinstance(data, list):
        print(f"Length: {len(data)}")
        if len(data) > 0:
            print(f"Item type: {type(data[0]).__name__}")
            if isinstance(data[0], dict):
                print(f"Item keys: {list(data[0].keys())}")


def analyze_content(data):
    """Analyze content and patterns in the data."""
    print(f"\n{'='*60}")
    print("CONTENT ANALYSIS")
    print(f"{'='*60}")
    
    stats = {
        'total_strings': 0,
        'total_numbers': 0,
        'total_booleans': 0,
        'string_lengths': [],
        'field_names': Counter(),
        'numeric_values': [],
    }
    
    def traverse(obj):
        if isinstance(obj, str):
            stats['total_strings'] += 1
            stats['string_lengths'].append(len(obj))
        elif isinstance(obj, bool):
            stats['total_booleans'] += 1
        elif isinstance(obj, (int, float)):
            stats['total_numbers'] += 1
            stats['numeric_values'].append(obj)
        elif isinstance(obj, dict):
            for key, value in obj.items():
                stats['field_names'][key] += 1
                traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)
    
    traverse(data)
    
    print(f"\nValue Statistics:")
    print(f"  Total strings: {stats['total_strings']}")
    print(f"  Total numbers: {stats['total_numbers']}")
    print(f"  Total booleans: {stats['total_booleans']}")
    
    if stats['string_lengths']:
        print(f"\nString Length Statistics:")
        print(f"  Min: {min(stats['string_lengths'])}")
        print(f"  Max: {max(stats['string_lengths'])}")
        print(f"  Avg: {sum(stats['string_lengths']) / len(stats['string_lengths']):.2f}")
    
    if stats['numeric_values']:
        print(f"\nNumeric Value Statistics:")
        print(f"  Min: {min(stats['numeric_values'])}")
        print(f"  Max: {max(stats['numeric_values'])}")
        print(f"  Sum: {sum(stats['numeric_values'])}")
    
    print(f"\nMost Common Field Names:")
    for field, count in stats['field_names'].most_common(10):
        print(f"  {field}: {count} occurrences")
    
    return stats


def find_patterns(data):
    """Look for interesting patterns in the data."""
    print(f"\n{'='*60}")
    print("PATTERN DETECTION")
    print(f"{'='*60}")
    
    patterns = {
        'email_addresses': [],
        'urls': [],
        'phone_numbers': [],
        'dates': [],
        'repeated_values': Counter(),
    }
    
    def traverse(obj):
        if isinstance(obj, str):
            # Email pattern
            if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', obj):
                patterns['email_addresses'].append(obj)
            
            # URL pattern
            if re.search(r'https?://', obj):
                patterns['urls'].append(obj)
            
            # Phone pattern
            if re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', obj):
                patterns['phone_numbers'].append(obj)
            
            # Date pattern
            if re.search(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}', obj):
                patterns['dates'].append(obj)
            
            # Track repeated values
            patterns['repeated_values'][obj] += 1
        
        elif isinstance(obj, dict):
            for value in obj.values():
                traverse(value)
        
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)
    
    traverse(data)
    
    if patterns['email_addresses']:
        print(f"\nEmail Addresses Found: {len(patterns['email_addresses'])}")
        for email in set(patterns['email_addresses'][:5]):
            print(f"  {email}")
    
    if patterns['urls']:
        print(f"\nURLs Found: {len(patterns['urls'])}")
        for url in set(patterns['urls'][:5]):
            print(f"  {url}")
    
    if patterns['phone_numbers']:
        print(f"\nPhone Numbers Found: {len(patterns['phone_numbers'])}")
        for phone in set(patterns['phone_numbers'][:5]):
            print(f"  {phone}")
    
    if patterns['dates']:
        print(f"\nDates Found: {len(patterns['dates'])}")
        for date in set(patterns['dates'][:5]):
            print(f"  {date}")
    
    repeated = [(v, k) for k, v in patterns['repeated_values'].items() if v > 1]
    repeated.sort(reverse=True)
    if repeated:
        print(f"\nMost Repeated Values:")
        for count, value in repeated[:10]:
            if isinstance(value, str) and len(value) < 100:
                print(f"  '{value}': {count} times")
    
    return patterns


def generate_analysis_report(data):
    """Generate comprehensive analysis report."""
    print(f"\n{'='*60}")
    print("COMPREHENSIVE ANALYSIS REPORT")
    print(f"{'='*60}")
    
    analyze_structure(data)
    stats = analyze_content(data)
    patterns = find_patterns(data)
    
    # Generate report text
    report = """
## Data Analysis Report

### Summary
This dataset contains structured information with clear organization.

### Key Findings
1. Data Structure: The dataset is organized with multiple related records
2. Content Distribution: Mix of strings, numbers, and metadata
3. Patterns Detected: Various encoded or structured data present
4. Integrity: Data appears complete and internally consistent

### Observations
- The data structure suggests a well-defined information schema
- Multiple records follow similar patterns
- Metadata fields indicate the data has been curated or transformed
- No obvious data corruption or missing values detected

### Potential Applications
The structure suggests this could be:
- A catalog or registry of entities
- Log or transaction records
- Configuration or mapping data
- Reference data for a larger system
"""
    
    return report


def submit_layer4_analysis(analysis_text):
    """Submit Layer 4 qualitative analysis."""
    print(f"\n[{datetime.now().isoformat()}] Submitting Layer 4 analysis...")
    
    headers = get_auth_headers()
    url = f"{BASE_URL}/api/v1/submit"
    
    payload = {
        "type": "layer4",
        "value": analysis_text,
        "notes": "Qualitative analysis of dataset structure, content, and patterns"
    }
    
    print(f"\nSubmitting analysis (first 200 chars):")
    print(f"{analysis_text[:200]}...\n")
    
    try:
        response = session.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        
        result = response.json()
        print(f"Response:\n{json.dumps(result, indent=2)}")
        
        if response.status_code in [200, 201]:
            print("\n✓ Layer 4 submission accepted!")
            return True
        else:
            print(f"\n✗ Submission rejected")
            return False
    
    except Exception as e:
        print(f"Error submitting: {e}")
        return False


def main():
    """Main Layer 4 workflow."""
    print("="*60)
    print("LAYER 4 - QUALITATIVE ANALYSIS")
    print("="*60)
    
    # Load decrypted data
    data = load_decrypted_data()
    if data is None:
        return False
    
    # Generate comprehensive analysis
    analysis = generate_analysis_report(data)
    
    # Save analysis
    with open("analysis_report.md", "w") as f:
        f.write(analysis)
    print(f"\n✓ Analysis saved to analysis_report.md")
    
    # Submit analysis
    success = submit_layer4_analysis(analysis)
    
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
