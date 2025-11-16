# CI/CD Documentation

This document describes the continuous integration and deployment workflows for `ascii-guard`.

## Overview

`ascii-guard` uses GitHub Actions for CI/CD automation with a focus on:
- **Quality**: Comprehensive testing across multiple Python versions
- **Security**: Zero-dependency verification and security scanning
- **Performance**: Fast builds with intelligent caching
- **Reliability**: Scheduled tests and cross-platform validation

## Workflows

### 1. CI Workflow (`ci.yml`)

**Triggers**: Push to `main`, Pull Requests, Manual dispatch

**Jobs**:

#### Lint & Test Matrix
- **Python versions**: 3.10, 3.11, 3.12, 3.13
- **OS**: Ubuntu (Linux)
- **Runs**: Pre-commit hooks (ruff, mypy), pytest with coverage
- **Caches**: pip packages, pre-commit hooks

#### Build Package
- Builds wheel and source distribution
- Validates package with `twine check`
- Uploads artifacts for review

#### Verify Zero Dependencies
- **Critical check** - Installs package without dev dependencies
- Verifies ONLY ascii-guard is installed (no runtime deps)
- Tests package works standalone

#### Test Import Without Dependencies
- Tests modules can be imported with just Python stdlib
- Verifies zero-dependency promise

**Coverage**:
- Uploads to Codecov (Python 3.10 only)
- Requires 80% minimum coverage

### 2. Release Workflow (`release.yml`)

**Triggers**: Tags matching `v*.*.*`, Manual dispatch

**Jobs**:

#### Validate Release
- Runs full test suite
- Runs pre-commit checks
- Verifies zero dependencies

#### Build and Publish to PyPI
- Builds package
- Publishes to PyPI using trusted publishing
- Uses OIDC token (no manual API key needed)

#### Create GitHub Release
- Creates GitHub release with:
  - Automatically generated release notes
  - Wheel and source distributions attached
  - Version extracted from git tag
  - Markdown formatted description

**Requirements**:
- Repository environment named `pypi`
- Trusted publishing configured in PyPI
- `contents: write` permission for GitHub releases

### 3. PR Checks Workflow (`pr-checks.yml`)

**Triggers**: Pull request events (opened, synchronize, reopened)

**Jobs**:

#### PR Metadata Check
- Validates PR title follows conventions
- Ensures PR description is provided

#### Dependency Check
- **Critical** - Verifies `dependencies = []` in `pyproject.toml`
- Checks for forbidden imports (click, typer, colorama, etc.)
- Ensures stdlib-only constraint

#### Code Quality
- Runs ruff format check
- Runs ruff linter
- Runs mypy type checking
- Checks for TODO/FIXME comments

#### Security Scan
- Runs Bandit security scanner
- Checks for potential secrets in code

#### Test Coverage Report
- Runs tests with coverage
- Requires minimum 80% coverage
- Generates coverage report

#### Documentation Check
- Validates README exists
- Checks for broken links
- Validates markdown files

### 4. Scheduled Tests Workflow (`scheduled.yml`)

**Triggers**: Weekly (Monday 00:00 UTC), Manual dispatch

**Jobs**:

#### Test All Python Versions & OS
- **Matrix**:
  - Python: 3.10, 3.11, 3.12, 3.13
  - OS: Ubuntu, macOS, Windows
- Full cross-platform validation

#### Test Minimum Python Version
- Tests exact minimum version (3.10.0)
- Ensures compatibility with oldest supported version

#### Test Development Python
- Tests Python 3.14-dev (continues on error)
- Early detection of future compatibility issues

#### Dependency Audit
- Runs `safety check` on dev dependencies
- Lists outdated dependencies

#### Performance Benchmark
- Creates large test file (100 boxes)
- Benchmarks lint and fix operations
- Tracks performance over time

#### Notify on Failure
- Creates GitHub issue if scheduled tests fail
- Labels: `ci`, `scheduled-test-failure`

## Caching Strategy

### Pip Cache
```yaml
path: ~/.cache/pip
key: ${{ runner.os }}-pip-${{ matrix.python-version }}-${{ hashFiles('pyproject.toml') }}
```
- Caches installed Python packages
- Speeds up dependency installation
- Invalidates when `pyproject.toml` changes

### Pre-commit Cache
```yaml
path: ~/.cache/pre-commit
key: ${{ runner.os }}-pre-commit-${{ matrix.python-version }}-${{ hashFiles('.pre-commit-config.yaml') }}
```
- Caches pre-commit hook environments
- Speeds up pre-commit runs
- Invalidates when config changes

## Dependabot Configuration

