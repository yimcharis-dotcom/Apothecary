"""
HKEX Stock Data Extractor - Final Simple Solution
Uses Playwright to extract data from the equities list page
"""
import datetime
import os
import logging
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuration
STOCK_CODE = "653"
OUTPUT_DIR = r"C:\Users\YC\OneDrive\Desktop\AI hub\Experiment\ex daily quote"
EXCEL_FILE = os.path.join(OUTPUT_DIR, "hkex_quote.testing.xlsx")


def normalize_symbol(sym: str) -> str:
    """Normalize stock code to remove leading zeros"""
    return str(int(sym))


def extract_stock_data_playwright(stock_code: str) -> dict:
    """
    Extract stock data using Playwright from the equities list page
    This is simpler than the quote page as data is in a clean table format
    """
    logging.info(f"Extracting stock data for stock {stock_code} using Playwright")

    with sync_playwright() as p:
        try:
            # Launch browser (headless=True for automation)
            browser = p.chromium.launch(headless=True)

            # Create context
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0'
            )

            page = context.new_page()

            # Navigate to equities list page
            url = "https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=en"
            logging.info(f"Loading page: {url}")
            page.goto(url, wait_until='networkidle', timeout=60000)

            # Wait for the page to load and search functionality to be available
            page.wait_for_selector('input[type="text"]', timeout=15000)

            # Enter stock code in search box
            logging.info(f"Searching for stock code {stock_code}")
            search_input = page.locator('input[type="text"]').first
            search_input.fill(stock_code)

            # Wait a bit for search results to filter
            page.wait_for_timeout(2000)

            # Wait for the table row with the stock code to appear
            # The table structure has stock code in a cell
            page.wait_for_selector(f'text={stock_code}', timeout=15000)

            # Extract data from the table row
            # Look for the row containing the stock code
            row = page.locator(f'tr:has-text("{stock_code}")').first

            if row:
                # Get all cells in the row
                cells = row.locator('td').all_text_contents()

                logging.info(f"Found {len(cells)} cells in row")
                logging.info(f"Cell contents: {cells}")

                # Parse the data based on table structure:
                # [Stock Code, Name, Nominal Price, Turnover, Market Cap, P/E, Div Yield, Chart]
                stock_data = {}

                if len(cells) >= 5:
                    # Market Cap is typically in the 5th column (index 4)
                    market_cap_text = cells[4] if len(cells) > 4 else ""

                    # Nominal Price is in the 3rd column (index 2)
                    price_text = cells[2] if len(cells) > 2 else ""

                    logging.info(f"Market Cap text: {market_cap_text}")
                    logging.info(f"Price text: {price_text}")

                    # Parse market cap (format: "221.80M")
                    if market_cap_text:
                        # Remove commas and extract number and unit
                        import re
                        match = re.search(r'([\d,]+\.?\d*)\s*([MBT])?', market_cap_text.replace(',', ''))
                        if match:
                            stock_data['market_cap'] = match.group(1)
                            stock_data['market_cap_unit'] = match.group(2) if match.group(2) else ''

                    # Parse price (format: "HK$0.132 +0.005 (+3.94%)")
                    # Extract just the price number
                    if price_text:
                        match = re.search(r'HK\$\s*([\d.]+)', price_text)
                        if match:
                            stock_data['prev_close'] = match.group(1)

                logging.info(f"Extracted data: {stock_data}")
                browser.close()
                return stock_data
            else:
                logging.error(f"Could not find table row for stock {stock_code}")
                browser.close()
                return {}

        except PlaywrightTimeoutError as e:
            logging.error(f"Timeout waiting for page elements: {e}")
            if 'browser' in locals():
                browser.close()
            return {}
        except Exception as e:
            logging.error(f"Error extracting stock data: {e}")
            if 'browser' in locals():
                browser.close()
            return {}


def parse_market_cap(cap_str: str, unit_str: str = '') -> tuple:
    """Parse market cap string into numeric value and unit"""
    if not cap_str:
        return None, None

    try:
        num_val = float(cap_str.replace(',', ''))
        unit = unit_str.upper() if unit_str else 'M'  # Default to M if not specified
        return num_val, unit
    except ValueError:
        return None, None


def load_last_row(df: pd.DataFrame, sym: str) -> dict | None:
    """Load the last row for the given stock symbol"""
    if df.empty:
        return None
    match = df[df["Stock Code"] == sym]
    if match.empty:
        return None
    return match.iloc[-1].to_dict()


def main() -> None:
    """Main execution function"""
    today = datetime.date.today()
    sym = normalize_symbol(STOCK_CODE)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        logging.info(f"Starting HKEX extraction for stock {sym} on {today}")

        # Extract stock data using Playwright
        stock_data = extract_stock_data_playwright(sym)

        if stock_data and 'prev_close' in stock_data:
            # Extract previous close
            close_val = float(stock_data['prev_close'])

            # Extract market cap
            mkt_val, mkt_unit = parse_market_cap(
                stock_data.get('market_cap', ''),
                stock_data.get('market_cap_unit', '')
            )

            row = {
                "Date": today.strftime("%Y-%m-%d"),
                "Stock Code": sym,
                "Close": close_val,
                "Market Cap": mkt_val,
                "Market Cap Unit": mkt_unit,
                "Carried Forward": False,
            }

            logging.info(f"Successfully extracted data: Close={close_val}, Market Cap={mkt_val}{mkt_unit}")
        else:
            raise RuntimeError("Failed to extract stock data")

    except Exception as e:
        logging.error(f"Extraction failed: {e}")

        # Try to load previous data if available
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            last = load_last_row(df, sym)
        else:
            last = None

        if last:
            row = {
                "Date": today.strftime("%Y-%m-%d"),
                "Stock Code": sym,
                "Close": last["Close"],
                "Market Cap": last.get("Market Cap"),
                "Market Cap Unit": last.get("Market Cap Unit"),
                "Carried Forward": True,
            }
            logging.warning(f"Using carried-forward data for stock {sym} due to error")
        else:
            logging.error("No previous data available, creating sample data")
            row = {
                "Date": today.strftime("%Y-%m-%d"),
                "Stock Code": sym,
                "Close": 0.0,
                "Market Cap": 0.0,
                "Market Cap Unit": "M",
                "Carried Forward": True,
            }

    # Update the Excel file with the new row
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        # Remove any existing entry for today
        df = df[~((df["Date"] == row["Date"]) & (df["Stock Code"] == row["Stock Code"]))]
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_excel(EXCEL_FILE, index=False)
    logging.info(f"Data successfully saved to {EXCEL_FILE}")


if __name__ == "__main__":
    main()
