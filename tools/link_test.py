import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()

def test_gemini():
    print("Testing Gemini API...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[FAIL] Error: GEMINI_API_KEY not found in .env")
        return False
    
    try:
        genai.configure(api_key=api_key)
        # Debug: List available models
        print("Available models:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" - {m.name}")
        
        # Selecting an available model from the debug list
        model = genai.GenerativeModel('models/gemini-3.1-flash-lite-preview')
        response = model.generate_content("Hello, connection test.")
        print(f"[OK] Gemini Response: {response.text.strip()}")
        return True
    except Exception as e:
        print(f"[FAIL] Gemini Error: {e}")
        return False

def test_google_workspace():
    print("\nTesting Google Workspace (Gmail/Docs) Connectivity...")
    creds_path = Path("credentials.json")
    if not creds_path.exists():
        print("[FAIL] Error: credentials.json not found in root directory.")
        print("Please follow the 'Google Cloud Setup Guide' and download your JSON.")
        return False

    SCOPES = [
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/documents'
    ]
    
    creds = None
    token_path = Path("token.json")
    
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing token...")
            creds.refresh(Request())
        else:
            print("Authentication required. A browser window will open...")
            # Note: run_local_server might struggle in a background shell.
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    try:
        # Test Gmail
        gmail_service = build('gmail', 'v1', credentials=creds)
        profile = gmail_service.users().getProfile(userId='me').execute()
        print(f"[OK] Gmail Connected: {profile['emailAddress']}")

        # Test Docs
        docs_service = build('docs', 'v1', credentials=creds)
        print("[OK] Google Docs API Connected.")
        
        return True
    except Exception as e:
        print(f"[FAIL] Google Workspace Error: {e}")
        return False

if __name__ == "__main__":
    print("=== B.L.A.S.T. Phase 2: Link Test ===\n")
    gemini_ok = test_gemini()
    workspace_ok = test_google_workspace()
    
    if gemini_ok and workspace_ok:
        print("\n[SUCCESS] ALL LINKS VERIFIED. Ready for Phase 3: Architect.")
    else:
        print("\n[FAILURE] Link Test FAILED. Please resolve the errors above.")
        sys.exit(1)
