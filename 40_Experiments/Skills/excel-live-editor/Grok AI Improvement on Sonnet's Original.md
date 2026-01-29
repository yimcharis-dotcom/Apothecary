---
Description: A robust Claude Skill for editing active Excel workbooks using xlwings, with features for discovery, backup, validation, change tracking, and compatibility across environments like IDEs, CLI, and Obsidian.
Tags:
  - Claude/skill
  - Excel
  - Xlwings
  - ai/tools
  - python
  - workflow
  - grok
Created: 2026-01-30
Updated: 2026-01-30
Aliases:
  - Excel-live-editor
  - Claude-excel-skill
Source: Grok AI Improvement on Sonnet's Original
Version: 1
---

# Excel Live Editor Skill

This Claude Skill enables AI-assisted editing of Excel spreadsheets that are already open on your system, using the xlwings library. It addresses the pain point of file-locking issues when collaborating between AI and visual tools like Excel, allowing you to edit data in a more efficient, visual way without needing to switch to Markdown, code, or IDE formats exclusively.

The skill is designed for users who prefer Excel's interface for data manipulation but want AI help for bulk updates, cleaning, or transformations. It keeps Excel open, provides backups, change tracking, and undo capabilities for safety.

## Original Context and Motivation
- **User Pain Point**: Difficulty editing tables or datasets in IDEs, Obsidian, or other environments. Preference for Excel due to familiarity. Issue with CSV/Excel file locking when editing from multiple ends.
- **Original Skill**: Created by Claude Sonnet using xlwings for live connections, with basic editing and diff reporting.
- **Improvements**: Enhanced for robustness (backups, validation, error handling), effectiveness (search/replace, pandas integration), and versatility (discovery functions, flexible connections, compatibility with IDE/CLI/Obsidian/Jupyter).

## When to Use This Skill
- Editing cells in an already open Excel file.
- Bulk updates, corrections, or data transformations.
- Viewing changes with diff reports.
- Keeping Excel open for continued manual work.
- Searching/finding data across sheets.
- AI-assisted data cleaning.

## Requirements
- Windows or macOS with Excel installed.
- Python libraries: `xlwings` (required), `pandas` (optional for advanced ops).
- Excel must be running with the target file open.

## Architecture Overview
```mermaid
flowchart LR
    A[IDE / CLI / Obsidian] -->|xlwings COM/AppleScript| B[Excel App (stays open)]
    B -->|read/write| A
```

## Core Functions

### 1. Discovery: List Open Workbooks and Sheets
Always start here to see available workbooks.

```python
import xlwings as xw

def list_open_workbooks():
    """List all open Excel workbooks and their sheets."""
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
        print("No Excel workbooks are currently open.")
        print("Please open Excel with your file first.")
        return None
    
    print("=== Open Workbooks ===")
    for i, wb in enumerate(result, 1):
        print(f"\n[{i}] {wb['name']}")
        print(f" Path: {wb['path']}")
        print(f" Sheets: {', '.join(wb['sheets'])}")
        print(f" Active: {wb['active_sheet']}")
    
    return result

list_open_workbooks()
```

### 2. Connect to Workbook
Flexible connection handling.

