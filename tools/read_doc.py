import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_docs_service():
    SCOPES = ['https://www.googleapis.com/auth/documents']
    token_path = Path("token.json")
    if not token_path.exists():
        raise FileNotFoundError("token.json not found. Run link_test.py first.")
    
    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    return build('docs', 'v1', credentials=creds)

def read_doc_content(doc_id):
    service = get_docs_service()
    doc = service.documents().get(documentId=doc_id).execute()
    
    content = doc.get('body').get('content')
    text = ""
    for element in content:
        if 'paragraph' in element:
            elements = element.get('paragraph').get('elements')
            for e in elements:
                if 'textRun' in e:
                    text += e.get('textRun').get('content')
    return text

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python read_doc.py <doc_id>")
        sys.exit(1)
    
    doc_id = sys.argv[1]
    print(f"--- Fetching Content for Doc: {doc_id} ---")
    try:
        content = read_doc_content(doc_id)
        print(content)
    except Exception as e:
        print(f"Error: {e}")
