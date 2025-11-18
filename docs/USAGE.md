# ascii-guard Usage Guide

Complete guide to using `ascii-guard` for linting and fixing ASCII art in your documentation.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Line Usage](#command-line-usage)
- [Examples](#examples)
- [Integration](#integration)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## Installation

### Via pip (Recommended)

```bash
pip install ascii-guard
```

### Via pipx (Isolated Installation)

```bash
pipx install ascii-guard
```

### From Source

```bash
git clone https://github.com/fxstein/ascii-guard.git
cd ascii-guard
pip install -e .
```

### Requirements

- Python 3.12 or later
- No other dependencies required!

---

## Quick Start

### Check a file for issues

```bash
ascii-guard lint README.md
```

### Auto-fix issues in a file

```bash
ascii-guard fix README.md
```

### Preview fixes without applying them

```bash
ascii-guard fix README.md --dry-run
```

---

## Command Line Usage

### `ascii-guard lint`

Scan files for ASCII art alignment issues.

```bash
ascii-guard lint [OPTIONS] FILES...
```

**Options:**
- `--json` - Output results in JSON format
- `--help` - Show help message

**Exit codes:**
- `0` - No issues found
- `1` - Issues found
- `2` - Error (invalid arguments, file not found, etc.)

**Examples:**

```bash
# Lint a single file
ascii-guard lint README.md

# Lint multiple files
ascii-guard lint README.md docs/guide.md

# Lint with JSON output (for CI/CD)
ascii-guard lint *.md --json

# Lint all markdown files recursively (bash)
ascii-guard lint **/*.md
```

**Sample output:**

```
README.md:15:45: error: Right border misaligned by 1 character
README.md:17:45: error: Bottom border too short (expected 46 chars, got 45)

Found 2 errors in 1 file
```

### `ascii-guard fix`

Automatically fix ASCII art alignment issues.

```bash
ascii-guard fix [OPTIONS] FILES...
```

**Options:**
- `--dry-run` - Preview changes without modifying files
- `--json` - Output results in JSON format
- `--help` - Show help message

**Exit codes:**
- `0` - Successfully fixed or no issues found
- `2` - Error (invalid arguments, permission denied, etc.)

**Examples:**

```bash
# Fix a single file
ascii-guard fix README.md

# Preview fixes without applying
ascii-guard fix README.md --dry-run

# Fix multiple files
ascii-guard fix docs/*.md

# Fix with JSON output
ascii-guard fix README.md --json
```

**Sample output:**

```
README.md: Fixed 2 issues in 1 box

✓ Fixed right border alignment (line 15)
✓ Extended bottom border to match width (line 17)
```

### `ascii-guard --version`

Show version information.

```bash
ascii-guard --version
```

---

## Examples

### Example 1: Simple Box

**Input** (broken):
```
┌─────────────────────┐
│ Box Content         │
└─────────────────────   ← Missing character
```

**Command**:
```bash
ascii-guard fix example.md
```

**Output** (fixed):
```
┌─────────────────────┐
│ Box Content         │
└─────────────────────┘
```

### Example 2: Multiple Boxes

**File**: `docs/architecture.md`

```markdown
# System Architecture

## Frontend

┌───────────────┐
│   React App   │
└───────────────┘
        │
        ▼
┌───────────────┐
│   API Layer   │
└───────────────┘
        │
        ▼
┌───────────────┐
│   Database    │
└───────────────┘
```

**Command**:
```bash
ascii-guard lint docs/architecture.md
```

**Result**: Validates all three boxes in the diagram.

### Example 3: Different Box Styles

`ascii-guard` supports multiple Unicode box-drawing styles:

**Single line**:
```
┌─────────┐
│ Content │
└─────────┘
```

**Double line**:
```
╔═════════╗
║ Content ║
╚═════════╝
```

**Heavy line**:
```
┏━━━━━━━━━┓
┃ Content ┃
┗━━━━━━━━━┛
```

**Rounded corners**:
```
╭─────────╮
│ Content │
╰─────────╯
```

All styles are automatically detected and validated.

### Example 4: Complex Flowchart

```markdown
┌──────────────┐
│    Start     │
└──────────────┘
       │
       ▼
┌──────────────┐      ┌──────────────┐
│  Process A   │─────▶│  Process B   │
└──────────────┘      └──────┬───────┘
       │                     │
       │   ┌─────────────────┘
       │   │
       ▼   ▼
   ┌──────────────┐
   │     End      │
   └──────────────┘
```

`ascii-guard` will validate:
- All box borders are properly aligned
- All boxes have consistent widths
- Corners are correct for the style used

---

## Integration

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/fxstein/ascii-guard
    rev: v0.1.0
    hooks:
      - id: ascii-guard
        args: [lint]
```

**Installation:**
```bash
pip install pre-commit
pre-commit install
```

**Usage:**
Pre-commit will automatically run `ascii-guard lint` on staged `.md` files.

### GitHub Actions

Add to `.github/workflows/docs.yml`:

```yaml
name: Documentation Quality

on: [push, pull_request]

jobs:
  lint-ascii-art:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install ascii-guard
        run: pip install ascii-guard

      - name: Check ASCII art
        run: ascii-guard lint **/*.md
```

### Make/Just Integration

**Makefile:**
```makefile
.PHONY: lint-docs
lint-docs:
	ascii-guard lint docs/**/*.md README.md

.PHONY: fix-docs
fix-docs:
	ascii-guard fix docs/**/*.md README.md
```

**Justfile:**
```just
# Check documentation ASCII art
lint-docs:
    ascii-guard lint docs/**/*.md README.md

# Fix documentation ASCII art
fix-docs:
    ascii-guard fix docs/**/*.md README.md
```

### VS Code Integration

**tasks.json:**
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Lint ASCII Art",
      "type": "shell",
      "command": "ascii-guard",
      "args": ["lint", "${file}"],
      "group": "test",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Fix ASCII Art",
      "type": "shell",
      "command": "ascii-guard",
      "args": ["fix", "${file}"],
      "group": "build",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

---

## Configuration

### File Patterns

By default, `ascii-guard` works with any text file. For markdown files with code blocks, ASCII art is detected anywhere in the file.

### Exit Codes

Use exit codes for CI/CD integration:

```bash
# Fail CI if issues found
ascii-guard lint docs/*.md || exit 1

# Allow warnings but fail on errors
ascii-guard lint docs/*.md --json | jq '.errors | length > 0' && exit 1
```

### JSON Output

Use `--json` for programmatic parsing:

```bash
ascii-guard lint README.md --json
```

**Output format:**
```json
{
  "files": [
    {
      "path": "README.md",
      "boxes_found": 3,
      "boxes_validated": 3,
      "errors": [
        {
          "line": 15,
          "column": 45,
          "message": "Right border misaligned",
          "severity": "error"
        }
      ],
      "warnings": []
    }
  ],
  "summary": {
    "total_files": 1,
    "files_with_errors": 1,
    "total_errors": 1,
    "total_warnings": 0
  }
}
```

---

## Troubleshooting

### Common Issues

#### "No boxes detected"

**Cause**: File doesn't contain recognizable ASCII box-drawing characters.

**Solution**: Ensure you're using Unicode box-drawing characters:
- ✅ Use: `┌─┐│└─┘`
- ❌ Don't use: `+--+|+--+`

#### "Permission denied"

**Cause**: Insufficient permissions to read or write file.

**Solution**:
```bash
# Check file permissions
ls -l filename.md

# Make readable
chmod +r filename.md

# For fix command, ensure write permission
chmod +w filename.md
```

#### "File not found"

**Cause**: Incorrect path or file doesn't exist.

**Solution**:
```bash
# Use absolute path
ascii-guard lint /full/path/to/file.md

# Or relative from current directory
ascii-guard lint ./docs/file.md
```

#### "Not a text file"

**Cause**: File contains binary data or non-UTF-8 encoding.

**Solution**: Ensure file is text-encoded in UTF-8:
```bash
# Check file encoding
file filename.md

# Convert to UTF-8 if needed
iconv -f ISO-8859-1 -t UTF-8 filename.md > filename_utf8.md
```

### Debug Mode

For detailed debugging information:

```bash
# Run with Python verbose mode
python -m ascii_guard.cli lint README.md

# Check version and installation
ascii-guard --version
pip show ascii-guard
```

### Getting Help

- **Documentation**: [https://github.com/fxstein/ascii-guard/tree/main/docs](https://github.com/fxstein/ascii-guard/tree/main/docs)
- **Issues**: [https://github.com/fxstein/ascii-guard/issues](https://github.com/fxstein/ascii-guard/issues)
- **Discussions**: [https://github.com/fxstein/ascii-guard/discussions](https://github.com/fxstein/ascii-guard/discussions)

---

## Advanced Usage

### Scripting

Use in shell scripts:

```bash
#!/bin/bash
set -e

echo "Checking documentation..."
if ascii-guard lint docs/**/*.md; then
    echo "✓ All ASCII art is properly formatted"
else
    echo "✗ Found ASCII art issues"
    echo "Run 'ascii-guard fix docs/**/*.md' to auto-fix"
    exit 1
fi
```

### Continuous Integration

**Example GitLab CI:**
```yaml
lint:ascii-art:
  image: python:3.12
  script:
    - pip install ascii-guard
    - ascii-guard lint docs/**/*.md
  only:
    changes:
      - docs/**/*.md
      - README.md
```

**Example CircleCI:**
```yaml
version: 2.1
jobs:
  lint-docs:
    docker:
      - image: python:3.12
    steps:
      - checkout
      - run: pip install ascii-guard
      - run: ascii-guard lint docs/**/*.md
```

### Python API (Future)

While not yet officially supported, you can import modules directly:

```python
from ascii_guard.detector import detect_boxes
from ascii_guard.validator import validate_box

# Read file
with open('README.md') as f:
    lines = f.readlines()

# Detect boxes
boxes = detect_boxes(lines)

# Validate each box
for box in boxes:
    errors = validate_box(box, lines)
    if errors:
        print(f"Box at line {box.top_line}: {len(errors)} errors")
```

**Note**: The Python API is not yet stable and may change in future versions.

---

## Best Practices

1. **Run before committing**: Use pre-commit hooks to catch issues early
2. **CI/CD integration**: Add to your CI pipeline to enforce quality
3. **Fix automatically**: Use `--dry-run` first, then apply fixes
4. **Consistent style**: Stick to one box-drawing style per document
5. **Test changes**: Review auto-fixes to ensure content is preserved

---

## What Gets Checked

`ascii-guard` validates:

✅ **Horizontal alignment**: Top and bottom borders match in width
✅ **Vertical alignment**: Left and right borders align vertically
✅ **Corner characters**: Corners match the border style
✅ **Border continuity**: No missing characters in borders
✅ **Style consistency**: Box uses one style throughout

What it **doesn't** check:
- ❌ Content inside boxes (preserves as-is)
- ❌ ASCII art that isn't box-shaped
- ❌ Markdown syntax or formatting
- ❌ Code block syntax

---

**Need more help?** Check the [FAQ](FAQ.md) or [open an issue](https://github.com/fxstein/ascii-guard/issues).
