# ascii-guard Design Documentation

**Version**: 1.1
**Status**: Implemented
**Python**: 3.10+
**Dependencies**: Minimal (tomli for Python 3.10, zero for 3.11+)

---

## Overview

`ascii-guard` is a minimal-dependency Python linter for detecting and fixing misaligned ASCII art boxes in text and markdown documentation. It's designed as a standalone tool that can be installed via PyPI and used in development workflows, CI/CD pipelines, and pre-commit hooks.

### Key Design Principles

1. **Minimal Runtime Dependencies**: Pure stdlib on Python 3.11+, one tiny dependency (tomli) for Python 3.10
2. **Fast**: Pure Python, no external process calls
3. **Standalone**: Works without complex external tools or libraries
4. **Safe**: Non-destructive, preserves content
5. **Simple**: Easy to install and use (`pip install ascii-guard`)

---

## Problem Statement

AI-generated ASCII art boxes in documentation often have formatting errors:
- Missing or extra characters in borders
- Misaligned vertical edges
- Inconsistent box widths
- Incorrect corner characters

**Example of broken box:**
```
┌─────────────────────┐
│ Box Content         │
└─────────────────────   ← Missing character, doesn't align
```

**After fixing:**
```
┌─────────────────────┐
│ Box Content         │
└─────────────────────┘  ← Perfect alignment
```

---

## Architecture

### Module Structure

```
ascii-guard/
├── src/ascii_guard/
│   ├── __init__.py       # Package metadata
│   ├── models.py         # Data structures (Box, ValidationError, LintResult)
│   ├── detector.py       # Box detection logic
│   ├── validator.py      # Validation rules
│   ├── fixer.py          # Auto-fix logic
│   ├── linter.py         # Main orchestration
│   └── cli.py            # Command-line interface
└── tests/                # Comprehensive test suite
```

### Core Components

#### 1. Models (`models.py`)

Data structures for representing boxes and validation results:

```python
@dataclass
class Box:
    """Represents an ASCII art box with borders."""
    top_line: int          # Line number of top border
    bottom_line: int       # Line number of bottom border
    left_col: int          # Column of left border
    right_col: int         # Column of right border
    lines: list[str]       # All lines of the box
    style: BoxStyle        # Unicode style (single/double/heavy)

@dataclass
class ValidationError:
    """Validation error with location and fix suggestion."""
    line: int              # 1-indexed line number
    column: int            # 1-indexed column number
    message: str           # Human-readable error
    severity: str          # 'error' or 'warning'
    fix_suggestion: str | None  # Optional fix suggestion

@dataclass
class LintResult:
    """Results from linting a file."""
    file_path: str
    boxes_found: int
    boxes_validated: int
    boxes_fixed: int
    errors: list[ValidationError]
    warnings: list[ValidationError]
```

#### 2. Detector (`detector.py`)

Detects ASCII art boxes in text files:

```python
def detect_boxes(lines: list[str]) -> list[Box]:
    """Detect all ASCII art boxes in text."""
    # 1. Scan for top-left corners (┌╔┏)
    # 2. Find matching top-right corners
    # 3. Trace down to find bottom corners
    # 4. Extract box region
    # 5. Determine box style (single/double/heavy)
```

**Supported Box Styles:**
- Single line: `┌─┐│└─┘`
- Double line: `╔═╗║╚═╝`
- Heavy line: `┏━┓┃┗━┛`
- Rounded corners: `╭─╮│╰─╯`

#### 3. Validator (`validator.py`)

Validates box structure and alignment:

```python
def validate_box(box: Box, lines: list[str]) -> list[ValidationError]:
    """Validate a single box for alignment issues."""
    errors = []

    # Check vertical alignment
    errors.extend(_validate_vertical_borders(box, lines))

    # Check horizontal alignment
    errors.extend(_validate_horizontal_borders(box, lines))

    # Check corners
    errors.extend(_validate_corners(box, lines))

    # Check width consistency
    errors.extend(_validate_width_consistency(box, lines))

    return errors
```

**Validation Rules:**
1. All vertical borders (│) must align in same column
2. Top and bottom borders must have equal width
3. Corner characters must match border style
4. No missing characters in borders
5. Content must fit within borders

#### 4. Fixer (`fixer.py`)

Automatically repairs broken boxes:

