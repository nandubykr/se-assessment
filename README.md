# SE Assessment - API Puzzle Solution

## Overview
This repository contains the solution to a 4-layer engineering assessment puzzle. The task involves exploring an HTTP API service to understand its functionality, decrypt data, find hidden answers, and provide qualitative analysis.

## Assessment Details
- **Candidate**: Shivanandu
- **Email**: cvanandbykr@gmail.com
- **Time Limit**: 3 hours (from first authenticated request)
- **Base URL**: https://ca-seassessment-api-dev.happywater-190f264d.northcentralus.azurecontainerapps.io

## Layers

### Layer 1: Data Integrity
Fetch the full dataset efficiently and prove byte-level integrity.

### Layer 2: Decryption
Decrypt the dataset using a key issued by the platform.

### Layer 3: Hidden Answer
Find a short alphabetic answer hidden across the decrypted records.

### Layer 4: Analysis
Provide qualitative analysis about the data.

## Scripts

### `health_check.py`
- Verifies API connectivity
- Does not start the 3-hour clock
- Safe to run multiple times

### `explore_api.py`
- Main exploration script
- Handles authentication with Bearer token
- Tracks remaining time
- Tests various endpoints

### `layer1_integrity.py`
- Fetches full dataset
- Verifies byte-level integrity
- Submits Layer 1 answer

### `layer2_decryption.py`
- Obtains decryption key from platform
- Decrypts the dataset
- Submits Layer 2 answer

### `layer3_search.py`
- Searches for hidden alphabetic answer
- Analyzes decrypted records
- Submits Layer 3 answer

### `layer4_analysis.py`
- Performs data analysis
- Generates insights
- Submits Layer 4 answer

## Running the Scripts

```bash
# Install dependencies
pip install -r requirements.txt

# Check health (no clock started)
python health_check.py

# Explore API endpoints
python explore_api.py

# Work through layers
python layer1_integrity.py
python layer2_decryption.py
python layer3_search.py
python layer4_analysis.py
```

## Authentication
All authenticated endpoints require:
```
Authorization: Bearer sa_9ede956507b4ac98ba4b3e8a6c3bdc17c26f0eb98e4277641a4e591dbe098de9
```

## Notes
- Rate limits are per-candidate and advertised in response headers
- Submissions are not idempotent - every attempt is recorded
- Invalid submissions return error messages with valid type values
- Data is encrypted and requires platform-issued decryption key
- The 3-hour clock starts with the first authenticated request
