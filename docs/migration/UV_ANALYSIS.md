# UV Migration Analysis

**Date:** 2025-12-13
**Purpose:** Comprehensive analysis of current Python package management setup to inform migration to `uv`

---

## Executive Summary

This document analyzes the current Python package management infrastructure in the ascii-guard project, identifying all components that use `venv`, `pip`, `pipx`, and Python version management. The analysis covers development workflows, CI/CD pipelines, pre-commit hooks, and release processes to ensure a complete migration to `uv`.

---

## 1. Current Python Version Management

### 1.1 Version Specification Files

- **`.python-version`**: Contains `3.14.2` (specific patch version)
  - Used by `pyenv` for local development
  - Referenced in `release/release.sh` for version validation
  - Current venv uses Python 3.14.2 from Homebrew

### 1.2 Version Requirements

- **`pyproject.toml`**: `requires-python = ">=3.10"`
  - Supports Python 3.10, 3.11, 3.12, 3.13, 3.14
  - Conditional dependency: `tomli>=2.0.0; python_version < '3.11'`

### 1.3 Version Usage in CI/CD

- **CI Matrix**: Tests against `["3.10", "3.11", "3.12", "3.13", "3.14"]`
- **Release Workflow**: Uses Python 3.13 for validation and builds
- **PR Checks**: Uses Python 3.12 for code quality checks
- **Scheduled Tests**: Tests `["3.10", "3.11", "3.12"]` on multiple OS platforms

---

## 2. Virtual Environment Management

### 2.1 Current Setup

- **Location**: `.venv/` directory (gitignored)
- **Creation Method**: `python3 -m venv .venv` or `python -m venv .venv`
- **Activation**: `source .venv/bin/activate` (bash/zsh)
- **Validation**: Scripts check for `.venv/bin/python` existence

### 2.2 Files Using venv

#### Setup Scripts
- **`setup.sh`**:
  - Creates venv: `python3 -m venv .venv`
  - Activates venv: `source .venv/bin/activate`
  - Upgrades pip: `pip install --upgrade pip --quiet`
  - Installs package: `pip install -e ".[dev]" --quiet`
  - Uses `.venv/bin/pre-commit`, `.venv/bin/ascii-guard`, `.venv/bin/pytest`, etc.

#### Release Scripts
- **`release/release.sh`**:
  - Validates venv existence: `[[ ! -d .venv ]]`
  - Checks venv Python: `.venv/bin/python --version`
  - Validates build module: `.venv/bin/python -c "import build"`
  - Builds package: `.venv/bin/python -m build`
  - Multiple references to `.venv/bin/python` and `.venv/bin/pip`

### 2.3 CI/CD venv Usage

#### GitHub Actions Workflows

**`.github/workflows/ci.yml`**:
- Caches venv: `path: .venv`
- Creates venv: `python -m venv .venv`
- Activates venv: `source .venv/bin/activate`
- Upgrades pip: `python -m pip install --upgrade pip`
- Installs: `pip install -e .[dev]`
- Runs commands: `source .venv/bin/activate` before each step

**`.github/workflows/release.yml`**:
- Three jobs use venv:
  1. `validate-release`: Creates venv, installs dev deps, runs tests
  2. `build-and-publish`: Creates venv, installs build tools, builds package
  3. `create-github-release`: Creates venv, builds package for release assets

**`.github/workflows/pr-checks.yml`**:
- `code-quality` job: `pip install -e .[dev]` (no explicit venv, uses system Python)
- `security-scan` job: `pip install 'bandit[toml]'` (no explicit venv)
- `test-coverage` job: `pip install -e .[dev]` (no explicit venv)

**`.github/workflows/scheduled.yml`**:
- `test-multi-platform`: `pip install -e .[dev]` (no explicit venv)
- `dependency-audit`: `pip install -e .[dev]` (no explicit venv)
- `performance-benchmark`: `pip install -e .` (no explicit venv)

