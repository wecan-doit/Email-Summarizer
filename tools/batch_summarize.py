import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_summarizer_model():
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model_name = os.getenv("GEMINI_MODEL", 'models/gemini-3.1-flash-lite-preview')
    return genai.GenerativeModel(model_name)

def summarize_newsletter(content, subject):
    """
    Passes newsletter content to Gemini for a structured summary.
    """
    model = get_summarizer_model()
    
    prompt = f"""
    You are an AI research assistant for a high-level entrepreneur. 
    Analyze the following newsletter content and provide a high-signal summary.
    
    RULES:
    1. Ignore promotional material, ads, or sponsor pitches.
    2. Focus on actionable insights, tool updates, or business strategies.
    3. Use an action-oriented, professional tone.
    
    NEWSLETTER SUBJECT: {subject}
    CONTENT:
    {content}
    
    OUTPUT JSON FORMAT:
    {{
      "is_relevant": boolean,
      "title": "string",
      "executive_summary": "string",
      "key_points": ["bullet 1", "bullet 2"],
      "so_what": "Why does this matter specifically to a content creator/entrepreneur?",
      "sentiment": "neutral | positive | negative",
      "tags": ["relevant", "keywords"]
    }}
    """
    
    try:
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        print(f"Error summarizing {subject}: {e}")
        return None

if __name__ == "__main__":
    test_content = "This is a test newsletter content about new AI tools in May 2026."
    print("Testing Gemini summarization...")
    summary = summarize_newsletter(test_content, "Test Subject")
    print(json.dumps(summary, indent=2))
