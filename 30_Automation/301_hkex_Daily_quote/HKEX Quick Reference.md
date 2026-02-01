---
title: HKEX Quick Reference - Cheat Sheet
tags:
  - automation
  - reference
  - cheatsheet
  - commands
  - quick-lookup
created: 2026-01-27
type: reference
related:
  - "[[Untitled 1/README]]"
  - "[[HKEX Code Guide]]"
  - "[[HKEX_Session_Transfer_Summary 1]]"
---

# HKEX Quick Reference

**Purpose:** Quick lookup for commands, paths, and common tasks.

**Learning how it works?** → [[HKEX Code Guide]]

**Just getting started?** → [[Untitled 1/README]]

---

## Quick Commands

### Run the Script

**Production (headless):**
```powershell
python "C:\Vault\Apothecary\__automation scripts\!hkex_playwright_quote_page_v0.1.0.py"
```

**Debug (visible browser):**
```powershell
python "C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_quote_page_debugging_v0.1.0.py"
```

**Test input only:**
```powershell
python "C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_input_test.py"
```

---

## File Locations

### Scripts

| File | Location | Purpose |
|------|----------|---------|
| Production script | `C:\Vault\Apothecary\__automation scripts\!hkex_playwright_quote_page_v0.1.0.py` | Runs daily (headless) |
| Debug script | `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_quote_page_debugging_v0.1.0.py` | For troubleshooting |
| Source (production) | `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_quote_page_v0.1.0.py` | Edit here, then copy |
| Source (debug) | `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_quote_page_debugging_v0.1.0.py` | Edit here |
| Input test | `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_input_test.py` | Test search box |

### Output

| File | Location |
|------|----------|
| Excel data | `C:\Users\YC\OneDrive\Desktop\AI hub\Experiment\ex daily quote\hkex_quote.testing.v2.xlsx` |
| Screenshots | Same folder as script (e.g., `after_typing_debug.png`) |

### Documentation

| File | Location | Purpose |
|------|----------|---------|
| README | `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\README.md` | Start here |
| Code Guide | `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\HKEX Code Guide.md` | Learning resource |
| Quick Reference | `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\HKEX Quick Reference.md` | This file |
| Session Transfer | `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\HKEX_Session_Transfer_Summary.md` | Technical history |
| Automation Guide | `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\HKEX_Daily_Quote_Automation.md` | Setup guide |

---

## Scheduled Task Commands

### Check Status
```powershell
schtasks /Query /TN "HKEX daily quote" /V /FO LIST
```

### Enable/Disable
```powershell
# Disable (pause automation)
schtasks /Change /TN "HKEX daily quote" /DISABLE

# Enable (resume automation)
schtasks /Change /TN "HKEX daily quote" /ENABLE
```

### Change Schedule
```powershell
# Change time to 8:00 PM
schtasks /Change /TN "HKEX daily quote" /ST 20:00

# Change time to 6:30 AM
schtasks /Change /TN "HKEX daily quote" /ST 06:30
```

### Update Script Path
```powershell
schtasks /Change /TN "HKEX daily quote" /TR "\"python\" \"C:\Path\To\New\Script.py\""
```

### Delete Task
```powershell
schtasks /Delete /TN "HKEX daily quote"
```

### Create New Task
```powershell
schtasks /Create /TN "HKEX daily quote" /TR "\"python\" \"C:\Vault\Apothecary\__automation scripts\!hkex_playwright_quote_page_v0.1.0.py\"" /SC DAILY /ST 19:00 /RU YC
```

---

## Important Variables

### In the Script (Lines 20-22)

```python
STOCK_CODE = "653"
OUTPUT_DIR = r"C:\Users\YC\OneDrive\Desktop\AI hub\Experiment\ex daily quote"
EXCEL_FILE = os.path.join(OUTPUT_DIR, "hkex_quote.testing.v2.xlsx")
```

**To change stock code:** Edit `STOCK_CODE = "653"` to another stock number

**To change output location:** Edit `OUTPUT_DIR` path

---

## CSS Selectors

### Current Selectors (If Website Changes, Update These)

| Element | Selector | Line # | Purpose |
|---------|----------|--------|---------|
| Search input | `input#tags` | 74 | Where we type stock code |
| Search input (alt) | `input[placeholder*="Stock Code" i]` | 81 | Backup selector |
| Previous Close | `dt.col_prevcls` | 200 | Extract price |
| Market Cap | `dt.col_mktcap` | 207 | Extract market cap |
| Stock link | `a:has-text("653")` | 185 | Click stock in results |
| Table rows | `table tbody tr` | 144 | Count results |

