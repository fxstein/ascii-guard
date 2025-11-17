# Project ToDo List

> **⚠️ IMPORTANT: This file should ONLY be edited through the `todo.ai` script!**

## Tasks
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
- [x] **#29** Harden pyenv+venv setup to prevent global Python pollution (2025-11-17)
  > PROBLEM: Current setup is fragile - relies on remembering to activate venv. We polluted pyenv global with pytest/pytest-cov during task#24 fixes. Pre-commit uses 'language: system' which depends on whatever Python is in PATH. SOLUTION: 1) Clean pyenv global (keep it pristine). 2) Change pre-commit pytest hook to explicitly use '.venv/bin/python -m pytest' so it always uses venv Python. 3) Add venv checks to critical scripts (release.sh). 4) Document in Cursor rules: NEVER pip install in pyenv global, ALWAYS use venv. 5) Test that commits work from fresh shell without manual venv activation.
  - [x] **#29.5** Test: Verify pre-commit works from fresh shell (no venv activated) (2025-11-17)
  - [x] **#29.4** Update .cursor/rules: AI must NEVER install packages in pyenv global (2025-11-17)
  - [x] **#29.3** Add venv validation to release.sh and other scripts (2025-11-17)
  - [x] **#29.2** Fix pre-commit to use .venv/bin/python explicitly (not system) (2025-11-17)
  - [x] **#29.1** Clean up pyenv global: uninstall pytest, pytest-cov (2025-11-17)
- [x] **#32** Create clean CI/CD monitoring helper script (2025-11-17)
- [x] **#31** Fix release.sh to use .venv/bin/python for package build (2025-11-17)
- [x] **#30** Fix CI: Create and use venv in GitHub Actions (2025-11-17)
- [x] **#28** Fix release notes: Script generates H1, AI summary has NO headers (2025-11-17)
  > Correct design: 1) release.sh generates proper H1 header: '# ascii-guard vX.Y.Z - Release Title' 2) AI agent writes AI_RELEASE_SUMMARY.md WITHOUT any headers (just content paragraphs) 3) Script appends AI content under the H1. Changes needed: A) Update release.sh line 316 to generate H1 instead of H2. B) Update set_version_override() to update H1 instead of H2+H1. C) Update .cursor/rules/ascii-guard-releases.mdc to instruct AI to NOT include headers in AI_RELEASE_SUMMARY.md. D) Update docs/RELEASE_DESIGN.md and release/RELEASE.md examples.
  - [x] **#28.5** Test: prepare + set-version with header-less AI summary (2025-11-17)
  - [x] **#28.4** Update docs/RELEASE_DESIGN.md and release/RELEASE.md examples (2025-11-17)
  - [x] **#28.3** Update .cursor/rules to instruct AI: NO headers in AI_RELEASE_SUMMARY.md (2025-11-17)
  - [x] **#28.2** Update set_version_override() to update only H1 header (2025-11-17)
  - [x] **#28.1** Update release.sh to generate H1 header instead of H2 (2025-11-17)
- [x] **#26** Fix set-version to update all version references in AI summary (2025-11-17)
  > Bug: set-version only updates '## Release X.Y.Z' header but does NOT update version numbers in the AI summary content. Example: Line 1 shows '## Release 1.0.0' but line 3 still shows '# ascii-guard v0.1.0'. Fix: set_version_override() in release.sh needs to update ALL version occurrences in RELEASE_NOTES.md, including the H1 header inside AI summary. Location: release.sh set_version_override() function around line 411-433.
- [x] **#25** Fix release script to validate generated files before commit (2025-11-17)
  > Added validation in execute_release() at line 573-593. Pre-commit runs on all generated release files before git commit. Fixes EOF/whitespace automatically. Tested: pre-commit hooks passed on release.sh changes.
  > Issue: release.sh generates AI_RELEASE_SUMMARY.md and RELEASE_NOTES.md but doesn't run pre-commit validation on them. When git commit runs, pre-commit hooks fix EOF/whitespace, causing commit to fail. Fix: Add validation step after generating release files - run pre-commit hooks on generated files BEFORE attempting git commit. Location: release.sh execute_release() function, after generate_release_notes() and before git commit.