```python
import xlwings as xw

def connect_to_workbook(name=None, sheet=None):
    """
    Connect to an open workbook.
    
    Args:
        name: Workbook name (e.g., 'Book1.xlsx'). If None, uses active workbook.
        sheet: Sheet name or index. If None, uses active sheet.
    
    Returns:
        tuple: (workbook, sheet) objects
    """
    try:
        app = xw.apps.active
        if app is None:
            raise Exception("No Excel application is running")
        
        # Get workbook
        if name:
            # Try exact match first
            try:
                wb = app.books[name]
            except KeyError:
                # Try partial match
                matches = [b for b in app.books if name.lower() in b.name.lower()]
                if len(matches) == 1:
                    wb = matches[0]
                elif len(matches) > 1:
                    raise Exception(f"Multiple matches for '{name}': {[b.name for b in matches]}")
                else:
                    raise Exception(f"No workbook matching '{name}'. Open workbooks: {[b.name for b in app.books]}")
        else:
            wb = app.books.active
        
        # Get sheet
        if sheet is not None:
            if isinstance(sheet, int):
                ws = wb.sheets[sheet]
            else:
                ws = wb.sheets[sheet]
        else:
            ws = wb.sheets.active
        
        print(f"Connected to: {wb.name} → Sheet: {ws.name}")
        return wb, ws
        
    except Exception as e:
        print(f"Connection Error: {e}")
        print("\nTroubleshooting:")
        print(" 1. Is Excel running?")
        print(" 2. Is the file open in Excel?")
        print(" 3. Run list_open_workbooks() to see available files")
        return None, None

# Usage
wb, sheet = connect_to_workbook('Book1.csv')
# or
wb, sheet = connect_to_workbook() # Use active workbook/sheet
```

### 3. Backup Before Changes
Always create a backup.

```python
import xlwings as xw
from datetime import datetime
import os

def create_backup(wb, backup_dir=None):
    """
    Create a backup copy of the workbook before making changes.
    
    Args:
        wb: xlwings Workbook object
        backup_dir: Directory for backups. Defaults to same folder as original.
    
    Returns:
        str: Path to backup file, or None if failed
    """
    try:
        original_path = wb.fullname
        original_dir = os.path.dirname(original_path)
        original_name = os.path.basename(original_path)
        name_part, ext = os.path.splitext(original_name)
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{name_part}_backup_{timestamp}{ext}"
        
        # Determine backup location
        if backup_dir:
            os.makedirs(backup_dir, exist_ok=True)
            backup_path = os.path.join(backup_dir, backup_name)
        else:
            backup_path = os.path.join(original_dir, backup_name)
        
        # Save a copy
        wb.save() # Save current state first
        wb.api.SaveCopyAs(backup_path)
        
        print(f"✓ Backup created: {backup_path}")
        return backup_path
        
    except Exception as e:
        print(f"⚠ Backup failed: {e}")
        print(" Proceeding without backup. Consider manual backup.")
        return None
```

### 4. Read Operations

```python
def read_cell(sheet, cell):
    """Read a single cell value."""
    return sheet.range(cell).value

def read_range(sheet, range_str):
    """Read a range of cells as 2D list."""
    return sheet.range(range_str).value

def read_column(sheet, col, start_row=1, end_row=None):
    """Read an entire column or portion of it."""
    if end_row:
        return sheet.range(f'{col}{start_row}:{col}{end_row}').value
    else:
        # Find last used row
        last_row = sheet.range(f'{col}1').end('down').row
        return sheet.range(f'{col}{start_row}:{col}{last_row}').value

def read_row(sheet, row_num, start_col='A', end_col=None):
    """Read an entire row or portion of it."""
    if end_col:
        return sheet.range(f'{start_col}{row_num}:{end_col}{row_num}').value
    else:
        last_col = sheet.range(f'A{row_num}').end('right').column
        return sheet.range((row_num, 1), (row_num, last_col)).value

def get_used_range_info(sheet):
    """Get information about the used range in the sheet."""
    used = sheet.used_range
    return {
        'first_row': used.row,
        'first_col': used.column,
        'last_row': used.last_cell.row,
        'last_col': used.last_cell.column,
        'rows': used.rows.count,
        'cols': used.columns.count,
        'address': used.address
    }

# Usage examples:
# value = read_cell(sheet, 'A1')
# data = read_range(sheet, 'A1:D10')
# col_a = read_column(sheet, 'A', start_row=2) # Skip header
# info = get_used_range_info(sheet)
```

### 5. Write Operations with Change Tracking

