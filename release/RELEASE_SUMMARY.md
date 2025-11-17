# ascii-guard v1.2.0

This release introduces comprehensive configuration file support, enabling project-wide customization and automated directory scanning. The new `.ascii-guard.toml` configuration system allows teams to define file filtering rules using familiar gitignore-style patterns, making it easy to exclude build directories, temporary files, and other irrelevant content from linting.

The major enhancement is directory scanning capability. Users can now run `ascii-guard lint .` to recursively scan entire project directories, with intelligent filtering based on configuration rules. The scanner automatically detects text files versus binary files, respects file size limits, and applies exclude/include patterns to focus on relevant documentation.

The implementation introduces a strategic dependency approach: Python 3.11+ users enjoy zero runtime dependencies using the stdlib `tomllib` module, while Python 3.10 users require only the lightweight `tomli` package for TOML parsing. This maintains the project's minimal dependency philosophy while expanding Python version compatibility.

Pattern matching supports essential gitignore-style syntax including wildcards (`*.md`), directory patterns (`node_modules/`), recursive patterns (`**/test/**`), and negation for include overrides (`!important.md`). The CLI now accepts both files and directories as arguments, with explicit file paths bypassing filters for maximum flexibility.

The release includes 79 new test cases across integration, config parsing, pattern matching, and scanner modules, bringing total test coverage to 163 tests. An example `.ascii-guard.toml` configuration file demonstrates best practices for project setup, and comprehensive design documentation in `docs/CONFIG_DESIGN.md` guides users through all configuration options.

This release maintains full backward compatibility—existing command-line usage continues to work unchanged, while new features are opt-in through configuration files and directory arguments.

---

### ✨ Added

- feat: Add comprehensive integration tests (task#17.10) ([69f5e5e](https://github.com/fxstein/ascii-guard/commit/69f5e5ede9cf7350ff12e6de5bf5ddadb05dba81))
- feat: Integrate config and scanner into CLI (task#17.9) ([681ef9b](https://github.com/fxstein/ascii-guard/commit/681ef9b324229ca69f1d29f9e3c0a46dca46330f))
- feat: Implement directory scanner with file filtering (task#17.8) ([1fe94bc](https://github.com/fxstein/ascii-guard/commit/1fe94bcde8f8f9bfdfaa537b82f2a98141f16104))
- feat: Implement pattern matching for file filtering (task#17.7) ([ccdf9c9](https://github.com/fxstein/ascii-guard/commit/ccdf9c953368b3e0f5d43b9c58bb1835c4d8f9e7))
- feat: Implement config parser with version-aware TOML import (task#17.5, task#17.6) ([b5e0677](https://github.com/fxstein/ascii-guard/commit/b5e0677fa721b551ea15d27440f4deb1deac8b72))
- feat: Design and plan config file implementation (task#17) ([28655f7](https://github.com/fxstein/ascii-guard/commit/28655f772e7d886e8cf93f331b6412f39a0a1f66))

### 🔄 Changed

- chore: Archive task#15 (DESIGN.md update complete) ([5114e00](https://github.com/fxstein/ascii-guard/commit/5114e000c7139a150d566165a798007ba5bf181c))
- chore: Mark task#15 complete (DESIGN.md update) ([984d9dc](https://github.com/fxstein/ascii-guard/commit/984d9dc91a74e7acc9a841900638ab509697281b))
- docs: Update DESIGN.md for Python 3.10+ support (task#15) ([2d85627](https://github.com/fxstein/ascii-guard/commit/2d85627346195473200d91accb13317825e32d75))

*Documentation, maintenance, and other commits: 4*

*Total commits: 13*