---

## 3. pip Usage

### 3.1 Installation Commands

**Direct pip installs:**
- `pip install --upgrade pip`
- `pip install -e .[dev]`
- `pip install -e .`
- `pip install build twine`
- `pip install build`
- `pip install 'bandit[toml]'`
- `pip install safety`

**pip list/check commands:**
- `pip list` (verify zero dependencies)
- `pip list --format=freeze` (dependency verification)
- `pip list --outdated` (dependency audit)

### 3.2 pip Caching

**CI/CD:**
- `.github/workflows/ci.yml`: Caches `~/.cache/pip`
- Cache key: `${{ runner.os }}-pip-${{ matrix.python-version }}-${{ hashFiles('pyproject.toml') }}`

### 3.3 pip in Documentation

- **README.md**: `pip install ascii-guard`
- **docs/USAGE.md**: `pip install ascii-guard`, `pip install -e .`
- **docs/FAQ.md**: `pip install --upgrade ascii-guard`
- **docs/API_REFERENCE.md**: `pip install ascii-guard`

---

## 4. pipx Usage

### 4.1 Current Usage

- **docs/USAGE.md**: Mentions `pipx install ascii-guard` as an installation option
- **No scripts or workflows use pipx** - only documentation reference

---

## 5. Pre-commit Hooks

### 5.1 Configuration

**`.pre-commit-config.yaml`**:
- Uses `language: system` for pytest hook
- Explicitly uses `.venv/bin/python -m pytest` for pytest hook
- Other hooks (ruff, mypy, pre-commit-hooks) use their own language environments

### 5.2 Installation

- **setup.sh**: Installs pre-commit hooks via `.venv/bin/pre-commit install`
- **CI/CD**: Caches `~/.cache/pre-commit` in `.github/workflows/ci.yml`

### 5.3 Execution

- **Local**: `pre-commit run --all-files`
- **CI/CD**: `pre-commit run --all-files --show-diff-on-failure`
- **Pre-commit pytest hook**: Uses `.venv/bin/python -m pytest`

---

## 6. Build and Packaging

### 6.1 Build Tools

- **Package**: `build` (from `[project.optional-dependencies.dev]`)
- **Publishing**: `twine` (from `[project.optional-dependencies.dev]`)
- **Build command**: `python -m build`
- **Check command**: `twine check dist/*`

### 6.2 Build Process

- **Release script**: Uses `.venv/bin/python -m build`
- **CI/CD build job**: Uses `python -m build` after venv activation
- **Release workflow**: Builds in multiple jobs for validation and publishing

---

## 7. Dependency Management

### 7.1 Runtime Dependencies

- **Minimal**: Only `tomli>=2.0.0; python_version < '3.11'` (conditional)
- **Zero dependencies** for Python 3.11+

### 7.2 Development Dependencies

