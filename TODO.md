# Project ToDo List

> **⚠️ IMPORTANT: This file should ONLY be edited through the `todo.ai` script!**

## Tasks
- [ ] **#17** Implement .ascii-guard config file with gitignore-style exclusion patterns `#feature`
  > ZERO dependencies: Use pathlib.Path.match() and fnmatch from stdlib. Config file format: .ascii-guard in project root or ~/.ascii-guard. Support gitignore syntax: *.log, build/, **/dist/**, !important.md (negation). CLI: auto-detect .ascii-guard, or --config flag to override. Example patterns: node_modules/, .git/, **/__pycache__/**, *.tmp
  - [ ] **#17.4** Add tests for config parsing and pattern matching `#feature`
  - [ ] **#17.3** Integrate config file loading into CLI (auto-detect or --config flag) `#feature`
  - [ ] **#17.2** Add path matcher with gitignore-style pattern support (fnmatch, pathlib) `#feature`
  - [ ] **#17.1** Create config parser module (read .ascii-guard, parse patterns) `#feature`
- [ ] **#16** Adapt release process for ascii-guard (release.sh, RELEASE.md, Cursor rules) `#release` `#automation`
- [ ] **#15** Review and update DESIGN.md based on PyPI release requirements `#documentation` `#design`
  > CRITICAL UPDATE NEEDED: DESIGN.md mentions dependencies (markdown, click, colorama) - these must be REMOVED. ascii-guard is ZERO dependency stdlib-only tool. Update dependencies section to reflect: Python 3.11+ stdlib only, NO external packages.
- [ ] **#14** Add CONTRIBUTING.md and CODE_OF_CONDUCT.md files `#documentation` `#community`
- [ ] **#13** Set up semantic versioning and release tagging workflow `#release` `#versioning`
- [x] **#12** Create GitHub repository and push initial setup `#setup` `#github`
- [x] **#11** Initialize git repository and create .gitignore for Python `#setup` `#git`
  > Python .gitignore must include: .venv/, venv/, __pycache__/, *.pyc, *.pyo, *.egg-info/, dist/, build/, .pytest_cache/, .mypy_cache/, .ruff_cache/, .coverage, htmlcov/. Use GitHub's Python template as base.
- [x] **#10** Write README with project overview and AI agent installation prompt `#documentation`
  > Emphasize in README: 'ZERO dependencies - pure Python stdlib only'. This is a KEY FEATURE. AI agent prompt should be: 'pip install ascii-guard' (no other deps needed). Highlight: lightweight, fast, no dependency hell.
  > README must include: (1) AI agent prompt for pip install, (2) Developer setup with venv isolation, (3) pre-commit installation instructions. Example: 'Install: python -m venv .venv && source .venv/bin/activate && pip install ascii-guard' for users, 'git clone && ./setup-venv.sh && pre-commit install' for contributors.
- [ ] **#9** Create comprehensive documentation (usage, examples, API) `#documentation`
- [ ] **#8** Configure PyPI publishing workflow with GitHub Actions `#cicd` `#pypi`
- [x] **#7** Set up GitHub Actions CI/CD workflow (lint, test, build) `#cicd` `#automation`
  > GitHub Actions workflow must use 'pre-commit run --all-files' for consistency. Same hooks locally and in CI. Add matrix testing for Python 3.11, 3.12, 3.13. Cache pip and pre-commit environments.
- [x] **#6** Add comprehensive test suite with pytest `#testing`
  > Test suite uses pytest (dev dependency only). The linter itself must work standalone with ZERO deps. Tests verify: stdlib-only usage, no import of external packages, works with python -m ascii_guard.
- [x] **#5** Implement CLI interface with lint and fix commands `#feature` `#cli`
  > CRITICAL: Use argparse (stdlib) only, NO click/typer. Simple CLI: 'ascii-guard lint <file>', 'ascii-guard fix <file>'. ANSI escape codes for colored output (no colorama). Keep it minimal and standalone.
- [x] **#4** Create core linter module structure (detection, validation, fixing) `#feature`
  > CRITICAL: ZERO runtime dependencies. Use only Python stdlib. No external libs (no markdown, no click, no colorama). Pure Python 3.11+ stdlib only. Parse files with open(), use argparse for CLI, ANSI codes for colors.
- [x] **#3** Set up development tooling (ruff, black, mypy, pytest) `#setup` `#tooling`
  > CRITICAL: Use pre-commit framework for ALL linting. Install: 'pip install pre-commit'. Config .pre-commit-config.yaml with: ruff (lint+format), mypy (types), pytest (tests), trailing-whitespace, end-of-file-fixer, check-yaml. Run 'pre-commit install' to enable hooks. NO system-level tool pollution.
  - [x] **#3.3** Add git hooks installation to setup process `#setup` `#tooling`
    > Requires git repository (task#11) to be initialized first. Run 'pre-commit install' after git init. Pre-commit config is ready in .pre-commit-config.yaml.
  - [x] **#3.2** Create .pre-commit-config.yaml with ruff, mypy, pytest hooks `#setup` `#tooling`
  - [x] **#3.1** Install and configure pre-commit framework `#setup` `#tooling`
- [x] **#2** Add Apache 2.0 license file and copyright headers `#setup` `#license`
- [x] **#1** Initialize Python project structure with pyproject.toml and standard layout `#setup`
  > pyproject.toml: ZERO runtime dependencies (dependencies = [ ]). Dev dependencies only: pytest, ruff, mypy, pre-commit. Package must be installable with 'pip install ascii-guard' with no external deps. Pure stdlib tool.
  > CRITICAL: Use venv isolation. Create .python-version (3.11+), setup-venv.sh script. Document in README: 'python -m venv .venv && source .venv/bin/activate && pip install -e .[dev]'. Add .venv/ to .gitignore.
  - [x] **#1.2** Create virtual environment setup script (setup-venv.sh) `#setup` `#venv`
  - [x] **#1.1** Create .python-version file for Python version pinning `#setup` `#venv`

------------------

## Recently Completed

---

**Last Updated:** Sun Nov 16 16:39:31 CET 2025
**Maintenance:** Use `todo.ai` script only

## Task Metadata

Task relationships and dependencies (managed by todo.ai tool).
View with: `./todo.ai show <task-id>`

<!-- TASK RELATIONSHIPS
-->
