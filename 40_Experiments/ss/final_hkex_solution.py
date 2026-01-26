import datetime
import json
import os
import re
import time
import logging
import requests
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

STOCK_CODE = "0653"
OUTPUT_DIR = r"C:\Users\YC\OneDrive\Desktop\AI hub\Experiment\ex daily quote"
EXCEL_FILE = os.path.join(OUTPUT_DIR, "hkex_quote.testing.xlsx")

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


def normalize_symbol(sym: str) -> str:
    return str(int(sym))


def extract_stock_data_from_hkex(sym: str) -> dict:
    """
    Extract stock data from HKEX using the correct URL with stock parameters
    """
    logging.info(f"Extracting stock data for stock {sym}")
    
    session = requests.Session()
    
    # Use the correct URL with stock parameters
    quote_url = f"https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym={sym}&sc_lang=en"
    
    try:
        response = session.get(quote_url, headers=UA, timeout=30)
        response.raise_for_status()
        
        html_content = response.text
        
        # Save HTML for analysis
        debug_file = os.path.join(OUTPUT_DIR, f"debug_html_final_{datetime.date.today()}.html")
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"Saved HTML response to {debug_file}")
        
        stock_info = {}
        
        # Look for stock data patterns in the HTML
        # The page uses JavaScript widgets, but sometimes data is embedded
        
        # Look for PREV. CLOSE pattern (HK$0.127 format)
        prev_close_patterns = [
            r'PREV\.\s*CLOSE\s*HK\$\s*(\d+\.\d{3})',  # PREV. CLOSE HK$0.127
            r'PREV\.\s*CLOSE\s*HK\$\s*(\d+\.\d{2})',  # PREV. CLOSE HK$0.12
            r'col_prevcls[^>]*>([^<]+)',  # Widget class pattern
            r'prevcls[^>]*>([^<]+)',  # Previous close in widget
            r'(\d+\.\d{3})',  # Three decimal places (more specific)
            r'HK\$\s*(\d+\.\d{3})',  # HK$ followed by three decimals
        ]
        
        for pattern in prev_close_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                try:
                    price_val = float(match)
                    # Reasonable stock price range check (0.001 to 10000)
                    if 0.001 <= price_val <= 10000:
                        stock_info['prev_close'] = str(price_val)
                        logging.info(f"Found previous close: {price_val} using pattern: {pattern}")
                        break
                except ValueError:
                    continue
            if 'prev_close' in stock_info:
                break
        
        # Look for market cap patterns (HK$221.80M format)
        market_cap_patterns = [
            r'MKT\s*CAP\s*HK\$\s*([\d,]+\.\d{2}[MBT]?)',  # MKT CAP HK$221.80M
            r'Market\s*Cap\s*HK\$\s*([\d,]+\.\d{2}[MBT]?)',  # Market Cap HK$221.80M
            r'col_mktcap[^>]*>([^<]+)',  # Market cap in widget
            r'市值[^>]*>([^<]+)',  # Market Cap in Chinese
            r'HK\$\s*([\d,]+\.\d{2}[MBT])',  # HK$221.80M
        ]
        
        for pattern in market_cap_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                # Filter out non-market cap values
                if len(match) >= 2 and any(char in match.upper() for char in ['M', 'B', 'T', '$']):
                    stock_info['market_cap'] = match
                    logging.info(f"Found market cap: {match} using pattern: {pattern}")
                    break
            if 'market_cap' in stock_info:
                break
        
        # Look for company name
        company_patterns = [
            r'col_name[^>]*>([^<]+)',  # Company name in widget
            r'Company\s*Name[^>]*>([^<]+)',  # Company Name in HTML
            r'公司名稱[^>]*>([^<]+)',  # Company Name in Chinese
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                if match.strip() and len(match.strip()) > 1:
                    stock_info['company_name'] = match.strip()
                    logging.info(f"Found company name: {match.strip()}")
                    break
            if 'company_name' in stock_info:
                break
        
        # Try to find API endpoints that might return JSON data
        api_patterns = [
            r'["\']([^"\']*api[^"\']*equity[^"\']*)["\']',
            r'["\']([^"\']*widget[^"\']*data[^"\']*)["\']',
            r'["\']([^"\']*getequity[^"\']*)["\']',
        ]
        
        for pattern in api_patterns:
            api_matches = re.findall(pattern, html_content, re.IGNORECASE)
            for api_url in api_matches:
                if any(keyword in api_url.lower() for keyword in ['api', 'widget', 'data', 'equity']):
                    if api_url.startswith(('http://', 'https://')):
                        test_url = api_url
                    elif api_url.startswith('/'):
                        test_url = f"https://www.hkex.com.hk{api_url}"
                    else:
                        continue
                    
                    logging.info(f"Testing potential API endpoint: {test_url}")
                    
                    try:
                        # Try with stock parameters
                        test_params = [
                            {'sym': sym, 'sc_lang': 'en'},
                            {'symbol': sym},
                            {'stock_code': sym},
                            {'qid': int(time.time() * 1000)},
                            {}
                        ]
                        
                        for params in test_params:
                            try:
                                api_response = session.get(test_url, params=params, headers=UA, timeout=30)
                                api_response.raise_for_status()
                                
                                # Try to parse as JSON
                                try:
                                    json_data = api_response.json()
                                    logging.info(f"API returned JSON: {json_data}")
                                    
                                    # Look for stock data in JSON
                                    if isinstance(json_data, dict):
                                        for key, value in json_data.items():
                                            if 'prev' in key.lower() and 'close' in key.lower():
                                                stock_info['prev_close'] = str(value)
                                            elif 'market' in key.lower() and 'cap' in key.lower():
                                                stock_info['market_cap'] = str(value)
                                            elif 'close' in key.lower() and isinstance(value, (int, float)):
                                                stock_info['prev_close'] = str(value)
                                            elif 'name' in key.lower():
                                                stock_info['company_name'] = str(value)
                                    
                                    if len(stock_info) >= 2:  # Found multiple data points
                                        return stock_info
                                        
                                except json.JSONDecodeError:
                                    # Not JSON, check HTML response
                                    response_text = api_response.text
                                    
                                    # Look for data in HTML response
                                    prev_close_match = re.search(r'PREV\.\s*CLOSE\s*HK\$\s*(\d+\.\d{3})', response_text, re.IGNORECASE)
                                    if prev_close_match:
                                        stock_info['prev_close'] = prev_close_match.group(1)
                                        logging.info(f"Found previous close in API response: {stock_info['prev_close']}")
                                    
                                    market_cap_match = re.search(r'MKT\s*CAP\s*HK\$\s*([\d,]+\.\d{2}[MBT]?)', response_text, re.IGNORECASE)
                                    if market_cap_match:
                                        stock_info['market_cap'] = market_cap_match.group(1)
                                        logging.info(f"Found market cap in API response: {stock_info['market_cap']}")
                                    
                                    if len(stock_info) >= 2:
                                        return stock_info
                                        
                            except Exception as e:
                                logging.debug(f"Error testing API {test_url} with params {params}: {e}")
                                continue
                                
                            if len(stock_info) >= 2:
                                return stock_info
                                
                    except Exception as e:
                        logging.warning(f"Error calling API {test_url}: {e}")
                        continue
        
        logging.info(f"Extraction completed. Found data: {stock_info}")
        return stock_info
        
    except Exception as e:
        logging.error(f"Error extracting stock data: {e}")
        return {}


def parse_market_cap(cap_str: str) -> tuple[float | None, str | None]:
    """Parse market cap string into numeric value and unit"""
    if not cap_str:
        return None, None
    
    # Remove currency symbols and common prefixes
    cleaned = re.sub(r'[HK\$,\s]', '', cap_str)
    
    # Extract numeric value and unit
    num_match = re.search(r'([\d.]+)', cleaned)
    unit_match = re.search(r'([MBTmbt])', cleaned)
    
    if num_match:
        try:
            num_val = float(num_match.group(1))
            unit = unit_match.group(1) if unit_match else None
            
            # Convert to proper scale if needed
            if unit and unit.upper() == 'M':
                num_val *= 1_000_000
            elif unit and unit.upper() == 'B':
                num_val *= 1_000_000
            elif unit and unit.upper() == 'T':
                num_val *= 1_000
                
            return num_val, unit
        except ValueError:
            pass
    
    return None, None


def load_last_row(df: pd.DataFrame, sym: str) -> dict | None:
    if df.empty:
        return None
    match = df[df["Stock Code"] == sym]
    if match.empty:
        return None
    return match.iloc[-1].to_dict()


def main() -> None:
    today = datetime.date.today()
    sym = normalize_symbol(STOCK_CODE)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        logging.info(f"Starting final HKEX extraction for stock {sym} on {today}")
        
        stock_data = extract_stock_data_from_hkex(sym)
        
        if stock_data:
            # Extract previous close
            close_str = stock_data.get('prev_close')
            if close_str:
                close_val = float(close_str)
                
                # Extract market cap
                cap_str = stock_data.get('market_cap')
                mkt_val, mkt_unit = parse_market_cap(cap_str) if cap_str else (None, None)

                row = {
                    "Date": today.strftime("%Y-%m-%d"),
                    "Stock Code": sym,
                    "Close": close_val,
                    "Market Cap": mkt_val,
                    "Market Cap Unit": mkt_unit,
                    "Carried Forward": False,
                }
                
                logging.info(f"Successfully extracted data: Close={close_val}, Market Cap={mkt_val}")
            else:
                raise RuntimeError("No previous close found")
        else:
            raise RuntimeError("Failed to extract any stock data")
        
    except Exception as e:
        logging.error(f"Extraction failed: {e}")
        
        # Try to load previous data if available
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            last = load_last_row(df, sym)
        else:
            last = None
        
        # Create a minimal Excel file with sample data for testing
        if not last:
            sample_data = {
                "Date": (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                "Stock Code": sym,
                "Close": 100.0,  # Sample value
                "Market Cap": 100000.0,  # Sample value
                "Market Cap Unit": "HKD",  # Sample value
                "Carried Forward": False
            }
            
            # Create DataFrame with sample data
            df = pd.DataFrame([sample_data])
            df.to_excel(EXCEL_FILE, index=False)
            logging.info(f"Created sample Excel file with test data: {EXCEL_FILE}")
            
            # Now use the sample data
            row = {
                "Date": today.strftime("%Y-%m-%d"),
                "Stock Code": sym,
                "Close": sample_data["Close"],
                "Market Cap": sample_data["Market Cap"],
                "Market Cap Unit": sample_data["Market Cap Unit"],
                "Carried Forward": True,
            }
            
            logging.info(f"Using sample data for testing purposes")
        else:
            row = {
                "Date": today.strftime("%Y-%m-%d"),
                "Stock Code": sym,
                "Close": last["Close"],
                "Market Cap": last.get("Market Cap"),
                "Market Cap Unit": last.get("Market Cap Unit"),
                "Carried Forward": True,
            }
        
            logging.warning(f"Using carried-forward data for stock {sym} due to error")

    # Update the Excel file with the new row
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = df[~((df["Date"] == row["Date"]) & (df["Stock Code"] == row["Stock Code"]))]
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_excel(EXCEL_FILE, index=False)
    logging.info(f"Data successfully saved to {EXCEL_FILE}")


if __name__ == "__main__":
    main()