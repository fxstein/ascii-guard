# Frequently Asked Questions (FAQ)

Common questions about `ascii-guard`.

## General

### What is ascii-guard?

`ascii-guard` is a zero-dependency Python linter for detecting and fixing misaligned ASCII art boxes in documentation. It's particularly useful for catching formatting errors in AI-generated diagrams.

### Why does this exist?

AI tools often generate ASCII art with subtle alignment issues (missing characters, off-by-one errors). These break the visual appearance of diagrams in documentation. `ascii-guard` automatically detects and fixes these issues.

### Is it free?

Yes! `ascii-guard` is open source under the Apache 2.0 license.

---

## Installation & Requirements

### What are the requirements?

- Python 3.10 or later
- That's it! Zero other dependencies for Python 3.11+ (Python 3.10 requires `tomli` for config support)

### Why Python 3.10+?

Python 3.10+ provides excellent Unicode support, modern type hints, and is widely available. Python 3.11+ uses only the standard library (zero dependencies), while Python 3.10 requires one small dependency (`tomli`) for TOML configuration file support.

### Can I use it with older Python versions?

No, `ascii-guard` requires Python 3.10+. If you're stuck on an older version, consider:
- Using `pyenv` to install Python 3.10+ alongside your system Python
- Using Docker with Python 3.10+
- Updating your Python installation

### Does it work on Windows/macOS/Linux?

Yes! `ascii-guard` is cross-platform and works on:
- Linux (all major distributions)
- macOS (10.15+)
- Windows (10+)

### How do I install it?

```bash
pip install ascii-guard
```

---

## Usage

### What files does it work on?

Any text file! It's designed for markdown (`.md`) files but works on:
- Markdown files (`.md`)
- Plain text files (`.txt`)
- Documentation files (`.rst`, `.adoc`)
- Any UTF-8 text file with ASCII art

### Does it modify my files?

Only when you use the `fix` command. The `lint` command only reports issues without modifying files.

```bash
ascii-guard lint file.md   # Read-only, no modifications
ascii-guard fix file.md     # Modifies file to fix issues
```

### How do I preview changes before applying them?

Use the `--dry-run` flag:

```bash
ascii-guard fix file.md --dry-run
```

This shows what would be changed without actually modifying the file.

### Can I use it in CI/CD?

Yes! `ascii-guard` is designed for CI/CD use:

```bash
# In your CI script
ascii-guard lint docs/**/*.md

# Use exit code to fail CI if issues found
```

