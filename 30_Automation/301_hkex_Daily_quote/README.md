---
title: HKEX Daily Quote Scraper - README
tags:
  - automation
  - python
  - playwright
  - daily-task
  - stock-data
created: 2026-01-27
status: active
automation: scheduled-daily-19:00
stock: "653"
related:
  - "[[HKEX Code Guide]]"
  - "[[HKEX Quick Reference]]"
  - "[[HKEX_Session_Transfer_Summary 1]]"
  - "[[HKEX_Daily_Quote_Automation]]"
---

# HKEX Daily Quote Scraper

**What it does:** Automatically grabs the stock price and market cap for HKEX stock 653 every day and saves it to Excel.

**Status:** ✅ Running daily at 7:00 PM via Windows Task Scheduler

---

## Quick Start

### Run It Manually

**Production (invisible):**
```powershell
python "C:\Vault\Apothecary\__automation scripts\!hkex_playwright_quote_page_v0.1.0.py"
```

**Debug (see what's happening):**
```powershell
python "C:\Vault\Apothecary\30_Automation\301_hkex_Daily_quote\scr\hkex_playwright_quote_page_debugging_v0.1.0.py"
```

### See the Data

Open the Excel file:
```
C:\Users\YC\OneDrive\Desktop\AI hub\Experiment\ex daily quote\hkex_quote.testing.v2.xlsx
```

---

## How It Works (Simple Version)

1. 🌐 Opens HKEX website
2. 🔍 Searches for stock code "653"
3. 🖱️ Clicks on the stock in results
4. 📊 Grabs **Previous Close** price and **Market Cap**
5. 💾 Saves to Excel with today's date

**If it fails:** Uses yesterday's data (marked as "Carried Forward")

---

## Scheduled Automation

### Current Schedule

- **Task Name:** `HKEX daily quote`
- **Runs:** Every day at **7:00 PM**
- **Status:** Enabled ✅
- **User:** YC (Interactive only)
- **Script:** `C:\Vault\Apothecary\__automation scripts\!hkex_playwright_quote_page_v0.1.0.py`

### Check Task Status

```powershell
schtasks /Query /TN "HKEX daily quote" /V /FO LIST
```

### Manage the Task

**Disable (pause automation):**
```powershell
schtasks /Change /TN "HKEX daily quote" /DISABLE
```

**Enable (resume automation):**
```powershell
schtasks /Change /TN "HKEX daily quote" /ENABLE
```

**Change the time (example: 8:00 PM):**
```powershell
schtasks /Change /TN "HKEX daily quote" /ST 20:00
```

**Delete the task:**
```powershell
schtasks /Delete /TN "HKEX daily quote"
```

> 💡 **Note:** Task runs in "Interactive only" mode, so you need to be logged in for it to work.

---

## Troubleshooting

### "Stock not found in results"
- The search might not be working properly
- Run the [[#Debug (see what's happening)|debug version]] to see what's happening
- Check the screenshots it creates: `filtered_results_debug.png`

### "Timeout error"
- Website is slow or down
- Try running it again
- Check your internet connection

### "No Excel file created"
- Check if OneDrive is synced
- Make sure the output folder exists
- Run the debug version to see the error

### "Task didn't run"
- Check if you were logged in at 7:00 PM
- Check Task Scheduler: `schtasks /Query /TN "HKEX daily quote"`
- Look at "Last Result" - if not `0`, there was an error

### "Carried Forward = True" in Excel
- Means the script failed to get fresh data
- It used yesterday's data instead
- Check what went wrong by running manually

---

## Learn More

- **[[HKEX Code Guide]]** - Understand how the code works (learning-focused)
- **[[HKEX Quick Reference]]** - Commands, paths, and quick fixes (cheat sheet)
- **[[HKEX_Session_Transfer_Summary 1]]** - Technical history and alternative approaches
- **[[HKEX_Daily_Quote_Automation]]** - Original automation setup guide

---

## Files in This Project

### Scripts (in `scr/` folder)
- `hkex_playwright_quote_page_v0.1.0.py` - Production version (headless)
- `hkex_playwright_quote_page_debugging_v0.1.0.py` - Debug version (visible browser)
- `hkex_playwright_input_test.py` - Test if search box works
- `hkex_playwright_input_test_v2.py` - Simplified input test

### Documentation
- `README.md` - This file (start here!)
- `HKEX Code Guide.md` - How the code works
- `HKEX Quick Reference.md` - Cheat sheet
- `HKEX_Session_Transfer_Summary.md` - Technical deep dive
- `HKEX_Daily_Quote_Automation.md` - Setup guide

### Runtime
- `C:\Vault\Apothecary\__automation scripts\!hkex_playwright_quote_page_v0.1.0.py` - The script that runs daily

---

## What Data Gets Saved

Each day, one row is added to the Excel file:

| Column | Example | Description |
|--------|---------|-------------|
| Date | 2026-01-27 | Today's date |
| Retrieved At | 2026-01-27 19:00:00 | Exact time data was grabbed |
| Stock Code | 653 | The stock code |
| Close | 0.127 | Previous close price (HK$) |
| Market Cap | 221.80 | Market capitalization value |
| Market Cap Unit | M | Unit (M=Million, B=Billion, T=Trillion) |
| Carried Forward | False | True if using yesterday's data |

---

## Dependencies

If you need to reinstall:

```powershell
pip install playwright pandas openpyxl
playwright install chromium
```

---

## Quick Tips

- 🐛 **Debugging?** Use the debug version - it shows the browser and takes screenshots
- 📁 **Moving files?** Update the scheduled task path with `schtasks /Change`
- 🔄 **Want more stocks?** See [[HKEX Code Guide#Adding More Stocks]]
- ⏰ **Change schedule?** See [[#Manage the Task]] above

---

**Last Updated:** 2026-01-27
