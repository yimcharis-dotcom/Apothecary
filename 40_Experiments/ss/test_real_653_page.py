import requests
import re
import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Test the real 653 page URL
stock_code = "653"
url = f"https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym={stock_code}&sc_lang=en"

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

def test_real_653_page():
    logging.info(f"Testing real 653 page URL: {url}")
    
    try:
        response = requests.get(url, headers=UA, timeout=30)
        response.raise_for_status()
        
        html_content = response.text
        
        # Save the HTML for analysis
        filename = f"real_653_page_{datetime.date.today()}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"Saved HTML content to {filename}")
        
        # Check if this is the actual stock page
        if stock_code in html_content:
            logging.info(f"✅ Stock code {stock_code} found in page content")
        else:
            logging.warning(f"❌ Stock code {stock_code} NOT found in page content")
        
        # Look for the JavaScript widget data
        logging.info("Looking for JavaScript widget data...")
        
        # Look for LabCI widget patterns
        widget_patterns = [
            r'LabCI\.WP\["createquoteequitiespageobj"\]',  # LabCI widget initialization
            r'col_prevcls[^>]*>([^<]+)',  # Previous close in widget
            r'col_last[^>]*>([^<]+)',  # Last price in widget
            r'col_mktcap[^>]*>([^<]+)',  # Market cap in widget
            r'col_name[^>]*>([^<]+)',  # Company name in widget
        ]
        
        for pattern in widget_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                logging.info(f"Found widget data with pattern {pattern}: {matches[:5]}")
        
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
                logging.info(f"Found JSON stock data with pattern {pattern}: {matches[:3]}")
        
        # Look for any data attributes or inline data
        data_patterns = [
            r'data-[^=]*="[^"]*"',  # Data attributes
            r'["\']data["\']:\s*[^,}]+',  # Data in JavaScript objects
        ]
        
        for pattern in data_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                logging.info(f"Found data patterns with {pattern}: {matches[:3]}")
        
        # Check if we can find any actual stock data
        stock_data_patterns = [
            r'(\d+\.\d{2})',  # Price patterns
            r'([HK\$MBT\d.,]+)',  # Market cap patterns
            r'(\d{4})',  # Stock codes
        ]
        
        for pattern in stock_data_patterns:
            matches = re.findall(pattern, html_content)
            if matches:
                # Filter out common non-stock numbers
                stock_numbers = [m for m in matches if len(m) >= 2 and not m.startswith('20')]
                if stock_numbers:
                    logging.info(f"Found potential stock data with pattern {pattern}: {stock_numbers[:10]}")
        
        # Check content type and response details
        content_type = response.headers.get('content-type', '')
        logging.info(f"Content-Type: {content_type}")
        logging.info(f"Response URL: {response.url}")
        
        # Check if this is the correct stock page
        if f'sym={stock_code}' in response.url:
            logging.info("✅ URL contains correct stock parameters")
        else:
            logging.warning("❌ URL does not contain expected stock parameters")
        
        # Look for any API endpoints in the JavaScript
        api_patterns = [
            r'["\']([^"\']*api[^"\']*equity[^"\']*)["\']',
            r'["\']([^"\']*widget[^"\']*data[^"\']*)["\']',
            r'["\']([^"\']*getequity[^"\']*)["\']',
        ]
        
        for pattern in api_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                if any(keyword in match.lower() for keyword in ['api', 'widget', 'data', 'equity']):
                    logging.info(f"Found potential API endpoint: {match}")
        
        logging.info("Real 653 page test completed")
        
    except Exception as e:
        logging.error(f"Error testing real 653 page: {e}")

if __name__ == "__main__":
    test_real_653_page()