Automated dependency updates via `.github/dependabot.yml`:

### GitHub Actions Updates
- Weekly updates on Monday
- Automatically updates action versions
- Labels: `dependencies`, `github-actions`

### Python Dev Dependencies
- Weekly updates on Monday
- **Runtime dependencies**: NONE (by design)
- Updates dev dependencies only (pytest, ruff, mypy, etc.)
- Ignores major version updates (requires manual review)

## Issue & PR Templates

### Bug Report Template
Structured form with:
- Bug description
- Reproduction steps
- Expected vs actual behavior
- Sample input file
- Version info (ascii-guard, Python, OS)
- Error output

### Feature Request Template
Structured form with:
- Problem statement
- Proposed solution
- Alternatives considered
- Use case examples
- Priority level

### Pull Request Template
Checklist covering:
- Type of change
- Changes made
- Testing performed
- Code quality checks
- Zero-dependency verification

## CI/CD Best Practices

### 1. Fail Fast
- `fail-fast: false` in matrix jobs
- All configurations tested even if one fails

### 2. Security
- No secrets in code
- Trusted publishing for PyPI (OIDC)
- Security scanning with Bandit

### 3. Performance
- Aggressive caching (pip, pre-commit)
- Parallel matrix jobs
- Fast test execution (<1 second)

### 4. Reliability
- Scheduled weekly tests
- Cross-platform validation
- Multiple Python versions

### 5. Zero Dependencies
- **Critical constraint** enforced at multiple levels:
  - PR checks verify `dependencies = []`
  - CI verifies no forbidden imports
  - Dedicated job tests standalone installation
  - Import tests verify stdlib-only

## Local Development

### Run CI Checks Locally

```bash
# Run all pre-commit hooks (same as CI)
pre-commit run --all-files

# Run tests with coverage (same as CI)
pytest --cov=ascii_guard --cov-report=term-missing

# Build package (same as CI)
python -m build
twine check dist/*

# Verify zero dependencies
pip install -e .
python -c "import ascii_guard; print(ascii_guard.__version__)"
```

### Test Matrix Locally

```bash
# Test multiple Python versions with tox (if installed)
tox

# Or use pyenv for version switching
pyenv install 3.10.0 3.11.0 3.12.0 3.13.0
pyenv local 3.10.0
pytest
```

## Troubleshooting

### CI Failures

**Pre-commit hooks fail**:
- Run `pre-commit run --all-files` locally
- Fix linting/formatting issues
- Commit and push

**Tests fail**:
- Run `pytest -v` locally for details
- Check specific Python version if matrix fails
- Review coverage report: `pytest --cov=ascii_guard --cov-report=html`

**Zero-dependency check fails**:
- Verify `pyproject.toml` has `dependencies = []`
- Check for forbidden imports in source code
- Run `pytest tests/test_stdlib_only.py -v` locally

**Build fails**:
- Run `python -m build` locally
- Check `pyproject.toml` configuration
- Verify all required files are included

### Release Issues

**PyPI publish fails**:
- Check PyPI trusted publishing is configured
- Verify repository environment `pypi` exists
- Ensure version number is updated

**GitHub release fails**:
- Verify tag format: `v*.*.*` (e.g., `v0.1.0`)
- Check `contents: write` permission
- Review tag creation command

## Maintenance

### Regular Tasks

**Weekly** (automated):
- Scheduled tests run
- Dependabot checks for updates

**Before Release**:
1. Update version in `pyproject.toml` and `src/ascii_guard/__init__.py`
2. Update `CHANGELOG.md`
3. Run full test suite locally
4. Create git tag: `git tag v0.1.0`
5. Push tag: `git push origin v0.1.0`

**After Release**:
1. Verify PyPI package: https://pypi.org/project/ascii-guard/
2. Verify GitHub release created
3. Test installation: `pip install ascii-guard`
4. Update documentation if needed

## Metrics & Monitoring

### CI Health
- Check GitHub Actions tab for workflow status
- Review scheduled test results weekly
- Monitor Codecov for coverage trends

### Package Health
- PyPI download statistics
- GitHub star/fork counts
- Issue/PR activity

### Performance
- Track test execution time
- Monitor CI job duration
- Review benchmark results from scheduled tests

## Future Improvements

Potential enhancements:
- [ ] Add CodeQL security scanning
- [ ] Integrate with SonarCloud for code quality
- [ ] Add automatic changelog generation
- [ ] Implement semantic release automation
- [ ] Add performance regression detection
- [ ] Create badge generation automation

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPA Packaging Guide](https://packaging.python.org/)
- [Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Codecov Documentation](https://docs.codecov.com/)