```python
def fix_box(box: Box, lines: list[str], errors: list[ValidationError]) -> list[str]:
    """Auto-fix alignment issues in a box."""
    fixed_lines = lines.copy()

    # Fix in order of priority:
    # 1. Fix corner characters
    # 2. Fix horizontal border length
    # 3. Fix vertical border alignment
    # 4. Adjust content padding if needed

    return fixed_lines
```

**Fix Strategy:**
- Non-destructive: Never loses content
- Idempotent: Running twice produces same result
- Conservative: Only fixes clear alignment issues
- Preserves: Content, spacing, indentation

#### 5. Linter (`linter.py`)

Main orchestration:

```python
def lint_file(file_path: str) -> LintResult:
    """Lint a single file."""
    lines = read_file(file_path)
    boxes = detect_boxes(lines)
    errors = []

    for box in boxes:
        box_errors = validate_box(box, lines)
        errors.extend(box_errors)

    return LintResult(...)

def fix_file(file_path: str, dry_run: bool = False) -> LintResult:
    """Fix issues in a file."""
    lines = read_file(file_path)
    boxes = detect_boxes(lines)

    for box in boxes:
        errors = validate_box(box, lines)
        if errors:
            lines = fix_box(box, lines, errors)

    if not dry_run:
        write_file(file_path, lines)

    return LintResult(...)
```

#### 6. CLI (`cli.py`)

Command-line interface using `argparse` (stdlib):

```python
def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='ascii-guard',
        description='Zero-dependency linter for ASCII art boxes'
    )

    subparsers = parser.add_subparsers()

    # lint command
    lint_parser = subparsers.add_parser('lint')
    lint_parser.add_argument('files', nargs='+')
    lint_parser.add_argument('--json', action='store_true')

    # fix command
    fix_parser = subparsers.add_parser('fix')
    fix_parser.add_argument('files', nargs='+')
    fix_parser.add_argument('--dry-run', action='store_true')
```

**CLI Features:**
- Colored output using ANSI escape codes (no `colorama`)
- JSON output mode for CI integration
- Dry-run mode for safe testing
- Exit codes: 0 (clean), 1 (issues found), 2 (error)

---

## Implementation Details

### Minimal Dependencies Strategy

To achieve minimal runtime dependencies, we use:

| Need | Solution |
|------|----------|
| **CLI parsing** | `argparse` (stdlib) |
| **File I/O** | `open()`, `pathlib` (stdlib) |
| **Text processing** | `str` methods (stdlib) |
| **Unicode handling** | Native Python 3.10+ Unicode support |
| **Colored output** | Raw ANSI escape codes |
| **Pattern matching** | `str.find()`, `str.index()` (stdlib) |
| **Config parsing** | `tomllib` (stdlib 3.11+) or `tomli` (3.10 only) |
| **Testing** | `pytest` (dev dependency only) |

### Character Detection

Box-drawing characters are detected using Unicode ranges:

```python
# Box drawing block: U+2500 to U+257F
HORIZONTAL_CHARS = {'─', '═', '━', '⎯'}
VERTICAL_CHARS = {'│', '║', '┃', '⎟'}
CORNER_CHARS = {
    'top_left': {'┌', '╔', '┏', '╭'},
    'top_right': {'┐', '╗', '┓', '╮'},
    'bottom_left': {'└', '╚', '┗', '╰'},
    'bottom_right': {'┘', '╝', '┛', '╯'}
}
```

### Performance Characteristics

- **File reading**: O(n) where n = file size
- **Box detection**: O(n × m) where m = average line length
- **Validation**: O(b × h) where b = boxes, h = box height
- **Fixing**: O(b × h)

**Typical performance:**
- Small file (< 1KB): < 10ms
- Medium file (< 100KB): < 100ms
- Large file (< 1MB): < 1s

### Error Handling

The tool uses defensive programming:

```python
try:
    lines = read_file(path)
except FileNotFoundError:
    print(f"Error: File not found: {path}", file=sys.stderr)
    sys.exit(2)
except PermissionError:
    print(f"Error: Permission denied: {path}", file=sys.stderr)
    sys.exit(2)
except UnicodeDecodeError:
    print(f"Error: Not a text file: {path}", file=sys.stderr)
    sys.exit(2)
```

---

## Usage Patterns

### 1. Command Line

