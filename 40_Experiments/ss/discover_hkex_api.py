"""
HKEX API Discovery Script
Intercepts network traffic to find the actual API endpoint for stock data
Target: Stock code 653 on HKEX
"""

import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright
import requests

# Configuration
TARGET_URL = "https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym=653&sc_lang=en"
STOCK_CODE = "653"
OUTPUT_FILE = r"C:\Vault\Apothecary\40_Experiments\hkex_network_traffic.json"

# Keywords to identify relevant requests
RELEVANT_KEYWORDS = ["api", "data", "equity", "quote", "widget", "stock", "653", "market", "price"]

# Store all captured network traffic
captured_requests = []
potential_api_endpoints = []


def is_relevant_request(url):
    """Check if URL is likely to contain stock data"""
    url_lower = url.lower()
    return any(keyword in url_lower for keyword in RELEVANT_KEYWORDS)


def has_stock_data(data):
    """Check if response data contains stock information for 653"""
    if not data:
        return False

    data_str = str(data).lower()
    # Look for price-like patterns, market cap, or stock code 653
    indicators = ["653", "market cap", "prev", "close", "price", "volume", "turnover"]
    return any(indicator in data_str for indicator in indicators)


async def intercept_network_traffic():
    """Use Playwright to intercept all network requests"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Playwright browser...")

    async with async_playwright() as p:
        # Launch browser with network interception enabled
        browser = await p.chromium.launch(headless=False)  # Set to True for headless mode
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # Track request-response pairs
        request_map = {}

        async def handle_request(request):
            """Capture request details"""
            try:
                request_data = {
                    "timestamp": datetime.now().isoformat(),
                    "url": request.url,
                    "method": request.method,
                    "resource_type": request.resource_type,
                    "headers": dict(request.headers),
                    "post_data": request.post_data if request.method == "POST" else None,
                    "is_relevant": is_relevant_request(request.url)
                }
                request_map[request.url] = request_data

                if request_data["is_relevant"]:
                    print(f"[REQUEST] {request.method} {request.url}")

            except Exception as e:
                print(f"Error handling request: {e}")

        async def handle_response(response):
            """Capture response details"""
            try:
                url = response.url
                request_data = request_map.get(url, {})

                response_data = {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "body": None,
                    "is_json": False
                }

                # Try to get response body
                try:
                    content_type = response.headers.get("content-type", "")

                    if "application/json" in content_type or response.url.endswith(".json"):
                        body = await response.json()
                        response_data["body"] = body
                        response_data["is_json"] = True

                        # Check if this response contains stock data
                        if has_stock_data(body):
                            print(f"[MATCH] Found potential stock data in: {url}")
                            potential_api_endpoints.append({
                                "url": url,
                                "method": request_data.get("method", "GET"),
                                "request_headers": request_data.get("headers", {}),
                                "post_data": request_data.get("post_data"),
                                "response": body
                            })
                    else:
                        # Try to read as text
                        text = await response.text()
                        if len(text) < 10000:  # Only store small text responses
                            response_data["body"] = text

                            # Check if text contains stock data
                            if has_stock_data(text):
                                print(f"[MATCH] Found potential stock data in: {url}")
                                potential_api_endpoints.append({
                                    "url": url,
                                    "method": request_data.get("method", "GET"),
                                    "request_headers": request_data.get("headers", {}),
                                    "post_data": request_data.get("post_data"),
                                    "response": text
                                })
                        else:
                            response_data["body"] = f"<large response: {len(text)} chars>"

                except Exception as e:
                    response_data["body_error"] = str(e)

                # Combine request and response data
                full_data = {**request_data, "response": response_data}
                captured_requests.append(full_data)

                if request_data.get("is_relevant"):
                    print(f"[RESPONSE] {response.status} - {url}")

            except Exception as e:
                print(f"Error handling response: {e}")

        # Set up event listeners
        page.on("request", handle_request)
        page.on("response", handle_response)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Navigating to HKEX page...")

        # Navigate to the page
        await page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Page loaded, waiting for additional requests...")

        # Wait for any additional async requests
        await asyncio.sleep(5)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Closing browser...")
        await browser.close()


def test_api_endpoint(endpoint_data):
    """Test if we can directly call the discovered API endpoint"""
    print(f"\n{'='*80}")
    print(f"Testing API Endpoint: {endpoint_data['url']}")
    print(f"{'='*80}")

    try:
        # Prepare headers (remove unnecessary ones)
        headers = endpoint_data.get("request_headers", {})
        essential_headers = {
            k: v for k, v in headers.items()
            if k.lower() in ["accept", "content-type", "user-agent", "referer", "accept-language"]
        }

        # Add common headers
        essential_headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
        })

        # Make request
        method = endpoint_data.get("method", "GET")
        url = endpoint_data["url"]

        if method == "POST":
            response = requests.post(
                url,
                headers=essential_headers,
                data=endpoint_data.get("post_data"),
                timeout=10
            )
        else:
            response = requests.get(url, headers=essential_headers, timeout=10)

        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            try:
                json_data = response.json()
                print(f"\nJSON Response (first 500 chars):")
                print(json.dumps(json_data, indent=2)[:500])
                return True, json_data
            except:
                print(f"\nText Response (first 500 chars):")
                print(response.text[:500])
                return True, response.text
        else:
            print(f"Failed with status code: {response.status_code}")
            return False, None

    except Exception as e:
        print(f"Error testing endpoint: {e}")
        return False, None


def generate_curl_command(endpoint_data):
    """Generate curl command for the API endpoint"""
    url = endpoint_data["url"]
    method = endpoint_data.get("method", "GET")
    headers = endpoint_data.get("request_headers", {})

    curl_parts = [f'curl -X {method}']

    # Add headers
    for key, value in headers.items():
        if key.lower() in ["accept", "content-type", "user-agent", "referer"]:
            curl_parts.append(f'-H "{key}: {value}"')

    # Add POST data if applicable
    if method == "POST" and endpoint_data.get("post_data"):
        curl_parts.append(f'-d \'{endpoint_data.get("post_data")}\'')

    # Add URL
    curl_parts.append(f'"{url}"')

    return ' \\\n  '.join(curl_parts)


def main():
    """Main execution function"""
    print("="*80)
    print("HKEX API Discovery Tool")
    print("="*80)
    print(f"Target URL: {TARGET_URL}")
    print(f"Stock Code: {STOCK_CODE}")
    print(f"Output File: {OUTPUT_FILE}")
    print("="*80)

    # Run the network interception
    asyncio.run(intercept_network_traffic())

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Network capture complete!")
    print(f"Total requests captured: {len(captured_requests)}")
    print(f"Potential API endpoints found: {len(potential_api_endpoints)}")

    # Save all captured traffic
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "target_url": TARGET_URL,
                "stock_code": STOCK_CODE,
                "total_requests": len(captured_requests),
                "potential_endpoints": len(potential_api_endpoints)
            },
            "captured_requests": captured_requests,
            "potential_api_endpoints": potential_api_endpoints
        }, f, indent=2, ensure_ascii=False)

    print(f"\nFull network traffic saved to: {OUTPUT_FILE}")

    # Test each potential endpoint
    print("\n" + "="*80)
    print("TESTING DISCOVERED ENDPOINTS")
    print("="*80)

    working_endpoints = []
    for i, endpoint in enumerate(potential_api_endpoints, 1):
        print(f"\n[Endpoint {i}/{len(potential_api_endpoints)}]")
        success, data = test_api_endpoint(endpoint)
        if success:
            working_endpoints.append({
                "endpoint": endpoint,
                "test_response": data
            })

    # Generate summary report
    print("\n" + "="*80)
    print("DISCOVERY SUMMARY")
    print("="*80)

    if working_endpoints:
        print(f"\n✓ Found {len(working_endpoints)} working API endpoint(s)!\n")

        for i, item in enumerate(working_endpoints, 1):
            endpoint = item["endpoint"]
            print(f"\n--- Working Endpoint {i} ---")
            print(f"URL: {endpoint['url']}")
            print(f"Method: {endpoint.get('method', 'GET')}")
            print(f"\nCURL Command:")
            print(generate_curl_command(endpoint))
            print(f"\nPython Requests Example:")
            print(f"""
import requests

response = requests.get(
    "{endpoint['url']}",
    headers={{
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*"
    }}
)
data = response.json()
print(data)
""")
    else:
        print("\n✗ No working API endpoints discovered.")
        print("The site may use:")
        print("  - Server-side rendering")
        print("  - Authentication/cookies")
        print("  - Anti-scraping measures")
        print("\nCheck the network traffic JSON file for more details.")

    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    main()
