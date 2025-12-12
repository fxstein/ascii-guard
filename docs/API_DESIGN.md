# Python API Design Document

**Date**: 2025-12-02
**Task**: #69.2-#69.8 - Design well-defined Python API for ascii-guard
**Status**: Draft for Review
**Based on**: [API_ANALYSIS.md](API_ANALYSIS.md)

---

## Overview

This document defines the public Python API for ascii-guard, providing a stable, well-documented interface for programmatic use. The API is designed to be:

- **Stable**: Public API functions maintain backward compatibility
- **Clear**: Well-documented with type hints and docstrings
- **Consistent**: Uniform patterns across all API functions
- **Complete**: Covers all common use cases

---

## Public API Surface

### Exports from `__init__.py`

The following will be exported from `ascii_guard` package root:

```python
# High-level functions
from ascii_guard import lint_file, fix_file, detect_boxes

# Data models
from ascii_guard import Box, ValidationError, LintResult, FixResult

# Version
from ascii_guard import __version__
```

### Module Structure

- **Public API**: Functions and classes exported from `__init__.py`
- **Internal API**: Functions in submodules (detector, validator, fixer) that are not exported
- **Private API**: Helper functions and implementation details (prefixed with `_` or not documented)

---

## API Functions

### 1. `lint_file()`

**Purpose**: Lint a file for ASCII art alignment issues.

**Signature**:
```python
def lint_file(
    file_path: str | Path,
    exclude_code_blocks: bool = False
) -> LintResult:
    """Lint a file for ASCII art alignment issues.

    Args:
        file_path: Path to file to lint (str or Path)
        exclude_code_blocks: If True, skip ASCII boxes inside markdown code blocks

    Returns:
        LintResult with errors and warnings

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file cannot be read
        ValueError: If file_path is invalid

    Example:
        >>> result = lint_file("README.md")
        >>> if result.has_errors:
        ...     print(f"Found {len(result.errors)} errors")
    """
```

**Design Decisions**:
- Accepts both `str` and `Path` for flexibility
- Returns `LintResult` dataclass (already well-designed)
- Clear error handling with specific exception types
- `exclude_code_blocks` parameter for flexibility

**Backward Compatibility**: ✅ Fully compatible with current implementation

---

### 2. `fix_file()`

**Purpose**: Fix ASCII art alignment issues in a file.

**Current Issue**: Returns `tuple[int, list[str]]` which is not user-friendly.

**Proposed Solution**: Create `FixResult` dataclass.

**New `FixResult` Model**:
```python
@dataclass
class FixResult:
    """Results from fixing a file."""

    file_path: str
    boxes_fixed: int
    lines: list[str]
    modified: bool  # True if file was actually modified

    @property
    def was_modified(self) -> bool:
        """Check if file was modified."""
        return self.modified
```

**New Signature**:
```python
def fix_file(
    file_path: str | Path,
    dry_run: bool = False,
    exclude_code_blocks: bool = False
) -> FixResult:
    """Fix ASCII art alignment issues in a file.

    Args:
        file_path: Path to file to fix (str or Path)
        dry_run: If True, don't write changes to file (returns fixed lines)
        exclude_code_blocks: If True, skip ASCII boxes inside markdown code blocks

    Returns:
        FixResult with fixed lines and metadata

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file cannot be read/written
        ValueError: If file_path is invalid

    Example:
        >>> result = fix_file("README.md", dry_run=True)
        >>> print(f"Would fix {result.boxes_fixed} boxes")
        >>> if not result.dry_run:
        ...     print(f"Fixed {result.boxes_fixed} boxes in {result.file_path}")
    """
```

**Design Decisions**:
- Replace tuple with `FixResult` dataclass for better API
- Add `modified` flag to indicate if file was actually changed
- Accepts both `str` and `Path`
- Maintains `dry_run` parameter

**Backward Compatibility**: ⚠️ Breaking change - return type changes from `tuple` to `FixResult`

**Migration Path**:
- Old code: `boxes_fixed, lines = fix_file(...)`
- New code: `result = fix_file(...)` then `result.boxes_fixed`, `result.lines`
- Provide deprecation period or version flag

---

### 3. `detect_boxes()`

**Purpose**: Detect ASCII art boxes in a file without validation.

**Signature**:
```python
def detect_boxes(
    file_path: str | Path,
    exclude_code_blocks: bool = False
) -> list[Box]:
    """Detect ASCII art boxes in a file.

    This function only detects boxes; it does not validate them.
    Use lint_file() for validation or validate_box() for individual boxes.

    Args:
        file_path: Path to file to analyze (str or Path)
        exclude_code_blocks: If True, skip ASCII boxes inside markdown code blocks

    Returns:
        List of detected Box objects

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file cannot be read
        ValueError: If file_path is invalid

    Example:
        >>> boxes = detect_boxes("README.md")
        >>> print(f"Found {len(boxes)} ASCII art boxes")
        >>> for box in boxes:
        ...     print(f"Box at line {box.top_line + 1}: {box.width}x{box.height}")
    """
```

