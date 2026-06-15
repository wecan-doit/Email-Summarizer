import requests
from bs4 import BeautifulSoup
import re

def extract_article_content(url):
    """
    Attempts to extract the primary text content from a given URL.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for script_or_style in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script_or_style.decompose()

        # Strategy 1: Look for common article tags
        article = soup.find('article')
        if not article:
            # Strategy 2: Look for main content divs
            article = soup.find('main') or soup.find('div', class_=re.compile(r'article|post|content|entry', re.I))
            
        if article:
            text = article.get_text(separator='\n')
        else:
            # Strategy 3: Fallback to body text if no clear article container
            text = soup.body.get_text(separator='\n') if soup.body else soup.get_text(separator='\n')

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return ""

if __name__ == "__main__":
    # Test with a known news URL if needed
    test_url = "https://example.com" 
    print(f"Testing extraction for {test_url}...")
    content = extract_article_content(test_url)
    print(content[:500] + "...")
