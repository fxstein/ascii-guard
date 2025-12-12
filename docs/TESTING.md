# Testing Guide

This document describes the testing strategy and guidelines for `ascii-guard`.

## Overview

The test suite ensures that `ascii-guard` correctly detects, validates, and fixes ASCII art boxes while maintaining its **ZERO dependency** constraint. Tests verify that only Python standard library is used at runtime.

## Test Structure

```
tests/
├── fixtures/                    # Test data files
│   ├── perfect_box.txt         # Perfect ASCII box
│   ├── broken_box.txt          # Box with alignment issues
│   ├── multiple_boxes.md       # Multiple boxes in one file
│   ├── no_boxes.txt            # File with no boxes
│   └── mixed_styles.txt        # Different box drawing styles
├── test_models.py              # Data model tests
├── test_detector.py            # Box detection tests
├── test_validator.py           # Validation logic tests
├── test_fixer.py               # Fixing logic tests
├── test_linter.py              # Integration tests
├── test_cli.py                 # CLI interface tests
├── test_stdlib_only.py         # ZERO dependency verification
└── test_version.py             # Version information tests
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=ascii_guard --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_detector.py
```

### Run Specific Test Class or Function

```bash
pytest tests/test_detector.py::TestBoxDetection
pytest tests/test_detector.py::TestBoxDetection::test_detect_perfect_box
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Only Fast Tests (Skip Slow Ones)

```bash
pytest -m "not slow"
```

## Test Categories

### 1. Unit Tests

**Purpose**: Test individual functions and classes in isolation.

**Files**:
- `test_models.py` - Data structures (Box, ValidationError, LintResult)
- `test_detector.py` - Box detection logic
- `test_validator.py` - Validation logic
- `test_fixer.py` - Fixing logic

**Example**:
```python
def test_detect_perfect_box(self, fixtures_dir: Path) -> None:
    """Test detection of a perfectly aligned box."""
    test_file = str(fixtures_dir / "perfect_box.txt")
    boxes = detect_boxes(test_file)
    assert len(boxes) == 1
```

### 2. Integration Tests

**Purpose**: Test how modules work together.

**Files**:
- `test_linter.py` - Tests `lint_file()` and `fix_file()` functions
- `test_cli.py` - Tests command-line interface

**Example**:
```python
def test_lint_and_fix_workflow(self, tmp_path: Path) -> None:
    """Test complete lint and fix workflow."""
    # Lint broken file
    result = lint_file(test_file)
    assert result.has_errors

    # Fix the file
    boxes_fixed, _ = fix_file(test_file)
    assert boxes_fixed > 0

    # Verify fix worked
    result_after = lint_file(test_file)
    assert result_after.is_clean
```

### 3. Critical Tests: ZERO Dependency Verification

**Purpose**: **CRITICAL** - Ensure NO external runtime dependencies.

**Files**:
- `test_stdlib_only.py` - Verifies stdlib-only implementation

**What it tests**:
- ✅ No external package imports in runtime code
- ✅ No `click`, `typer`, `colorama`, or `markdown` libraries
- ✅ Only `argparse` for CLI (stdlib)
- ✅ Only ANSI escape codes for colors (no colorama)
- ✅ `pyproject.toml` has `dependencies = []`
- ✅ All modules can import without external deps

**Example**:
```python
def test_no_external_imports_in_package(self) -> None:
    """Test that no external packages are imported."""
    # Parse all .py files and check imports
    for py_file in src_files:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                # Verify all imports are stdlib
```

**This is a CRITICAL test** - If this fails, the core promise of `ascii-guard` is broken.

### 4. CLI Tests

**Purpose**: Test command-line interface behavior.

**Files**:
- `test_cli.py` - Tests `lint` and `fix` commands

**Coverage**:
- Command parsing
- File handling
- Output formatting (colors, messages)
- Error handling
- Quiet mode
- Dry-run mode

**Example**:
```python
def test_fix_command_dry_run(self, tmp_path: Path) -> None:
    """Test fix command with dry-run mode."""
    result = cmd_fix(Args(files=[str(test_file)], dry_run=True))
    assert "Would fix" in captured.out
    # File should be unchanged
