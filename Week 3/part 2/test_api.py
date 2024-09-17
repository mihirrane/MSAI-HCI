import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Path to your service account JSON key file
SERVICE_ACCOUNT_FILE = 'path/to/your-service-account-key.json'

# Define the required scopes
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    # If the credentials are not valid, refresh them
    if not credentials.valid:
        credentials.refresh(Request())
    
    return credentials.token

# Get the access token
access_token = get_access_token()

url = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}
data = {
    "prompt": {"text": "Your prompt here"},
    "temperature": 0,
    "maxOutputTokens": 800,
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())