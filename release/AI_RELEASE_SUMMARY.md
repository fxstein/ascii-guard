This release introduces comprehensive configuration file support, enabling project-wide customization and automated directory scanning. The new `.ascii-guard.toml` configuration system allows teams to define file filtering rules using familiar gitignore-style patterns, making it easy to exclude build directories, temporary files, and other irrelevant content from linting.

The major enhancement is directory scanning capability. Users can now run `ascii-guard lint .` to recursively scan entire project directories, with intelligent filtering based on configuration rules. The scanner automatically detects text files versus binary files, respects file size limits, and applies exclude/include patterns to focus on relevant documentation.

The implementation introduces a strategic dependency approach: Python 3.11+ users enjoy zero runtime dependencies using the stdlib `tomllib` module, while Python 3.10 users require only the lightweight `tomli` package for TOML parsing. This maintains the project's minimal dependency philosophy while expanding Python version compatibility.

Pattern matching supports essential gitignore-style syntax including wildcards (`*.md`), directory patterns (`node_modules/`), recursive patterns (`**/test/**`), and negation for include overrides (`!important.md`). The CLI now accepts both files and directories as arguments, with explicit file paths bypassing filters for maximum flexibility.

The release includes 79 new test cases across integration, config parsing, pattern matching, and scanner modules, bringing total test coverage to 163 tests. An example `.ascii-guard.toml` configuration file demonstrates best practices for project setup, and comprehensive design documentation in `docs/CONFIG_DESIGN.md` guides users through all configuration options.

This release maintains full backward compatibility—existing command-line usage continues to work unchanged, while new features are opt-in through configuration files and directory arguments.
