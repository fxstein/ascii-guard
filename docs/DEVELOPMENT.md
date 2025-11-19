# Development Guide

Complete guide for contributing to ascii-guard development.

## Prerequisites

- **Python 3.10+** (3.12+ recommended)
- **git**
- **Basic familiarity with**: pytest, type hints, pre-commit hooks

## Quick Start

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/ascii-guard.git
cd ascii-guard

# One-step setup (creates venv, installs deps, configures hooks, runs tests)
./setup.sh

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS/WSL
.venv\Scripts\activate     # Windows (cmd.exe)
```

The `setup.sh` script automatically:
1. ✅ Checks Python version (3.10+ required)
2. ✅ Creates isolated virtual environment (.venv)
3. ✅ Installs ascii-guard in editable mode
4. ✅ Installs all dev dependencies (pytest, ruff, mypy, pre-commit, build, twine)
5. ✅ Configures pre-commit git hooks
6. ✅ Runs verification tests

**Platform compatibility**: Linux, macOS, Windows (WSL/Git Bash)

---

## Development Workflow

### Creating a Feature

```bash
# Create a feature branch
git checkout -b feature/my-awesome-feature

# Make your changes
# ... edit code ...

# Run tests
pytest

# Run pre-commit checks manually (optional - they run on commit)
pre-commit run --all-files

# Commit changes (pre-commit hooks run automatically)
git add .
git commit -m "feat: Add awesome feature"

# Push to your fork
git push origin feature/my-awesome-feature

# Open a pull request on GitHub
```

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `ci`: CI/CD changes
- `build`: Build system changes
- `chore`: Maintenance tasks

**Examples**:
```
feat(detector): Add support for rounded corner boxes

Implements detection of ╭╮╰╯ rounded corner characters.
Adds validation rules for rounded corner alignment.

Closes #42
```

```
fix(validator): Correct column counting for wide Unicode chars

Wide Unicode characters (emoji, CJK) were causing incorrect
column alignment calculations. Now uses wcwidth logic.

Fixes #123
```

---

## Coding Standards

### Zero Dependencies (CRITICAL)

**`ascii-guard` has ZERO runtime dependencies.** Only Python stdlib is allowed.

❌ **DO NOT** add:
- External packages (requests, click, colorama, etc.)
- System command calls (`subprocess`)
- Platform-specific code without fallbacks

✅ **DO USE**:
- Python standard library only
- Cross-platform code
- Pure Python implementations

**Exception**: Python 3.10 requires `tomli` for TOML support (stdlib `tomllib` added in 3.11).

### Code Style

We use `ruff` for linting and formatting:

```bash
# Check code style
ruff check src/ tests/

# Auto-format code
ruff format src/ tests/
```

**Key rules**:
- Line length: 100 characters
- Use type hints for all functions
- Follow PEP 8
- Use f-strings for string formatting
- Prefer explicit over implicit

### Type Hints

All functions must have complete type hints:

```python
def detect_boxes(lines: list[str]) -> list[Box]:
    """Detect ASCII art boxes in text lines.

    Args:
        lines: Lines of text to scan

    Returns:
        List of detected Box objects
    """
    ...
```

Check types with:
```bash
mypy src/
```

We use `mypy --strict` mode - all code must pass strict type checking.

### Docstring Style

Use Google-style docstrings:

```python
def validate_box(box: Box, lines: list[str]) -> list[ValidationError]:
    """Validate ASCII art box for alignment issues.

    Args:
        box: Box structure to validate
        lines: All lines from the file

    Returns:
        List of validation errors found

    Raises:
        ValueError: If box coordinates are invalid
    """
    ...
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ascii_guard --cov-report=term-missing

# Run with HTML coverage report
pytest --cov=ascii_guard --cov-report=html
# Open htmlcov/index.html in browser

# Run specific test file
pytest tests/test_detector.py

# Run specific test
pytest tests/test_detector.py::test_detect_single_box

# Run tests matching pattern
pytest -k "test_box"
```

### Test Requirements

**All new features must include tests.**

- **Coverage**: 80% minimum (aim for 95%+)
- **Unit tests**: For individual functions
- **Integration tests**: For workflows
- **Edge cases**: Test boundary conditions
- **Zero-dependency tests**: Verify no external deps loaded

### Writing Tests

```python
def test_detect_single_box():
    """Test detection of a single ASCII box."""
    content = """
    ┌──────────┐
    │ Content  │
    └──────────┘
    """
    boxes = detect_boxes(content.splitlines())
    assert len(boxes) == 1
    assert boxes[0].top_line == 1
    assert boxes[0].width == 12
