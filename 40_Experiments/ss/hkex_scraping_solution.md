# HKEX Stock Data Scraping Solution

## Current Situation

The HKEX website (<https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym=653&sc_lang=en>) loads stock data dynamically via JavaScript, which means:

- The HTML source code doesn't contain the actual stock information
- Simple HTTP requests with `requests` library cannot extract the data
- The data (Previous Close: HK$0.127, Market Cap: HK$221.80M, etc.) is visible in the browser but not in the raw HTML

## Required Solution: Headless Browser Automation

To extract the data you need, we must use a browser automation tool that can:

1. Load the webpage in a real browser environment
2. Execute JavaScript to populate the data
3. Wait for the data to appear
4. Extract the visible information

### Recommended Approach: Selenium with Chrome WebDriver

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os

def scrape_hkex_stock_data(stock_code="653"):
    # Setup Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Remove this line if you want to see the browser
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to the HKEX page
        url = f"https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym={stock_code}&sc_lang=en"
        driver.get(url)
        
        # Wait for the page to load and for the stock data to appear
        wait = WebDriverWait(driver, 10)
        
        # Wait for key elements to be present (adjust selectors based on actual page structure)
        prev_close_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'PREV. CLOSE')]/following-sibling::*[1] | //td[contains(text(), 'PREV. CLOSE')]/following-sibling::*[1]"))
        )
        
        # Alternative approach - wait for any price-related elements to load
        # Look for elements containing the text "PREV. CLOSE" and extract the adjacent value
        prev_close = driver.find_element(By.XPATH, "//span[contains(text(), 'PREV. CLOSE') or contains(text(), 'Prev Close')]/following-sibling::span[1]").text
        market_cap = driver.find_element(By.XPATH, "//span[contains(text(), 'MKT CAP') or contains(text(), 'Market Cap')]/following-sibling::span[1]").text
        
        # Extract other required data
        current_price = driver.find_element(By.XPATH, "//span[contains(@class, 'price')] | //span[contains(@class, 'last-price')]").text
        
        print(f"Stock {stock_code} Data:")
        print(f"Previous Close: {prev_close}")
        print(f"Market Cap: {market_cap}")
        print(f"Current Price: {current_price}")
        
        return {
            "stock_code": stock_code,
            "prev_close": prev_close,
            "market_cap": market_cap,
            "current_price": current_price,
            "date": time.strftime("%Y-%m-%d")
        }
        
    finally:
        driver.quit()

def save_to_excel(data, output_dir=r"C:\Users\YC\OneDrive\Desktop\AI hub\Experiment\ex daily quote"):
    os.makedirs(output_dir, exist_ok=True)
    excel_file = os.path.join(output_dir, "hkex_quote.testing.xlsx")
    
    # Create or update the Excel file
    df = pd.DataFrame([data])
    
    if os.path.exists(excel_file):
        existing_df = pd.read_excel(excel_file)
        # Replace existing entry for same date and stock code
        existing_df = existing_df[~((existing_df["Date"] == data["date"]) & (existing_df["Stock Code"] == data["stock_code"]))]
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_excel(excel_file, index=False)
    print(f"Data saved to {excel_file}")

# Example usage
if __name__ == "__main__":
    stock_data = scrape_hkex_stock_data("653")
    save_to_excel(stock_data)
```

### Installation Requirements

Before using the Selenium approach, you'll need to install:

```bash
pip install selenium pandas openpyxl
```

And download ChromeDriver from <https://chromedriver.chromium.org/> (matching your Chrome version)

### Alternative XPath Selectors

Since I can't see the exact HTML structure of the page, here are potential selectors for the data points you need:

- **Previous Close**: Look for elements near text containing "PREV. CLOSE" or "Prev Close"
- **Market Cap**: Look for elements near text containing "MKT CAP" or "Market Cap"

## Alternative Solutions

If Selenium proves challenging:

1. **Check for API endpoints**: Look for hidden API calls in the browser's Network tab when the page loads
2. **Use third-party services**: Services like Yahoo Finance might provide HKEX data
3. **Manual inspection**: Inspect the network requests during page load to find the actual data API

## Summary

The stock information you need (Previous Close: HK$0.127, Market Cap: HK$221.80M) is available on the public HKEX page, but requires a JavaScript-enabled browser to extract it. The Selenium approach is the most reliable solution for this type of dynamic content.
