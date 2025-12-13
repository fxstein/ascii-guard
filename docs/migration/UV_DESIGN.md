# UV Migration Design Document

**Date:** 2025-12-13
**Purpose:** Detailed design for migrating ascii-guard from venv/pip to uv

---

## Executive Summary

This document provides a comprehensive design for migrating the ascii-guard project from traditional Python package management (venv + pip + pyenv) to `uv`, a fast, modern Python package manager. The migration eliminates all manual venv management, pip commands, and Python version management while maintaining full compatibility with existing workflows.

---

## 1. Migration Goals

### 1.1 Primary Objectives

1. **Replace venv**: Use `uv venv` for all virtual environment creation
2. **Replace pip**: Use `uv pip` or `uv sync` for all package installation
3. **Simplify Python version management**: Use uv's built-in Python management
4. **Maintain compatibility**: All existing workflows must continue to work
5. **Improve performance**: Leverage uv's 10-100x speed improvements
6. **Update documentation**: All docs reflect uv-based workflows

### 1.2 Non-Goals

- ❌ Changing project structure or dependencies
- ❌ Modifying test suites or coverage requirements
- ❌ Changing release process (only the tools used)
- ❌ Breaking backward compatibility for end users

---

## 2. uv Overview

### 2.1 What is uv?

`uv` is an extremely fast Python package installer and resolver written in Rust, created by Astral (makers of Ruff). It serves as a drop-in replacement for pip, pip-tools, virtualenv, and pyenv (project-level).

### 2.2 Key Features

- **Speed**: 10-100x faster than pip
- **Unified tool**: Replaces multiple tools (pip, venv, pip-tools)
- **Python management**: Can install and manage Python versions
- **Compatible**: Works with existing pyproject.toml, requirements.txt
- **CI/CD ready**: Official GitHub Actions support

### 2.3 Installation

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip/pipx (temporary, until uv is installed)
pipx install uv
```

---

## 3. Architecture Changes

### 3.1 Current Architecture

```
┌─────────────┐
│   pyenv     │ → Python version management
└─────────────┘
       ↓
┌─────────────┐
│ python -m   │ → Create virtual environment
│    venv     │
└─────────────┘
       ↓
┌─────────────┐
│     pip     │ → Install packages
└─────────────┘
```

### 3.2 Target Architecture

```
┌─────────────┐
│     uv      │ → Python version + venv + packages
└─────────────┘
```

**Single tool handles:**
- Python version installation and management
- Virtual environment creation
- Package installation and dependency resolution
- Build and publish workflows (via uv build)

---

## 4. Component-by-Component Migration

### 4.1 Python Version Management

#### Current State
- `.python-version` file (pyenv)
- `pyenv local` commands in scripts
- `actions/setup-python@v6` in CI/CD

#### Target State
- **Keep `.python-version`**: uv respects this file
- **Local development**: Use `uv python pin 3.14.2` to explicitly manage Python version (recommended)
  - Ensures `uv run` always uses the exact interpreter version defined for the project
  - Prevents inconsistent local environments (some developers might accidentally use system Python)
- **CI/CD**: Use `astral-sh/setup-uv@v4` action (installs uv + Python)

#### Migration Steps
1. Install uv locally
2. Verify uv respects `.python-version`
3. Update CI/CD to use `setup-uv` action
4. Remove pyenv references from scripts

---

### 4.2 Virtual Environment Management

#### Current State
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Target State
```bash
uv venv
source .venv/bin/activate  # Still works! uv creates compatible venvs
```

#### Key Points
- ✅ uv creates **compatible** virtual environments (same structure as venv)
- ✅ `source .venv/bin/activate` still works
- ✅ `.venv/bin/python` paths still work
- ✅ Pre-commit hooks continue to work without changes

#### Migration Steps
1. Replace `python -m venv .venv` with `uv venv`
2. Keep activation scripts (they work with uv venvs)
3. Update setup.sh to use `uv venv`
4. Update CI/CD workflows

---

### 4.3 Package Installation

#### Current State
```bash
pip install --upgrade pip
pip install -e .[dev]
```

#### Target State
```bash
# Option 1: uv sync (recommended - uses pyproject.toml)
uv sync --dev

