"""
Parse the discovered HKEX API response to extract stock data
"""
import json
import re

# Load the captured network traffic
with open(r"C:\Vault\Apothecary\40_Experiments\hkex_network_traffic.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find the getequityquote endpoint
for endpoint in data['potential_api_endpoints']:
    if 'getequityquote' in endpoint['url']:
        print("="*80)
        print("FOUND: getequityquote API Endpoint")
        print("="*80)
        print(f"\nURL: {endpoint['url']}")
        print(f"Method: {endpoint['method']}")

        # The response is JSONP (wrapped in jQuery callback)
        response_text = endpoint['response']

        # Extract JSON from JSONP wrapper
        # Format: jQuery35107923502247005435_1769448622391({...json...})
        match = re.search(r'jQuery\d+_\d+\((.*)\)', response_text)
        if match:
            json_str = match.group(1)
            json_data = json.loads(json_str)

            print("\n" + "="*80)
            print("EXTRACTED STOCK DATA")
            print("="*80)

            # Print the full JSON nicely formatted
            print(json.dumps(json_data, indent=2))

            # Extract key fields
            if 'data' in json_data and 'quote' in json_data['data']:
                quote = json_data['data']['quote']

                print("\n" + "="*80)
                print("KEY STOCK INFORMATION")
                print("="*80)

                # Previous close
                if 'prev_close' in quote or 'hc' in quote:
                    prev_close = quote.get('prev_close') or quote.get('hc')
                    print(f"Previous Close: HK${prev_close}")

                # Market cap
                if 'mkt_cap' in quote:
                    mkt_cap = quote.get('mkt_cap')
                    mkt_cap_unit = quote.get('mkt_cap_u', '')
                    print(f"Market Cap: {mkt_cap}{mkt_cap_unit}")

                # Other useful fields
                print(f"\nHigh: {quote.get('hi', 'N/A')}")
                print(f"Low: {quote.get('lo', 'N/A')}")
                print(f"Last: {quote.get('ls', 'N/A')}")
                print(f"Stock Code: {quote.get('ric', 'N/A')}")
                print(f"Currency: {quote.get('ccy', 'N/A')}")
                print(f"Historical Close Date: {quote.get('hist_closedate', 'N/A')}")

                print("\n" + "="*80)
                print("AVAILABLE FIELDS IN QUOTE DATA")
                print("="*80)
                for key in sorted(quote.keys()):
                    print(f"  {key}: {quote[key]}")
        else:
            print("\nCould not extract JSON from JSONP wrapper")

        break
