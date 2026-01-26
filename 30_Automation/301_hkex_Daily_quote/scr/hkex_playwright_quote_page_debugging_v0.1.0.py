"""
HKEX Stock Data Extractor - Navigation Solution
Navigates from landing page like a real user for maximum robustness
Uses the exact selectors identified from DevTools inspection
"""
import datetime
import os
import logging
import re
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
EXCEL_FILE = os.path.join(OUTPUT_DIR, "hkex_quote.testing.v2.xlsx")


def normalize_symbol(sym: str) -> str:
    """Normalize stock code to remove leading zeros"""
    return str(int(sym))


def extract_stock_data_playwright(stock_code: str) -> dict:
    """
    Extract stock data using Playwright - navigates from landing page
    Steps: Landing page -> Search for stock -> Click stock -> Extract data
    """
    logging.info(f"Extracting stock data for stock {stock_code} using Playwright")

    with sync_playwright() as p:
        try:
            # Launch browser with maximized window
            browser = p.chromium.launch(
                headless=False,  # Debugging: visible browser
                args=['--start-maximized'],
                slow_mo=200
            )

            context = browser.new_context(
                no_viewport=True,  # Use native maximized window size
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0'
            )

            page = context.new_page()

            logging.info("⚠️ BROWSER WINDOW SHOULD BE OPENING NOW - CHECK YOUR TASKBAR!")

            # Step 1: Navigate to landing page
            landing_url = "https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=en"
            logging.info(f"Step 1: Loading landing page")
            page.goto(landing_url, timeout=90000)

            # Wait for page to be ready
            page.wait_for_load_state('networkidle', timeout=90000)
            logging.info("Landing page loaded")

            # Zoom out to see more content
            page.evaluate("document.body.style.zoom='0.67'")
            logging.info("Zoomed out to 67%")

            # Step 2: Try multiple search strategies
            logging.info(f"Step 2: Searching for stock {stock_code}")

            # Strategy 1: Visible click + typing so you can see it happen
            logging.info(f"Strategy 1: Searching by stock code '{stock_code}' (visible typing)")
            page.bring_to_front()
            page.wait_for_selector('input#tags', state="attached", timeout=30000)
            all_tags = page.locator('input#tags')
            logging.info(f"#tags count: {all_tags.count()}")

            # Prefer the filter input by accessible name (most reliable)
            search_input = page.get_by_role("textbox", name=re.compile(r"Stock Code", re.I))
            if search_input.count() == 0:
                search_input = page.locator('input#tags[placeholder*="Stock Code" i]').first
            if search_input.count() == 0:
                search_input = page.locator('#hkexw-equities .searchbox input#tags').first
            if search_input.count() == 0:
                search_input = all_tags.first
            search_input.wait_for(state='visible', timeout=30000)
            placeholder = search_input.get_attribute("placeholder")
            logging.info(f"Search placeholder: {placeholder}")
            search_handle = search_input.element_handle()
            if search_handle:
                page.evaluate(
                    "el => { el.style.outline='3px solid red'; el.style.background='#ffffcc'; }",
                    search_handle
                )
            box = search_input.bounding_box()
            if box:
                page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            else:
                search_input.click(force=True)
            page.wait_for_timeout(500)
            search_input.focus()
            page.keyboard.press("Control+A")
            page.keyboard.type(stock_code, delay=120)
            page.wait_for_timeout(500)

            # Verify it worked (from the visible input)
            actual_value = search_input.input_value()
            active_id = page.evaluate("() => document.activeElement && document.activeElement.id")
            logging.info(f"Active element id: {active_id}")
            logging.info(f"Search box contains: '{actual_value}'")
            page.screenshot(path="after_typing_debug.png")
            logging.info("Screenshot saved: after_typing_debug.png")

            # Fallback if UI typing didn't stick
            if actual_value.strip() != stock_code:
                logging.info("Visible typing didn't stick, using JS fallback")
                page.evaluate(f"""() => {{
                    const candidates = Array.from(
                        document.querySelectorAll('input[placeholder*="Stock" i], .searchbox input, #tags')
                    );
                    const input = candidates.find(el => el.offsetParent !== null) || candidates[0];
                    if (input) {{
                        input.value = '{stock_code}';
                        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                }}""")
                page.wait_for_timeout(500)
                actual_value = search_input.input_value()
                logging.info(f"Search box contains after JS fallback: '{actual_value}'")

            # Apply filters (Enter first)
            logging.info("Applying filters via Enter (primary)")
            try:
                search_input.press('Enter')
            except Exception as e:
                logging.info(f"Enter press failed: {e}")

            # No APPLY FILTERS click to avoid unexpected scrolling
            page.wait_for_timeout(5000)

            # Check if stock appears in results
            table_rows = page.locator('table tbody tr').count()
            logging.info(f"Rows after filtering: {table_rows}")
            stock_found = page.locator(f'a:has-text("{stock_code}")').count() > 0

            if not stock_found:
                # Strategy 2: Try company name
                logging.info("Stock code search failed, trying company name...")

                page.evaluate("""() => {
                    const input = document.querySelector('input[placeholder*="Stock"]') ||
                                 document.querySelector('.searchbox input') ||
                                 document.querySelector('#tags');
                    if (input) {
                        input.value = 'China Overseas Grand Oceans';
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        input.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }""")
                page.wait_for_timeout(1000)

                try:
                    apply_button.click()
                except:
                    pass

                page.wait_for_timeout(5000)
                stock_found = page.locator(f'a:has-text("{stock_code}")').count() > 0
                logging.info(f"Company name search result: {stock_found}")

            # Take screenshot to see filtered results
            page.screenshot(path="filtered_results_debug.png")
            logging.info("Screenshot saved: filtered_results_debug.png")

            # Pause so user can see the results before continuing
            logging.info("Pausing 3 seconds so you can see the results...")
            page.wait_for_timeout(3000)

            # Step 3: Click on the stock code link in the results
            logging.info(f"Step 3: Looking for stock {stock_code} in filtered results")

            # Find and click the stock link
            stock_link = page.locator(f'a:has-text("{stock_code}")').first

            # Scroll into view and click
            logging.info(f"Clicking on stock {stock_code}")
            stock_link.click()

            # Wait for navigation to quote page
            logging.info("Waiting for quote page to load...")
            page.wait_for_load_state('networkidle', timeout=60000)
            logging.info(f"Navigated to quote page: {page.url}")

            # Step 4: Extract data from quote page
            logging.info("Step 4: Extracting stock data")

            # Wait for data elements to be populated
            page.wait_for_selector('dt.col_prevcls', state='visible', timeout=30000)

            # Extract Previous Close
            prev_close_element = page.locator('dt.col_prevcls').first
            prev_close_text = prev_close_element.text_content()
            logging.info(f"Previous close: {prev_close_text}")

            # Extract Market Cap
            mkt_cap_element = page.locator('dt.col_mktcap').first
            mkt_cap_text = mkt_cap_element.text_content()
            logging.info(f"Market cap: {mkt_cap_text}")

            stock_data = {}

            # Parse Previous Close
            if prev_close_text:
                match = re.search(r'([\d,]+\.?\d*)', prev_close_text.replace(',', ''))
                if match:
                    stock_data['prev_close'] = match.group(1)

            # Parse Market Cap
            if mkt_cap_text:
                match = re.search(r'([\d,]+\.?\d*)\s*([MBT])', mkt_cap_text.replace(',', ''))
                if match:
                    stock_data['market_cap'] = match.group(1)
                    stock_data['market_cap_unit'] = match.group(2)

            browser.close()

            if not stock_data:
                raise Exception("No data extracted from page")

            logging.info(f"Successfully extracted: {stock_data}")
            return stock_data

        except PlaywrightTimeoutError as e:
            logging.error(f"Timeout: {e}")
            logging.info("Browser will stay open for 10 seconds so you can see what happened...")
            page.wait_for_timeout(10000)
            if 'browser' in locals():
                browser.close()
            return {}
        except Exception as e:
            logging.error(f"Error: {e}")
            logging.info("Browser will stay open for 10 seconds so you can see what happened...")
            page.wait_for_timeout(10000)
            if 'browser' in locals():
                browser.close()
            return {}