# Option 2: uv pip install (drop-in replacement)
uv pip install -e .[dev]
```

#### Key Differences

**uv sync:**
- Reads `pyproject.toml` directly
- Creates `uv.lock` file (**mandatory** - see section 4.3.1 for lock file strategy)
- Installs project in editable mode automatically
- Handles dev dependencies via `--dev` flag

**uv pip install:**
- Drop-in replacement for pip
- Faster than pip
- Works with existing pip commands

#### Recommendation
Use `uv sync --dev` for development setup (cleaner, faster, uses pyproject.toml directly).

#### 4.3.1 Lock File Strategy (Critical for Reproducibility)

**Requirement**: **Mandate and commit `uv.lock`** to the repository.

**Rationale:**
- Ensures 100% deterministic builds across all environments
- Prevents "it works on my machine" bugs
- Without a lock file, `uv sync` resolves dependencies based on `pyproject.toml` ranges, meaning different developers or CI runs could get different transitive dependency versions

**Implementation:**
1. Generate lock file: `uv sync --dev` (creates `uv.lock`)
2. Commit `uv.lock` to repository (add to `.gitignore` exclusion if needed)
3. CI should use `uv sync --frozen` to fail if lock file is out of sync with `pyproject.toml`
4. Update `.gitignore` to ensure `uv.lock` is tracked

**CI/CD Usage:**
```bash
# Development: Update lock file when dependencies change
uv sync --dev

