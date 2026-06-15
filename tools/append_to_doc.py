import os
from pathlib import Path
from google_auth_util import get_google_api_service

def create_daily_doc(title):
    """Creates a new Google Doc and returns its ID."""
    service = get_google_api_service('docs', 'v1', ['https://www.googleapis.com/auth/documents'])
    doc = service.documents().create(body={'title': title}).execute()
    return doc.get('documentId')

def append_summary_to_doc(doc_id, summary_data):
    """
    Appends formatted summary data to a Google Doc using batchUpdate.
    """
    service = get_google_api_service('docs', 'v1', ['https://www.googleapis.com/auth/documents'])
    
    # 1. Get current end index
    doc = service.documents().get(documentId=doc_id).execute()
    end_index = doc.get('body').get('content')[-1].get('endIndex') - 1
    
    # 2. Prepare text
    title = f"{summary_data.get('title', 'No Title')}\n"
    body = f"TL;DR: {summary_data.get('executive_summary', '')}\n"
    key_points = "\n".join([f"• {p}" for p in summary_data.get('key_points', [])]) + "\n"
    so_what = f"So What? {summary_data.get('so_what', '')}\n\n"
    
    full_text = title + body + key_points + so_what
    
    # 3. Create requests
    requests = [
        {
            'insertText': {
                'location': {'index': end_index},
                'text': full_text
            }
        },
        # Title as Heading 2
        {
            'updateParagraphStyle': {
                'range': {
                    'startIndex': end_index,
                    'endIndex': end_index + len(title)
                },
                'paragraphStyle': {'namedStyleType': 'HEADING_2'},
                'fields': 'namedStyleType'
            }
        },
        # Bold the "So What?"
        {
            'updateTextStyle': {
                'range': {
                    'startIndex': end_index + len(title) + len(body) + len(key_points),
                    'endIndex': end_index + len(full_text)
                },
                'textStyle': {'bold': True},
                'fields': 'bold'
            }
        }
    ]
    
    service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    return True

if __name__ == "__main__":
    # Test dictionary
    test_data = {
        "title": "AI Growth in 2026",
        "executive_summary": "Summarizing the rapid adoption of agentic AI.",
        "key_points": ["Point 1", "Point 2"],
        "so_what": "You need to automate your newsletter workflow now."
    }
    # This requires a real Doc ID to test
    print("Test append_summary_to_doc manually with a valid ID.")