def parse_market_cap(cap_str: str, unit_str: str = '') -> tuple:
    """Parse market cap string into numeric value and unit"""
    if not cap_str:
        return None, None

    try:
        num_val = float(cap_str.replace(',', ''))
        unit = unit_str.upper() if unit_str else 'M'
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
    retrieved_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sym = normalize_symbol(STOCK_CODE)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        logging.info(f"Starting HKEX extraction for stock {sym} on {today}")

        # Extract stock data
        stock_data = extract_stock_data_playwright(sym)

        if stock_data and 'prev_close' in stock_data:
            close_val = float(stock_data['prev_close'])

            mkt_val, mkt_unit = parse_market_cap(
                stock_data.get('market_cap', ''),
                stock_data.get('market_cap_unit', '')
            )

            row = {
                "Date": today.strftime("%Y-%m-%d"),
                "Retrieved At": retrieved_at,
                "Stock Code": sym,
                "Close": close_val,
                "Market Cap": mkt_val,
                "Market Cap Unit": mkt_unit,
                "Carried Forward": False,
            }

            logging.info(f"Data extracted successfully: Close={close_val}, Market Cap={mkt_val}{mkt_unit}")
        else:
            raise RuntimeError("Failed to extract stock data")

    except Exception as e:
        logging.error(f"Extraction failed: {e}")

        # Fallback: Use previous day's data
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            last = load_last_row(df, sym)
        else:
            last = None

        if last:
            row = {
                "Date": today.strftime("%Y-%m-%d"),
                "Retrieved At": retrieved_at,
                "Stock Code": sym,
                "Close": last["Close"],
                "Market Cap": last.get("Market Cap"),
                "Market Cap Unit": last.get("Market Cap Unit"),
                "Carried Forward": True,
            }
            logging.warning(f"Using carried-forward data from previous day")
        else:
            logging.error("No previous data available, skipping update")
            return

    # Update Excel file
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        # Remove existing entry for today (if any)
        df = df[~((df["Date"] == row["Date"]) & (df["Stock Code"] == row["Stock Code"]))]
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_excel(EXCEL_FILE, index=False)
    logging.info(f"Data saved to {EXCEL_FILE}")


if __name__ == "__main__":
    main()