# CI/CD: Use frozen mode to ensure reproducibility
uv sync --frozen --dev
```

#### Migration Steps
1. Replace `pip install --upgrade pip` → Remove (not needed)
2. Replace `pip install -e .[dev]` → `uv sync --dev`
3. Generate and commit `uv.lock` file
4. Update all scripts and workflows to use `--frozen` in CI
5. Test package installation

---

### 4.4 Build and Publish

#### Current State
```bash
pip install build twine
python -m build
twine check dist/*
twine upload dist/*
```

#### Target State
```bash
# Option 1: Use uv to install build tools, then use standard commands
uv sync --dev  # Installs build, twine
uv run python -m build  # Or: source .venv/bin/activate && python -m build
twine check dist/*

# Option 2: Use uv build (newer, uv-native)
uv build
uv publish  # (when available, or use twine)
```

#### Recommendation
- **For now**: Use `uv sync --dev` to install build/twine, then use standard `python -m build` and `twine`
- **Future**: Migrate to `uv build` when stable

#### Migration Steps
1. Update release script to use `uv sync --dev`
2. Keep `python -m build` and `twine` commands (they work with uv-installed packages)
3. Test build and publish workflow

---

### 4.5 Pre-commit Hooks

#### Current State
```yaml
- repo: local
  hooks:
    - id: pytest-fast
      entry: .venv/bin/python -m pytest
```

#### Target State
```yaml
# No changes needed! uv creates compatible venvs
- repo: local
  hooks:
    - id: pytest-fast
      entry: .venv/bin/python -m pytest  # Still works!
```

#### Key Point
✅ **No changes required** - uv creates standard-compliant virtual environments that work with pre-commit hooks exactly as before.

#### Migration Steps
1. Verify pre-commit hooks work with uv venv
2. No code changes needed

---

### 4.6 CI/CD Workflows

#### Current State (ci.yml)
```yaml
- name: Set up Python
  uses: actions/setup-python@v6
  with:
    python-version: ${{ matrix.python-version }}

- name: Cache pip packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip

- name: Create and activate venv
  run: |
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -e .[dev]
```

#### Target State
```yaml
permissions:
  contents: read  # Least privilege - only grant write where needed

- name: Install uv
  uses: astral-sh/setup-uv@v4
  with:
    version: "latest"  # TODO: Pin to SHA (see section 4.6.1)
    enable-cache: true  # Native caching (replaces manual cache step)
    cache-dependency-glob: "uv.lock"

- name: Set up Python
  uses: astral-sh/setup-uv@v4
  with:
    python-version: ${{ matrix.python-version }}

- name: Install dependencies
  run: |
    uv venv
    uv sync --frozen --dev  # Use --frozen to ensure lock file matches
```

#### Key Changes
1. Add `permissions: contents: read` (least privilege - see section 4.6.1)
2. Replace `setup-python@v6` with `setup-uv@v4`
3. Use native caching via `enable-cache: true` (replaces manual cache step)
4. Replace venv creation with `uv venv`
5. Replace pip install with `uv sync --frozen --dev` (use `--frozen` in CI)
6. Remove `pip upgrade` step (not needed)

#### 4.6.1 Security Enhancements

**Action Pinning (Critical):**
- **Gap**: Using mutable tags (e.g., `uses: actions/checkout@v4`) is a security risk
- **Risk**: Tags can be overwritten or hijacked, leading to supply chain attacks
- **Recommendation**: Pin all Actions to full commit SHAs for immutable security
  ```yaml
  uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
  ```
- **Mitigation**: Configure Dependabot to manage these SHA updates automatically

**Workflow Permissions (Least Privilege):**
- **Gap**: Workflows currently run with default permissions (often too permissive)
- **Risk**: Compromised steps could modify the repository
- **Recommendation**: Define strict top-level permissions in every workflow file
  ```yaml
  permissions:
    contents: read  # minimal default
  ```
- **Grant Write Access Explicitly**: Only add `contents: write` or `id-token: write` to specific jobs that require it (e.g., releases)

#### Migration Steps
1. Update `.github/workflows/ci.yml`
2. Update `.github/workflows/release.yml`
3. Update `.github/workflows/pr-checks.yml`
4. Update `.github/workflows/scheduled.yml`
5. Test all workflows

---

### 4.7 Setup Script (setup.sh)

#### Current State
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip --quiet
pip install -e ".[dev]" --quiet
.venv/bin/pre-commit install
```

#### Target State
```bash
# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

uv venv
source .venv/bin/activate
uv sync --dev
.venv/bin/pre-commit install
```

#### Migration Steps
1. Add uv installation check/install
2. Replace venv creation
3. Replace pip installs
4. Keep pre-commit installation (works as-is)
5. Test setup script

---

### 4.8 Release Script (release/release.sh)

#### Current State
```bash
# Validates .venv exists
[[ ! -d .venv ]]

# Checks Python version
.venv/bin/python --version

# Validates build module
.venv/bin/python -c "import build"

# Builds package
.venv/bin/python -m build
```

#### Target State
```bash
# Validates .venv exists (still works)
[[ ! -d .venv ]]

# Checks Python version (still works)
.venv/bin/python --version

# Validates build module (still works)
.venv/bin/python -c "import build"

# Ensures uv is available
if ! command -v uv &> /dev/null; then
    echo "ERROR: uv not found"
    exit 1
fi

# Syncs dependencies
uv sync --dev

# Builds package (same command)
.venv/bin/python -m build
```

#### Key Points
- ✅ Most validation code works unchanged (uv venvs are compatible)
- ✅ Add uv availability check
- ✅ Use `uv sync --dev` instead of pip install
- ✅ Keep build commands (they work with uv-installed packages)

#### Migration Steps
1. Add uv check
2. Replace pip install with uv sync
3. Keep all validation logic
4. Test release process

---

### 4.9 Documentation Updates

#### Files to Update

**README.md:**
- Change: `pip install ascii-guard` → Keep (end users still use pip)
- Add: Developer setup uses uv

**docs/USAGE.md:**
- Change: `pip install ascii-guard` → Keep (end users)
- Change: `pip install -e .` → `uv sync --dev` (developers)
- Change: `pipx install ascii-guard` → Keep (end users)

**docs/API_REFERENCE.md:**
- Change: `pip install ascii-guard` → Keep (end users)

**docs/FAQ.md:**
- Change: `pip install --upgrade ascii-guard` → Keep (end users)

**CONTRIBUTING.md:**
- Update: Development setup instructions to use uv
- Update: `./setup.sh` now uses uv

#### Key Principle
- **End users**: Still use `pip install ascii-guard` (no change)
- **Developers**: Use `uv sync --dev` for development setup

#### Migration Steps
1. Update all developer-facing documentation
2. Keep end-user installation instructions (pip)
3. Add uv installation instructions
4. Update setup examples

---

## 5. CI/CD Compatibility Analysis

### 5.1 uv in GitHub Actions

#### Official Action
- **Action**: `astral-sh/setup-uv@v4`
- **Features**:
  - Installs uv automatically
  - Can install Python versions
  - Caches uv dependencies
  - Works on Linux, macOS, Windows

#### Example Workflow
```yaml
permissions:
  contents: read  # Least privilege default

- name: Install uv
  uses: astral-sh/setup-uv@v4
  with:
    version: "latest"  # TODO: Pin to SHA
    enable-cache: true
    cache-dependency-glob: "uv.lock"

- name: Set up Python
  uses: astral-sh/setup-uv@v4
  with:
    python-version: "3.12"

- name: Install dependencies
  run: uv sync --frozen --dev  # Use --frozen in CI

- name: Run tests
  run: uv run pytest
```

### 5.2 Matrix Testing

✅ **Fully supported**: uv works with matrix strategies for multiple Python versions.

### 5.3 Caching

- **Native caching**: Use `enable-cache: true` in `setup-uv` action (recommended)
  - Automatically handles save/restore logic correctly
  - Uses `cache-dependency-glob: "uv.lock"` for optimal cache keys
  - Less verbose and less prone to configuration errors than manual cache setup
- **Manual caching** (alternative): `~/.cache/uv` (replaces `~/.cache/pip`)
- **venv cache**: `.venv` (still works, but uv is faster so less critical)

### 5.4 Multi-platform Support

✅ **Fully supported**: uv works on Linux, macOS, Windows (same as current setup).

---

## 6. Zero Dependency Verification

### 6.1 Current Verification

```bash
pip list --format=freeze | grep -v "^ascii-guard" | grep -v "^pip==" | grep -v "^setuptools==" | grep -v "^wheel=="
```

### 6.2 uv Verification

```bash
# Option 1: Use uv pip list (same output format)
uv pip list --format=freeze | grep -v "^ascii-guard" | ...

# Option 2: Use uv tree (shows dependency tree)
uv tree

# Option 3: Install without dev deps and check
uv sync  # No --dev flag
uv pip list
```

#### Recommendation
Use `uv pip list` (same format as pip, existing scripts work with minimal changes).

---

## 7. Migration Strategy

### 7.1 Phased Approach

**Phase 1: Preparation**
1. Create analysis document (✅ Done)
2. Create design document (✅ Done)
3. Create task list
4. Test uv locally

**Phase 2: Local Development**
1. Install uv
2. Run `uv python pin 3.14.2` to explicitly pin Python version
3. Generate `uv.lock` file with `uv sync --dev`
4. Commit `uv.lock` to repository
5. Update setup.sh
6. Test local development workflow
7. Verify pre-commit hooks

**Phase 3: CI/CD Migration**
1. Generate and commit `uv.lock` file
2. Update ci.yml (test workflow)
   - Add permissions section
   - Use native caching
   - Pin actions to SHAs (or configure Dependabot)
   - Use `uv sync --frozen --dev`
3. Update pr-checks.yml
4. Update scheduled.yml
5. Update release.yml (last, most critical)

**Phase 4: Scripts and Documentation**
1. Update release.sh
2. Update all documentation
3. Update Cursor rules

**Phase 5: Testing and Release**
1. Full CI/CD test run
2. Release dry-run
3. Release new version with uv

### 7.2 Rollback Plan

If issues arise:
1. Revert workflow files (git)
2. Revert scripts (git)
3. Keep using venv/pip temporarily
4. Fix issues and retry

---

## 8. Testing Checklist

### 8.1 Local Testing

- [ ] Install uv
- [ ] Run `uv python pin 3.14.2` to pin Python version
- [ ] Run `uv venv`
- [ ] Run `uv sync --dev` (generates `uv.lock`)
- [ ] Verify `uv.lock` file is created
- [ ] Commit `uv.lock` to repository
- [ ] Activate venv and verify packages
- [ ] Run `pytest`
- [ ] Run `ruff check`
- [ ] Run `mypy src/`
- [ ] Run `pre-commit run --all-files`
- [ ] Run `python -m build`
- [ ] Verify zero dependencies
- [ ] Test `uv sync --frozen --dev` (should work with committed lock file)

### 8.2 CI/CD Testing

- [ ] Test ci.yml workflow (all Python versions)
- [ ] Test pr-checks.yml workflow
- [ ] Test scheduled.yml workflow
- [ ] Test release.yml workflow (dry-run)
- [ ] Verify native caching works (`enable-cache: true`)
- [ ] Verify `uv sync --frozen` fails if lock file is out of sync
- [ ] Verify permissions are set correctly (least privilege)
- [ ] Verify coverage reporting
- [ ] Verify zero dependency checks

### 8.3 Release Testing

- [ ] Run `./release/release.sh --prepare` (dry-run)
- [ ] Verify package builds correctly
- [ ] Verify package can be installed via pip
- [ ] Verify package works after pip install
- [ ] Full end-to-end release test (if possible)

---

## 9. Performance Improvements

### 9.1 Expected Improvements

- **Package installation**: 10-100x faster
- **Dependency resolution**: Much faster
- **CI/CD runtime**: Significantly reduced
- **Developer experience**: Faster feedback loops

### 9.2 Metrics to Track

- CI/CD workflow duration (before/after)
- Local setup time (before/after)
- Package installation time (before/after)

---

## 10. Risk Mitigation

### 10.1 Identified Risks

1. **CI/CD breakage**: Test thoroughly before merging
2. **Release process failure**: Test release workflow extensively
3. **Developer confusion**: Update all documentation clearly
4. **Compatibility issues**: uv venvs are compatible, but test thoroughly

### 10.2 Mitigation Strategies

1. **Incremental migration**: Update one workflow at a time
2. **Extensive testing**: Test all workflows before final migration
3. **Clear documentation**: Update all docs with uv examples
4. **Rollback plan**: Keep ability to revert quickly

---

## 11. Success Criteria

### 11.1 Migration Complete When

- ✅ All CI/CD workflows use uv
- ✅ All scripts use uv
- ✅ All documentation updated
- ✅ Local development works with uv
- ✅ Release process works with uv
- ✅ Zero dependency verification works
- ✅ All tests pass
- ✅ Performance improved

### 11.2 Validation

- All GitHub Actions workflows pass
- Release process completes successfully
- Developers can set up environment with uv
- End users unaffected (still use pip)

---

## 12. Timeline Estimate

- **Analysis & Design**: 1 day ✅
- **Local Testing**: 1 day
- **CI/CD Migration**: 2-3 days
- **Scripts & Docs**: 1-2 days
- **Testing & Release**: 1-2 days

**Total**: ~1 week for complete migration

---

## 13. Security and Reliability Enhancements

### 13.1 Lock File Strategy

**Mandatory**: Commit `uv.lock` to repository for 100% reproducible builds.

- **Development**: `uv sync --dev` (updates lock file when dependencies change)
- **CI/CD**: `uv sync --frozen --dev` (fails if lock file is out of sync)
- **Benefits**: Prevents "it works on my machine" bugs, ensures identical dependency versions across all environments

### 13.2 Security Best Practices

**Action Pinning:**
- Pin all GitHub Actions to commit SHAs instead of tags
- Configure Dependabot to manage SHA updates automatically
- Example: `uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11`

**Workflow Permissions:**
- Set `permissions: contents: read` as default (least privilege)
- Only grant `contents: write` or `id-token: write` to specific jobs that require it
- Prevents compromised steps from modifying the repository

### 13.3 Efficiency Improvements

**Native Caching:**
- Use `enable-cache: true` in `setup-uv` action
- Automatically handles cache save/restore with optimal keys
- Less verbose and less error-prone than manual cache configuration

**Python Version Pinning:**
- Use `uv python pin <version>` to explicitly manage project Python version
- Ensures consistent environments across all developers
- Prevents accidental use of system Python

---

## 14. References

- [uv Documentation](https://docs.astral.sh/uv/)
- [uv GitHub](https://github.com/astral-sh/uv)
- [uv GitHub Actions](https://github.com/astral-sh/setup-uv)
- [uv vs pip benchmark](https://github.com/astral-sh/uv#benchmarks)
- [UV_DESIGN_GAP_ANALYSIS.md](./UV_DESIGN_GAP_ANALYSIS.md) - Security and reliability gap analysis

---

**End of Design Document**