```

### 5. Edge Case Tests

**Purpose**: Test boundary conditions and unusual inputs.

**Examples**:
- Empty files
- Single-line files
- Very large files
- Nested boxes
- Boxes at file start/end
- Very wide boxes
- Mixed box drawing styles

## Test Fixtures

Test fixtures are located in `tests/fixtures/` and provide realistic test data.

### Available Fixtures

1. **perfect_box.txt** - Well-formed ASCII box with no issues
2. **broken_box.txt** - Box with misaligned bottom edge
3. **multiple_boxes.md** - Markdown file with 4 boxes (some broken)
4. **no_boxes.txt** - Plain text with no ASCII art
5. **mixed_styles.txt** - Different box styles (single, double, heavy, ASCII)

### Using Fixtures

```python
@pytest.fixture
def fixtures_dir(self) -> Path:
    """Return the path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"

def test_with_fixture(self, fixtures_dir: Path) -> None:
    test_file = str(fixtures_dir / "perfect_box.txt")
    result = lint_file(test_file)
    assert result.is_clean
```

### Creating Test Files Dynamically

```python
def test_custom_case(self, tmp_path: Path) -> None:
    """Test with dynamically created file."""
    test_file = tmp_path / "custom.txt"
    test_file.write_text("┌────┐\n│ OK │\n└────┘\n")

    result = lint_file(str(test_file))
    assert result.is_clean
```

## Writing New Tests

### Test Naming Convention

- Test files: `test_<module>.py`
- Test classes: `Test<Feature>`
- Test functions: `test_<what_it_tests>`

### Test Structure

```python
def test_feature_description(self) -> None:
    """Brief description of what this test verifies."""
    # Arrange - Set up test data
    box = create_test_box()

    # Act - Perform the operation
    result = validate_box(box)

    # Assert - Verify expected outcome
    assert result.is_valid
```

### Best Practices

1. **One concept per test** - Each test should verify one thing
2. **Descriptive names** - Test name should describe what's being tested
3. **Clear assertions** - Use descriptive assertion messages
4. **Use fixtures** - Reuse common setup via fixtures
5. **Test edge cases** - Don't just test the happy path
6. **Keep tests fast** - Use `tmp_path` for file operations
7. **Type hints** - Use type hints in test functions

### Example: Adding a New Test

```python
def test_box_with_unicode_content(self, tmp_path: Path) -> None:
    """Test handling boxes containing Unicode characters."""
    test_file = tmp_path / "unicode.txt"
    test_file.write_text(
        "┌──────────┐\n"
        "│ Hello 世界 │\n"
        "└──────────┘\n",
        encoding="utf-8"
    )

    result = lint_file(str(test_file))
    assert result.boxes_found == 1
    assert result.is_clean
```

## Coverage Requirements

### Target Coverage

- **Overall**: >90% line coverage
- **Core modules** (detector, validator, fixer): >95%
- **CLI**: >85%
- **Critical paths**: 100% (zero-dependency checks, error handling)

### Checking Coverage

```bash
# Generate HTML coverage report
pytest --cov=ascii_guard --cov-report=html

# Open report in browser
open htmlcov/index.html
```

### Coverage Exemptions

Some lines are difficult to test and may be exempted:
- Defensive error handling for impossible cases
- CLI `if __name__ == "__main__"` blocks
- Type checking branches (when using `TYPE_CHECKING`)

## Continuous Integration

Tests run automatically via **pre-commit hooks** and **GitHub Actions**.

### Pre-commit Hook

```yaml
- repo: local
  hooks:
    - id: pytest-fast
      name: pytest (fast tests only)
      entry: pytest
      language: system
      types: [python]
      pass_filenames: false
      always_run: true
      args: ["-m", "not slow"]
```

### GitHub Actions (Future)

Will run:
- Full test suite
- Coverage report
- Python 3.10+ (3.12 recommended)
- Zero-dependency verification

## Debugging Tests

### Run with Debugging Output

```bash
# Show print statements
pytest -s

# Show detailed output
pytest -vv

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf
```

### Using pytest Fixtures for Debugging

```python
def test_with_debug_output(self, capsys: pytest.CaptureFixture[str]) -> None:
    """Test with captured output."""
    result = some_function()

    captured = capsys.readouterr()
    print(captured.out)  # Debug output

    assert "expected" in captured.out
```

## Test Maintenance

### When to Update Tests

- ✅ When adding new features
- ✅ When fixing bugs (add regression test)
- ✅ When refactoring (ensure behavior unchanged)
- ✅ When changing CLI interface
- ✅ When updating box character support

### Keeping Tests Fast

- Use `tmp_path` instead of real files
- Mock external calls (though we have none!)
- Mark slow tests with `@pytest.mark.slow`
- Keep test data small

### Regular Test Review

- Review test coverage monthly
- Remove obsolete tests
- Update fixtures as needed
- Ensure tests still reflect current behavior

## Troubleshooting

### Common Issues

**Import errors**:
```bash
# Ensure package is installed in dev mode
pip install -e .[dev]
```

**Fixture not found**:
```python
# Use relative import for fixtures
from pathlib import Path
fixtures_dir = Path(__file__).parent / "fixtures"
```

**Coverage not measuring**:
```bash
# Install coverage
pip install pytest-cov
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

## Summary

The `ascii-guard` test suite ensures:

1. ✅ **ZERO runtime dependencies** (most critical!)
2. ✅ Correct ASCII box detection
3. ✅ Accurate validation of alignment
4. ✅ Reliable fixing of broken boxes
5. ✅ Robust CLI interface
6. ✅ Comprehensive edge case handling
7. ✅ High code coverage (>90%)

**Remember**: The `test_stdlib_only.py` tests are CRITICAL. If they fail, stop and fix immediately. The zero-dependency promise is non-negotiable.