```python
from datetime import datetime

class ChangeTracker:
    """Track all changes made during a session for diff/undo."""
    
    def __init__(self):
        self.changes = []
    
    def record(self, sheet_name, cell, old_value, new_value):
        self.changes.append({
            'sheet': sheet_name,
            'cell': cell,
            'old': old_value,
            'new': new_value,
            'timestamp': datetime.now().isoformat()
        })
    
    def show_diff(self):
        """Display all changes made."""
        if not self.changes:
            print("No changes recorded.")
            return
        
        print("\n" + "="*60)
        print("CHANGES MADE")
        print("="*60)
        
        for i, c in enumerate(self.changes, 1):
            old_display = repr(c['old']) if c['old'] is not None else '(empty)'
            new_display = repr(c['new']) if c['new'] is not None else '(empty)'
            print(f"{i:3}. [{c['sheet']}] {c['cell']}: {old_display} → {new_display}")
        
        print("="*60)
        print(f"Total: {len(self.changes)} changes")
    
    def get_undo_script(self):
        """Generate a script to undo all changes."""
        if not self.changes:
            return "# No changes to undo"
        
        lines = ["# Undo script - run to revert changes", ""]
        for c in reversed(self.changes):
            old_val = repr(c['old'])
            lines.append(f"sheet.range('{c['cell']}').value = {old_val}")
        
        return "\n".join(lines)

# Global tracker instance
tracker = ChangeTracker()

def write_cell(sheet, cell, value, track=True):
    """Write a single cell with change tracking."""
    old_value = sheet.range(cell).value
    sheet.range(cell).value = value
    
    if track:
        tracker.record(sheet.name, cell, old_value, value)
    
    return old_value

def write_cells(sheet, updates, track=True):
    """
    Write multiple cells at once.
    
    Args:
        sheet: xlwings Sheet object
        updates: dict of {cell: value} or list of (cell, value) tuples
    
    Returns:
        list of (cell, old_value, new_value) tuples
    """
    results = []
    
    if isinstance(updates, dict):
        updates = updates.items()
    
    for cell, new_value in updates:
        old_value = write_cell(sheet, cell, new_value, track=track)
        results.append((cell, old_value, new_value))
    
    return results

def write_column_values(sheet, col, values, start_row=1, track=True):
    """
    Write values to a column starting at specified row.
    
    Args:
        sheet: xlwings Sheet object
        col: Column letter (e.g., 'A')
        values: List of values to write
        start_row: Starting row number
    """
    for i, value in enumerate(values):
        cell = f'{col}{start_row + i}'
        write_cell(sheet, cell, value, track=track)
```

### 6. Search and Find

```python
def find_value(sheet, search_term, column=None, exact=False):
    """
    Find cells containing a value.
    
    Args:
        sheet: xlwings Sheet object
        search_term: Value to search for
        column: Limit search to specific column (e.g., 'A')
        exact: If True, match exactly. If False, partial match for strings.
    
    Returns:
        List of dicts with cell address, value, row, column
    """
    results = []
    used = sheet.used_range
    
    for row in range(used.row, used.last_cell.row + 1):
        col_start = used.column
        col_end = used.last_cell.column + 1
        
        # If column specified, only search that column
        if column:
            col_idx = ord(column.upper()) - ord('A') + 1
            col_start = col_idx
            col_end = col_idx + 1
        
        for col in range(col_start, col_end):
            cell = sheet.range((row, col))
            value = cell.value
            
            if value is None:
                continue
            
            # Check for match
            match = False
            if exact:
                match = (value == search_term)
            else:
                # Partial match for strings
                if isinstance(value, str) and isinstance(search_term, str):
                    match = search_term.lower() in value.lower()
                else:
                    match = (value == search_term)
            
            if match:
                results.append({
                    'address': cell.address,
                    'value': value,
                    'row': row,
                    'column': col,
                    'column_letter': chr(ord('A') + col - 1)
                })
    
    return results

def find_and_replace(sheet, find_text, replace_text, column=None, exact=False, track=True):
    """
    Find and replace values in sheet.
    
    Returns:
        Number of replacements made
    """
    matches = find_value(sheet, find_text, column=column, exact=exact)
    
    for match in matches:
        cell = match['address'].replace('$', '')
        old_value = match['value']
        
        if exact:
            new_value = replace_text
        else:
            # Partial replacement for strings
            if isinstance(old_value, str):
                new_value = old_value.replace(find_text, replace_text)
            else:
                new_value = replace_text
        
        write_cell(sheet, cell, new_value, track=track)
    
    print(f"Replaced {len(matches)} occurrences")
    return len(matches)
```