**From `pyproject.toml`**:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
    "pre-commit>=3.5.0",
    "build>=1.0.0",
    "twine>=4.0.0",
]
```

### 7.3 Dependency Verification

- **CI job**: `verify-zero-dependencies` checks for zero runtime deps
- **PR check**: `dependency-check` validates pyproject.toml structure
- **Release validation**: Runs `test_stdlib_only.py` to verify zero deps

---

## 8. Python Version Management Tools

### 8.1 pyenv

- **Referenced in**: `release/release.sh` (suggests `pyenv install` and `pyenv local`)
- **`.python-version`**: Used by pyenv for local version
- **Not used in CI/CD**: GitHub Actions uses `actions/setup-python@v6`

### 8.2 System Python

- **setup.sh**: Checks for `python3` command
- **CI/CD**: Uses `actions/setup-python@v6` to set up Python versions
- **Release script**: Validates venv Python version matches `.python-version`

---

## 9. CI/CD Pipeline Analysis

### 9.1 Workflows Summary

| Workflow | Python Setup | venv Usage | pip Usage | Purpose |
|----------|--------------|------------|-----------|---------|
| `ci.yml` | `setup-python@v6` (matrix) | ✅ Explicit venv | ✅ Upgrade pip, install deps | Lint & test |
| `release.yml` | `setup-python@v6` (3.13) | ✅ Explicit venv | ✅ Upgrade pip, install deps | Release validation & publish |
| `pr-checks.yml` | `setup-python@v6` (3.12) | ❌ No venv | ✅ Direct pip install | Code quality checks |
| `scheduled.yml` | `setup-python@v6` (matrix) | ❌ No venv | ✅ Direct pip install | Multi-platform tests |

### 9.2 Caching Strategy

- **pip cache**: `~/.cache/pip` (ci.yml only)
- **pre-commit cache**: `~/.cache/pre-commit` (ci.yml only)
- **venv cache**: `.venv` (ci.yml and release.yml)

### 9.3 Testing Requirements

- **Matrix testing**: Python 3.10-3.14 in CI
- **Multi-platform**: Ubuntu, macOS, Windows in scheduled tests
- **Zero dependency verification**: Critical for release validation
- **Coverage reporting**: Codecov integration

---

## 10. Documentation References

### 10.1 Installation Instructions

- **README.md**: `pip install ascii-guard`
- **docs/USAGE.md**: `pip install ascii-guard`, `pipx install ascii-guard`, `pip install -e .`
- **docs/API_REFERENCE.md**: `pip install ascii-guard`
- **docs/FAQ.md**: `pip install --upgrade ascii-guard`

### 10.2 Development Setup

- **CONTRIBUTING.md**: References venv setup (needs verification)
- **setup.sh**: Complete venv-based setup script
- **Cursor rules**: Document venv usage patterns

---

## 11. Scripts and Automation

### 11.1 Setup Scripts

- **`setup.sh`**: Complete venv-based development setup
- **`release/release.sh`**: Venv validation and package building

### 11.2 Monitoring Scripts

- **`scripts/wait-for-ci.sh`**: CI monitoring (no Python deps)
- **`scripts/monitor-ci.sh`**: CI monitoring (no Python deps)

---

## 12. uv Compatibility Assessment

### 12.1 uv Capabilities

✅ **uv can handle:**
- Python version management (replaces pyenv for project-level)
- Virtual environment creation and management
- Package installation (replaces pip)
- Dependency resolution (faster than pip)
- Build and publish workflows
- CI/CD integration (GitHub Actions support)

### 12.2 uv Advantages

- **Speed**: 10-100x faster than pip
- **Unified tool**: Replaces pip, venv, pip-tools, pyenv (project-level)
- **Better dependency resolution**: More reliable than pip
- **Built-in virtualenv**: No need for `python -m venv`
- **CI/CD ready**: Official GitHub Actions support

### 12.3 Potential Challenges

- **Learning curve**: Team needs to learn uv commands
- **Documentation updates**: All docs need uv examples
- **CI/CD migration**: All workflows need updates
- **Pre-commit hooks**: May need adjustment for uv environments
- **Release scripts**: Need to use uv instead of pip/venv

---

## 13. Migration Impact Summary

### 13.1 Files Requiring Changes

**High Priority:**
- `.github/workflows/ci.yml` (venv, pip, caching)
- `.github/workflows/release.yml` (venv, pip, build)
- `.github/workflows/pr-checks.yml` (pip installs)
- `.github/workflows/scheduled.yml` (pip installs)
- `setup.sh` (venv creation, pip installs)
- `release/release.sh` (venv validation, build commands)
- `.pre-commit-config.yaml` (pytest hook path)

**Medium Priority:**
- `README.md` (installation instructions)
- `docs/USAGE.md` (installation examples)
- `docs/API_REFERENCE.md` (installation examples)
- `docs/FAQ.md` (upgrade instructions)
- `CONTRIBUTING.md` (development setup)

**Low Priority:**
- `.python-version` (may be replaced by uv's Python management)
- Cursor rules (update venv references)

### 13.2 Components to Eliminate

- ❌ `python -m venv .venv` → ✅ `uv venv`
- ❌ `source .venv/bin/activate` → ✅ `uv run` or `source .venv/bin/activate` (uv creates compatible venvs)
- ❌ `pip install` → ✅ `uv pip install` or `uv sync`
- ❌ `python -m pip install --upgrade pip` → ✅ Not needed (uv manages pip)
- ❌ `pip list` → ✅ `uv pip list` or `uv tree`
- ❌ `python -m build` → ✅ `uv build` (or keep using build, but install via uv)
- ❌ `pyenv local` → ✅ `uv python pin` or `.python-version` (uv respects it)

### 13.3 Components to Keep (uv-compatible)

- ✅ `pyproject.toml` (uv uses it natively)
- ✅ `.pre-commit-config.yaml` (hooks work with uv venvs)
- ✅ `pre-commit` framework (works with any Python environment)
- ✅ `build` and `twine` packages (install via uv, use normally)
- ✅ CI/CD matrix testing (uv supports multiple Python versions)

---

## 14. Risk Assessment

### 14.1 Low Risk

- ✅ Package building (uv supports standard build tools)
- ✅ Testing workflows (uv can install and run pytest)
- ✅ Pre-commit hooks (compatible with uv venvs)

### 14.2 Medium Risk

- ⚠️ Release process (needs thorough testing)
- ⚠️ Zero dependency verification (needs validation with uv)
- ⚠️ Documentation accuracy (many files need updates)

### 14.3 High Risk

- 🔴 CI/CD pipeline changes (affects all PRs and releases)
- 🔴 Developer workflow changes (team needs training)
- 🔴 Release script validation (critical for publishing)

---

## 15. Testing Requirements

### 15.1 Pre-Migration Testing

- [ ] Verify uv installation and basic commands
- [ ] Test uv venv creation and activation
- [ ] Test uv package installation
- [ ] Test uv with pre-commit hooks
- [ ] Test uv build and publish workflow

### 15.2 Migration Testing

- [ ] Test all CI/CD workflows with uv
- [ ] Test release process end-to-end
- [ ] Test zero dependency verification
- [ ] Test multi-platform compatibility
- [ ] Test developer setup script

### 15.3 Post-Migration Testing

- [ ] Full CI/CD pipeline run
- [ ] Release dry-run
- [ ] Documentation verification
- [ ] Developer onboarding test

---

## 16. Next Steps

1. **Create Design Document**: Detailed migration plan with uv-specific changes
2. **Create Task List**: Break down migration into implementable tasks
3. **Test uv Locally**: Verify uv works with current project structure
4. **Update CI/CD**: Migrate workflows one by one
5. **Update Scripts**: Convert setup.sh and release.sh to uv
6. **Update Documentation**: Update all installation and setup instructions
7. **Test Release Process**: Full end-to-end release test
8. **Release New Version**: Publish migration as new version

---

## Appendix: File Inventory

### Files with venv references:
- `setup.sh` (multiple)
- `release/release.sh` (multiple)
- `.github/workflows/ci.yml` (multiple)
- `.github/workflows/release.yml` (multiple)
- `.pre-commit-config.yaml` (pytest hook)

### Files with pip references:
- `setup.sh`
- `release/release.sh`
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`
- `.github/workflows/pr-checks.yml`
- `.github/workflows/scheduled.yml`
- `README.md`
- `docs/USAGE.md`
- `docs/API_REFERENCE.md`
- `docs/FAQ.md`

### Files with pipx references:
- `docs/USAGE.md` (documentation only)

### Files with Python version management:
- `.python-version`
- `release/release.sh` (pyenv references)
- `.github/workflows/*.yml` (setup-python actions)

---

**End of Analysis Document**