**Design Decisions**:
- Public API for programmatic box detection
- Returns list of `Box` objects for further processing
- Accepts both `str` and `Path`
- Clear documentation that this is detection-only, not validation

**Backward Compatibility**: ✅ Fully compatible (already exists, just needs to be exported)

---

## Programmatic Box Detection and Validation

### 4. `validate_box()`

**Purpose**: Validate a single Box object.

**Signature**:
```python
def validate_box(box: Box) -> list[ValidationError]:
    """Validate a single ASCII art box.

    Args:
        box: Box object to validate

    Returns:
        List of ValidationError objects (empty if box is valid)

    Example:
        >>> boxes = detect_boxes("README.md")
        >>> for box in boxes:
        ...     errors = validate_box(box)
        ...     if errors:
        ...         print(f"Box has {len(errors)} validation errors")
    """
```

**Design Decisions**:
- Useful for programmatic validation of individual boxes
- Returns list of errors (empty if valid)
- Works with `Box` objects from `detect_boxes()`

**Backward Compatibility**: ✅ Fully compatible (already exists, just needs to be exported)

---

### 5. `fix_box()`

**Purpose**: Fix a single Box object.

**Signature**:
```python
def fix_box(box: Box) -> list[str]:
    """Fix alignment issues in a single box.

    Args:
        box: Box object to fix

    Returns:
        List of fixed lines (replacement for box.lines)

    Example:
        >>> boxes = detect_boxes("README.md")
        >>> for box in boxes:
        ...     errors = validate_box(box)
        ...     if errors:
        ...         fixed_lines = fix_box(box)
        ...         # Apply fixed_lines to file
    """
```

**Design Decisions**:
- Useful for programmatic fixing of individual boxes
- Returns fixed lines that can be applied to file
- Works with `Box` objects from `detect_boxes()`

**Backward Compatibility**: ✅ Fully compatible (already exists, just needs to be exported)

---

## Data Models

### `Box`

**Status**: Public API (exported from `__init__.py`)

```python
@dataclass
class Box:
    """Represents an ASCII art box structure."""

    top_line: int  # Line number of top border (0-indexed)
    bottom_line: int  # Line number of bottom border (0-indexed)
    left_col: int  # Column of left border (0-indexed)
    right_col: int  # Column of right border (0-indexed)
    lines: list[str]  # All lines of the box
    file_path: str  # Source file path

    @property
    def width(self) -> int:
        """Calculate box width."""
        return self.right_col - self.left_col + 1

    @property
    def height(self) -> int:
        """Calculate box height."""
        return self.bottom_line - self.top_line + 1
```

**Design Decisions**:
- Core data structure, must be public
- Well-designed with helpful properties
- No changes needed

---

### `ValidationError`

**Status**: Public API (exported from `__init__.py`)

```python
@dataclass
class ValidationError:
    """Represents a validation error in an ASCII art box."""

    line: int  # Line number (0-indexed)
    column: int  # Column number (0-indexed)
    message: str  # Error description
    severity: str  # 'error' or 'warning'
    fix: str | None = None  # Suggested fix

    def __str__(self) -> str:
        """Format error for display."""
        return f"Line {self.line + 1}, Col {self.column + 1}: {self.message}"
```

**Design Decisions**:
- Error representation, must be public
- Well-designed with helpful `__str__` method
- No changes needed

---

### `LintResult`

**Status**: Public API (exported from `__init__.py`)

```python
@dataclass
class LintResult:
    """Results from linting a file."""

    file_path: str
    boxes_found: int
    errors: list[ValidationError]
    warnings: list[ValidationError]

    @property
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0

    @property
    def is_clean(self) -> bool:
        """Check if file is clean (no errors or warnings)."""
        return not self.has_errors and not self.has_warnings
```

**Design Decisions**:
- Return type for `lint_file()`, must be public
- Well-designed with helpful properties
- No changes needed

---

### `FixResult` (NEW)

**Status**: Public API (exported from `__init__.py`)

```python
@dataclass
class FixResult:
    """Results from fixing a file."""

    file_path: str
    boxes_fixed: int
    lines: list[str]
    modified: bool  # True if file was actually modified

    @property
    def was_modified(self) -> bool:
        """Check if file was modified."""
        return self.modified
```

**Design Decisions**:
- New dataclass to replace tuple return from `fix_file()`
- Provides better API than tuple
- Includes `modified` flag for clarity

---

## Backward Compatibility Strategy

### Current State

**Current imports that work**:
```python
from ascii_guard.linter import lint_file, fix_file
from ascii_guard.detector import detect_boxes
from ascii_guard.models import Box, ValidationError, LintResult
```

### Compatibility Approach

**Option 1: Full Backward Compatibility (Recommended)**
- Keep all existing imports working
- Add new exports to `__init__.py` without removing old ones
- Users can migrate gradually
- No breaking changes

**Option 2: Deprecation Path**
- Keep old imports working with deprecation warnings
- Encourage migration to new imports
- Remove in future major version

**Recommendation**: **Option 1** - Full backward compatibility