### 7. Pandas Integration (Optional)
For advanced data operations.

```python
import pandas as pd
import xlwings as xw

def sheet_to_dataframe(sheet, header_row=1):
    """Convert sheet data to pandas DataFrame."""
    # Get used range
    used = sheet.used_range
    data = used.value
    
    if not data:
        return pd.DataFrame()
    
    # If header_row specified, use that row as column names
    if header_row and len(data) > header_row - 1:
        headers = data[header_row - 1]
        data = data[header_row:]
        df = pd.DataFrame(data, columns=headers)
    else:
        df = pd.DataFrame(data)
    
    return df

def dataframe_to_sheet(sheet, df, start_cell='A1', include_header=True, track=False):
    """
    Write DataFrame to sheet.
    
    Note: This overwrites existing data. Consider backup first.
    """
    if include_header:
        # Write header
        sheet.range(start_cell).value = [df.columns.tolist()]
        # Adjust start for data
        start_row = int(start_cell[1:]) + 1
        data_start = f'{start_cell[0]}{start_row}'
    else:
        data_start = start_cell
    
    # Write data
    sheet.range(data_start).value = df.values.tolist()
    
    print(f"Wrote {len(df)} rows × {len(df.columns)} columns starting at {start_cell}")

# Example: Clean data using pandas
# df = sheet_to_dataframe(sheet)
# df['Name'] = df['Name'].str.strip() # Remove whitespace
# df['Date'] = pd.to_datetime(df['Date']) # Parse dates
# dataframe_to_sheet(sheet, df, include_header=True)
```

### 8. Save and Finalize

```python
def save_workbook(wb, show_diff=True):
    """Save the workbook and optionally show changes made."""
    global tracker
    
    try:
        wb.save()
        print(f"\n✓ Saved: {wb.name}")
        
        if show_diff and tracker.changes:
            tracker.show_diff()
        
        print("\n💡 Excel remains open. You can continue editing.")
        
    except Exception as e:
        print(f"✗ Save failed: {e}")
        print(" Try saving manually in Excel (Ctrl+S)")

def finish_session(wb, save=True, show_diff=True, show_undo=False):
    """
    Complete an editing session.
    
    Args:
        wb: Workbook object
        save: Whether to save changes
        show_diff: Whether to display changes made
        show_undo: Whether to print undo script
    """
    global tracker
    
    if save:
        save_workbook(wb, show_diff=show_diff)
    
    if show_undo and tracker.changes:
        print("\n--- UNDO SCRIPT (save this to revert) ---")
        print(tracker.get_undo_script())
        print("--- END UNDO SCRIPT ---")
    
    # Reset tracker for next session
    tracker = ChangeTracker()
```

## Complete Workflow Examples

### Example 1: Simple Cell Updates

```python
import xlwings as xw

# 1. Connect
wb, sheet = connect_to_workbook('data.csv')
if not wb:
    raise SystemExit("Cannot proceed without connection")

# 2. Backup
create_backup(wb)

# 3. Make changes
updates = {
    'A31': 'Quora',
    'A35': 'ggml.ai',
    'A38': 'Microsoft',
}
write_cells(sheet, updates)

# 4. Save and show diff
finish_session(wb)
```

### Example 2: Find and Replace

```python
import xlwings as xw

wb, sheet = connect_to_workbook()
create_backup(wb)

# Find all cells containing "Corp." and replace with "Corporation"
find_and_replace(sheet, 'Corp.', 'Corporation', exact=False)

finish_session(wb)
```

### Example 3: Bulk Column Cleanup