See [USAGE.md](USAGE.md#integration) for examples.

### Does it work with pre-commit hooks?

Yes! Add to `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/fxstein/ascii-guard
    rev: v1.6.0
    hooks:
      - id: ascii-guard
```

---

## Features & Capabilities

### What box-drawing characters are supported?

All Unicode box-drawing characters:

- **Single line**: `┌─┐│└─┘`
- **Double line**: `╔═╗║╚═╝`
- **Heavy line**: `┏━┓┃┗━┛`
- **Rounded corners**: `╭─╮│╰─╯`

### What about ASCII-style boxes (`+--+`)?

Currently, only Unicode box-drawing characters are supported. ASCII-style boxes (`+`, `-`, `|`) are not validated.

**Workaround**: Convert ASCII boxes to Unicode:
```
┌───┐      instead of      +---+
│   │                       |   |
└───┘                       +---+
```

### Can it detect nested boxes?

Yes, `ascii-guard` detects and validates nested boxes independently.

### Does it validate box content?

No, `ascii-guard` only validates the border structure. Content inside boxes is preserved as-is and not validated.

### Can it fix arrow alignment?

Not currently. `ascii-guard` focuses on box borders. Arrow characters (`→`, `←`, `↑`, `↓`) are preserved but not validated.

### Does it work on flowcharts?

Yes, if the flowchart uses box-drawing characters for boxes. It validates each box independently.

---

## Technical Questions

### Does it have any dependencies?

**Zero runtime dependencies!** Only the Python standard library is used.

Development dependencies (testing, linting) are separate and not required to use the tool.

### How fast is it?

Very fast! Typical performance:
- Small file (< 1KB): < 10ms
- Medium file (< 100KB): < 100ms
- Large file (< 1MB): < 1 second

### Is the output deterministic?

Yes! Running `ascii-guard` multiple times on the same file produces identical results.

### Can I use it programmatically?

Yes! ascii-guard provides a stable Python API. Import from the package root:

```python
from ascii_guard import lint_file, fix_file, detect_boxes

# Lint a file
result = lint_file('README.md')
if result.has_errors:
    print(f"Found {len(result.errors)} errors")

# Fix a file
fix_result = fix_file('README.md')
print(f"Fixed {fix_result.boxes_fixed} boxes")
```

**Backward compatibility**: Old import paths still work:
- `from ascii_guard import lint_file` (recommended)
- `from ascii_guard.linter import lint_file` (still works)

See [USAGE.md](USAGE.md#python-api) for complete examples and [API_REFERENCE.md](API_REFERENCE.md) for full API documentation.

### Does it preserve file encodings?

`ascii-guard` expects UTF-8 encoded files. Non-UTF-8 files may cause errors.

### What about Git line endings?

`ascii-guard` preserves whatever line endings exist in your files (LF or CRLF). It doesn't modify line ending style.

---

## Troubleshooting

### It's not detecting my boxes

**Possible causes:**

1. **Using ASCII characters instead of Unicode**
   - ❌ `+--+` (ASCII)
   - ✅ `┌─┐` (Unicode)

2. **Mixed box styles in same box**
   - Each box should use consistent characters

3. **Incomplete boxes**
   - Must have all four corners to be detected

### The fix command doesn't work

**Check:**

1. **File permissions**: Ensure the file is writable
   ```bash
   ls -l file.md
   chmod +w file.md
   ```

2. **File encoding**: Must be UTF-8
   ```bash
   file -I file.md
   ```

3. **Valid box structure**: Must have recognizable borders

### False positives: It reports issues that aren't real

**This shouldn't happen!** If you encounter false positives:

1. Please [open an issue](https://github.com/fxstein/ascii-guard/issues) with:
   - The ASCII art that triggered the false positive
   - Your Python version
   - Your `ascii-guard` version

2. As a workaround, you can skip validation for that file temporarily

### It changed my content!

**This should never happen!** `ascii-guard` is designed to only modify borders, never content.

If content was modified:
1. Check your Git diff to see exactly what changed
2. Please [open an issue](https://github.com/fxstein/ascii-guard/issues) immediately with:
   - Before/after content
   - The command you ran
   - Your Python and `ascii-guard` versions

---

## Configuration & Customization

### Can I exclude certain files or directories?

Yes! Use a configuration file `.ascii-guard.toml` in your project root:

```toml
[files]
# Exclude patterns (gitignore-style)
exclude = [
    "node_modules/",
    "build/",
    "*.tmp",
    "**/__pycache__/**"
]

# Include patterns (override excludes)
include = [
    "!important.md"
]
```

**Default exclusions** (when no config file exists):
- `.git/`, `node_modules/`, `__pycache__/`
- `.venv/`, `venv/`, `.tox/`
- `build/`, `dist/`
- `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`
- `*.egg-info/`

See [Configuration](USAGE.md#configuration) for full details.

### Can I configure which box styles to allow?

Not yet. All Unicode box-drawing styles are accepted. Style configuration may be added in a future version.

### Can I customize the error messages?

Not currently. Error messages are standardized for consistency.

### Can I disable certain validation rules?

Not yet. All validation rules are always active. Configurable rules may be added in future versions.

---

## Contributing & Development

### How can I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Development setup
- Coding standards
- How to submit pull requests

### I found a bug, what should I do?

[Open an issue](https://github.com/fxstein/ascii-guard/issues/new) with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- ASCII art sample that triggers the bug
- Your environment (Python version, OS, etc.)

### I have a feature request

[Open a discussion](https://github.com/fxstein/ascii-guard/discussions) or issue describing:
- The feature you'd like
- Your use case (why is it needed?)
- How you'd expect it to work

### Can I add my own validation rules?

Not yet through configuration, but you can:
1. Fork the repository
2. Modify `src/ascii_guard/validator.py`
3. Submit a pull request if the rule would be useful to others

### Why doesn't ascii-guard run on its own repository?

`ascii-guard` **intentionally does not lint itself** in pre-commit hooks or CI/CD pipelines.

**Reason**: The ascii-guard repository contains many intentionally broken ASCII boxes used for:
- **Documentation examples** showing "before/after" states
- **Test fixtures** with broken boxes for validation testing
- **Tutorial content** demonstrating common mistakes

Running ascii-guard would flag all these examples as errors, creating false positives and blocking commits.

**For contributors**: See the [CONTRIBUTING.md](../CONTRIBUTING.md#why-ascii-guard-doesnt-lint-itself) section for details on testing your changes.

---

## Comparison & Alternatives

### How is this different from regular linters?

Regular linters (markdownlint, vale, etc.) check markdown syntax and writing style, but they don't validate ASCII art alignment. `ascii-guard` specifically focuses on box-drawing character alignment.

### Should I use this instead of other linters?

No, use it **in addition to** other linters! `ascii-guard` is specialized for ASCII art validation and doesn't replace general-purpose linters.

### Are there alternatives?

Not really! There are no other tools specifically focused on ASCII art box alignment validation. This was created to fill that gap.

---

## Release & Versioning

### What version should I use?

Always use the latest stable version from PyPI:
```bash
pip install --upgrade ascii-guard
```

### How often are releases made?

Following semantic versioning:
- **Patch releases** (bug fixes): As needed
- **Minor releases** (new features): Every few months
- **Major releases** (breaking changes): Rare, with migration guides

### Where can I see the changelog?

[CHANGELOG.md](../CHANGELOG.md) (to be created at first release)

---

## License & Legal

### What license is it under?

Apache License 2.0 - permissive open source license allowing commercial use.

### Can I use it in commercial projects?

Yes! The Apache 2.0 license allows commercial use with no restrictions.

### Do I need to credit ascii-guard?

Not required, but appreciated! You can mention it in your project's acknowledgments.

---

## Support

### Where can I get help?

1. **Documentation**: Check [README.md](../README.md) and [USAGE.md](USAGE.md)
2. **FAQ**: You're reading it!
3. **Issues**: [GitHub Issues](https://github.com/fxstein/ascii-guard/issues)
4. **Discussions**: [GitHub Discussions](https://github.com/fxstein/ascii-guard/discussions)

### Is there commercial support?

Not currently. This is a community-maintained open source project.

### Can I hire someone to add a feature?

Consider:
1. Opening an issue describing your need
2. Submitting a pull request yourself
3. Sponsoring development (if sponsorships are available)

---

**Have a question not answered here?** [Open a discussion!](https://github.com/fxstein/ascii-guard/discussions)