```

---

## Common Tasks

### Adding a New Feature

1. **Create issue** describing the feature
2. **Write tests** for the new functionality
3. **Implement feature** to make tests pass
4. **Update documentation** (README, USAGE.md, docstrings)
5. **Run full test suite** and linters
6. **Submit PR** with clear description

### Fixing a Bug

1. **Write failing test** that reproduces the bug
2. **Fix the bug** to make test pass
3. **Verify fix** doesn't break other tests
4. **Update CHANGELOG** if user-facing
5. **Submit PR** referencing the issue

### Updating Documentation

Documentation is in:
- `README.md`: User-facing overview
- `docs/USAGE.md`: Complete usage guide
- `docs/DEVELOPMENT.md`: This file
- `docs/DESIGN.md`: Architecture and design decisions
- `docs/TESTING.md`: Testing strategy
- `CONTRIBUTING.md`: Contribution guidelines

### Running Linters

Pre-commit hooks run automatically, but you can run manually:

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
pre-commit run mypy --all-files
```

---

## Project Structure

```
ascii-guard/
├── src/
│   └── ascii_guard/
│       ├── __init__.py       # Package initialization, version
│       ├── cli.py            # Command-line interface (argparse)
│       ├── config.py         # Configuration file handling
│       ├── detector.py       # Box detection logic
│       ├── fixer.py          # Auto-fix logic
│       ├── linter.py         # Linting orchestration
│       ├── models.py         # Data structures (Box, ValidationError)
│       ├── patterns.py       # Box-drawing character patterns
│       ├── scanner.py        # File scanning logic
│       └── validator.py      # Validation rules
├── tests/
│   ├── fixtures/             # Test files
│   ├── test_*.py             # Test modules
│   └── __init__.py
├── docs/                     # Documentation
├── release/                  # Release automation
├── .github/                  # GitHub Actions workflows
├── setup.sh                  # Development setup script
├── pyproject.toml            # Project metadata and dependencies
└── README.md                 # User-facing documentation
```

---

## Architecture

### Core Concepts

1. **Scanner**: Finds files to check based on config
2. **Detector**: Identifies ASCII boxes in text
3. **Validator**: Checks boxes for alignment issues
4. **Fixer**: Auto-corrects detected issues
5. **Linter**: Orchestrates the workflow

### Data Flow

```
Files → Scanner → Detector → Validator → Linter
                     ↓
                   Fixer (if --fix)
```

See [DESIGN.md](DESIGN.md) for detailed architecture documentation.

---

## Troubleshooting

### Virtual Environment Issues

```bash
# Rebuild from scratch
rm -rf .venv
./setup.sh
```

### Pre-commit Hook Failures

```bash
# Run hooks manually to see errors
pre-commit run --all-files

# Update hooks
pre-commit autoupdate

# Skip hooks temporarily (use sparingly!)
git commit --no-verify
```

### Test Failures

```bash
# Run tests with verbose output
pytest -vv

# Run with print statements visible
pytest -s

# Run with debugger on failure
pytest --pdb
```

### Import Errors

Make sure you're in the virtual environment:
```bash
# Check which python is active
which python

# Should show: /path/to/ascii-guard/.venv/bin/python
# If not, activate:
source .venv/bin/activate
```

### Type Check Failures

```bash
# Run mypy with verbose output
mypy --show-error-codes src/

# Check specific file
mypy src/ascii_guard/detector.py
```

---

## Release Process

**For maintainers only.** See [RELEASE_DESIGN.md](RELEASE_DESIGN.md) for details.

```bash
# Ensure clean working directory
git status

# Run release script
./release/release.sh --help
```

---

## Additional Resources

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [DESIGN.md](DESIGN.md) - Architecture and design decisions
- [TESTING.md](TESTING.md) - Testing strategy and patterns
- [USAGE.md](USAGE.md) - Complete user documentation
- [FAQ.md](FAQ.md) - Frequently asked questions
- [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) - Community guidelines

---

## Getting Help

- **Questions**: [GitHub Discussions](https://github.com/fxstein/ascii-guard/discussions)
- **Bugs**: [GitHub Issues](https://github.com/fxstein/ascii-guard/issues)
- **Security**: See [SECURITY.md](../SECURITY.md)

---

**Happy coding!** 🚀