**Rationale**:
- No breaking changes for existing users
- Allows gradual migration
- Both import styles work:
  - `from ascii_guard import lint_file` (new, recommended)
  - `from ascii_guard.linter import lint_file` (old, still works)

### Breaking Change: `fix_file()` Return Type

**Issue**: `fix_file()` currently returns `tuple[int, list[str]]`, will return `FixResult`.

**Options**:
1. **Immediate breaking change** (major version bump)
2. **Deprecation period** (keep tuple, add FixResult in minor version)
3. **Compatibility shim** (support both for one version)

**Recommendation**: **Option 1** - Immediate breaking change with major version bump

**Rationale**:
- Clean API design is more important than backward compatibility here
- Major version bump signals breaking change
- Migration is simple: `boxes_fixed, lines = fix_file(...)` → `result = fix_file(...)`

---

## API Versioning and Stability Guarantees

### Versioning Strategy

- **Major version** (X.0.0): Breaking changes to public API
- **Minor version** (0.X.0): New features, additions to public API (backward compatible)
- **Patch version** (0.0.X): Bug fixes, internal changes (backward compatible)

### Stability Guarantees

#### Public API (Stable)
- Functions and classes exported from `__init__.py`
- Guaranteed backward compatibility within major version
- Changes only in major versions
- Well-documented with type hints

**Public API includes**:
- `lint_file()`, `fix_file()`, `detect_boxes()`
- `validate_box()`, `fix_box()`
- `Box`, `ValidationError`, `LintResult`, `FixResult`
- `__version__`

#### Internal API (Unstable)
- Functions in submodules not exported from `__init__.py`
- May change in any version (patch, minor, or major)
- No stability guarantees
- Use at your own risk

**Internal API includes**:
- All helper functions in `detector`, `validator`, `fixer`
- `cli`, `scanner`, `patterns`, `config` modules
- Any function not explicitly exported

### Documentation Requirements

All public API functions must have:
- Complete docstrings with Args, Returns, Raises
- Type hints for all parameters and return values
- Usage examples
- Clear error documentation

---

## Implementation Plan

### Phase 1: Design Review
- [x] Complete API analysis (task #69.1)
- [ ] Review and approve this design document (task #69.9)

### Phase 2: Implementation
- [ ] Create `FixResult` dataclass in `models.py` (task #69.10)
- [ ] Update `fix_file()` to return `FixResult` (task #69.12)
- [ ] Export public API from `__init__.py` (task #69.10)
- [ ] Update function signatures and documentation (task #69.11, #69.12)

### Phase 3: Testing
- [ ] Add unit tests for public API (task #69.14)
- [ ] Add integration tests (task #69.15)
- [ ] Verify backward compatibility (task #69.16)

### Phase 4: Documentation
- [ ] Update USAGE.md with official API section (task #69.17)
- [ ] Update FAQ.md (task #69.18)
- [ ] Add API reference documentation (task #69.19)

### Phase 5: Release
- [ ] Prepare release notes (task #69.20)
- [ ] Major version bump (breaking change for `fix_file()`)

---

## Examples

### Basic Usage

```python
from ascii_guard import lint_file, fix_file

# Lint a file
result = lint_file("README.md")
if result.has_errors:
    print(f"Found {len(result.errors)} errors")

# Fix a file
fix_result = fix_file("README.md", dry_run=True)
print(f"Would fix {fix_result.boxes_fixed} boxes")
```

### Programmatic Box Detection

```python
from ascii_guard import detect_boxes, validate_box, fix_box

# Detect boxes
boxes = detect_boxes("README.md")
print(f"Found {len(boxes)} boxes")

# Validate each box
for box in boxes:
    errors = validate_box(box)
    if errors:
        print(f"Box at line {box.top_line + 1} has {len(errors)} errors")
        # Fix the box
        fixed_lines = fix_box(box)
```

### Error Handling

```python
from ascii_guard import lint_file
from pathlib import Path

try:
    result = lint_file("README.md")
    if result.is_clean:
        print("File is clean!")
    else:
        for error in result.errors:
            print(f"{error}")
except FileNotFoundError:
    print("File not found")
except OSError as e:
    print(f"Error reading file: {e}")
```

---

## Open Questions

1. **Should `validate_box()` and `fix_box()` be public?**
   - ✅ Yes - Useful for programmatic use cases
   - Decision: Include in public API

2. **How to handle `fix_file()` breaking change?**
   - ✅ Major version bump
   - Decision: v2.0.0 with clear migration guide

3. **Should we support `Path` objects everywhere?**
   - ✅ Yes - More Pythonic
   - Decision: Accept both `str | Path` for all file_path parameters

---

## Review Checklist

- [ ] API surface is well-defined
- [ ] All functions have complete documentation
- [ ] Backward compatibility strategy is clear
- [ ] Versioning strategy is defined
- [ ] Examples are comprehensive
- [ ] Breaking changes are identified and justified
- [ ] Implementation plan is feasible

---

**Next Steps**: Review this design document, then proceed with implementation.
