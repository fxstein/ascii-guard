# Python API Analysis

**Date**: 2025-12-02
**Task**: #69.1 - Analyze current internal API and identify stable functions
**Purpose**: Document current API structure to inform public API design

---

## Current API Structure

### 1. Public-Ready Functions (High-level, Stable)

#### `linter.lint_file()`
- **Signature**: `lint_file(file_path: str, exclude_code_blocks: bool = False) -> LintResult`
- **Status**: Well-documented, used in tests, CLI, and examples
- **Stability**: Stable signature, clear return type
- **Usage**: Primary entry point for linting files

#### `linter.fix_file()`
- **Signature**: `fix_file(file_path: str, dry_run: bool = False, exclude_code_blocks: bool = False) -> tuple[int, list[str]]`
- **Status**: Well-documented, used in tests and CLI
- **Returns**: `(boxes_fixed_count, fixed_lines)`
- **Issue**: Return type could be improved (named tuple or dataclass)
- **Usage**: Primary entry point for fixing files

#### `detector.detect_boxes()`
- **Signature**: `detect_boxes(file_path: str, exclude_code_blocks: bool = False) -> list[Box]`
- **Status**: Used in linter.py and examples
- **Stability**: Stable, well-documented
- **Usage**: Programmatic box detection

---

### 2. Data Models (Should be Public)

#### `models.Box`
- **Type**: Dataclass
- **Usage**: Core data structure, used everywhere
- **Properties**: `width`, `height`
- **Fields**: `top_line`, `bottom_line`, `left_col`, `right_col`, `lines`, `file_path`

#### `models.ValidationError`
- **Type**: Dataclass
- **Usage**: Error representation
- **Fields**: `line`, `column`, `message`, `severity`, `fix`
- **Methods**: `__str__()` for display

#### `models.LintResult`
- **Type**: Dataclass
- **Usage**: Return type for `lint_file()`
- **Properties**: `has_errors`, `has_warnings`, `is_clean`
- **Fields**: `file_path`, `boxes_found`, `errors`, `warnings`

---

### 3. Validation/Fixing (Mid-level, Could be Public)

#### `validator.validate_box()`
- **Signature**: `validate_box(box: Box) -> list[ValidationError]`
- **Status**: Used internally, could be useful for programmatic validation
- **Stability**: Stable signature
- **Usage**: Validate a single box object

#### `fixer.fix_box()`
- **Signature**: `fix_box(box: Box) -> list[str]`
- **Status**: Used internally, could be useful for programmatic fixing
- **Stability**: Stable signature
- **Usage**: Fix a single box object

---

### 4. Internal/Helper Functions (Should Remain Private)

These functions are implementation details and should not be part of the public API:

**Detector helpers:**
- `detector.has_box_drawing_chars()`
- `detector.is_in_code_fence()`
- `detector.is_ignore_marker()`
- `detector.is_in_ignore_region()`
- `detector.find_top_left_corner()`
- `detector.find_bottom_left_corner()`
- `detector.find_all_top_left_corners()`

**Validator helpers:**
- `validator.is_divider_line()`
- `validator.is_table_separator_line()`
- `validator.get_column_positions()`

**CLI functions:**
- `cli.*` functions (CLI-specific, not for programmatic use)

**Internal utilities:**
- `scanner.*` functions (internal file scanning)
- `patterns.*` functions (internal pattern matching)
- `config.*` functions (internal config handling)

---

## Current Usage Patterns

### Test Imports
- `from ascii_guard.linter import fix_file, lint_file`
- Tests primarily use high-level `linter` module functions

### Documentation Examples
- Some examples show: `detector.detect_boxes`, `validator.validate_box`
- Some examples show: `linter.lint_file`, `linter.fix_file`
- **Issue**: Inconsistent examples across documentation

### CLI Usage
- CLI uses: `linter.lint_file`, `linter.fix_file`
- CLI is separate from programmatic API

### Package Exports
- Currently only exports: `__version__` from `__init__.py`
- No public API exported

---

## Issues Identified

1. **Return Type Inconsistency**: `fix_file()` returns `tuple[int, list[str]]` - should use named tuple or dataclass for better API
2. **No Public API**: Nothing exported from `__init__.py` except version
3. **Inconsistent Examples**: Documentation shows different import patterns (detector/validator vs linter)
4. **No Stability Guarantees**: No documentation about which functions are stable vs internal
5. **Mixed Abstraction Levels**: Some examples show low-level functions (detector, validator) that should be internal

---

## Recommendations

### High Priority (Public API)
1. Export from `__init__.py`:
   - `lint_file()` - Primary linting function
   - `fix_file()` - Primary fixing function
   - `detect_boxes()` - Box detection (useful for programmatic use)
   - `Box`, `ValidationError`, `LintResult` - Core data models

### Medium Priority (Consider for Public API)
1. `validate_box()` - Useful for programmatic validation
2. `fix_box()` - Useful for programmatic fixing

### Low Priority (Keep Internal)
1. All helper functions in detector, validator, fixer
2. CLI functions
3. Scanner, patterns, config utilities

### API Improvements Needed
1. Create `FixResult` dataclass to replace `tuple[int, list[str]]` return from `fix_file()`
2. Standardize on `linter` module as primary public interface
3. Document stability guarantees (public vs internal)
4. Update all examples to use public API

---

## Next Steps

1. Define public API surface (task #69.2)
2. Design improved return types (task #69.3, #69.4)
3. Create design document (task #69.8)
