---
title: HKEX Code Guide - How It Works
tags:
  - automation
  - learning
  - code-explanation
  - playwright
  - python
  - web-scraping
created: 2026-01-27
purpose: learning
difficulty: beginner-friendly
related:
  - "[[Untitled 1/README]]"
  - "[[HKEX Quick Reference]]"
  - "[[hkex_playwright_quote_page_v0.1.0.py]]"
  - "[[hkex_playwright_quote_page_debugging_v0.1.0.py]]"
---

# HKEX Code Guide - How It Works

**Purpose:** Understand how the HKEX scraper works so you can modify and maintain it.

**Start here if:** You want to learn how the code works, not just run it.

**Just want to run it?** → [[Untitled 1/README]]

---

## Table of Contents

- [[#The Big Picture]]
- [[#Main Script Structure]]
- [[#Part 1 Browser Setup]]
- [[#Part 2 Finding the Search Box]]
- [[#Part 3 Typing and Searching]]
- [[#Part 4 Clicking the Stock]]
- [[#Part 5 Extracting Data]]
- [[#Part 6 Saving to Excel]]
- [[#Part 7 Error Handling]]
- [[#Common Modifications]]
- [[#Understanding the Selectors]]

---

## The Big Picture

Think of this script as a **robot that does what you'd do manually**:

1. 🌐 Opens a web browser (Chrome)
2. 🔍 Goes to HKEX website
3. ⌨️ Types "653" in the search box
4. 🖱️ Clicks on the stock in the results
5. 👀 Reads the price and market cap from the page
6. 💾 Writes it to an Excel file

**The tool we use:** [Playwright](https://playwright.dev/) - it controls the browser like a human would.

---

## Main Script Structure

The script has these main functions:

```python
def extract_stock_data_playwright(stock_code)  # Does steps 1-5
def parse_market_cap(cap_str, unit_str)        # Cleans up the market cap data
def load_last_row(df, sym)                     # Gets yesterday's data (fallback)
def main()                                      # Runs everything
```

**Flow:**
```
main() 
  → extract_stock_data_playwright()  [gets data from website]
  → parse_market_cap()                [cleans the data]
  → Save to Excel
  → If error: load_last_row()         [use yesterday's data]
```

---

## Part 1: Browser Setup

**Location:** Lines 38-51 in [[hkex_playwright_quote_page_v0.1.0.py]]

```python
browser = p.chromium.launch(
    headless=True,
    args=['--start-maximized'],
    slow_mo=0
)
```

### What This Does
- **`chromium.launch()`** - Opens Chrome browser
- **`headless=True`** - Runs invisibly (no window)
- **`--start-maximized`** - Opens full screen
- **`slow_mo=0`** - No delay between actions (fast)

### You Can Change
- **`headless=False`** - See the browser window (for debugging)
- **`slow_mo=200`** - Add 200ms delay between actions (easier to watch)

**Debug version uses:** `headless=False, slow_mo=200`

---

### Browser Context

```python
context = browser.new_context(
    no_viewport=True,
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0'
)
```

### What This Does
- **`no_viewport=True`** - Use full screen size (not a fixed size)
- **`user_agent`** - Pretends to be a regular Chrome browser

**Why?** Some websites block bots. This makes us look like a real user.

---

## Part 2: Finding the Search Box

**Location:** Lines 68-85

```python
search_input = page.get_by_role("textbox", name=re.compile(r"Stock Code", re.I))
if search_input.count() == 0:
    search_input = page.locator('input#tags[placeholder*="Stock Code" i]').first
if search_input.count() == 0:
    search_input = page.locator('#hkexw-equities .searchbox input#tags').first
if search_input.count() == 0:
    search_input = all_tags.first
```

### What This Does
Tries **4 different ways** to find the search box (most reliable first):

1. **By role** - Looks for a textbox with "Stock Code" in the name
2. **By placeholder** - Finds `<input>` with placeholder containing "Stock Code"
3. **By CSS path** - Specific location in the page structure
4. **By ID** - Just finds any `input#tags` element

### Why Multiple Strategies?
If HKEX changes their website slightly, one method might fail but another still works.

**This is called "defensive coding"** - plan for things to break!

---

### Making the Search Box Visible (Debug Mode)

```python
page.evaluate(
    "el => { el.style.outline='3px solid red'; el.style.background='#ffffcc'; }",
    search_handle
)
```

### What This Does
- Adds a **red border** around the search box
- Makes the background **yellow**
- So you can see exactly what element it found

**Only in debug version!** Helps you verify it found the right element.

---

## Part 3: Typing and Searching

**Location:** Lines 95-139

### Step 3a: Click the Search Box

```python
box = search_input.bounding_box()
if box:
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
```

### What This Does
- Gets the position of the search box on screen
- Moves the mouse to the center of it
- Clicks it (to focus)

**Why not just `.click()`?** Sometimes that doesn't work if the element is hidden or behind something.

---

### Step 3b: Type the Stock Code

```python
page.keyboard.press("Control+A")
page.keyboard.type(stock_code, delay=120)
```

### What This Does
- **`Control+A`** - Select all text (clear any existing text)
- **`type()`** - Types "653" character by character
- **`delay=120`** - Waits 120ms between keystrokes (looks more human)

---

### Step 3c: Fallback (If Typing Didn't Work)

```python
if actual_value.strip() != stock_code:
    page.evaluate(f"""() => {{
        const input = document.querySelector('input[placeholder*="Stock" i]');
        if (input) {{
            input.value = '{stock_code}';
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
    }}""")
```

### What This Does
- Checks if the typing actually worked
- If not, uses **JavaScript** to directly set the value
- Triggers the `input` event (tells the website something was typed)

**Why?** Sometimes UI typing fails due to website quirks. This is the backup plan.

---

### Step 3d: Apply the Search

```python
search_input.press('Enter')
page.wait_for_timeout(2000)
```

### What This Does
- Presses Enter key (submits the search)
- Waits 2 seconds for results to load

**Alternative:** Could click "APPLY FILTERS" button, but Enter is simpler.

---

## Part 4: Clicking the Stock

**Location:** Lines 143-194

### Step 4a: Check If Stock Appears

```python
table_rows = page.locator('table tbody tr').count()
stock_found = page.locator(f'a:has-text("{stock_code}")').count() > 0
```

### What This Does
- Counts how many rows are in the results table
- Checks if any link contains "653"

**Known Issue:** Sometimes stock 653 doesn't appear in results! See [[HKEX_Session_Transfer_Summary 1#WHY NAVIGATION APPROACH FAILED]].

---

### Step 4b: Fallback - Try Company Name

```python
if not stock_found:
    page.evaluate("""() => {
        const input = document.querySelector('input[placeholder*="Stock"]');
        if (input) {
            input.value = 'China Overseas Grand Oceans';
            // ...
        }
    }""")
```

### What This Does
If searching by stock code "653" didn't work, try searching by company name instead.

**Company name:** "China Overseas Grand Oceans"

---

### Step 4c: Click the Stock Link

```python
stock_link = page.locator(f'a:has-text("{stock_code}")').first
stock_link.click()
page.wait_for_load_state('networkidle', timeout=30000)
```

### What This Does
- Finds the first link containing "653"
- Clicks it
- Waits for the new page to fully load (up to 30 seconds)

**`networkidle`** means "wait until no more network requests for 500ms" - ensures page is done loading.

---

## Part 5: Extracting Data

**Location:** Lines 196-225

### Step 5a: Wait for Data Elements

```python
page.wait_for_selector('dt.col_prevcls', state='visible', timeout=15000)
```

### What This Does
Waits up to 15 seconds for the "Previous Close" element to appear on the page.

**Why wait?** The page might load in stages. We need to wait for the actual data to appear.

---

### Step 5b: Extract the Text

```python
prev_close_element = page.locator('dt.col_prevcls').first
prev_close_text = prev_close_element.text_content()

mkt_cap_element = page.locator('dt.col_mktcap').first
mkt_cap_text = mkt_cap_element.text_content()
```

### What This Does
- Finds the HTML elements containing the data
- Gets the text inside them

**Example values:**
- `prev_close_text` = "HK$0.127"
- `mkt_cap_text` = "HK$221.80M"

---

### Step 5c: Parse the Values

```python
# Parse Previous Close
match = re.search(r'([\d,]+\.?\d*)', prev_close_text.replace(',', ''))
if match:
    stock_data['prev_close'] = match.group(1)

# Parse Market Cap
match = re.search(r'([\d,]+\.?\d*)\s*([MBT])', mkt_cap_text.replace(',', ''))
if match:
    stock_data['market_cap'] = match.group(1)
    stock_data['market_cap_unit'] = match.group(2)
```

### What This Does
Uses **regex (regular expressions)** to extract just the numbers:

**Previous Close:**
- Input: "HK$0.127"
- Regex finds: "0.127"
- Saves: `'prev_close': '0.127'`

**Market Cap:**
- Input: "HK$221.80M"
- Regex finds: "221.80" and "M"
- Saves: `'market_cap': '221.80'`, `'market_cap_unit': 'M'`

---

### Understanding the Regex

```python
r'([\d,]+\.?\d*)'
```

Breaking it down:
- `[\d,]+` - One or more digits or commas (e.g., "1,234")
- `\.?` - Optional decimal point
- `\d*` - Zero or more digits after decimal
- `()` - Capture this part

**Matches:** 0.127, 221.80, 1,234.56

---

```python
r'([\d,]+\.?\d*)\s*([MBT])'
```

Breaking it down:
- `([\d,]+\.?\d*)` - The number (same as above)
- `\s*` - Optional whitespace
- `([MBT])` - One letter: M, B, or T
- `()` - Capture both parts separately

**Matches:** "221.80M", "1.5 B", "2T"

---

## Part 6: Saving to Excel

**Location:** Lines 274-345 in `main()`

### Step 6a: Prepare the Data Row

```python
row = {
    "Date": today.strftime("%Y-%m-%d"),
    "Retrieved At": retrieved_at,
    "Stock Code": sym,
    "Close": close_val,
    "Market Cap": mkt_val,
    "Market Cap Unit": mkt_unit,
    "Carried Forward": False,
}
```

### What This Does
Creates a dictionary (like a table row) with all the data for today.

**Example:**
```python
{
    "Date": "2026-01-27",
    "Retrieved At": "2026-01-27 19:00:00",
    "Stock Code": "653",
    "Close": 0.127,
    "Market Cap": 221.80,
    "Market Cap Unit": "M",
    "Carried Forward": False
}
```

---

### Step 6b: Load Existing Excel File

```python
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
    df = df[~((df["Date"] == row["Date"]) & (df["Stock Code"] == row["Stock Code"]))]
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
else:
    df = pd.DataFrame([row])
```

### What This Does

**If Excel file exists:**
1. Load it into a DataFrame (pandas table)
2. Remove any existing row for today (prevents duplicates)
3. Add the new row

**If Excel file doesn't exist:**
- Create a new DataFrame with just this one row

---

### Step 6c: Save to Excel

```python
df.to_excel(EXCEL_FILE, index=False)
```

### What This Does
- Saves the DataFrame to Excel
- `index=False` - Don't add row numbers as a column

**File location:** `C:\Users\YC\OneDrive\Desktop\AI hub\Experiment\ex daily quote\hkex_quote.testing.v2.xlsx`

---

## Part 7: Error Handling

**Location:** Lines 310-333

### The Fallback Strategy

```python
except Exception as e:
    logging.error(f"Extraction failed: {e}")
    
    # Load yesterday's data
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        last = load_last_row(df, sym)
    
    if last:
        row = {
            "Date": today.strftime("%Y-%m-%d"),
            "Retrieved At": retrieved_at,
            "Stock Code": sym,
            "Close": last["Close"],
            "Market Cap": last.get("Market Cap"),
            "Market Cap Unit": last.get("Market Cap Unit"),
            "Carried Forward": True,  # ← Mark as old data
        }
```

### What This Does

**If extraction fails:**
1. Log the error
2. Load the Excel file
3. Get the last row for stock 653
4. Use that data but with today's date
5. Set `Carried Forward = True` (so you know it's not fresh)

**Why?** Better to have yesterday's data than no data at all!

---

## Common Modifications

### Change the Stock Code

**File:** Both `.py` files, Line 20

```python
STOCK_CODE = "653"  # ← Change this
```

**Example:** To track stock 700 (Tencent):
```python
STOCK_CODE = "700"
```

**Also update:** Line 158 if using company name fallback

---

### Change the Excel File Location

**File:** Both `.py` files, Lines 21-22

```python
OUTPUT_DIR = r"C:\Users\YC\OneDrive\Desktop\AI hub\Experiment\ex daily quote"
EXCEL_FILE = os.path.join(OUTPUT_DIR, "hkex_quote.testing.v2.xlsx")
```

**Example:** Save to Documents folder:
```python
OUTPUT_DIR = r"C:\Users\YC\Documents\Stock Data"
EXCEL_FILE = os.path.join(OUTPUT_DIR, "hkex_quotes.xlsx")
```

**Don't forget:** Update the scheduled task path! See [[Untitled 1/README#Manage the Task]]

---

### Add More Data Fields

**Step 1:** Find the CSS selector on the HKEX page (use browser DevTools)

**Step 2:** Add extraction code (around Line 207):
```python
# Extract Day Range
day_range_element = page.locator('dt.col_dayrange').first
day_range_text = day_range_element.text_content()
stock_data['day_range'] = day_range_text
```

**Step 3:** Add to the row dictionary (around Line 296):
```python
row = {
    "Date": today.strftime("%Y-%m-%d"),
    "Retrieved At": retrieved_at,
    "Stock Code": sym,
    "Close": close_val,
    "Market Cap": mkt_val,
    "Market Cap Unit": mkt_unit,
    "Day Range": stock_data.get('day_range'),  # ← New field
    "Carried Forward": False,
}
```

---

### Track Multiple Stocks

**Option 1:** Run the script multiple times with different stock codes

**Option 2:** Modify the script to loop through multiple stocks:

```python
STOCK_CODES = ["653", "700", "1299"]  # Multiple stocks

for stock_code in STOCK_CODES:
    stock_data = extract_stock_data_playwright(stock_code)
    # ... save to Excel ...
```

**Note:** This will take longer (3-5 minutes per stock).

---

### Change the Schedule Time

See [[Untitled 1/README#Manage the Task]] or [[HKEX Quick Reference#Scheduled Task Commands]]

```powershell
schtasks /Change /TN "HKEX daily quote" /ST 20:00
```

---

## Understanding the Selectors

### What Are CSS Selectors?

CSS selectors are patterns that identify HTML elements on a webpage.

**Think of it like an address:**
- `dt.col_prevcls` = "Find a `<dt>` element with class `col_prevcls`"
- `input#tags` = "Find an `<input>` element with id `tags`"
- `table tbody tr` = "Find `<tr>` elements inside `<tbody>` inside `<table>`"

---

### The Selectors We Use

| Selector | What It Finds | Purpose |
|----------|---------------|---------|
| `input#tags` | Search input box | Where we type stock code |
| `dt.col_prevcls` | Previous close price | Extract price data |
| `dt.col_mktcap` | Market cap | Extract market cap |
| `table tbody tr` | Table rows | Count results |
| `a:has-text("653")` | Link containing "653" | Click the stock |

---

### How to Find Selectors (If Website Changes)

1. Open the HKEX page in Chrome
2. Right-click the element → "Inspect"
3. Look at the HTML in DevTools
4. Find unique identifiers:
   - `id="something"` → Use `#something`
   - `class="something"` → Use `.something`
   - Combination: `<dt class="col_prevcls">` → Use `dt.col_prevcls`

**Test it:** In DevTools Console, type:
```javascript
document.querySelector('dt.col_prevcls')
```
If it returns the element, the selector works!

---

## Debugging Tips

### Use the Debug Version

```powershell
python "C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_quote_page_debugging_v0.1.0.py"
```

**What it does differently:**
- Shows the browser window
- Runs slower (200ms between actions)
- Takes screenshots
- Keeps browser open 10 seconds on error

---

### Check the Screenshots

The script creates these images:
- `after_typing_debug.png` - After typing in search box
- `filtered_results_debug.png` - After search results appear

**Look for:**
- Is the search box highlighted (red border, yellow background)?
- Did the text actually appear in the search box?
- Does stock 653 appear in the results table?

---

### Read the Logs

The script prints detailed logs:

```
2026-01-27 19:00:00 - INFO - Step 1: Loading landing page
2026-01-27 19:00:05 - INFO - Landing page loaded
2026-01-27 19:00:05 - INFO - Step 2: Searching for stock 653
2026-01-27 19:00:06 - INFO - Search box contains: '653'
```

**If something fails, the logs will tell you where.**

---

### Common Issues and Fixes

**"Element not found"**
- Selector might be wrong
- Page might not be fully loaded
- Try increasing timeout values

**"Timeout waiting for selector"**
- Website is slow
- Element doesn't exist (website changed)
- Check if you can see it manually in the browser

**"Stock not found in results"**
- Known issue! See [[HKEX_Session_Transfer_Summary 1#WHY NAVIGATION APPROACH FAILED]]
- Consider using the direct URL approach instead

---

## Alternative Approach: Direct URL

**Current approach:** Landing page → Search → Click → Extract

**Alternative:** Go directly to the quote page

```python
url = f"https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym={stock_code}&sc_lang=en"
page.goto(url, wait_until='networkidle', timeout=60000)

# Then extract directly (skip all the search stuff)
page.wait_for_selector('dt.col_prevcls', state='visible', timeout=30000)
# ... extract data ...
```

**Advantages:**
- ✅ 10x faster (3 seconds vs 30+ seconds)
- ✅ More reliable (fewer steps to fail)
- ✅ Simpler code

**See:** [[HKEX_Session_Transfer_Summary 1#THE WORKING CODE]] for full implementation

---

## Learn More

- **[[Untitled 1/README]]** - Quick start and basic usage
- **[[HKEX Quick Reference]]** - Commands and paths cheat sheet
- **[[HKEX_Session_Transfer_Summary 1]]** - Deep technical dive and alternatives
- **[Playwright Docs](https://playwright.dev/python/)** - Official documentation
- **[Pandas Docs](https://pandas.pydata.org/)** - Working with DataFrames

---

**Questions?** Try running the debug version and watching what happens!

**Last Updated:** 2026-01-27
