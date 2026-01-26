# HKEX Daily Quote Automation

**Created:** 2026-01-27  
**Purpose:** Daily headless extraction of HKEX stock quote data into Excel.

---

## Overview
- Extracts Previous Close and Market Cap for stock code 653.
- Writes to a versioned Excel file with a retrieval timestamp.
- Runs daily via Windows Task Scheduler.

---

## Folder Structure (current)
- Project root: `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote`
- Source scripts: `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr`
- Runtime script: `C:\Vault\Apothecary\__automation scripts\!hkex_playwright_quote_page_v0.1.0.py`
- Debug script: `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_quote_page_debugging_v0.1.0.py`
- Input tests:  
  - `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_input_test.py`  
  - `C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_input_test_v2.py`

---

## Scheduled Task
- **Name:** HKEX daily quote  
- **Schedule:** Daily at 19:00  
- **Command:**  
  ```
  "python" "C:\Vault\Apothecary\__automation scripts\!hkex_playwright_quote_page_v0.1.0.py"
  ```
- **Check task:**  
  ```
  schtasks /Query /TN "HKEX daily quote" /V /FO LIST
  ```
- **If task does not run:** Task Scheduler > Properties > Security options > set "Run only when user is logged on".

---

## Output
- **Excel file:**  
  `C:\Users\YC\OneDrive\Desktop\AI hub\Experiment\ex daily quote\hkex_quote.testing.v2.xlsx`
- **Columns:**  
  `Date`, `Retrieved At`, `Stock Code`, `Close`, `Market Cap`, `Market Cap Unit`, `Carried Forward`

---

## How it Works (high level)
1) Open HKEX Equities page.  
2) Enter stock code and press Enter.  
3) Click the stock row in the table.  
4) Extract Previous Close + Market Cap.  
5) Append a new row to Excel (one per day).

---

## Run Manually
**Production (headless):**
```
python "C:\Vault\Apothecary\__automation scripts\!hkex_playwright_quote_page_v0.1.0.py"
```

**Debug (visible browser):**
```
python "C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_quote_page_debugging_v0.1.0.py"
```

---

## Update Workflow
1) Edit the source in `scr\`.
2) Copy to runtime:
```
Copy-Item "C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_quote_page_v0.1.0.py" `
  "C:\Vault\Apothecary\__automation scripts\!hkex_playwright_quote_page_v0.1.0.py" -Force
```
3) If the runtime path changes, update the scheduled task:
```
schtasks /Change /TN "HKEX daily quote" /TR "\"python\" \"C:\Vault\Apothecary\__automation scripts\!hkex_playwright_quote_page_v0.1.0.py\""
```

---

## Dependencies
```
pip install playwright pandas openpyxl
playwright install chromium
```

---

## Troubleshooting
- **No Excel output:** Check the output path and OneDrive sync.  
- **Task fails:** Run manually to see the error.  
- **Input not typing:** Use the debug script to view the UI.  
- **Site change:** Update selectors in the script.