- [x] **#24** Fix release process issues identified during v0.1.0 attempt (2025-11-17)
  - [x] **#24.5** Test complete release workflow with dry-run after fixes (2025-11-17)
    > Dry-run test passed: environment validation ✓, prepare phase ✓, execute --dry-run ✓. All components working correctly. CI/CD was green before testing.
    > After completing tasks 24.1-24.4, run: ./release/release.sh --prepare then ./release/release.sh --execute --dry-run. Verify: 1) No Python errors, 2) No pre-commit failures, 3) All version files updated correctly, 4) Dry-run simulates complete workflow.
  - [x] **#24.4** Update release.sh to NEVER use --no-verify flag (2025-11-17)
    > Search release.sh for '--no-verify' and 'git commit.*--no-verify'. Remove all instances. Release commits MUST pass pre-commit hooks.
  - [x] **#24.3** Fix pre-commit issues: run hooks on all files and commit fixes (2025-11-17)
    > Run: pre-commit run --all-files. If failures, stage fixed files and commit WITHOUT --no-verify. This ensures clean state before any release.
  - [x] **#24.2** Add environment validation to release.sh (check Python, build module, gh CLI) (2025-11-17)
    > Add validate_environment() function at start of release.sh --prepare. Check: 1) Python version matches .python-version, 2) python3 -m build available, 3) gh CLI installed. Exit with clear error if validation fails.
  - [x] **#24.1** Resolve Python version mismatch: install 3.12 OR revert all configs to 3.10 (2025-11-17)
    > Python 3.12.7 installed and working. Venv rebuilt with Python 3.12. Fixed pre-commit to use .venv/bin/pytest for proper isolation.
    > Check: pyenv versions | grep 3.12. If not found, either install Python 3.12 OR revert .python-version, pyproject.toml, setup-venv.sh, and all GitHub Actions workflows back to 3.10.1
- [x] **#23** Redesign release process for proper version management `#release` (2025-11-17)
  - [x] **#23.6** Test redesigned workflow with dry-run mode (2025-11-17)
    > Use release/TESTING.md checklist with dry-run. Verify: (1) GitHub release check works, (2) All version files updated in prepare, (3) set-version updates all files, (4) AI summary lifecycle correct. Document any issues found.
  - [x] **#23.5** Commit AI summary with release, delete and commit cleanup after success (2025-11-17)
    > EXECUTE must: (1) Commit version files + release notes + AI summary together, (2) Create tag and push, (3) AFTER successful GitHub Actions, delete AI_RELEASE_SUMMARY.md in separate commit with message 'chore: Clean up release artifacts for vX.Y.Z'. Keeps dev environment clean.
  - [x] **#23.4** Update set-version to modify all version files and release notes (2025-11-17)
    > set-version must: (1) Update ALL version files from VERSION_FILES list, (2) Update RELEASE_NOTES.md header, (3) Update .prepare_state with new version. Ensures consistency across all version references.
  - [x] **#23.3** Move version updates from execute to prepare phase (2025-11-17)
    > PREPARE phase must update ALL version files immediately after determining new version. This allows review of actual version changes before execute. EXECUTE only commits the already-modified files.
  - [x] **#23.2** Add GitHub release check to determine current version (2025-11-17)
    > Add get_github_latest_release() function using 'gh release list --limit 1' to determine actual latest release. If no releases exist, use 0.0.0 as base. Use GitHub as source of truth, not local files.
  - [x] **#23.1** Document all files containing version numbers for tracking (2025-11-17)
    > Create VERSION_FILES.md documenting all files containing version numbers: pyproject.toml (version field), src/ascii_guard/__init__.py (__version__), any others. Update release.sh to use this list for all version operations.


## Deleted Tasks
- [D] **#27** Remove H2 header from release notes - fix markdown hierarchy (deleted 2025-11-17, expires 2025-12-17)
- [D] **#22** 16.5 `Test` `complete` `release` `workflow` `end-to-end` (deleted 2025-11-16, expires 2025-12-16)
- [D] **#21** 16.4 `Create` `.cursor/rules/ascii-guard-releases.mdc` `for` `AI` `release` `guidance` (deleted 2025-11-16, expires 2025-12-16)
- [D] **#20** 16.3 `Implement` `release.sh` `execute` `mode` `with` `GitHub` `tag` `push` (deleted 2025-11-16, expires 2025-12-16)
- [D] **#19** 16.2 `Implement` `release.sh` `set-version` `override` `mode` (deleted 2025-11-16, expires 2025-12-16)
- [D] **#18** 16.1 `Implement` `release.sh` `core` `functions` `and` `prepare` `mode` (deleted 2025-11-16, expires 2025-12-16)

---

**Last Updated:** Mon Nov 17 02:10:22 CET 2025
**Maintenance:** Use `todo.ai` script only

## Task Metadata

Task relationships and dependencies (managed by todo.ai tool).
View with: `./todo.ai show <task-id>`

<!-- TASK RELATIONSHIPS
-->
