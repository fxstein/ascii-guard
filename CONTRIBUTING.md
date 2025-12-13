# Contributing to ascii-guard

Thank you for considering contributing to `ascii-guard`! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title** describing the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **ASCII art sample** that causes the issue (if applicable)
- **Python version** (`python --version`)
- **ascii-guard version** (`ascii-guard --version`)
- **Operating system** and version

**Example bug report:**
```markdown
**Title**: Misdetects rounded corners as errors

**Steps to Reproduce**:
1. Create file with rounded box: ╭─╮│╰─╯
2. Run `ascii-guard lint file.md`
3. Reports false positive error

**Expected**: No errors (rounded corners are valid)
**Actual**: Reports "Invalid corner character"

**Environment**:
- Python: 3.12.0
- ascii-guard: 0.1.0
- OS: macOS 14.0
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:

1. **Check existing issues** for similar suggestions
2. **Provide clear use case** - why is this useful?
3. **Describe the proposed solution**
4. **Consider alternatives** you've thought about

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the development setup** below
3. **Make your changes** following our coding standards
4. **Add tests** for any new functionality
5. **Update documentation** if needed
6. **Ensure all tests pass** (`pytest`)
7. **Run pre-commit hooks** (`pre-commit run --all-files`)
8. **Write clear commit messages**
9. **Submit your pull request**

## Development Setup

**Prerequisites:**
- Python 3.10 or later
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager

**Install uv:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or: brew install uv
# or: pipx install uv
```

**Quick Start:**

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/ascii-guard.git
cd ascii-guard

# One-step setup (handles everything automatically)
./setup.sh

# Use uv run for commands (no need to activate venv)
uv run pytest              # Run tests
uv run ruff check .        # Lint code
uv run mypy src/           # Type check
uv run ascii-guard lint .  # Try the tool
```

That's it! The script sets up everything you need using `uv`.

**For detailed development guide (setup, workflow, testing, architecture), see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)**

## Coding Standards

### Zero Dependencies

**CRITICAL**: `ascii-guard` has **zero runtime dependencies**. Only Python stdlib is allowed.

❌ **DO NOT** add:
- External packages (requests, click, colorama, etc.)
- System command calls (`subprocess`)
- Platform-specific code without fallbacks

✅ **DO USE**:
- Python standard library only
- Cross-platform code
- Pure Python implementations

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

All functions must have type hints:

```python
def detect_boxes(lines: list[str]) -> list[Box]:
    """Detect ASCII art boxes in text lines."""
    ...
```

Check types with:
```bash
mypy src/
```

### Testing

**All new features must include tests.**

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ascii_guard --cov-report=term-missing

# Run specific test file
pytest tests/test_detector.py

# Run specific test
pytest tests/test_detector.py::test_detect_single_box
```

**Test requirements**:
- Coverage: 80% minimum
- Unit tests for new functions
- Integration tests for workflows
- Edge case tests
- Zero-dependency verification tests

### Documentation

Update documentation for any user-facing changes:

- **README.md**: User-facing features
- **docs/DESIGN.md**: Architecture changes
- **Docstrings**: All public functions
- **CHANGELOG.md**: User-visible changes

**Docstring style**:
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

## Commit Message Guidelines

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

## Testing Your Changes

### Local Testing

```bash
# Run full test suite
pytest

# Run with coverage
pytest --cov=ascii_guard --cov-report=html
# Open htmlcov/index.html to see coverage report

# Test on real files (if working on non-documentation files)
ascii-guard lint your-file.md
ascii-guard fix your-file.md --dry-run
```

### Why ascii-guard Doesn't Lint Itself

**Important**: `ascii-guard` is **intentionally NOT run** on its own repository in:
- Pre-commit hooks (`.pre-commit-config.yaml`)
- CI/CD pipelines (`.github/workflows/`)

**Reason**: This repository contains many intentionally broken ASCII boxes for:
1. **Documentation examples** - `README.md` and `docs/*.md` show "before/after" states
2. **Test fixtures** - `tests/fixtures/*.md` contain broken boxes for validation tests
3. **Tutorial content** - Demonstrating common mistakes requires broken examples

Running ascii-guard on these files would create false positives and prevent commits.

**For contributors**:
- Don't worry about broken ASCII boxes in documentation/tests
- If you're adding new code/docs, manually verify ASCII boxes if needed:
  ```bash
  # Check a specific file (skip code blocks if it has examples)
  ascii-guard lint --exclude-code-blocks your-new-file.md
  ```
- Use ignore markers for intentional examples (see docs/USAGE.md#ignore-markers)

### CI Testing

When you open a pull request, GitHub Actions will automatically:
- Run tests on Python 3.12
- Check code formatting
- Run type checking
- Verify zero dependencies
- Check code coverage

Fix any CI failures before requesting review.

## Review Process

1. **Automated checks** must pass (CI, tests, linting)
2. **Maintainer review** - usually within a week
3. **Feedback addressed** - may require changes
4. **Approval** - once all concerns resolved
5. **Merge** - maintainer will squash and merge

## Release Process

(For maintainers only)

Releases follow semantic versioning (vX.Y.Z):
- X (major): Breaking changes
- Y (minor): New features (backward compatible)
- Z (patch): Bug fixes

## Recognition

Contributors are recognized in:
- GitHub contributors page
- CHANGELOG.md for significant contributions
- Release notes

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Chat**: (TBD)

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0, the same license as the project.

---

Thank you for contributing to `ascii-guard`! 🎉
