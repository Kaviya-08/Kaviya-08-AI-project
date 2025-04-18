import requests
from bs4 import BeautifulSoup
import re

class NewsService:
    def __init__(self, groq_service):
        self.groq_service = groq_service
        # Common headers to avoid being blocked by websites
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_article(self, url):
        """Scrape content from a news article URL."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Try to find the main article content
            article = None
            
            # Try common article containers
            for selector in ['article', '.article', '.story', '.content', '#content', '.post', 'main']:
                article = soup.select_one(selector)
                if article and len(article.get_text(strip=True)) > 300:
                    break
            
            # If no article container found, look for paragraphs
            if not article:
                article = soup
            
            # Get all paragraphs
            paragraphs = article.find_all('p')
            content = ' '.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30])
            
            # Clean up content
            content = re.sub(r'\s+', ' ', content)  # Replace multiple spaces
            
            return content if content else None
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
