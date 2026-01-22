---
tags:
  - runbook
  - hkicpa
  - ai/automation
  - python
status: draft
---

# HKICPA Volume II – Download Runbook (CSV-driven)

## What this does
- Downloads all HKICPA Volume II PDFs.
- Uses `hkicpa_manifest.csv` as the master list (filenames live here).
- Output: `downloads/` (or `downloads_clean/` if renaming from raw).
## What you need (one-time setup)
1. Create a folder `C:\HKICPA`
2.  Install dependencies:
```
pip install pandas pypdf requests
```
3.  Save these 6 scripts in the folder:

- `python_attach_urls.py`
- `python_download_from_csv.py`
- `python_download_raw.py`
- `python_extract_links.py`
- `python_generate_manifest.py`
- `python_rename_from_csv.py`
## Every update cycle (step-by-step)
### Step 1: Prepare source files

1. Download **HKICPA Volume II contents PDF** → save as `contentpage.pdf`
2. Open `contentpage.pdf`, select the contents listing (from PREFACE through all entries)
3. Copy and paste into `contents_raw.txt` (UTF-8 text file)
4. Remove page headers/footers (e.g. "contents (10/25)", roman numerals) KEEP:
   - Section headers (`Section 1: ...`, `Section 2: ...`)
   - All entry lines with code, title, and date (e.g. `HKAS 1 Presentation of Financial Statements... 12/07(5/24)`)
### Step 2: Extract URLs from PDF
```powershell
python python_extract_links.py
```
- **Input:** `contentpage.pdf`
- **Output:** `hkicpa_links.txt` (one URL per line, de-duplicated)
### Step 3: Generate manifest draft
- **Input:** `contents_raw.txt`
```
python python_generate_manifest.py
```
- **Output:** `hkicpa_manifest_draft.csv`
- **Columns:** `row`, `section`, `code`, `title`, `issue_review`, `filename`
### Step 4: Review and finalize manifest
1. Open `hkicpa_manifest_draft.csv` in Excel
2. Check codes, titles, filenames, section assignments
3. Fix any edge cases manually if needed
4. **Save as** `hkicpa_manifest.csv` (this becomes your master manifest)
### Step 5: Attach URLs to manifest
- **Inputs:** `hkicpa_manifest.csv` + `hkicpa_links.txt`
- ```powershell
   python python_attach_urls.py
```
- **Output:** Updates `hkicpa_manifest.csv` (adds `url` column)
- **Safeguard:** Aborts if URL count ≠ manifest row count
- **Preservation:** Only touches the `url` column; code/title/filename unchanged
### Step 6: Download PDFs
Choose **one** path:
#### Option A – Direct clean download
- **Input:** `hkicpa_manifest.csv` (must have `url` and `filename` columns)
```powershell
python python_download_from_csv.py
```
- **Output:** `downloads/` folder with PDFs using clean names from manifest
#### Option B – Raw mirror, then rename
```powershell
python python_download_raw.py
python python_rename_from_csv.py
```
- **Raw download:** Creates `downloads_raw/` with original server filenames
- **Rename:** Copies from `downloads_raw/` to `downloads_clean/` with clean names
  
- ***Recommended**: Keeps `downloads_raw/` as backup mirror; no re-download needed if you want to rename again*
## Quick Run (typical workflow)
```powershell
python python_extract_links.py
python python_generate_manifest.py
# Open hkicpa_manifest_draft.csv in Excel, review, save as hkicpa_manifest.csv
python python_attach_urls.py
python python_download_from_csv.py
```
**Output:** `downloads/` folder with ~100 PDFs, each named like `HKAS 1-Presentation of Financial Statements-12-07(5-24).pdf`
## Troubleshooting

### URL count mismatch
If you get "URL count ≠ manifest row count" error:
- Ensure `contents_raw.txt` matches the number of links in `contentpage.pdf`
- Re-run `python_extract_links.py` and check `hkicpa_links.txt`
- Re-run `python_generate_manifest.py` and recount entries
### Download fails or timeouts
- Re-run the download script (it doesn't skip files yet)
- No automatic retry — you must manually re-run
### Filenames look wrong
- Fix in `hkicpa_manifest.csv` (edit the `filename` column in Excel)
- DO NOT manually rename files after download
- Re-run download script to apply changes

## Scripts (where to find them)
[[python_extract_links.py]] — Extracts URLs from PDF annotations
[[python_generate_manifest.py]] — Parses contents into CSV
[[python_attach_urls.py]] — Adds URLs to manifest with safeguard
[[python_download_from_csv.py]] — Downloads with clean filenames
[[python_rename_from_csv.py]] — Renames from raw mirror to clean names

### Optional script
[[python_download_raw.py]] — Downloads raw mirror (for Path B)

## Change Log 
v1.0 used text files; deprecated in favor of CSV manifest workflow.
# Known issues for later improvement

| Issue                     | Impact                                            | Fix                                                                                       |
| ------------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **No error recovery**     | Single download failure stops entire batch        | Add retry logic with exponential backoff                                                  | 
| **Missing validation**    | `contents_raw.txt` parsing errors discovered late | Add pre-flight check for expected format HKICPA-Volume-II-Download-Runbook.md​            |
| **Hard-coded filenames**  | Not reusable for other PDF collections            | Parameterize file paths via config file or CLI args HKICPA-Volume-II-Download-Runbook.md​ |
| **No progress tracking**  | ~100 PDFs with no indication of completion %      | Add progress bar (use library) Canonical-scripts.md​                                      |
| **Manual step at Step 4** | Excel review breaks automation                    | Add flag for trusted runs HKICPA-Volume-II-Download-Runbook.md​                           |
