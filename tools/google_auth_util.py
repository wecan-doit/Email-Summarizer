from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_google_api_service(service_name: str, version: str, scopes: list[str]):
    """
    Creates and returns a Google API service client.

    Args:
        service_name: The name of the API service (e.g., 'gmail', 'docs').
        version: The version of the API service (e.g., 'v1').
        scopes: A list of authorization scopes required.

    Returns:
        An authorized Google API service client.
    """
    token_path = Path("token.json")
    if not token_path.exists():
        raise FileNotFoundError("token.json not found. Run link_test.py first.")
    
    creds = Credentials.from_authorized_user_file(str(token_path), scopes)
    return build(service_name, version, credentials=creds)
