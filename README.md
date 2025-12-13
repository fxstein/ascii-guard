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

We recommend using `uv` for the fastest installation experience, but `pip` and `pipx` are fully supported alternatives. `uv` provides faster dependency resolution and better reproducibility, while `pip` and `pipx` work with any standard Python environment.

### Recommended: Using uv (Fastest)

```bash
# Install ascii-guard
uv tool install ascii-guard
```

> **Note:** If `uv` is not installed, you may install it with: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Alternative: Using pip

```bash
pip install ascii-guard
```

### Alternative: Using pipx (Isolated Environment)

```bash
pipx install ascii-guard
```

That's it! No other dependencies needed.

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

## 🎭 Ignore Markers

Need to show intentionally broken boxes in your docs? Use ignore markers:

```markdown
**❌ Common Mistake (don't do this):**

<!-- ascii-guard-ignore-next -->
┌─────────────────────┐
│ Box Content         │
└────────────────────┘   ← Misaligned on purpose for demonstration

**✅ Correct Way:**

┌─────────────────────┐
│ Box Content         │
└─────────────────────┘  ← Perfect alignment
```

The ignore markers are invisible in rendered markdown but tell ascii-guard to skip validation. Perfect for:
- Before/after comparisons
- Tutorial examples showing common mistakes
- Documentation with intentionally broken examples

See [USAGE.md](docs/USAGE.md#ignore-markers) for complete syntax and examples.

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

## 📋 Validation Rules

ascii-guard checks for:

1. **Vertical alignment** - All `│` characters in a column align
2. **Horizontal alignment** - All `─` characters connect properly
3. **Corner correctness** - Corner characters match adjacent lines
4. **Width consistency** - Top, middle, and bottom borders match
5. **Content fit** - Content stays within box borders

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

**Prerequisites:**
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Fork and clone the repository
git clone https://github.com/YOUR-USERNAME/ascii-guard.git
cd ascii-guard

# One-step setup (creates venv, installs deps, configures hooks)
./setup.sh

# Use uv run for commands
uv run pytest              # Run tests
uv run ruff check .        # Lint code
uv run mypy src/           # Type check

# Make your changes and submit a PR
```

**For detailed development guide, see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)**

**For contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md)**

---

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

Copyright 2025 Oliver Ratzesberger

---

## 🔗 Links

- **Repository**: https://github.com/fxstein/ascii-guard
- **Issues**: https://github.com/fxstein/ascii-guard/issues
- **PyPI**: https://pypi.org/project/ascii-guard/
- **Documentation**:
  - [User Guide](docs/USAGE.md) - Complete usage documentation
  - [Python API Reference](docs/API_REFERENCE.md) - Complete API documentation
  - [Development Guide](docs/DEVELOPMENT.md) - Setup, workflow, architecture
  - [FAQ](docs/FAQ.md) - Frequently asked questions

---

## 🙏 Acknowledgments

Inspired by the need for better ASCII art formatting in AI-generated documentation.

Built with ❤️ using only Python's standard library.

---

**Note**: ascii-guard is stable and actively maintained. Contributions and feedback are welcome!
