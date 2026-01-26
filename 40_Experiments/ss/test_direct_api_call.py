"""
Test if we can call the HKEX API directly without rendering the page
"""
import requests
import json
import re

# The discovered API endpoint (without token to test if it's required)
BASE_URL = "https://www1.hkex.com.hk/hkexwidget/data/getequityquote"

# The token from the discovery (might be static or dynamic)
TOKEN = "evLtsLsBNAUVTPxtGqVeG5XaFKW1pZVBK4BNrS2JM+bVP6g95/dLbtBjVdyRFkSs"

STOCK_CODE = "653"

print("="*80)
print("TEST 1: Call API with token")
print("="*80)

params_with_token = {
    'sym': STOCK_CODE,
    'token': TOKEN,
    'lang': 'eng',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.hkex.com.hk/'
}

try:
    response = requests.get(BASE_URL, params=params_with_token, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")

    if response.status_code == 200:
        text = response.text
        # Handle JSONP if present
        match = re.search(r'jQuery\d+_\d+\((.*)\)' if 'jQuery' in text else r'(.+)', text)
        if match:
            json_str = match.group(1) if 'jQuery' in text else text
            try:
                data = json.loads(json_str)
                quote = data.get('data', {}).get('quote', {})

                print("\n✓ SUCCESS! Got stock data:")
                print(f"  Previous Close (hc): {quote.get('hc')}")
                print(f"  Market Cap: {quote.get('mkt_cap')}{quote.get('mkt_cap_u')}")
                print(f"  Last Price (ls): {quote.get('ls')}")
                print(f"  Company: {quote.get('nm')}")
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}")
                print(f"Response text (first 500 chars): {text[:500]}")
    else:
        print(f"✗ Failed: {response.text[:200]}")

except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*80)
print("TEST 2: Call API without token")
print("="*80)

params_without_token = {
    'sym': STOCK_CODE,
    'lang': 'eng',
}

try:
    response = requests.get(BASE_URL, params=params_without_token, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        text = response.text
        match = re.search(r'jQuery\d+_\d+\((.*)\)' if 'jQuery' in text else r'(.+)', text)
        if match:
            json_str = match.group(1) if 'jQuery' in text else text
            try:
                data = json.loads(json_str)
                quote = data.get('data', {}).get('quote', {})

                if quote:
                    print("\n✓ SUCCESS! Token not required!")
                    print(f"  Previous Close (hc): {quote.get('hc')}")
                    print(f"  Market Cap: {quote.get('mkt_cap')}{quote.get('mkt_cap_u')}")
                else:
                    print("\n✗ No quote data in response")
            except json.JSONDecodeError:
                print(f"✗ Could not parse JSON: {text[:200]}")
    else:
        print(f"✗ Failed without token: {response.text[:200]}")

except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*80)
print("TEST 3: Try different stock code (0001)")
print("="*80)

params_test = {
    'sym': '1',  # Stock 0001
    'lang': 'eng',
}

try:
    response = requests.get(BASE_URL, params=params_test, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        text = response.text
        match = re.search(r'jQuery\d+_\d+\((.*)\)' if 'jQuery' in text else r'(.+)', text)
        if match:
            json_str = match.group(1) if 'jQuery' in text else text
            try:
                data = json.loads(json_str)
                quote = data.get('data', {}).get('quote', {})

                if quote:
                    print(f"\n✓ Works for other stocks too!")
                    print(f"  Company: {quote.get('nm')}")
                    print(f"  Previous Close: {quote.get('hc')}")
            except:
                pass

except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*80)
