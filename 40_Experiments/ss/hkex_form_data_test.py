import datetime
import json
import os
import re
import time
import logging
import requests

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


def test_form_data_approach(sym: str) -> dict:
    """
    Test the Form Data Approach to extract stock data from HKEX
    """
    logging.info(f"Testing Form Data Approach for stock {sym}")
    
    # First, get the main page to analyze its structure
    quote_url = f"https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym={sym}&sc_lang=en"
    
    session = requests.Session()
    
    try:
        # Get the main page
        response = session.get(quote_url, headers=UA, timeout=30)
        response.raise_for_status()
        
        html_content = response.text
        
        # Save HTML for analysis
        debug_file = os.path.join(OUTPUT_DIR, f"debug_html_form_data_{datetime.date.today()}.html")
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"Saved HTML response to {debug_file}")
        
        # Look for forms in the HTML
        form_pattern = r'<form[^>]*>(.*?)</form>'
        forms = re.findall(form_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        logging.info(f"Found {len(forms)} forms on the page")
        
        stock_info = {}
        
        # Analyze each form
        for i, form in enumerate(forms):
            logging.info(f"Analyzing form {i+1}")
            
            # Look for form attributes
            action_match = re.search(r'action="([^"]*)"', form, re.IGNORECASE)
            method_match = re.search(r'method="([^"]*)"', form, re.IGNORECASE)
            
            if action_match:
                action_url = action_match.group(1)
                logging.info(f"Form {i+1} action: {action_url}")
                
                # If we find a form action, try to submit it
                if action_url and action_url != '#':
                    # Try to extract form data
                    input_pattern = r'<input[^>]*name="([^"]*)"[^>]*value="([^"]*)"[^>]*>'
                    inputs = re.findall(input_pattern, form, re.IGNORECASE)
                    
                    form_data = {}
                    for name, value in inputs:
                        form_data[name] = value
                    
                    # Add our stock symbol if not present
                    if 'sym' not in form_data:
                        form_data['sym'] = sym
                    
                    logging.info(f"Form {i+1} data: {form_data}")
                    
                    # Try to submit the form
                    try:
                        if method_match and method_match.group(1).upper() == 'POST':
                            form_response = session.post(action_url, data=form_data, headers=UA, timeout=30)
                        else:
                            form_response = session.get(action_url, params=form_data, headers=UA, timeout=30)
                        
                        form_response.raise_for_status()
                        
                        # Analyze the response
                        form_html = form_response.text
                        
                        # Look for stock data in the response
                        prev_close_match = re.search(r'([\d,]+\.\d{2})', form_html)
                        if prev_close_match:
                            stock_info['prev_close'] = prev_close_match.group(1).replace(',', '')
                            logging.info(f"Found previous close in form response: {stock_info['prev_close']}")
                        
                        market_cap_match = re.search(r'([HK\$MBT\d.,]+)', form_html)
                        if market_cap_match:
                            stock_info['market_cap'] = market_cap_match.group(1)
                            logging.info(f"Found market cap in form response: {stock_info['market_cap']}")
                        
                        if stock_info:
                            return stock_info
                            
                    except Exception as e:
                        logging.warning(f"Error submitting form {i+1}: {e}")
                        continue
        
        # If no forms worked, try to find hidden API endpoints
        logging.info("No working forms found, searching for API endpoints...")
        
        # Look for JavaScript that might contain API calls
        js_pattern = r'<script[^>]*>(.*?)</script>'
        scripts = re.findall(js_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        for script in scripts:
            # Look for fetch or XMLHttpRequest calls
            api_patterns = [
                r'fetch\(["\']([^"\']*api[^"\']*)["\']',
                r'XMLHttpRequest.*?open\(["\']GET["\'],\s*["\']([^"\']*)["\']',
                r'["\']url["\']\s*:\s*["\']([^"\']*)["\']'
            ]
            
            for pattern in api_patterns:
                api_matches = re.findall(pattern, script, re.IGNORECASE)
                for api_url in api_matches:
                    if 'api' in api_url.lower() or 'data' in api_url.lower():
                        logging.info(f"Found potential API endpoint: {api_url}")
                        
                        try:
                            # Try to call the API directly
                            api_response = session.get(api_url, headers=UA, timeout=30)
                            api_response.raise_for_status()
                            
                            # Check if it's JSON
                            try:
                                api_data = api_response.json()
                                logging.info(f"API returned JSON data: {api_data}")
                                
                                # Look for stock data in JSON
                                if isinstance(api_data, dict):
                                    for key, value in api_data.items():
                                        if 'prev' in key.lower() and 'close' in key.lower():
                                            stock_info['prev_close'] = str(value)
                                        elif 'market' in key.lower() and 'cap' in key.lower():
                                            stock_info['market_cap'] = str(value)
                                
                                if stock_info:
                                    return stock_info
                                    
                            except json.JSONDecodeError:
                                # Not JSON, check HTML response
                                api_html = api_response.text
                                prev_close_match = re.search(r'([\d,]+\.\d{2})', api_html)
                                if prev_close_match:
                                    stock_info['prev_close'] = prev_close_match.group(1).replace(',', '')
                                    logging.info(f"Found previous close in API response: {stock_info['prev_close']}")
                                
                                if stock_info:
                                    return stock_info
                                    
                        except Exception as e:
                            logging.warning(f"Error calling API {api_url}: {e}")
                            continue
        
        logging.info("Form Data Approach completed - no data found")
        return stock_info
        
    except Exception as e:
        logging.error(f"Error in Form Data Approach: {e}")
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
        logging.info(f"Starting Form Data Approach test for stock {sym} on {today}")
        
        stock_data = test_form_data_approach(sym)
        
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
                
                logging.info(f"Successfully fetched data using Form Data Approach: Close={close_val}, Market Cap={mkt_val}")
            else:
                raise RuntimeError("No previous close found")
        else:
            raise RuntimeError("Form Data Approach failed to extract any data")
        
    except Exception as e:
        logging.error(f"Form Data Approach failed: {e}")
        
        # Try to load previous data if available
        if os.path.exists(EXCEL_FILE):
            import pandas as pd
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