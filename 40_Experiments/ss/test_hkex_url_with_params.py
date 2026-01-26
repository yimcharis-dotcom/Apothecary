import requests
import re
import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Test the URL with stock parameters
stock_code = "653"
url = f"https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym={stock_code}&sc_lang=en"

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

def test_url_with_params():
    logging.info(f"Testing URL with stock parameters: {url}")
    
    try:
        response = requests.get(url, headers=UA, timeout=30)
        response.raise_for_status()
        
        html_content = response.text
        
        # Save the HTML for analysis
        filename = f"test_url_with_params_{datetime.date.today()}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"Saved HTML content to {filename}")
        
        # Look for specific stock data patterns
        logging.info("Analyzing content for stock data...")
        
        # Look for previous close patterns
        prev_close_patterns = [
            r'Previous\s*Close[^>]*>([^<]+)',  # Previous Close in HTML
            r'前收市價[^>]*>([^<]+)',  # Previous Close in Chinese
            r'(\d+\.\d{2})\s*\(Prev\)',  # Number with (Prev) label
            r'Prev[^>]*>\s*([\d,]+\.\d{2})',  # Prev label with number
        ]
        
        for pattern in prev_close_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                logging.info(f"Found previous close matches with pattern {pattern}: {matches[:3]}")
        
        # Look for market cap patterns
        market_cap_patterns = [
            r'Market\s*Cap[^>]*>([^<]+)',  # Market Cap in HTML
            r'市值[^>]*>([^<]+)',  # Market Cap in Chinese
            r'(\d+[\.]?\d*[MBT])\s*\(Market\s*Cap\)',  # Market cap with label
            r'([HK\$MBT\d.,]+)',  # Various market cap formats
        ]
        
        for pattern in market_cap_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                logging.info(f"Found market cap matches with pattern {pattern}: {matches[:3]}")
        
        # Look for stock symbol and name
        symbol_patterns = [
            r'Stock\s*Code[^>]*>([^<]+)',  # Stock Code in HTML
            r'股票代號[^>]*>([^<]+)',  # Stock Code in Chinese
            r'(\d{4})\s*-\s*[^<]+',  # 4-digit stock code
            r'Company\s*Name[^>]*>([^<]+)',  # Company Name
            r'公司名稱[^>]*>([^<]+)',  # Company Name in Chinese
        ]
        
        for pattern in symbol_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                logging.info(f"Found stock info matches with pattern {pattern}: {matches[:3]}")
        
        # Look for current price patterns
        current_price_patterns = [
            r'Last\s*Price[^>]*>([^<]+)',  # Last Price in HTML
            r'最後成交價[^>]*>([^<]+)',  # Last Price in Chinese
            r'(\d+\.\d{2})\s*\(Last\)',  # Number with (Last) label
            r'Last[^>]*>\s*([\d,]+\.\d{2})',  # Last label with number
        ]
        
        for pattern in current_price_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                logging.info(f"Found current price matches with pattern {pattern}: {matches[:3]}")
        
        # Look for any JSON data that might contain stock information
        json_patterns = [
            r'\{[^{}]*"prev[^{}]*":\s*"[^"]*"[^{}]*\}',  # Previous close JSON
            r'\{[^{}]*"close[^{}]*":\s*"[^"]*"[^{}]*\}',  # Close price JSON
            r'\{[^{}]*"mkt[^{}]*":\s*"[^"]*"[^{}]*\}',  # Market cap JSON
            r'\{[^{}]*"sym[^{}]*":\s*"[^"]*"[^{}]*\}',  # Symbol JSON
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                logging.info(f"Found JSON stock data with pattern {pattern}: {matches[:2]}")
        
        # Check if we found the specific stock
        if stock_code in html_content:
            logging.info(f"✅ Stock code {stock_code} found in page content")
        else:
            logging.warning(f"❌ Stock code {stock_code} NOT found in page content")
        
        # Check content type and response details
        content_type = response.headers.get('content-type', '')
        logging.info(f"Content-Type: {content_type}")
        logging.info(f"Response URL: {response.url}")
        
        # Check if this is the correct stock page
        if f'sym={stock_code}' in response.url:
            logging.info("✅ URL contains correct stock parameters")
        else:
            logging.warning("❌ URL does not contain expected stock parameters")
        
        logging.info("URL with parameters test completed successfully")
        
    except Exception as e:
        logging.error(f"Error testing URL with parameters: {e}")

if __name__ == "__main__":
    test_url_with_params()