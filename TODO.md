# Project ToDo List

> **⚠️ IMPORTANT: This file should ONLY be edited through the `todo.ai` script!**

## Tasks
- [ ] **#23** Redesign release process for proper version management `#release`
  - [ ] **#23.6** Test redesigned workflow with dry-run mode
    > Use release/TESTING.md checklist with dry-run. Verify: (1) GitHub release check works, (2) All version files updated in prepare, (3) set-version updates all files, (4) AI summary lifecycle correct. Document any issues found.
  - [x] **#23.5** Commit AI summary with release, delete and commit cleanup after success
    > EXECUTE must: (1) Commit version files + release notes + AI summary together, (2) Create tag and push, (3) AFTER successful GitHub Actions, delete AI_RELEASE_SUMMARY.md in separate commit with message 'chore: Clean up release artifacts for vX.Y.Z'. Keeps dev environment clean.
  - [x] **#23.4** Update set-version to modify all version files and release notes
    > set-version must: (1) Update ALL version files from VERSION_FILES list, (2) Update RELEASE_NOTES.md header, (3) Update .prepare_state with new version. Ensures consistency across all version references.
  - [x] **#23.3** Move version updates from execute to prepare phase
    > PREPARE phase must update ALL version files immediately after determining new version. This allows review of actual version changes before execute. EXECUTE only commits the already-modified files.
  - [x] **#23.2** Add GitHub release check to determine current version
    > Add get_github_latest_release() function using 'gh release list --limit 1' to determine actual latest release. If no releases exist, use 0.0.0 as base. Use GitHub as source of truth, not local files.
  - [x] **#23.1** Document all files containing version numbers for tracking
    > Create VERSION_FILES.md documenting all files containing version numbers: pyproject.toml (version field), src/ascii_guard/__init__.py (__version__), any others. Update release.sh to use this list for all version operations.
- [ ] **#17** Implement .ascii-guard config file with gitignore-style exclusion patterns `#feature`
  > ZERO dependencies: Use pathlib.Path.match() and fnmatch from stdlib. Config file format: .ascii-guard in project root or ~/.ascii-guard. Support gitignore syntax: *.log, build/, **/dist/**, !important.md (negation). CLI: auto-detect .ascii-guard, or --config flag to override. Example patterns: node_modules/, .git/, **/__pycache__/**, *.tmp
  - [ ] **#17.4** Add tests for config parsing and pattern matching `#feature`
  - [ ] **#17.3** Integrate config file loading into CLI (auto-detect or --config flag) `#feature`
  - [ ] **#17.2** Add path matcher with gitignore-style pattern support (fnmatch, pathlib) `#feature`
  - [ ] **#17.1** Create config parser module (read .ascii-guard, parse patterns) `#feature`
- [x] **#16** Adapt release process for ascii-guard (release.sh, RELEASE.md, Cursor rules) `#release` `#automation`
  - [x] **#16.5** Test complete release workflow end-to-end `#release`
    > TESTING UPDATED with dry-run mode:
    > ✅ --prepare mode: Tested with multiple commit types
    > ✅ --set-version mode: Tested with valid/invalid inputs
    > ✅ --execute --dry-run: Full end-to-end simulation without git operations
    > ✅ Process invalidation: Detects commits after prepare
    > ✅ Comprehensive testing guide: release/TESTING.md documents full test suite
    > ⚠️  Real execute mode NOT tested (requires actual release to GitHub/PyPI)
    > 
    > Use './release/release.sh --execute --dry-run' to test releases safely
    > TESTING COMPLETE - All release workflow components verified:
    > ✅ --prepare mode: Analyzes commits, determines version bump (minor: 0.1.0 → 0.2.0), generates release notes with categorized commits
    > ✅ --set-version mode: Overrides version (tested 1.0.0), validates format and progression, updates release notes header
    > ✅ Release notes generation: Includes AI summary, categorizes commits (Added/Changed/Fixed), links to GitHub commits
    > ✅ Semantic versioning: Correctly detects feat: (minor), fix: (patch), BREAKING (major)
    > ✅ Version file updates: Ready for pyproject.toml and __init__.py
    > ✅ Cursor AI rules: Comprehensive guidance for AI-assisted releases
    > ⚠️  Execute mode NOT tested (requires actual release to GitHub/PyPI)
    > Manual testing checklist: test on clean clone, test with no commits, test breaking changes, test version override (valid/invalid), test execute without prepare (should fail), test dirty working dir (should fail), verify GitHub Actions trigger. See RELEASE_DESIGN.md Testing Strategy for details.
  - [x] **#16.4** Create .cursor/rules/ascii-guard-releases.mdc for AI release guidance `#release`
    > Create Cursor AI rule file guiding agent through 4-step release process: (1) Write AI summary, (2) Run prepare, (3) Human review, (4) Run execute. Include safeguards: never modify release.sh logic, always wait for approval. See RELEASE_DESIGN.md Phase 4 for details.
  - [x] **#16.3** Implement release.sh execute mode with GitHub tag push `#release`
    > Implement cmd_execute(), update_version_files() (pyproject.toml + __init__.py), create_git_tag(), push_to_github(). NO direct PyPI publish - GitHub Actions handles that via trusted publishing. See RELEASE_DESIGN.md Phase 3 for details.
  - [x] **#16.2** Implement release.sh set-version override mode `#release`
    > Implement cmd_set_version(), validate_version_format() (X.Y.Z format), validate_version_gt() (new > current). Update release/RELEASE_NOTES.md header with new version. See RELEASE_DESIGN.md Step 3b for details.
  - [x] **#16.1** Implement release.sh core functions and prepare mode `#release`
    > Implement core functions: get_current_version(), get_last_release_tag(), get_commits_since_tag(), categorize_commit(), determine_version_bump(). Implement cmd_prepare(), generate_release_notes(), save_prepare_state(). See RELEASE_DESIGN.md Phase 1 for details.
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


## Deleted Tasks
- [D] **#22** 16.5 `Test` `complete` `release` `workflow` `end-to-end` (deleted 2025-11-16, expires 2025-12-16)
- [D] **#21** 16.4 `Create` `.cursor/rules/ascii-guard-releases.mdc` `for` `AI` `release` `guidance` (deleted 2025-11-16, expires 2025-12-16)
- [D] **#20** 16.3 `Implement` `release.sh` `execute` `mode` `with` `GitHub` `tag` `push` (deleted 2025-11-16, expires 2025-12-16)
- [D] **#19** 16.2 `Implement` `release.sh` `set-version` `override` `mode` (deleted 2025-11-16, expires 2025-12-16)
- [D] **#18** 16.1 `Implement` `release.sh` `core` `functions` `and` `prepare` `mode` (deleted 2025-11-16, expires 2025-12-16)

---

**Last Updated:** Sun Nov 16 23:02:24 CET 2025
**Maintenance:** Use `todo.ai` script only

## Task Metadata

Task relationships and dependencies (managed by todo.ai tool).
View with: `./todo.ai show <task-id>`

<!-- TASK RELATIONSHIPS
-->