**How to find new selectors:** See [[HKEX Code Guide#How to Find Selectors]]

---

## URLs

### HKEX Pages

| Page | URL |
|------|-----|
| Landing page | `https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=en` |
| Quote page (direct) | `https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym=653&sc_lang=en` |

**Direct URL approach:** Replace `653` with any stock code

---

## Excel Schema

### Columns in Output File

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| Date | String | 2026-01-27 | Date of data (YYYY-MM-DD) |
| Retrieved At | String | 2026-01-27 19:00:00 | Exact timestamp |
| Stock Code | String | 653 | Stock code (normalized, no leading zeros) |
| Close | Float | 0.127 | Previous close price (HK$) |
| Market Cap | Float | 221.80 | Market cap value |
| Market Cap Unit | String | M | M=Million, B=Billion, T=Trillion |
| Carried Forward | Boolean | False | True if using yesterday's data |

---

## Regex Patterns

### Used in the Script

**Extract price (Line 216):**
```python
r'([\d,]+\.?\d*)'
```
- Matches: `0.127`, `1,234.56`, `999`
- From: "HK$0.127" → extracts `0.127`

**Extract market cap (Line 222):**
```python
r'([\d,]+\.?\d*)\s*([MBT])'
```
- Matches: `221.80M`, `1.5 B`, `2T`
- From: "HK$221.80M" → extracts `221.80` and `M`

**Learn more:** [[HKEX Code Guide#Understanding the Regex]]

---

## Error Messages Decoded

### Common Errors and What They Mean

| Error | Meaning | Fix |
|-------|---------|-----|
| `TimeoutError: Timeout 30000ms exceeded` | Element didn't appear in time | Increase timeout or check if element exists |
| `Error: No data extracted from page` | Couldn't find price/market cap | Check if selectors are still correct |
| `FileNotFoundError` | Excel file path doesn't exist | Check OUTPUT_DIR, create folder if needed |
| `PermissionError` | Excel file is open | Close Excel and try again |
| `playwright._impl._api_types.Error: Executable doesn't exist` | Chromium not installed | Run `playwright install chromium` |

### Task Scheduler Error Codes

| Last Result | Meaning | Fix |
|-------------|---------|-----|
| 0 | Success ✅ | All good! |
| 1 | Incorrect function | Check script path |
| 267011 | Task has not run yet | Wait for scheduled time |
| 267009 | Task is currently running | Wait for it to finish |

---

## Update Workflow

### When You Modify the Script

**Step 1:** Edit the source file
```
C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_quote_page_v0.1.0.py
```

**Step 2:** Test it
```powershell
python "C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_quote_page_v0.1.0.py"
```

**Step 3:** Copy to runtime location
```powershell
Copy-Item "C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_quote_page_v0.1.0.py" "C:\Vault\Apothecary\__automation scripts\!hkex_playwright_quote_page_v0.1.0.py" -Force
```

**Step 4:** Test the scheduled task
```powershell
schtasks /Run /TN "HKEX daily quote"
```

---

## Dependencies

### Install/Reinstall

```powershell
# Install Python packages
pip install playwright pandas openpyxl

# Install Chromium browser
playwright install chromium

# Check versions
pip show playwright
pip show pandas
pip show openpyxl
```

### Current Versions (as of 2026-01-27)

- Python: 3.x
- Playwright: Latest
- Pandas: Latest
- Openpyxl: Latest

---

## Timeouts Reference

### Key Timeout Values in Script

| Action | Timeout | Line # | Adjustable? |
|--------|---------|--------|-------------|
| Page load | 45s (prod) / 90s (debug) | 58 | Yes |
| Network idle | 45s (prod) / 90s (debug) | 61 | Yes |
| Search input | 15s (prod) / 30s (debug) | 74 | Yes |
| Filter results | 2s (prod) / 5s (debug) | 141 | Yes |
| Quote page load | 30s (prod) / 60s (debug) | 193 | Yes |
| Data elements | 15s (prod) / 30s (debug) | 200 | Yes |

**To increase timeout:** Change the `timeout=` parameter

**Example:**
```python
page.wait_for_selector('dt.col_prevcls', state='visible', timeout=30000)
# Change to 60 seconds:
page.wait_for_selector('dt.col_prevcls', state='visible', timeout=60000)
```

---

## Debugging Checklist

### When Something Goes Wrong

**Step 1:** Run debug version
```powershell
python "C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_quote_page_debugging_v0.1.0.py"
```

**Step 2:** Check screenshots
- `after_typing_debug.png` - Did text appear in search box?
- `filtered_results_debug.png` - Does stock 653 appear in results?

**Step 3:** Read the logs
- Look for the last successful step
- Check error messages

**Step 4:** Common fixes
- [ ] Internet connection working?
- [ ] OneDrive synced?
- [ ] Excel file not open?
- [ ] Logged into Windows?
- [ ] HKEX website accessible?

**Step 5:** Check if website changed
- Open `https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym=653&sc_lang=en`
- Right-click → Inspect
- Check if `dt.col_prevcls` still exists

---

## Common Modifications

### Change Stock Code
**File:** Line 20
```python
STOCK_CODE = "700"  # Tencent
```

### Change Excel File Name
**File:** Line 22
```python
EXCEL_FILE = os.path.join(OUTPUT_DIR, "my_stocks.xlsx")
```

### Make Browser Visible (for debugging)
**File:** Line 41
```python
headless=False  # Change from True
```

### Slow Down Execution (easier to watch)
**File:** Line 43
```python
slow_mo=500  # Add delay in milliseconds
```

### Add More Data Fields
See [[HKEX Code Guide#Add More Data Fields]]

---

## Screenshot Reference

### Screenshots Created by Debug Version

| File | When Created | Shows |
|------|--------------|-------|
| `after_typing_debug.png` | After typing in search box | Search box with "653" typed (should have red border) |
| `filtered_results_debug.png` | After search results load | Table of stocks (should include stock 653) |
| `input_test_after_typing.png` | Input test script | Search box after typing |
| `input_test_after_apply.png` | Input test script | Results after applying filters |
| `input_test_after_stock_click.png` | Input test script | Quote page after clicking stock |

**Location:** Same folder where you run the script

---

## Alternative Approaches

### Direct URL Method (Faster, More Reliable)

**Instead of:** Landing page → Search → Click → Extract

**Use:** Direct URL → Extract

**Code snippet:**
```python
url = f"https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym={stock_code}&sc_lang=en"
page.goto(url, wait_until='networkidle', timeout=60000)
page.wait_for_selector('dt.col_prevcls', state='visible', timeout=30000)
# Extract data...
```

**Full implementation:** See [[HKEX_Session_Transfer_Summary 1#THE WORKING CODE]]

**Advantages:**
- ✅ 10x faster (3s vs 30s)
- ✅ More reliable
- ✅ Simpler code

---

## Quick Troubleshooting

### Problem: Stock not found in results
**Solution:** Known issue. Try direct URL approach or company name search.
**See:** [[HKEX_Session_Transfer_Summary 1#WHY NAVIGATION APPROACH FAILED]]

### Problem: Timeout errors
**Solution:** Increase timeout values or check internet connection.
**See:** [[#Timeouts Reference]]

### Problem: Task didn't run
**Solution:** Check if logged in. Task runs in "Interactive only" mode.
**See:** [[Untitled 1/README#Scheduled Automation]]

### Problem: Excel file not updating
**Solution:** Check if file is open in Excel. Close it and try again.

### Problem: "Carried Forward = True" in Excel
**Solution:** Script failed to get fresh data. Run manually to see error.
**See:** [[HKEX Code Guide#Part 7 Error Handling]]

---

## Related Documentation

- **[[Untitled 1/README]]** - Start here! Quick overview and basic usage
- **[[HKEX Code Guide]]** - Learn how the code works (detailed explanations)
- **[[HKEX_Session_Transfer_Summary 1]]** - Technical deep dive and alternative approaches
- **[[HKEX_Daily_Quote_Automation]]** - Original automation setup guide

---

## External Resources

- [Playwright Python Docs](https://playwright.dev/python/) - Official documentation
- [Pandas Documentation](https://pandas.pydata.org/) - Working with DataFrames
- [Regex101](https://regex101.com/) - Test regex patterns
- [HKEX Website](https://www.hkex.com.hk/) - The source

---

**Last Updated:** 2026-01-27

**Quick tip:** Bookmark this page in Obsidian for fast access! 📌