```python
import xlwings as xw

wb, sheet = connect_to_workbook('companies.xlsx')
create_backup(wb)

# Read column A to find issues
col_data = read_column(sheet, 'A', start_row=2) # Skip header

# Define corrections based on analysis
corrections = {
    'A5': 'Apple Inc.', # Was "APPLE"
    'A12': 'Google LLC', # Was "google"
    'A23': 'Microsoft', # Was "MSFT"
}
write_cells(sheet, corrections)

finish_session(wb, show_undo=True)
```

### Example 4: Data Validation Before Write

```python
import xlwings as xw

def validate_and_write(sheet, updates, validators=None):
    """
    Validate data before writing.
    
    validators: dict of {column: validation_function}
    """
    errors = []
    valid_updates = {}
    
    for cell, value in updates.items():
        col = cell[0] # Extract column letter
        
        if validators and col in validators:
            is_valid, error_msg = validators[col](value)
            if not is_valid:
                errors.append(f"{cell}: {error_msg}")
                continue
        
        valid_updates[cell] = value
    
    if errors:
        print("Validation errors:")
        for e in errors:
            print(f" ✗ {e}")
        print(f"\nSkipped {len(errors)} invalid entries")
    
    if valid_updates:
        write_cells(sheet, valid_updates)
        print(f"Wrote {len(valid_updates)} valid entries")
    
    return len(errors) == 0

# Example validators
def not_empty(value):
    if not value or (isinstance(value, str) and not value.strip()):
        return False, "Value cannot be empty"
    return True, None

def is_number(value):
    try:
        float(value)
        return True, None
    except (ValueError, TypeError):
        return False, f"'{value}' is not a number"

# Usage
wb, sheet = connect_to_workbook()
updates = {'A1': 'Test', 'B1': '', 'C1': 'not-a-number'}
validate_and_write(sheet, updates, validators={
    'B': not_empty,
    'C': is_number
})
```

## Error Recovery

### If Excel Crashes
```python
# Your changes are tracked. To recover:
print(tracker.changes) # See what was changed
# If you saved a backup:
# 1. Reopen Excel
# 2. Open the backup file
# 3. Reapply changes if needed
```

### If Script Fails Mid-Edit
```python
# Check current state
wb, sheet = connect_to_workbook()
print(f"Current A31: {read_cell(sheet, 'A31')}")

# The tracker still has recorded changes
tracker.show_diff()

# Generate undo script if needed
print(tracker.get_undo_script())
```

## Compatibility Notes

| Environment | Works? | Notes |
|-------------|--------|-------|
| Windows + Excel | ✅ | Full support via COM |
| macOS + Excel | ✅ | Full support via AppleScript |
| Linux | ❌ | No Excel available |
| VS Code | ✅ | Run in terminal or notebook |
| PyCharm | ✅ | Run in console |
| Obsidian (Templater) | ✅ | With Python path configured |
| Jupyter | ✅ | Each cell can interact |
| CLI | ✅ | Run as script |

This skill integrates well with other tools:
- **MCP (Model Context Protocol)**: Can connect to external data sources for importing into Excel.
- **Other Claude Skills**: Composable with data-analysis or report-generation Skills.
- **External Tools**: Use with Git for version control of backups, or automate via CLI scripts in workflows.

## Tips
1. Always run `list_open_workbooks()` first to see what's available.
2. Create backups before bulk changes.
3. Use the tracker—it's your safety net.
4. Make changes in small batches and save often.
5. Verify changes visually in Excel.
6. Save undo scripts for important edits.

## Summary of Improvements

| Aspect | Original | Improved |
|--------|----------|----------|
| **Discovery** | None | List open workbooks, sheet info |
| **Connection** | Hardcoded names | Flexible, partial matching, error guidance |
| **Safety** | None | Backup creation, change tracking, undo scripts |
| **Validation** | None | Pre-write validation framework |
| **Search** | None | Find, find-and-replace |
| **Pandas** | None | DataFrame conversion for complex ops |
| **Error handling** | Basic | Comprehensive with recovery guidance |
| **Documentation** | Minimal | Complete with examples |

This enhanced skill provides a more reliable and versatile workflow for AI-assisted Excel editing. For further customizations, such as specific data transformations or integrations, provide more details!