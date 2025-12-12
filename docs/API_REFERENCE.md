# Python API Reference

Complete reference documentation for the ascii-guard Python API.

**Version**: 1.6.0+
**Status**: Stable Public API

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Functions](#api-functions)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Examples](#examples)

---

## Installation

```bash
pip install ascii-guard
```

---

## Quick Start

```python
from ascii_guard import lint_file, fix_file

# Lint a file
result = lint_file("README.md")
if result.has_errors:
    print(f"Found {len(result.errors)} errors")

# Fix a file
result = fix_file("README.md")
print(f"Fixed {result.boxes_fixed} boxes")
```

---

## API Functions

### `lint_file()`

Lint a file for ASCII art alignment issues.

**Signature:**
```python
def lint_file(
    file_path: str | Path,
    exclude_code_blocks: bool = False
) -> LintResult
```

**Parameters:**
- `file_path` (str | Path): Path to file to lint
- `exclude_code_blocks` (bool): If True, skip ASCII boxes inside markdown code blocks. Default: False

**Returns:**
- `LintResult`: Results object with errors and warnings

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `OSError`: If file cannot be read
- `ValueError`: If file_path is invalid

**Example:**
```python
from ascii_guard import lint_file
from pathlib import Path

# Lint a file
result = lint_file("README.md")

# Check results
if result.is_clean:
    print("File is clean!")
else:
    print(f"Found {len(result.errors)} errors")
    for error in result.errors:
        print(f"  Line {error.line + 1}: {error.message}")

# Works with Path objects too
result = lint_file(Path("docs/guide.md"))
```

---

### `fix_file()`

Fix ASCII art alignment issues in a file.

**Signature:**
```python
def fix_file(
    file_path: str | Path,
    dry_run: bool = False,
    exclude_code_blocks: bool = False
) -> FixResult
```

**Parameters:**
- `file_path` (str | Path): Path to file to fix
- `dry_run` (bool): If True, don't write changes to file. Default: False
- `exclude_code_blocks` (bool): If True, skip ASCII boxes inside markdown code blocks. Default: False

**Returns:**
- `FixResult`: Results object with fixed lines and metadata

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `OSError`: If file cannot be read/written
- `ValueError`: If file_path is invalid

**Example:**
```python
from ascii_guard import fix_file

# Preview fixes without applying
result = fix_file("README.md", dry_run=True)
print(f"Would fix {result.boxes_fixed} boxes")

# Actually fix the file
result = fix_file("README.md")
if result.modified:
    print(f"Fixed {result.boxes_fixed} boxes")
    print(f"File modified: {result.file_path}")
else:
    print("No fixes needed")
```

---

### `detect_boxes()`

Detect ASCII art boxes in a file without validation.

**Signature:**
```python
def detect_boxes(
    file_path: str | Path,
    exclude_code_blocks: bool = False
) -> list[Box]
```

**Parameters:**
- `file_path` (str | Path): Path to file to analyze
- `exclude_code_blocks` (bool): If True, skip ASCII boxes inside markdown code blocks. Default: False

**Returns:**
- `list[Box]`: List of detected Box objects

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `OSError`: If file cannot be read
- `ValueError`: If file_path is invalid

**Example:**
```python
from ascii_guard import detect_boxes

boxes = detect_boxes("README.md")
print(f"Found {len(boxes)} ASCII art boxes")

for box in boxes:
    print(f"Box at line {box.top_line + 1}: {box.width}x{box.height}")
    print(f"  Lines: {box.top_line + 1} to {box.bottom_line + 1}")
```

---

### `validate_box()`

Validate a single Box object.

**Signature:**
```python
def validate_box(box: Box) -> list[ValidationError]
```

**Parameters:**
- `box` (Box): Box object to validate

**Returns:**
- `list[ValidationError]`: List of validation errors (empty if box is valid)

**Example:**
```python
from ascii_guard import detect_boxes, validate_box

boxes = detect_boxes("README.md")
for box in boxes:
    errors = validate_box(box)
    if errors:
        print(f"Box at line {box.top_line + 1} has {len(errors)} errors:")
        for error in errors:
            print(f"  {error}")
```

---

### `fix_box()`

Fix alignment issues in a single box.

**Signature:**
```python
def fix_box(box: Box) -> list[str]
```

**Parameters:**
- `box` (Box): Box object to fix

**Returns:**
- `list[str]`: List of fixed lines (replacement for `box.lines`)

**Example:**
```python
from ascii_guard import detect_boxes, validate_box, fix_box

boxes = detect_boxes("README.md")
for box in boxes:
    errors = validate_box(box)
    if errors:
        fixed_lines = fix_box(box)
        # Apply fixed_lines to file at box.top_line
        print(f"Fixed box at line {box.top_line + 1}")
```

---

## Data Models

### `Box`

Represents an ASCII art box structure.

**Fields:**
- `top_line` (int): Line number of top border (0-indexed)
- `bottom_line` (int): Line number of bottom border (0-indexed)
- `left_col` (int): Column of left border (0-indexed)
- `right_col` (int): Column of right border (0-indexed)
- `lines` (list[str]): All lines of the box
- `file_path` (str): Source file path

**Properties:**
- `width` (int): Box width in characters
- `height` (int): Box height in lines

**Example:**
```python
from ascii_guard import detect_boxes

boxes = detect_boxes("README.md")
for box in boxes:
    print(f"Box: {box.width}x{box.height}")
    print(f"Location: line {box.top_line + 1}, col {box.left_col + 1}")
    print(f"Lines: {len(box.lines)}")
```

---

### `ValidationError`

Represents a validation error in an ASCII art box.

**Fields:**
- `line` (int): Line number (0-indexed)
- `column` (int): Column number (0-indexed)
- `message` (str): Error description
- `severity` (str): 'error' or 'warning'
- `fix` (str | None): Suggested fix (optional)

**Methods:**
- `__str__()`: Format error for display (returns "Line X, Col Y: message")

**Example:**
```python
from ascii_guard import lint_file

result = lint_file("README.md")
for error in result.errors:
    print(f"{error}")  # Uses __str__()
    print(f"  Severity: {error.severity}")
    if error.fix:
        print(f"  Suggested fix: {error.fix}")
```

---

### `LintResult`

Results from linting a file.

**Fields:**
- `file_path` (str): Path to the linted file
- `boxes_found` (int): Number of boxes detected
- `errors` (list[ValidationError]): List of validation errors
- `warnings` (list[ValidationError]): List of validation warnings

**Properties:**
- `has_errors` (bool): True if there are any errors
- `has_warnings` (bool): True if there are any warnings
- `is_clean` (bool): True if file is clean (no errors or warnings)

**Example:**
```python
from ascii_guard import lint_file

result = lint_file("README.md")
print(f"File: {result.file_path}")
print(f"Boxes found: {result.boxes_found}")
print(f"Errors: {len(result.errors)}")
print(f"Warnings: {len(result.warnings)}")
print(f"Clean: {result.is_clean}")
```

---

### `FixResult`

Results from fixing a file.

**Fields:**
- `file_path` (str): Path to the fixed file
- `boxes_fixed` (int): Number of boxes that were fixed
- `lines` (list[str]): Fixed file lines
- `modified` (bool): True if file was actually modified

**Properties:**
- `was_modified` (bool): Alias for `modified`

**Example:**
```python
from ascii_guard import fix_file

result = fix_file("README.md")
print(f"File: {result.file_path}")
print(f"Boxes fixed: {result.boxes_fixed}")
print(f"Modified: {result.modified}")
print(f"Total lines: {len(result.lines)}")
```

---

## Error Handling

All API functions raise standard Python exceptions:

- `FileNotFoundError`: File doesn't exist
- `OSError`: File I/O errors (read/write permissions, encoding issues)
- `ValueError`: Invalid parameters

**Example:**
```python
from ascii_guard import lint_file
from pathlib import Path

try:
    result = lint_file("README.md")
    if result.is_clean:
        print("File is clean!")
except FileNotFoundError:
    print("File not found")
except OSError as e:
    print(f"Error reading file: {e}")
except ValueError as e:
    print(f"Invalid parameter: {e}")
```

---

## Examples

### Complete Workflow

```python
from ascii_guard import lint_file, fix_file

# 1. Lint to check for issues
result = lint_file("README.md")

if result.has_errors:
    print(f"Found {len(result.errors)} errors")

    # 2. Fix the file
    fix_result = fix_file("README.md")

    if fix_result.modified:
        print(f"Fixed {fix_result.boxes_fixed} boxes")

        # 3. Verify fixes
        verify_result = lint_file("README.md")
        if verify_result.is_clean:
            print("All issues fixed!")
    else:
        print("No fixes applied")
else:
    print("File is already clean")
```

### Programmatic Box Processing

```python
from ascii_guard import detect_boxes, validate_box, fix_box
from pathlib import Path

# Detect boxes
boxes = detect_boxes("README.md")

# Process each box
for box in boxes:
    print(f"Processing box at line {box.top_line + 1}")

    # Validate
    errors = validate_box(box)
    if errors:
        print(f"  Found {len(errors)} errors")

        # Fix
        fixed_lines = fix_box(box)
        print(f"  Fixed to {len(fixed_lines)} lines")

        # Apply to file (pseudo-code)
        # with open(box.file_path, 'r') as f:
        #     lines = f.readlines()
        # lines[box.top_line:box.bottom_line+1] = fixed_lines
        # with open(box.file_path, 'w') as f:
        #     f.writelines(lines)
```

### Batch Processing

```python
from ascii_guard import lint_file
from pathlib import Path

# Process multiple files
files = ["README.md", "docs/guide.md", "docs/FAQ.md"]
total_errors = 0

for file_path in files:
    result = lint_file(file_path)
    if result.has_errors:
        print(f"{file_path}: {len(result.errors)} errors")
        total_errors += len(result.errors)
    else:
        print(f"{file_path}: OK")

print(f"\nTotal errors: {total_errors}")
```

### Dry Run Before Fixing

```python
from ascii_guard import lint_file, fix_file

# Check what would be fixed
result = lint_file("README.md")
if result.has_errors:
    print(f"Would fix {len(result.errors)} issues")

    # Preview fixes
    fix_result = fix_file("README.md", dry_run=True)
    print(f"Would fix {fix_result.boxes_fixed} boxes")

    # Show first few fixed lines
    print("\nFirst few fixed lines:")
    for i, line in enumerate(fix_result.lines[:5]):
        print(f"  {i+1}: {line}")

    # Actually apply fixes
    # fix_result = fix_file("README.md")
```

---

## Backward Compatibility

Old import paths still work for backward compatibility:

```python
# New (recommended)
from ascii_guard import lint_file, fix_file

# Old (still works)
from ascii_guard.linter import lint_file, fix_file
from ascii_guard.detector import detect_boxes
from ascii_guard.models import Box, ValidationError, LintResult
```

**Note**: The new package root imports are recommended for clarity and consistency.

---

## Version Information

```python
from ascii_guard import __version__

print(f"ascii-guard version: {__version__}")
```

---

## See Also

- [Usage Guide](USAGE.md) - Complete usage documentation
- [API Design](API_DESIGN.md) - Design decisions and rationale
- [FAQ](FAQ.md) - Frequently asked questions
