# ascii-guard v1.1.0

This release expands Python version compatibility and fixes CI testing infrastructure.

**Python Version Support Expansion**

The most significant change in this release is adding support for **Python 3.10 and 3.11**, expanding from the previous 3.12-only requirement. After thorough code review, we confirmed that `ascii-guard` uses only standard library features compatible with Python 3.10+:

- No Python 3.12-specific syntax (no `match` statements or structural pattern matching)
- Type hints use `list[X]` and `tuple[X, Y]` syntax (available since Python 3.9)
- Zero runtime dependencies maintained - pure stdlib only

This change enables integration into projects still using Python 3.10 or 3.11, including the original use case: [ocroot](https://github.com/fxstein/ocroot) which uses Python 3.10.1.

**CI/CD Infrastructure Fix**

Fixed a scheduled workflow failure where performance benchmarks were generating ASCII boxes with variable-width content, causing false-positive alignment errors. The fix introduces a static `tests/fixtures/benchmark_test.md` file with 100 properly formatted boxes, ensuring:

- Reproducible benchmark results
- Faster execution (no runtime generation overhead)
- No false errors during performance testing
- Valid test data that passes linter validation

**Testing Coverage**

All features are now tested across:
- **Python versions:** 3.10, 3.11, 3.12
- **Platforms:** Ubuntu, macOS, Windows (in scheduled workflows)
- **Zero-dependency verification:** Ensures no runtime dependencies across all versions

**Integration Ready**

Users can now install `ascii-guard` on any Python 3.10+ environment:

```bash
pip install ascii-guard
```

Or integrate into pre-commit hooks for Python 3.10+ projects:

```yaml
- repo: https://github.com/fxstein/ascii-guard
  rev: v1.1.0
  hooks:
    - id: ascii-guard
```

**Quality & Stability**

- All CI/CD workflows passing across all Python versions
- 100% backward compatible with existing Python 3.12 users
- No breaking changes to API or CLI interface
- Zero runtime dependencies maintained

---

### ✨ Added

- feat: Add support for Python 3.10 and 3.11 ([f14e862](https://github.com/fxstein/ascii-guard/commit/f14e8628ecf70358287af21e281cebbdb507bd04))
- feat(task#32): Add clean CI/CD monitoring helper scripts ✅ ([7aa3203](https://github.com/fxstein/ascii-guard/commit/7aa32036d3ba3d32c4b45edd1cc031d7fd526d92))

### 🔄 Changed

- chore: Update release log for 1.0.0 ([b009a4c](https://github.com/fxstein/ascii-guard/commit/b009a4c6fb5c70f47d758320869b3d5fd1608ce6))

### 🐛 Fixed

- fix: Use static benchmark test file to prevent scheduled test failures ([926cf1a](https://github.com/fxstein/ascii-guard/commit/926cf1a1c84a5bb3a131e0fb522193e1a2e2b55e))

*Documentation, maintenance, and other commits: 6*

*Total commits: 10*
