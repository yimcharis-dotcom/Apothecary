import datetime
import json
import os
import re
import time
import logging

import pandas as pd
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


def fetch_token(session: requests.Session, sym: str) -> str:
    quote_url = (
        "https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/"
        f"Equities-Quote?sym={sym}&sc_lang=en"
    )
    
    # Add a delay to be respectful to the server
    time.sleep(1)
    
    response = session.get(quote_url, headers=UA, timeout=30)
    response.raise_for_status()  # Raise an exception for bad status codes
    html = response.text
    
    # Multiple regex patterns as fallbacks in case the site structure changes
    patterns = [
        r"getToken.*?return\\s+\"([^\"]+)\"",
        r'"token"\s*:\s*"([^"]+)"',
        r"'token'\s*:\s*'([^']+)'"
    ]
    
    for pattern in patterns:
        m = re.search(pattern, html, re.S)
        if m:
            token = m.group(1)
            logging.info(f"Successfully extracted token for stock {sym}")
            return token
    
    # If no pattern matches, log the failure and raise an error
    logging.error("All token extraction patterns failed")
    logging.debug(f"HTML snippet for debugging: {html[:1000]}...")
    raise RuntimeError("Token not found on quote page using any known pattern")


def fetch_quote(session: requests.Session, sym: str, token: str) -> dict:
    api_url = "https://www1.hkex.com.hk/hkexwidget/data/getequityquote"
    qid = int(time.time() * 1000)
    params = {
        "sym": sym,
        "token": token,
        "lang": "eng",
        "qid": qid,
        "callback": "c",
    }
    
    response = session.get(api_url, params=params, headers=UA, timeout=30)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    text = response.text
    json_str = text[text.find("(") + 1 : text.rfind(")")]
    payload = json.loads(json_str)
    
    if payload.get("data", {}).get("responsecode") != "000":
        logging.error(f"HKEX response not OK: {payload}")
        raise RuntimeError(f"HKEX response not OK: {payload.get('data', {}).get('responsecode')}")
    
    logging.info(f"Successfully fetched quote data for stock {sym}")
    return payload["data"]["quote"]


def parse_mkt_cap(quote: dict) -> tuple[float | None, str | None]:
    mkt_val = quote.get("mkt_cap")
    mkt_unit = quote.get("mkt_cap_u")
    try:
        mkt_val = float(mkt_val)
    except Exception:
        mkt_val = None
    return mkt_val, mkt_unit


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

    with requests.Session() as session:
        try:
            logging.info(f"Starting to fetch data for stock {sym} on {today}")
            
            # Add delay before fetching token to be respectful to the server
            time.sleep(1)
            token = fetch_token(session, sym)
            
            # Add delay before fetching quote to be respectful to the server
            time.sleep(1)
            quote = fetch_quote(session, sym, token)

            close_str = quote.get("prev_close")
            if close_str in (None, "", "-", "N/A"):
                raise RuntimeError("Prev close not found in quote JSON")

            close_val = float(str(close_str).replace(",", ""))
            mkt_val, mkt_unit = parse_mkt_cap(quote)

            row = {
                "Date": today.strftime("%Y-%m-%d"),
                "Stock Code": sym,
                "Close": close_val,
                "Market Cap": mkt_val,
                "Market Cap Unit": mkt_unit,
                "Carried Forward": False,
            }
            
            logging.info(f"Successfully fetched fresh data for stock {sym}")
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred while fetching data: {e}")
            logging.error(f"Status code: {e.response.status_code if e.response else 'Unknown'}")
            
            # Try to load previous data if available
            if os.path.exists(EXCEL_FILE):
                df = pd.read_excel(EXCEL_FILE)
                last = load_last_row(df, sym)
            else:
                df = pd.DataFrame()
                last = None

            if not last:
                logging.critical("No previous data available and current fetch failed")
                raise RuntimeError(f"Failed to fetch data and no previous data available: {e}")

            row = {
                "Date": today.strftime("%Y-%m-%d"),
                "Stock Code": sym,
                "Close": last["Close"],
                "Market Cap": last.get("Market Cap"),
                "Market Cap Unit": last.get("Market Cap Unit"),
                "Carried Forward": True,
            }
            
            logging.warning(f"Using carried-forward data for stock {sym} due to fetch failure")
        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}")
            
            # Try to load previous data if available
            if os.path.exists(EXCEL_FILE):
                df = pd.read_excel(EXCEL_FILE)
                last = load_last_row(df, sym)
            else:
                df = pd.DataFrame()
                last = None

            if not last:
                logging.critical("No previous data available and current fetch failed")
                raise RuntimeError(f"Failed to fetch data and no previous data available: {e}")

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
