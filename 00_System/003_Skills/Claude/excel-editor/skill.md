---
name: excel-editor
description: Edit active Excel workbooks using xlwings Python library. Connects to open Excel instances, makes cell updates, saves changes, and leaves Excel open for the user to continue working.
---

# Excel Editor Skill

This skill enables direct editing of active Excel workbooks using the xlwings Python library. It connects to your currently open Excel instance, makes changes, saves, and leaves Excel open.

## When to Use This Skill

Use this skill when:
- User asks to edit specific cells in an open Excel file
- User wants to update multiple rows/columns in Excel
- User needs bulk data corrections in Excel
- User wants to see a diff of changes made to Excel data
- User has Excel open and wants changes without closing/reopening

## Requirements

- xlwings Python library installed (`pip install xlwings`)
- Excel must be open on Windows
- Python must be available

## Key Functions

### 1. Connect to Active Excel

```python
import xlwings as xw

# Connect to active Excel app
app = xw.apps.active
wb = app.books['YourFile.csv']  # or .xlsx
sheet = wb.sheets[0]  # First sheet
```

### 2. Read Cell Values

```python
# Read single cell
value = sheet.range('A1').value

# Read range
data = sheet.range('A1:C10').value

# Read entire column
col_data = sheet.range('A:A').value
```

### 3. Write Cell Values

```python
# Write single cell
sheet.range('A1').value = 'New Value'

# Write multiple cells
sheet.range('A1').value = [['Row1', 'Data'], ['Row2', 'More']]

# Update specific row
sheet.range(f'A{row_num}').value = 'Updated'
```

### 4. Save and Keep Open

```python
# Save changes
wb.save()

# DO NOT close - leave Excel open for user
# Do NOT call wb.close()
```

## Workflow Example

When user asks to correct provider names in Column A:

1. **Connect to active Excel**
```python
app = xw.apps.active
wb = app.books['Book1.csv']
sheet = wb.sheets[0]
```

2. **Show current values**
```python
print(f"Row 31 current: {sheet.range('A31').value}")
```

3. **Make changes**
```python
sheet.range('A31').value = 'Quora'
sheet.range('A35').value = 'ggml.ai'
# ... more changes
```

4. **Save**
```python
wb.save()
print('Changes saved!')
```

5. **Show diff**
```python
changes = [
    (31, 'POE (Quora)', 'Quora'),
    (35, 'Llama.cpp', 'ggml.ai'),
]
for row, old, new in changes:
    current = sheet.range(f'A{row}').value
    status = 'OK' if current == new else 'MISMATCH'
    print(f'Row {row}: {old} → {new} | Current: {current} [{status}]')
```

## Important Notes

- **Always save** after making changes: `wb.save()`
- **Never close** the workbook: Do NOT use `wb.close()`
- **User keeps control**: Leave Excel open so user can continue working
- **Show diffs**: Always show before/after comparison so user knows what changed
- **Handle errors**: If no active Excel, inform user to open Excel first

## Error Handling

```python
try:
    app = xw.apps.active
    wb = app.books['Book1.csv']
except Exception as e:
    print(f'Error: {e}')
    print('Please make sure Excel is open with Book1.csv loaded.')
```

## Example: Bulk Column Update

```python
import xlwings as xw

# Connect
app = xw.apps.active
wb = app.books['Book1.csv']
sheet = wb.sheets[0]

# Define changes
updates = {
    31: 'Quora',
    35: 'ggml.ai',
    38: 'Microsoft',
}

# Apply changes
print('Applying changes to Column A:')
for row, new_value in updates.items():
    old_value = sheet.range(f'A{row}').value
    sheet.range(f'A{row}').value = new_value
    print(f'  Row {row}: {old_value} → {new_value}')

# Save
wb.save()
print('\nChanges saved! Excel remains open.')
```

## Tips

1. **Verify before changing**: Always read current value first
2. **Batch changes**: Group multiple edits into one script for efficiency
3. **Show progress**: Print status as changes are made
4. **Validate after**: Check that changes were applied correctly
5. **Keep user informed**: Show clear before/after comparisons
