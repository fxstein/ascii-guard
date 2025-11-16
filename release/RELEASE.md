# ascii-guard Release Process Documentation

**Status**: Planning
**Audience**: Release Managers, Contributors
**Project**: ascii-guard Python Package

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Two-File Architecture](#two-file-architecture)
4. [Complete Release Workflow](#complete-release-workflow)
5. [Flow Chart](#flow-chart)
6. [Git Tracking Strategy](#git-tracking-strategy)
7. [Version Numbering](#version-numbering)
8. [PyPI Publishing](#pypi-publishing)
9. [AI Integration](#ai-integration)
10. [Troubleshooting](#troubleshooting)
11. [References](#references)

---

## Quick Start

**Human-readable summary:**

1. **Ask AI**: "Release ascii-guard"
2. **AI writes summary**: Creates `release/AI_RELEASE_SUMMARY.md`
3. **AI runs prepare**: Generates complete `release/RELEASE_NOTES.md`
4. **You review/edit**: Edit `release/RELEASE_NOTES.md` if needed
   - Optional: "change version to 1.0.0" (if you want to override)
5. **AI executes**: Creates GitHub release and publishes to PyPI

**That's it.** The entire process is AI-driven with human review and optional version control.

---

## Prerequisites

### Required Tools

```bash
# Install GitHub CLI
brew install gh

# Verify installation
gh --version

# Authenticate
gh auth login

# Install Python build tools
pip install build twine

# Verify PyPI credentials
# Create ~/.pypirc with token or use keyring
```

### Pre-Release Checklist

- [ ] All tests pass: `pytest`
- [ ] Linter passes: `ruff check .`
- [ ] Type checking passes: `mypy src/`
- [ ] All changes committed and pushed
- [ ] No uncommitted changes in working directory
- [ ] GitHub CLI authenticated: `gh auth status`
- [ ] PyPI credentials configured: `~/.pypirc` or keyring
- [ ] README.md and docs are current

---

## Two-File Architecture

The release process uses **TWO separate files** to prevent confusion and duplication:

### File 1: `release/AI_RELEASE_SUMMARY.md`

**Purpose**: AI-written input summary

- **Created by**: AI in Step 1
- **Contains**: 2-3 paragraph human-readable summary
- **Format**: Plain text, no commit lists
- **Audience**: End users reading the release
- **Lifecycle**: Created → Read by script → Committed → Deleted

**Example content:**
```markdown
This release adds comprehensive support for detecting and fixing misaligned
ASCII art boxes in documentation. The linter now handles nested boxes,
T-junctions, and cross intersections with improved accuracy.

Key improvements include automatic border alignment correction, better
handling of Unicode box-drawing characters, and a new --dry-run mode
for previewing fixes before applying them.

Users can now lint and fix ASCII art in markdown files with a simple
command-line interface, ensuring consistent visual formatting.
```

### File 2: `release/RELEASE_NOTES.md`

**Purpose**: Complete release notes (AI summary + commits)

- **Created by**: Script in Step 2 (prepare)
- **Contains**: AI summary + categorized commit list
- **Format**: Markdown with sections (Breaking/Added/Changed/Fixed)
- **Audience**: Developers and PyPI consumers
- **Lifecycle**: Generated → **YOU EDIT THIS** → Committed → Deleted

**Example content:**
```markdown
## Release 0.1.0

[AI summary from above]

---

### Added
- feat: Implement ASCII box detection algorithm ([abc123f](link))
- feat: Add CLI interface with lint and fix commands ([def456a](link))

### Fixed
- fix: Correct corner character validation ([ghi789b](link))

*Total commits: 3*
```

### Why Two Files?

**Problem we solved:**
- Previously used one file for both input and output
- Script would overwrite its own output, causing duplication
- Unclear which file to edit during review

**Solution:**
- **AI_RELEASE_SUMMARY.md** = AI writes here (INPUT)
- **RELEASE_NOTES.md** = Script generates here, YOU EDIT HERE (OUTPUT)
- Clear separation prevents confusion and duplication

---

## Complete Release Workflow

### Step 1: AI Writes Summary

**Command to AI**: "Release ascii-guard"

**AI Action**: Creates `release/AI_RELEASE_SUMMARY.md`

```markdown
# AI writes 2-3 paragraphs explaining:
- What changed in this release
- Why it matters to users
- Key benefits and improvements
```

**File location**: `release/AI_RELEASE_SUMMARY.md`

---

### Step 2: Prepare Release

**Command**: `./release/release.sh --prepare`

**Script Actions**:

1. **Analyze commits** since last release
   - Parse commit messages
   - Categorize: Breaking/Added/Changed/Fixed/Other
   - Generate GitHub links for each commit

2. **Determine version bump** (automatic)
   - MAJOR: `feat!:` or `BREAKING` in commits
   - MINOR: `feat:` commits
   - PATCH: `fix:`, `chore:`, `docs:` commits

3. **Read AI summary** from `AI_RELEASE_SUMMARY.md`

4. **Generate complete notes** to `RELEASE_NOTES.md`
   - Header: `## Release X.Y.Z`
   - AI summary (human-readable)
   - Separator: `---`
   - Categorized commit list
   - Footer: Total commit count

5. **Display preview** to terminal

6. **Save prepare state** to `release/.prepare_state`
   - Stores: NEW_VERSION, BUMP_TYPE, CURRENT_VERSION, LAST_TAG
   - Used by execute step

7. **Output message**:
   ```
   ✅ Release preview prepared successfully!
   📋 Version: 0.1.0 → 0.2.0
   📋 Type: minor release

   📝 REVIEW AND EDIT: release/RELEASE_NOTES.md
      (This is the file that will be used for the release)

   When ready, execute this release:
     ./release/release.sh --execute
   ```

**Files created**:
- `release/RELEASE_NOTES.md` (complete notes - **EDIT THIS**)
- `release/.prepare_state` (metadata)

---

### Step 3: Review and Edit (HUMAN)

**THIS IS YOUR STEP**

**File to edit**: `release/RELEASE_NOTES.md`

**What to review**:
- AI summary accuracy and clarity
- Commit categorization (is "fix" really a "feat"?)
- Any commits that should be excluded
- Grammar, spelling, clarity
- **Version number** (can be overridden if needed)

**Example edits**:
```bash
vim release/RELEASE_NOTES.md

# Common edits:
# - Rewrite AI summary for clarity
# - Move commits between categories
# - Remove internal/unimportant commits
# - Add additional context or warnings
```

**DO NOT EDIT**:
- `release/AI_RELEASE_SUMMARY.md` (input already consumed)
- `release/release.sh` (never change release logic)

---

### Step 3b: Override Version (OPTIONAL)

**When to use**: When you want a specific version number instead of the auto-detected one.

**Use case examples**:
- "This should be our 1.0.0 release" (major milestone)
- "Let's call this 2.0.0" (major refactor)
- "Make this 0.10.0" (align with marketing)

**Command**: `./release/release.sh --set-version X.Y.Z`

**Example**:
```bash
# After prepare shows version 0.2.0, you decide it should be 1.0.0
./release/release.sh --set-version 1.0.0

# Output:
✅ Version override successful!
📋 Current version: 0.1.0
📋 Auto-detected: 0.2.0 (minor)
📋 New version: 1.0.0 (major)
📝 Updated: release/RELEASE_NOTES.md
```

**What it validates**:
1. **Format**: Must be `X.Y.Z` (semantic versioning)
   - ✅ Valid: `1.0.0`, `2.5.3`, `10.0.0`
   - ❌ Invalid: `1.0`, `v1.0.0`, `1.0.0-beta`

2. **Progression**: New version must be > current version
   - Current: `0.1.0`, New: `1.0.0` → ✅ Valid (1 > 0)
   - Current: `0.1.0`, New: `0.1.0` → ❌ Invalid (equal)
   - Current: `0.1.0`, New: `0.0.9` → ❌ Invalid (less)

**Natural language with AI**:
- "change version to 1.0.0"
- "make this version 2.0.0"
- "set version to 1.5.0"
- "this should be 1.0.0"

→ AI will run: `./release/release.sh --set-version X.Y.Z`

---

### Step 4: Execute Release

**Command**: `./release/release.sh --execute`

**Script Actions**:

1. **Load prepare state** from `release/.prepare_state`
   - Verify prepare was run
   - Load version numbers and metadata

2. **Copy RELEASE_NOTES.md** → `RELEASE_SUMMARY.md`
   - Historical record of this release
   - Gets committed to repo

3. **Update versions**:
   - `pyproject.toml`: version field
   - `src/ascii_guard/__init__.py`: __version__ variable

4. **Build Python package**:
   ```bash
   python -m build
   # Creates dist/ascii_guard-X.Y.Z-py3-none-any.whl
   # Creates dist/ascii_guard-X.Y.Z.tar.gz
   ```

5. **Commit version bump**:
   ```bash
   git add pyproject.toml src/ascii_guard/__init__.py
   git add release/RELEASE_SUMMARY.md
   git add release/AI_RELEASE_SUMMARY.md  # Historical record
   git add release/RELEASE_NOTES.md       # Historical record
   git commit -m "release: Version X.Y.Z"
   ```
   - Gets tagged with `vX.Y.Z`
   - Used for GitHub release

6. **Create git tag**:
   ```bash
   git tag -a "vX.Y.Z" -m "Release version X.Y.Z"
   ```

7. **Push to GitHub**:
   ```bash
   git push origin main
   git push origin vX.Y.Z
   ```

8. **Create GitHub release**:
   ```bash
   gh release create "vX.Y.Z" \
     --title "X.Y.Z" \
     --notes-file "release/RELEASE_NOTES.md" \
     dist/ascii_guard-X.Y.Z-py3-none-any.whl \
     dist/ascii_guard-X.Y.Z.tar.gz
   ```

9. **Publish to PyPI**:
   ```bash
   python -m twine upload dist/ascii_guard-X.Y.Z*
   ```

10. **Cleanup working files**:
    ```bash
    rm -f release/AI_RELEASE_SUMMARY.md
    rm -f release/RELEASE_NOTES.md
    rm -f release/.prepare_state
    rm -rf dist/ build/
    ```

11. **Log success** to `release/RELEASE_LOG.log`

12. **Commit release log** (separate commit):
    ```bash
    git add release/RELEASE_LOG.log
    git commit -m "chore: Update release log for vX.Y.Z"
    git push origin main
    ```

**Result**: Release is live on GitHub and PyPI!

---

## Flow Chart

```
┌─────────────────────────────────────────────────────────────────┐
│                    RELEASE WORKFLOW                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Step 1: AI Writes Summary                                        │
│ ─────────────────────────────                                    │
│ AI creates release/AI_RELEASE_SUMMARY.md                         │
│ - 2-3 paragraph human-readable summary                           │
│ - Focus on user benefits                                         │
│ - Plain text, no commits                                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Prepare Release                                          │
│ ───────────────────────                                          │
│ Command: ./release/release.sh --prepare                          │
│                                                                   │
│ Actions:                                                          │
│ 1. Analyze commits since last release                            │
│ 2. Determine version bump (MAJOR/MINOR/PATCH)                    │
│ 3. Read AI_RELEASE_SUMMARY.md                                    │
│ 4. Generate complete RELEASE_NOTES.md                            │
│ 5. Display preview                                               │
│ 6. Save prepare state                                            │
│                                                                   │
│ Files Created:                                                    │
│ - release/RELEASE_NOTES.md ← EDIT THIS                           │
│ - release/.prepare_state                                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Review & Edit (HUMAN)                                    │
│ ─────────────────────────────────                                │
│ Edit: release/RELEASE_NOTES.md                                   │
│                                                                   │
│ Optional: ./release/release.sh --set-version X.Y.Z              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Execute Release                                          │
│ ───────────────────────                                          │
│ Command: ./release/release.sh --execute                          │
│                                                                   │
│ Actions:                                                          │
│ 1. Load prepare state                                            │
│ 2. Update versions (pyproject.toml, __init__.py)                │
│ 3. Build Python package (wheel + sdist)                          │
│ 4. Commit version bump + release files                           │
│ 5. Create git tag (vX.Y.Z)                                       │
│ 6. Push to GitHub (main + tag)                                   │
│ 7. Create GitHub release (with wheel/sdist)                      │
│ 8. Publish to PyPI (twine upload)                                │
│ 9. Cleanup working files                                         │
│ 10. Log to RELEASE_LOG.log                                       │
│                                                                   │
│ Result: 🎉 Release is LIVE on GitHub + PyPI!                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Git Tracking Strategy

### What Gets Tracked (Committed to Git)

| File | Tracked? | Why |
|------|----------|-----|
| `pyproject.toml` | ✅ Yes | Main project config, version is updated |
| `src/ascii_guard/__init__.py` | ✅ Yes | Package version constant |
| `release/RELEASE_SUMMARY.md` | ✅ Yes | Historical record of this release |
| `release/AI_RELEASE_SUMMARY.md` | ✅ Yes (during execute) | Audit trail: what AI wrote |
| `release/RELEASE_NOTES.md` | ✅ Yes (during execute) | Audit trail: what was reviewed/edited |
| `release/RELEASE_LOG.log` | ✅ Yes | Operational audit log |
| `release/release.sh` | ✅ Yes | Release automation script |
| `release/RELEASE.md` | ✅ Yes | This documentation |
| `.cursor/rules/ascii-guard-releases.mdc` | ✅ Yes | AI release guidance |

### What Gets Deleted (After Commit)

| File | Deleted? | When | Why |
|------|----------|------|-----|
| `release/AI_RELEASE_SUMMARY.md` | ✅ Yes | After execute | Working file, already committed |
| `release/RELEASE_NOTES.md` | ✅ Yes | After execute | Working file, already committed |
| `release/.prepare_state` | ✅ Yes | After execute | Temporary metadata |
| `dist/` | ✅ Yes | After execute | Build artifacts (on PyPI now) |
| `build/` | ✅ Yes | After execute | Build cache |

### What's Gitignored

| File | Gitignored? | Why |
|------|-------------|-----|
| `dist/` | ✅ Yes | Build artifacts |
| `build/` | ✅ Yes | Build cache |
| `*.egg-info/` | ✅ Yes | Package metadata |
| `release/.prepare_state` | ✅ Yes | Temporary working file |

---

## Version Numbering

ascii-guard uses [Semantic Versioning](https://semver.org/):

### Version Format: `MAJOR.MINOR.PATCH`

**MAJOR (X.0.0)**: Breaking changes
- Changes that break existing API
- Require code changes in user projects
- Example: `feat!: Change CLI argument format`

**MINOR (0.X.0)**: New features
- New linting rules
- New CLI commands or options
- Backward-compatible additions
- Example: `feat: Add support for double-line boxes`

**PATCH (0.0.X)**: Bug fixes
- Bug fixes in detection logic
- Documentation updates
- Performance improvements
- Example: `fix: Correct corner character validation`

### Automatic Version Detection

The release script analyzes commit messages:

```bash
# MAJOR bump triggers
feat!: ...          # Breaking feature
fix!: ...           # Breaking fix
BREAKING CHANGE:    # Explicit breaking change

# MINOR bump triggers
feat: ...           # New feature
feature: ...        # New feature (alt)

# PATCH bump triggers
fix: ...            # Bug fix
chore: ...          # Maintenance
docs: ...           # Documentation
refactor: ...       # Code refactoring
```

### Version Tracking Locations

1. **`pyproject.toml`**: version field
   ```toml
   [project]
   version = "0.1.0"
   ```

2. **`src/ascii_guard/__init__.py`**: __version__ constant
   ```python
   __version__ = "0.1.0"
   ```

Both are updated automatically during release.

---

## PyPI Publishing

### PyPI Configuration

**Option 1: Token-based (Recommended)**

Create `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...your-token...
```

**Option 2: Keyring**

```bash
# Store token in keyring
keyring set https://upload.pypi.org/legacy/ __token__
```

### Test PyPI (Optional)

Test releases on TestPyPI first:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ ascii-guard
```

### Publishing Process

The release script automatically:
1. Builds wheel and sdist
2. Uploads to PyPI with twine
3. Verifies upload success

### Manual PyPI Publish

If needed:

```bash
# Build
python -m build

# Check package
twine check dist/*

# Upload
twine upload dist/ascii_guard-X.Y.Z*
```

---

## AI Integration

### Cursor Rule: `.cursor/rules/ascii-guard-releases.mdc`

**Purpose**: Guides AI through the release process

**Key Instructions**:
1. Generate AI summary in `release/AI_RELEASE_SUMMARY.md`
2. Run prepare: `./release/release.sh --prepare`
3. Prompt human to review `release/RELEASE_NOTES.md`
4. Run execute: `./release/release.sh --execute`

**Safeguards**:
- NEVER modify `release/release.sh` logic
- NEVER filter commits in code
- ALWAYS edit release notes files, not scripts
- ALWAYS wait for human review before execute
- ALWAYS verify PyPI credentials before publishing

---

## Troubleshooting

### Error: "PyPI authentication failed"

**Problem**: Missing or invalid PyPI credentials

**Solution**:
```bash
# Check ~/.pypirc exists
cat ~/.pypirc

# Or set up keyring
keyring set https://upload.pypi.org/legacy/ __token__

# Test authentication
twine check dist/*  # After building
```

### Error: "Package build failed"

**Problem**: Missing build dependencies

**Solution**:
```bash
# Install build tools
pip install build twine

# Verify installation
python -m build --version
twine --version
```

### Error: "Version already exists on PyPI"

**Problem**: Trying to release a version that's already published

**Solution**:
- PyPI does not allow overwriting versions
- Increment version and try again
- Use `--set-version` to bump version number

---

## References

### Related Files

- **`.cursor/rules/ascii-guard-releases.mdc`**: AI agent guidance for releases
- **`release/release.sh`**: Release automation script
- **`pyproject.toml`**: Project configuration and version
- **`CHANGELOG.md`**: Historical release notes
- **`TODO.md`**: Task tracking

### External Resources

- [Semantic Versioning](https://semver.org/): Version numbering rules
- [GitHub CLI](https://cli.github.com/): Release creation tool
- [Conventional Commits](https://www.conventionalcommits.org/): Commit message format
- [PyPI Publishing](https://packaging.python.org/tutorials/packaging-projects/): Python package publishing guide
- [twine](https://twine.readthedocs.io/): PyPI upload tool

---

**Document Version**: 1.0
**Project**: ascii-guard
**Adapted From**: ocroot release process

For questions or issues with the release process, open a GitHub issue.
