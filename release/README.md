# Release Automation

Release automation system for ascii-guard. This directory contains the complete release workflow, documentation, and history.

## 🚀 Quick Start (For Maintainers)

### Performing a Release

```bash
# Step 1: AI generates release summary first
# (See RELEASE.md for details)

# Step 2: Prepare release (updates version, creates changelog)
./release/release.sh --prepare

# Step 3: Verify and commit changes
git add .
git commit -m "chore: prepare release vX.Y.Z"

# Step 4: Publish release (creates tag, pushes to GitHub, builds package)
./release/release.sh --publish

# Step 5: The package is auto-published to PyPI via GitHub Actions
```

**⚠️ Important**: Always generate AI release summary BEFORE running `--prepare`

---

## 📁 Files in This Directory

### 🔧 Automation Script

#### [release.sh](release.sh)
The main release automation script.
- **Usage**: `./release.sh [--prepare|--publish|--help]`
- **Prepare mode**: Updates versions, generates changelog
- **Publish mode**: Creates git tag, pushes to GitHub, triggers PyPI publish
- **Features**: Environment validation, safety checks, rollback on errors
- **Platform**: bash (Linux, macOS, Windows WSL/Git Bash)

---

### 📖 Documentation

#### [RELEASE.md](RELEASE.md)
**Complete release process documentation.**
- Quick start guide
- Prerequisites and setup
- Two-file architecture (RELEASE_SUMMARY.md vs RELEASE_LOG.log)
- Complete workflow steps
- Flow charts
- Git tracking strategy
- Version numbering (semantic versioning)
- PyPI publishing with Trusted Publishing
- AI integration requirements
- Troubleshooting guide

#### [VERSION_FILES.md](VERSION_FILES.md)
**Reference for all version numbers in the project.**
- Lists all files containing version numbers
- Exact locations and line numbers
- Format for each version reference
- Purpose of each version file

#### [TESTING.md](TESTING.md)
**Release automation testing guide.**
- How to test release script
- Dry-run procedures
- Test scenarios
- Validation steps

---

### 📝 Release History & Artifacts

#### [RELEASE_SUMMARY.md](RELEASE_SUMMARY.md)
**Git-tracked release summary (source of truth).**
- Human-readable changelog
- Lists all releases with dates
- Feature highlights per release
- Breaking changes and migration guides
- Bug fixes and improvements
- Tracked in git for history

#### [RELEASE_LOG.log](RELEASE_LOG.log)
**Machine-readable release log (git-ignored).**
- Detailed release metadata
- Timestamps and version numbers
- Command execution history
- Environment information
- NOT tracked in git (generated during release)

---

## 🔄 Release Workflow

### Two-File Architecture

The release system uses two complementary files:

1. **RELEASE_SUMMARY.md** (Git-tracked)
   - Human-readable changelog
   - Tracked in version control
   - Part of repository history
   - Used by developers and users

2. **RELEASE_LOG.log** (Git-ignored)
   - Machine-readable metadata
   - Local execution history
   - Not tracked in git
   - Used for debugging and auditing

### Version Management

**Source of Truth**: GitHub releases (via `gh` CLI)

Version numbers follow [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 1.4.0)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Files updated during release:
- `pyproject.toml` - Package version
- `src/ascii_guard/__init__.py` - Runtime version
- `RELEASE_SUMMARY.md` - Changelog entry

---

## 🛡️ Safety Features

The release script includes multiple safety checks:

1. ✅ **Environment validation** - Checks Python version, venv, tools
2. ✅ **Clean working directory** - No uncommitted changes
3. ✅ **Version validation** - Ensures proper semantic versioning
4. ✅ **AI summary check** - Enforces Cursor rules (summary must be fresh)
5. ✅ **Dry-run support** - Test before committing
6. ✅ **Rollback on errors** - Automatic cleanup on failure

---

## 📋 Prerequisites

Before performing a release, ensure:

- ✅ Python 3.10+ installed
- ✅ Virtual environment set up (`.venv/`)
- ✅ GitHub CLI (`gh`) installed and authenticated
- ✅ Clean working directory (no uncommitted changes)
- ✅ All tests passing
- ✅ On `main` branch
- ✅ Latest changes pulled from remote

---

## 🚨 Troubleshooting

### "AI summary not found or too old"

**Error**: Release script rejects because AI summary is missing or older than 30 seconds.

**Solution**: Generate AI release summary first:
1. Ask AI to generate `release/AI_RELEASE_SUMMARY.md`
2. Wait for it to complete
3. Immediately run `./release/release.sh --prepare` (within 30 seconds)

### "Virtual environment not found"

**Error**: `.venv/` directory missing or corrupted.

**Solution**: Run `./setup.sh` to recreate the environment.

### "GitHub CLI not authenticated"

**Error**: `gh` commands fail with authentication error.

**Solution**: Run `gh auth login` and follow the prompts.

---

## 🔗 Related Documentation

- [docs/RELEASE_DESIGN.md](../docs/RELEASE_DESIGN.md) - Architectural design documentation
- [docs/CI_CD.md](../docs/CI_CD.md) - GitHub Actions workflows
- [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md) - General development guide

---

## 📚 Additional Resources

- [Semantic Versioning](https://semver.org/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [GitHub CLI](https://cli.github.com/)

---

**For maintainers only.** Regular contributors should see [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md) for development workflow.
