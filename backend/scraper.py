import requests
from bs4 import BeautifulSoup
from typing import Tuple, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scrape_wikipedia(url: str) -> Tuple[str, str, List[str], str]:
    """
    Scrape Wikipedia article and extract key information
    
    Args:
        url: Wikipedia article URL
        
    Returns:
        Tuple of (title, summary_text, sections, raw_html)
    """
    try:
        # Add User-Agent to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract title
        title_element = soup.find("h1", class_="firstHeading")
        title = title_element.text if title_element else "Unknown Title"
        
        # Extract paragraphs for summary
        paragraphs = soup.find_all("p")
        summary = " ".join([p.text for p in paragraphs[:15]])  # First 15 paragraphs
        
        # Extract section headers
        sections = []
        for header in soup.find_all(["h2", "h3"]):
            span = header.find("span", class_="mw-headline")
            if span:
                sections.append(span.text)
        
        sections = list(dict.fromkeys(sections))[:10]  # Remove duplicates, limit to 10
        
        logger.info(f"✅ Scraped: {title}")
        
        return title, summary, sections, response.text
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Scraping failed: {e}")
        raise Exception(f"Failed to scrape URL: {e}")


def extract_key_entities(text: str) -> dict:
    """
    Extract named entities from text (basic implementation)
    For production, use spaCy or similar NLP library
    """
    # This is a simplified version
    # For real use case, integrate with spaCy or similar
    return {
        "people": [],
        "organizations": [],
        "locations": []
    }