```bash
# Lint files
ascii-guard lint README.md docs/*.md

# Fix files
ascii-guard fix README.md --dry-run  # Preview
ascii-guard fix README.md            # Apply fixes

# JSON output for CI
ascii-guard lint *.md --json
```

### 2. Pre-commit Hook

`.pre-commit-config.yaml`:
```yaml
  - repo: https://github.com/fxstein/ascii-guard
    rev: v1.1.0
    hooks:
      - id: ascii-guard
```

### 3. GitHub Actions

```yaml
- name: Check ASCII art
  run: |
    pip install ascii-guard
    ascii-guard lint **/*.md
```

### 4. Python API (future)

```python
from ascii_guard import lint_file, fix_file

result = lint_file('README.md')
if not result.is_clean():
    fix_file('README.md')
```

---

## Testing Strategy

Comprehensive test suite with 91 tests covering:

1. **Unit Tests**: Each module tested independently
2. **Integration Tests**: Full lint/fix workflows
3. **Fixture Tests**: Real-world ASCII art samples
4. **Edge Cases**: Empty files, malformed boxes, mixed styles
5. **Zero-Dependency Tests**: Verify no imports of external packages

**Test Coverage**: 80%+ required by CI

---

## Distribution

### PyPI Package

**Package name**: `ascii-guard`
**Installation**: `pip install ascii-guard`
**Entry point**: `ascii-guard` command

**Package metadata** (`pyproject.toml`):
```toml
[project]
name = "ascii-guard"
version = "1.1.0"
requires-python = ">=3.10"
dependencies = []  # ZERO runtime dependencies

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy", "pre-commit"]
```

### GitHub Releases

Each release includes:
- Source tarball (`.tar.gz`)
- Wheel distribution (`.whl`)
- Release notes with changelog
- Installation instructions

---

## Future Enhancements

### Planned for v1.2.0 (In Progress)

1. **Config File Support** (Task #17)
   - `.ascii-guard.toml` file for configuration
   - File inclusion/exclusion patterns (gitignore-style)
   - Directory scanning with smart defaults
   - Configurable file extensions
   - Max file size limits
   - See `docs/CONFIG_DESIGN.md` for details

### Future Releases

2. **Rule Configuration** (v1.3.0+)
   - Enable/disable specific validation rules
   - Custom validation profiles
   - Output format customization

3. **Additional Box Styles** (v1.4.0+)
   - ASCII-style boxes (`+--+`)
   - Custom character sets

4. **Advanced Validation** (v2.0.0+)
   - Nested boxes
   - Complex flowcharts
   - Arrow alignment

5. **Performance** (v2.0.0+)
   - Parallel file processing
   - Incremental validation

6. **Editor Integration** (v2.0.0+)
   - VS Code extension
   - Language server protocol

---

## Design Decisions

### Why Minimal Dependencies?

1. **Reliability**: Few external packages means less breakage
2. **Security**: Smaller attack surface (tomli is reference TOML implementation)
3. **Speed**: Minimal dependency resolution overhead
4. **Simplicity**: Easy to audit and maintain
5. **Portability**: Works anywhere Python 3.10+ works
6. **Strategic**: tomli became stdlib tomllib in 3.11, ensuring zero deps for modern Python

### Why Python 3.10+?

- Modern type hints (`str | None`) - available since 3.10
- Stable and widely adopted versions
- Good Unicode handling
- Performance improvements over 3.9
- Long support window (3.10 EOL Oct 2026, 3.11 EOL Oct 2027, 3.12 EOL Oct 2028)
- Enables integration into existing projects still on 3.10/3.11

### Why Not Use Existing Tools?

No existing tool validates ASCII art alignment:
- General linters don't understand box-drawing
- Markdown linters ignore code blocks
- Pre-commit hooks check syntax, not visual alignment

---

## Success Metrics

1. ✅ Zero runtime dependencies verified
2. ✅ Works on all major platforms (Linux, macOS, Windows)
3. ✅ Fast (< 1s for typical documentation files)
4. ✅ Safe (non-destructive, preserves content)
5. ✅ Well-tested (80%+ coverage, 91 tests)
6. ✅ Easy to use (simple CLI, clear error messages)
7. ✅ CI-ready (JSON output, proper exit codes)

---

**Document Version**: 2.2 (Updated for TOML config and minimal dependencies)
**Last Updated**: 2025-11-17
**Status**: Implementation Complete + Config Enhancement Planned
