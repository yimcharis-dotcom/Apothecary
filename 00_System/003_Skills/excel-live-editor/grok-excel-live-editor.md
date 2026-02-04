---
name: excel-live-editor
description: Edit active Excel workbooks using xlwings. Connects to open Excel instances, provides discovery, backup, validation, change tracking, and leaves Excel open for continued user work. Ideal for AI-assisted data editing in environments like IDEs, CLI, or Obsidian where visual Excel interface is preferred over MD or code formats.
license: MIT
metadata:
  author: Grok AI (based on Claude Sonnet's original)
  version: "1.1"
  category: data-editing
  requirements: xlwings, pandas (optional)
---
# Excel Live Editor Skill

This skill enables AI-assisted editing of Excel spreadsheets that are already open on your system, using the xlwings library. It addresses file-locking issues when collaborating between AI and visual tools like Excel, allowing efficient, visual data manipulation without switching to Markdown, code, or IDE formats exclusively.

Use this skill when the user prefers Excel's interface for data work but needs AI help for bulk updates, cleaning, or transformations. It keeps Excel open, provides backups, change tracking, and undo capabilities for safety.

## When to Use This Skill
- The task involves editing cells, ranges, columns, or rows in an open Excel file.
- Bulk updates, corrections, data cleaning, or transformations are needed.
- Searching, finding, or replacing values across sheets.
- Generating diff reports or undo scripts for changes.
- Integrating with pandas for complex data operations.
- Keeping Excel open for manual verification and continued editing.
- Working in environments like IDEs (VS Code, PyCharm), CLI, Jupyter, or Obsidian where direct Excel interaction is beneficial.

Do not use if:
- The file is not already open in Excel.
- No Python environment with xlwings is available (Claude can guide installation if needed).
- The task is purely read-only or doesn't require live editing.

## Requirements
- Windows or macOS with Microsoft Excel installed.
- Python libraries: `pip install xlwings` (required), `pip install pandas` (optional for advanced operations).
- Excel must be running with the target workbook open.
- For Obsidian or other non-IDE environments: Ensure Python is configured (e.g., via Templater plugin or external script runner).

## Step-by-Step Instructions
1. **Assess the Task**: Understand the user's request. Identify the workbook, sheet, and specific edits (e.g., cell updates, find/replace, data cleaning).
2. **Discover Open Workbooks**: Always start by listing open workbooks to confirm availability. Use the `list_open_workbooks()` function.
3. **Connect to Workbook**: Use `connect_to_workbook(name, sheet)` with flexible matching. Handle errors gracefully and suggest troubleshooting.
4. **Create Backup**: Before any writes, call `create_backup(wb)` to save a timestamped copy.
5. **Read Data**: Use read functions (e.g., `read_cell`, `read_range`, `read_column`) to analyze current data. Optionally convert to pandas DataFrame for complex analysis.
6. **Validate Changes**: If applicable, use `validate_and_write` with custom validators to ensure data integrity.
7. **Make Changes**: Use write functions (e.g., `write_cell`, `write_cells`, `find_and_replace`) with tracking enabled.
8. **Integrate Pandas (if needed)**: For bulk transformations, convert sheet to DataFrame, process, and write back.
9. **Finalize Session**: Call `finish_session(wb)` to save, show diff, and optionally provide undo script. Remind user that Excel remains open.
10. **Error Handling**: If issues arise, use recovery steps like checking tracker or restoring from backup.
11. **Output to User**: Provide a summary of changes, diff, and any undo instructions. Suggest visual verification in Excel.

## Core Scripts
Place these in the `scripts/` folder or execute them inline via Claude's code execution. All functions assume `import xlwings as xw` and other imports as needed.

### Discovery and Connection
```python
def list_open_workbooks():
    result = []
    for app in xw.apps:
        for wb in app.books:
            sheets = [s.name for s in wb.sheets]
            result.append({
                'name': wb.name,
                'path': wb.fullname,
                'sheets': sheets,
                'active_sheet': wb.sheets.active.name
            })
    if not result:
        return "No open workbooks. Open Excel first."
    return result

def connect_to_workbook(name=None, sheet=None):
    app = xw.apps.active
    if not app:
        raise Exception("No Excel running.")
    if name:
        matches = [b for b in app.books if name.lower() in b.name.lower()]
        if len(matches) != 1:
            raise Exception("Ambiguous or no match for workbook.")
        wb = matches[0]
    else:
        wb = app.books.active
    ws = wb.sheets[sheet] if sheet else wb.sheets.active
    return wb, ws
```

### Backup
```python
from datetime import datetime
import os

def create_backup(wb, backup_dir=None):
    original_path = wb.fullname
    name_part, ext = os.path.splitext(os.path.basename(original_path))
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{name_part}_backup_{timestamp}{ext}"
    backup_path = os.path.join(backup_dir or os.path.dirname(original_path), backup_name)
    wb.save()
    wb.api.SaveCopyAs(backup_path)
    return backup_path
```

### Read Operations
```python
def read_cell(sheet, cell):
    return sheet.range(cell).value

def read_range(sheet, range_str):
    return sheet.range(range_str).value

# Additional read functions as in the full code...
```

### Change Tracking and Write Operations
```python
class ChangeTracker:
    def __init__(self):
        self.changes = []
    def record(self, sheet_name, cell, old, new):
        self.changes.append({'sheet': sheet_name, 'cell': cell, 'old': old, 'new': new, 'timestamp': datetime.now().isoformat()})
    def show_diff(self):
        # Implementation as in full code...
    def get_undo_script(self):
        # Implementation as in full code...

tracker = ChangeTracker()

def write_cell(sheet, cell, value, track=True):
    old = sheet.range(cell).value
    sheet.range(cell).value = value
    if track:
        tracker.record(sheet.name, cell, old, value)
    return old

# Additional write functions...
```

### Search and Replace
```python
def find_value(sheet, search_term, column=None, exact=False):
    # Implementation as in full code...

def find_and_replace(sheet, find_text, replace_text, column=None, exact=False, track=True):
    # Implementation as in full code...
```

### Pandas Integration
```python
import pandas as pd

def sheet_to_dataframe(sheet, header_row=1):
    # Implementation as in full code...

def dataframe_to_sheet(sheet, df, start_cell='A1', include_header=True):
    # Implementation as in full code...
```

### Finalize
```python
def save_workbook(wb, show_diff=True):
    wb.save()
    if show_diff:
        tracker.show_diff()

def finish_session(wb, save=True, show_diff=True, show_undo=False):
    if save:
        save_workbook(wb, show_diff)
    if show_undo:
        print(tracker.get_undo_script())
    global tracker
    tracker = ChangeTracker()
```

### Validation
```python
def validate_and_write(sheet, updates, validators=None):
    # Implementation as in full code...
```

## Examples
### Example 1: Simple Updates
User: "Update cells A 1 to 'Hello' and B 2 to 42 in my open Book 1. Xlsx"
- Connect: wb, sheet = connect_to_workbook ('Book 1')
- Backup: create_backup (wb)
- Write: write_cells (sheet, {'A 1': 'Hello', 'B 2': 42})
- Finish: finish_session (wb, show_diff=True)

Output: Summary of changes, diff, and confirmation Excel is open.

### Example 2: Data Cleaning with Pandas
User: "Clean column A in my data sheet by stripping whitespace"
- Connect and backup.
- Df = sheet_to_dataframe (sheet)
- Df['A'] = df['A']. Str.Strip ()
- Dataframe_to_sheet (sheet, df)
- Finish with diff.

## Guidelines & Best Practices
- Always backup before writes.
- Use small batches for changes to avoid overwhelming Excel.
- Verify connections and provide user-friendly error messages.
- For Obsidian: Integrate via Python scripts or plugins; run code externally if needed.
- Compatibility: Works in IDEs, CLI, Jupyter; for broader tools, combine with MCP for external data.
- If errors: Guide user to check Excel status, run discovery, or restore backup.

## Error Recovery
- Use tracker. Show_diff () to review changes.
- Generate undo script and instruct user to run it on a backup copy.
- If crash: Reopen backup and reapply if needed.
```
```

### Implementation Walkthrough
To implement this as a Claude Skill:

1. **Create the Folder**: Make a directory named `excel-live-editor` in your Claude Skills location (e.g., `~/.claude/skills/` for global or `.claude/skills/` for project-specific).

2. **Add SKILL. Md**: Copy the entire Markdown content above into a file named `SKILL.md` inside the folder. This is the core—Claude loads it dynamically.

3. **Add Scripts Folder (Optional but Recommended)**: Create a `scripts/` subfolder. Extract the Python code blocks from SKILL. Md into separate .py files (e.g., `discovery.py`, `backup.py`) for modularity. In SKILL. Md, reference them like "Run scripts/discovery. Py".

4. **Install Dependencies**: Ensure xlwings and pandas are installed in your Python env: `pip install xlwings pandas`.

5. **Test in Claude**: Open Claude. Ai or API, describe a task like "Edit my open Excel file: update A 1 to 'Test'". Claude should auto-invoke the skill if the description matches.

6. **For Obsidian Integration**: Use Obsidian's Templater or Advanced URI plugins to run Python scripts. Or, document the skill in an Obsidian note (as in previous response) and copy-paste code to a terminal/IDE when needed.

7. **Versatility Enhancements**: For external compatibility, add MCP hooks in instructions (e.g., fetch data from APIs and import to Excel). For internal, stack with other Skills like data-analysis.

If issues, refine the description in YAML for better matching, or add more examples. Let me know if you need tweaks!