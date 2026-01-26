import requests
import re
import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Test the specific URL you mentioned
url = "https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote"

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

def test_url():
    logging.info(f"Testing URL: {url}")
    
    try:
        response = requests.get(url, headers=UA, timeout=30)
        response.raise_for_status()
        
        html_content = response.text
        
        # Save the HTML for analysis
        filename = f"test_url_content_{datetime.date.today()}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"Saved HTML content to {filename}")
        
        # Look for stock data patterns
        logging.info("Analyzing content for stock data...")
        
        # Look for price patterns
        price_patterns = [
            r'([\d,]+\.\d{2})',  # Numbers with decimal points
            r'HK\$\s*([\d,]+\.\d{2})',  # HK$ followed by numbers
            r'(\d+\.\d{2})\s*HKD',  # Numbers followed by HKD
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, html_content)
            if matches:
                logging.info(f"Found price matches with pattern {pattern}: {matches[:5]}")  # Show first 5
        
        # Look for market cap patterns
        market_cap_patterns = [
            r'([HK\$MBT\d.,]+)',  # Various market cap formats
            r'Market\s*Cap[^>]*>([^<]+)',  # Market Cap in HTML
            r'市值[^>]*>([^<]+)',  # Market Cap in Chinese
        ]
        
        for pattern in market_cap_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                logging.info(f"Found market cap matches with pattern {pattern}: {matches[:3]}")  # Show first 3
        
        # Look for stock symbol patterns
        symbol_patterns = [
            r'Stock\s*Code[^>]*>([^<]+)',  # Stock Code in HTML
            r'股票代號[^>]*>([^<]+)',  # Stock Code in Chinese
            r'(\d{4})\s*-\s*[^<]+',  # 4-digit stock code
        ]
        
        for pattern in symbol_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                logging.info(f"Found stock code matches with pattern {pattern}: {matches[:3]}")  # Show first 3
        
        # Look for any JSON data
        json_patterns = [
            r'\{[^{}]*"[^"]*":\s*"[^"]*"[^{}]*\}',  # Simple JSON objects
            r'\[[^\[\]]*\{[^\[\]]*\}[^\[\]]*\]',  # Arrays with JSON objects
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                logging.info(f"Found JSON-like data with pattern {pattern}: {matches[:2]}")  # Show first 2
        
        # Check if this is a redirect or different page
        if response.url != url:
            logging.info(f"URL redirected to: {response.url}")
        
        # Check content type
        content_type = response.headers.get('content-type', '')
        logging.info(f"Content-Type: {content_type}")
        
        # Check if it's the main page or a specific stock page
        if 'Equities-Quote' in response.url and 'sym=' not in response.url:
            logging.info("This appears to be the main equities quote page (not a specific stock)")
            logging.info("You may need to add stock parameters like ?sym=653&sc_lang=en")
        
        logging.info("URL test completed successfully")
        
    except Exception as e:
        logging.error(f"Error testing URL: {e}")

if __name__ == "__main__":
    test_url()