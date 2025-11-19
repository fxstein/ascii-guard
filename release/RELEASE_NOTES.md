# ascii-guard v1.4.0

This release strengthens ascii-guard's validation capabilities and test quality. The linter now validates ASCII boxes inside markdown code blocks by default, fixing a regression where code examples were incorrectly skipped. Users who prefer the old behavior can use the new `--exclude-code-blocks` flag. Additionally, table column continuity validation has been added, detecting missing bottom junction points (`┴`) in tables with column separators, ensuring visual consistency across complex ASCII art structures.

The test suite has been significantly expanded with comprehensive coverage improvements across all modules. Test coverage increased from 93% to 96%, with critical modules like cli.py jumping from 83% to 97% and detector.py achieving 100% coverage. These improvements include edge case testing for exception handling, configuration validation, and pattern matching, providing stronger confidence in code quality and reducing the likelihood of regressions.

Users benefit from more accurate validation, fewer false negatives in code examples, better detection of stylistic inconsistencies in tables, and a more robust, well-tested codebase. The enhanced test coverage ensures that future updates maintain high quality standards while the new validation features help maintain professional documentation with consistently formatted ASCII art.

---

### ✨ Added

- feat: Add table column continuity validation (task#53) ([3eb5e49](https://github.com/fxstein/ascii-guard/commit/3eb5e49199231d971137bbaeabbd8675a318282b))
- chore: Add task list for table column continuity validation (task#53) ([5d8ea86](https://github.com/fxstein/ascii-guard/commit/5d8ea86c4cd42fbd79fd421955d2b3d95fc32451))
- fix: Validate ASCII boxes in code blocks by default, add --exclude-code-blocks flag (Issue #11) ([adf322b](https://github.com/fxstein/ascii-guard/commit/adf322b92caa926b50b0bc66b0de5e5ec1613797))
- chore: Add task list for Issue #11 - code block detection regression (task#52) ([9e295a0](https://github.com/fxstein/ascii-guard/commit/9e295a0df255aa6a7344054ca53c494881962864))
- chore: Add retry-push files to gitignore ([980923b](https://github.com/fxstein/ascii-guard/commit/980923bf9384f97923f26c148bfa3647f3b72abe))

### 🔄 Changed

- chore: update task tracker (task#54.1, task#54.2 complete) ([275a78a](https://github.com/fxstein/ascii-guard/commit/275a78a9b7301a6ed3e0510c60d4c5c86b28522a))
- test: improve cli and config coverage to 97% and 95% (task#54.1, task#54.2) ([1b1251c](https://github.com/fxstein/ascii-guard/commit/1b1251c0c3fa9e5fbd742269f65eb1dc5cc3beaf))
- test: Improve cli.py coverage from 79% to 82% (task#54.1, task#54) ([163913c](https://github.com/fxstein/ascii-guard/commit/163913cefd54ff0c9854d5b2ffc8dfe78d781514))
- test: Improve config.py coverage from 84% to 92% (task#54.2) ([e6a0d86](https://github.com/fxstein/ascii-guard/commit/e6a0d8672e38cd178e9a035bdbcd7035e6370ba0))
- test: Improve linter.py coverage from 84% to 97% (task#54.5) ([eed9124](https://github.com/fxstein/ascii-guard/commit/eed912407f4ff72e45bac484ab6ef7a637e00301))
- test: Improve patterns.py coverage from 85% to 89% (task#54.7) ([133bf0b](https://github.com/fxstein/ascii-guard/commit/133bf0b33a1660694b403f7eb71511aaddbc4157))
- test: Improve validator.py coverage from 88% to 94% (task#54.9) ([68b80c2](https://github.com/fxstein/ascii-guard/commit/68b80c246db7456caae5dc094e23e7fbc06f6e28))
- test: Improve test coverage for models.py and fixer.py (task#54.6, task#54.4) ([c4f0b0e](https://github.com/fxstein/ascii-guard/commit/c4f0b0e4f66c50a906c7f81d24fe82aebfada3e9))

*Documentation, maintenance, and other commits: 2*

*Total commits: 15*
