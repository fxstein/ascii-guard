# ascii-guard v2.0.0

This release introduces a comprehensive, well-defined Python API for ascii-guard, making it easy to use the tool programmatically in Python applications and scripts. The API provides stable, well-documented functions for linting, fixing, and detecting ASCII art boxes, with full type hints and comprehensive error handling.

Key improvements include a new FixResult dataclass that replaces the previous tuple return from fix_file(), providing a cleaner and more maintainable API. All file path parameters now accept both string and Path objects for better flexibility. The public API is now exported from the package root, allowing clean imports like `from ascii_guard import lint_file, fix_file, detect_boxes`.

The release includes complete API documentation with a new API_REFERENCE.md guide, updated usage examples in USAGE.md, and enhanced FAQ entries. Import paths remain backward compatible (old imports still work), while new package root imports are recommended. The implementation maintains 96% test coverage and all 247 tests pass successfully.

## ⚠️ Breaking Changes

- **`fix_file()` return type changed**: Now returns `FixResult` dataclass instead of `tuple[int, list[str]]`
  - **Migration**: Change `boxes_fixed, lines = fix_file(...)` to `result = fix_file(...)` then use `result.boxes_fixed` and `result.lines`
  - **Impact**: Code that unpacks the return value from `fix_file()` will need to be updated

---

### ✨ Added

- chore: Update Python version to 3.13 and add release summary ([80f16f0](https://github.com/fxstein/ascii-guard/commit/80f16f0351df7fd58bee79f400b0bf3fbe490308))
- docs: Add Python API documentation (task#69.17-69.19) ([37dce64](https://github.com/fxstein/ascii-guard/commit/37dce64175df11e87f4937661dc775b256791778))
- docs: Add Python API design document (task#69.2-69.8, approved) ([2077ff1](https://github.com/fxstein/ascii-guard/commit/2077ff19fc14959a4ddfaa212d1b2c41da14ac0d))
- docs: Add API analysis document for Python API design (task#69.1) ([43a6dfd](https://github.com/fxstein/ascii-guard/commit/43a6dfd0298a741b460c9806d3b81f33a4c45e42))

### 🔄 Changed

- chore: Update task status for testing phase completion (task#69.14-69.16) ([26b8cf7](https://github.com/fxstein/ascii-guard/commit/26b8cf70c920bd60ff1c4adc87e7606f3890a78f))
- fix: Update remaining test to use FixResult (task#69) ([0f4b3c9](https://github.com/fxstein/ascii-guard/commit/0f4b3c9f5a531218c42397618946d24d1cc97ede))
- docs: Update documentation with Python version corrections and task updates ([f2e0e06](https://github.com/fxstein/ascii-guard/commit/f2e0e061c90fedf9bd25ab42ea271dd73013df5f))
- chore: Update release log for 1.6.0 ([d6f885a](https://github.com/fxstein/ascii-guard/commit/d6f885a2486acfa9b53d7fd50eee4ccf93c9ded0))

*Total commits: 8*
