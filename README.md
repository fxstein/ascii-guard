# ascii-guard

**Zero-dependency Python linter for detecting and fixing misaligned ASCII art boxes in documentation.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/fxstein/ascii-guard/actions/workflows/ci.yml/badge.svg)](https://github.com/fxstein/ascii-guard/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/fxstein/ascii-guard/branch/main/graph/badge.svg)](https://codecov.io/gh/fxstein/ascii-guard)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/fxstein/ascii-guard/pulls)

---

## 🎯 Why ascii-guard?

AI-generated ASCII flowcharts and diagrams often have subtle formatting errors where box borders are misaligned by 1-2 characters. This breaks visual integrity and makes documentation harder to read.

**ascii-guard** automatically detects and fixes these alignment issues, ensuring your ASCII art looks perfect.

### ✨ Key Features

- 🚀 **Minimal dependencies** - Zero for Python 3.11+, one tiny dep for Python 3.10 (`tomli`)
- 💾 **Tiny footprint** - Lightweight and fast
- 🔒 **Minimal supply chain risk** - Pure stdlib on 3.11+
- ⚡ **Quick startup** - No import overhead
- 📦 **Simple installation** - One command, automatic dependency handling
- 🛡️ **Type-safe** - Full mypy strict mode
- ✅ **Well tested** - Comprehensive test coverage

---

## 📦 Installation

### For Users (AI Agents)

```bash
pip install ascii-guard
```

That's it! No other dependencies needed.

### For Developers

```bash
# Clone repository
git clone https://github.com/fxstein/ascii-guard.git
cd ascii-guard

# Set up development environment (creates venv, installs dev deps)
./setup-venv.sh

# Activate virtual environment
source .venv/bin/activate

# Install pre-commit hooks
pre-commit install
```

---

## 🚀 Quick Start

### Check files for ASCII art issues

```bash
ascii-guard lint README.md
ascii-guard lint docs/**/*.md
```

### Auto-fix alignment issues

```bash
ascii-guard fix README.md
ascii-guard fix --dry-run docs/guide.md  # Preview changes first
```

### Example

**Before** (misaligned):
```
┌─────────────────────┐
│ Box Content         │
└────────────────────┘   ← Missing one character!
```

**After** (fixed):
```
┌─────────────────────┐
│ Box Content         │
└─────────────────────┘  ← Perfect alignment ✓
```

---

## 🎨 Supported Box-Drawing Characters

ascii-guard supports Unicode box-drawing characters:

| Type | Characters | Description |
|------|------------|-------------|
| **Horizontal** | `─` (U+2500) | Horizontal line |
| **Vertical** | `│` (U+2502) | Vertical line |
| **Corners** | `┌` `┐` `└` `┘` | Standard corners |
| **T-junctions** | `├` `┤` `┬` `┴` | Connection points |
| **Cross** | `┼` | Four-way intersection |
| **Heavy lines** | `━` `┃` `┏` `┓` `┗` `┛` | Bold variants |
| **Double lines** | `═` `║` `╔` `╗` `╚` `╝` | Double-line variants |

---

## 🛠️ Development

### Project Structure

```
ascii-guard/
├── src/ascii_guard/    # Source code (ZERO dependencies)
│   ├── __init__.py     # Package initialization
│   ├── cli.py          # CLI interface (argparse only)
│   └── core.py         # Linting logic (stdlib only)
├── tests/              # Test suite (pytest)
├── docs/               # Documentation
└── pyproject.toml      # Project configuration
```

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_cli.py

# Run with verbose output
pytest -v

# Fast tests only (pre-commit)
pytest -m "not slow"
```

### Linting and Type Checking

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run linter only
ruff check .

# Run formatter
ruff format .

# Run type checker
mypy src/
```

### Virtual Environment Isolation

ascii-guard uses **strict virtual environment isolation** to ensure minimal system pollution:

```bash
# Development dependencies are isolated in .venv/
# Runtime has minimal dependencies:
#   - Python 3.11+: Zero dependencies (uses stdlib tomllib)
#   - Python 3.10: One dependency (tomli for TOML config)
# All tools (ruff, mypy, pytest) are dev-only

# Verify minimal runtime dependencies
python -c "import ascii_guard; print('Success - no imports failed')"
```

---

## 📋 Validation Rules

ascii-guard checks for:

1. **Vertical alignment** - All `│` characters in a column align
2. **Horizontal alignment** - All `─` characters connect properly
3. **Corner correctness** - Corner characters match adjacent lines
4. **Width consistency** - Top, middle, and bottom borders match
5. **Content fit** - Content stays within box borders

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

1. Fork and clone the repository
2. Run `./setup-venv.sh` to set up your environment
3. Make your changes
4. Run tests and linters: `pre-commit run --all-files`
5. Submit a pull request

### Code Style

- **Minimal dependencies** - Only essential runtime dependencies (tomli for Python 3.10)
- **Type-safe** - All code must pass `mypy --strict`
- **Tested** - Maintain high test coverage
- **Formatted** - Code is auto-formatted with ruff

---

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

Copyright 2025 Oliver Ratzesberger

---

## 🔗 Links

- **Repository**: https://github.com/fxstein/ascii-guard
- **Issues**: https://github.com/fxstein/ascii-guard/issues
- **PyPI**: https://pypi.org/project/ascii-guard/ _(coming soon)_
- **Documentation**: [docs/](docs/)

---

## 🙏 Acknowledgments

Inspired by the need for better ASCII art formatting in AI-generated documentation.

Built with ❤️ using only Python's standard library.

---

**Note**: This project is in active development (v0.1.0-alpha). The core linter functionality is being implemented. Contributions and feedback are welcome!
