# Test Suite

Comprehensive test suite for ascii-guard. This directory contains all tests organized by component.

## 🚀 Quick Start

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ascii_guard --cov-report=term-missing

# Run with HTML coverage report
pytest --cov=ascii_guard --cov-report=html
# Open htmlcov/index.html

# Run specific test file
pytest tests/test_detector.py

# Run specific test
pytest tests/test_detector.py::test_detect_single_box

# Run tests matching pattern
pytest -k "test_box"

# Run with verbose output
pytest -v

# Fast tests only (excludes slow tests)
pytest -m "not slow"
```

---

## 📁 Test Files

### Core Component Tests

#### [test_detector.py](test_detector.py)
Tests for box detection logic.
- Box boundary detection
- Code fence handling
- Ignore marker support
- Edge cases (nested boxes, empty lines)

#### [test_validator.py](test_validator.py)
Tests for validation rules.
- Alignment checking
- Border consistency
- Width validation
- Table junction detection
- Error message generation

#### [test_fixer.py](test_fixer.py)
Tests for auto-fix functionality.
- Border alignment corrections
- Width adjustments
- Junction point insertion
- Edge case handling

#### [test_linter.py](test_linter.py)
Tests for linter orchestration.
- File processing workflow
- Error/warning aggregation
- Result formatting
- I/O error handling

### Input/Output Tests

#### [test_scanner.py](test_scanner.py)
Tests for file scanning.
- Directory traversal
- File filtering (extensions, excludes)
- Gitignore pattern matching
- Symlink handling

#### [test_cli.py](test_cli.py)
Tests for command-line interface.
- Argument parsing (`lint`, `fix`, `show-config`)
- Help messages
- Exit codes
- Error handling

### Data & Configuration Tests

#### [test_models.py](test_models.py)
Tests for data structures.
- `Box` model
- `ValidationError` model
- `LintResult` model
- Model serialization

#### [test_config.py](test_config.py)
Tests for configuration system.
- TOML file loading
- Configuration validation
- Default values
- Override behavior

#### [test_patterns.py](test_patterns.py)
Tests for box-drawing character patterns.
- Character classification
- Pattern recognition
- Corner detection
- Unicode handling

### Integration & Special Tests

#### [test_integration.py](test_integration.py)
End-to-end integration tests.
- Complete workflows (lint → validate → fix)
- Multi-file processing
- Real-world scenarios

#### [test_stdlib_only.py](test_stdlib_only.py)
**Zero-dependency verification.**
- Ensures no external packages imported at runtime
- Critical for maintaining zero-dependency promise
- Python 3.11+: Zero dependencies
- Python 3.10: Only `tomli` allowed

#### [test_version.py](test_version.py)
Version consistency tests.
- `__version__` accessibility
- Version format validation

---

## 📂 Test Fixtures

### [fixtures/](fixtures/)
Test data files for various scenarios.

#### [perfect_box.txt](fixtures/perfect_box.txt)
Well-formed ASCII box with no issues.
- Used for baseline validation
- Tests for false positives

#### [broken_box.txt](fixtures/broken_box.txt)
Intentionally broken box with common errors.
- Misaligned borders
- Missing corners
- Width inconsistencies

#### [multiple_boxes.md](fixtures/multiple_boxes.md)
Markdown file with multiple boxes.
- Tests batch processing
- Tests box isolation

#### [mixed_styles.txt](fixtures/mixed_styles.txt)
Boxes with different drawing styles.
- Standard corners (`┌┐└┘`)
- Heavy lines (`┏┓┗┛`)
- Double lines (`╔╗╚╝`)

#### [no_boxes.txt](fixtures/no_boxes.txt)
Plain text with no ASCII boxes.
- Tests for false positives
- Boundary condition testing

#### [benchmark_test.md](fixtures/benchmark_test.md)
Large file for performance testing.
- Marked as slow test (`@pytest.mark.slow`)
- Used for regression testing

---

## 📊 Test Organization

### Test Categories

Tests are organized by:
1. **Component** - Each module has its own test file
2. **Functionality** - Grouped by feature within files
3. **Edge Cases** - Special classes for boundary conditions
4. **Performance** - Marked with `@pytest.mark.slow`

### Test Naming Convention

```python
def test_<component>_<scenario>_<expected_result>():
    """Test description in docstring."""
    ...
```

Examples:
- `test_detect_single_box()` - Basic detection
- `test_detect_nested_boxes_in_code_fence()` - Complex scenario
- `test_fix_misaligned_bottom_border()` - Specific fix

---

## ✅ Coverage Requirements

- **Overall**: 80% minimum (currently 96%+)
- **Core modules**: 90%+ preferred
- **Critical paths**: 100% required
  - Box detection logic
  - Validation rules
  - Fix algorithms
  - Zero-dependency verification

### Viewing Coverage

```bash
# Terminal report
pytest --cov=ascii_guard --cov-report=term-missing

# HTML report (interactive)
pytest --cov=ascii_guard --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## 🧪 Writing New Tests

### Basic Test Structure

```python
def test_feature_name():
    """Test description explaining what and why."""
    # Arrange - Set up test data
    content = """
    ┌──────────┐
    │ Content  │
    └──────────┘
    """

    # Act - Execute the functionality
    result = detect_boxes(content.splitlines())

    # Assert - Verify expected behavior
    assert len(result) == 1
    assert result[0].width == 12
```

### Using Fixtures

```python
def test_with_file_fixture(tmp_path):
    """Test using temporary file."""
    test_file = tmp_path / "test.md"
    test_file.write_text("content here")

    result = lint_file(str(test_file))
    assert result.errors == 0
```

### Testing Edge Cases

```python
class TestEdgeCases:
    """Group related edge case tests."""

    def test_empty_input(self):
        """Test behavior with empty input."""
        assert detect_boxes([]) == []

    def test_single_line(self):
        """Test behavior with single line."""
        assert detect_boxes(["┌─┐"]) == []
```

---

## 🔍 Debugging Tests

### Running Individual Tests

```bash
# Single test with output
pytest tests/test_detector.py::test_detect_single_box -s

# With debugger on failure
pytest --pdb

# With verbose stack traces
pytest -vv --tb=long
```

### Common Issues

**Import errors**: Ensure virtual environment is activated
```bash
source .venv/bin/activate
```

**Fixture not found**: Check pytest plugin installation
```bash
pip install -e ".[dev]"
```

**Coverage missing**: Install pytest-cov
```bash
pip install pytest-cov
```

---

## 🚨 Pre-commit Tests

Fast tests run automatically on commit:
```bash
# Manual pre-commit test run
pre-commit run pytest-fast --all-files

# Skip slow tests
pytest -m "not slow"
```

---

## 🔗 Related Documentation

- [docs/TESTING.md](../docs/TESTING.md) - Testing strategy and patterns
- [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md) - Development workflow
- [docs/DESIGN.md](../docs/DESIGN.md) - Architecture overview

---

## 📚 Testing Best Practices

1. **Test behavior, not implementation** - Focus on what, not how
2. **One assertion per test** (when practical) - Easier to debug
3. **Use descriptive names** - Test name explains purpose
4. **Include docstrings** - Explain why the test exists
5. **Test edge cases** - Empty input, single item, large input
6. **Mock external dependencies** - Keep tests fast and isolated
7. **Keep tests independent** - No shared state between tests

---

**For development guide, see [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md)**
