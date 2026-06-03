"""
Configuration and constants for API exploration
"""

# API Configuration
BASE_URL = "https://ca-seassessment-api-dev.happywater-190f264d.northcentralus.azurecontainerapps.io"
API_KEY = "sa_9ede956507b4ac98ba4b3e8a6c3bdc17c26f0eb98e4277641a4e591dbe098de9"

# Endpoints
HEALTH_ENDPOINT = f"{BASE_URL}/api/v1/health"
SUBMIT_ENDPOINT = f"{BASE_URL}/api/v1/submit"
TIME_ENDPOINT = f"{BASE_URL}/api/v1/time"

# Known endpoints to explore
ENDPOINTS_TO_EXPLORE = [
    "/api/v1/data",
    "/api/v1/dataset",
    "/api/v1/records",
    "/api/v1/key",
    "/api/v1/decrypt",
    "/api/v1/search",
]

# Headers for authenticated requests
def get_auth_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


# Submission types
SUBMISSION_TYPES = {
    "layer1": "Layer 1 - Data Integrity",
    "layer2": "Layer 2 - Decryption",
    "layer3": "Layer 3 - Hidden Answer",
    "layer4": "Layer 4 - Analysis",
}
