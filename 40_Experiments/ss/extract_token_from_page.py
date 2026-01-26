"""
Extract the API token from the HKEX page to use for API calls
"""
import requests
import re

STOCK_CODE = "653"
PAGE_URL = f"https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym={STOCK_CODE}&sc_lang=en"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

print("="*80)
print("Extracting token from HKEX page")
print("="*80)

try:
    # Get the page HTML
    response = requests.get(PAGE_URL, headers=headers, timeout=30)
    html = response.text

    print(f"Status Code: {response.status_code}")
    print(f"HTML Length: {len(html)} chars")

    # Look for token patterns in the HTML
    # The token might be embedded in JavaScript
    token_patterns = [
        r'token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
        r'getequityquote\?[^"\']*token=([^&"\']+)',
        r'evLtsLsBNAUVTPxtGqVeG[^"\'&\s]+',  # Pattern from discovered URL
    ]

    found_tokens = set()
    for pattern in token_patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        for match in matches:
            if len(match) > 20:  # Tokens are typically long
                found_tokens.add(match)
                print(f"\nFound potential token (pattern: {pattern}):")
                print(f"  {match[:50]}...")

    if found_tokens:
        print(f"\n Total unique tokens found: {len(found_tokens)}")

        # Test the first token
        token = list(found_tokens)[0]
        print(f"\nTesting API call with extracted token...")

        api_url = "https://www1.hkex.com.hk/hkexwidget/data/getequityquote"
        params = {
            'sym': STOCK_CODE,
            'token': token,
            'lang': 'eng',
        }

        api_response = requests.get(api_url, params=params, headers=headers, timeout=10)
        print(f"API Status Code: {api_response.status_code}")

        if api_response.status_code == 200:
            print("SUCCESS! Token works!")
            print(f"Response (first 300 chars): {api_response.text[:300]}")
        else:
            print(f"FAILED: {api_response.text[:200]}")
    else:
        print("\nNo tokens found in HTML")

        # Save HTML for manual inspection
        debug_file = "hkex_page_for_token_analysis.html"
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Saved HTML to {debug_file} for manual inspection")

except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*80)
