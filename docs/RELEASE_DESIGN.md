# Release Process Design for ascii-guard

**Status**: Design Phase (Task #16)
**Purpose**: Design document for implementing an automated release process for ascii-guard

---

## Overview

This document outlines the design for implementing a fully automated, AI-friendly release process for `ascii-guard`.

### Goals

1. **AI-Driven**: AI agent can orchestrate releases with minimal human intervention
2. **Human Review**: Critical review checkpoint before publishing
3. **Automated**: Single command to prepare, single command to execute
4. **Safe**: No accidental publishes, clear rollback path
5. **Traceable**: Full audit trail of what was released and why
6. **CI/CD Gated**: No release proceeds if CI/CD is failing

### Critical CI/CD Requirements

**MANDATORY PRE-RELEASE CHECKS:**

1. **Before Starting Release Preparation**:
   - Check CI/CD status for latest commit: `gh run list --limit 1`
   - If ANY workflow has failed: **STOP and decline to start release**
   - Must fix CI/CD errors FIRST before attempting any release
   - Communicate clearly: "CI/CD is failing, cannot proceed with release"

2. **During Release Preparation**:
   - Any commit made during preparation → Monitor CI/CD actions
   - Wait for ALL GitHub Actions to complete
   - Check status: `gh run list --limit 5`
   - Only proceed to `--execute` if ALL actions show `completed success`

3. **Never Bypass**:
   - Never use `--no-verify` on release commits
   - Never work around CI/CD failures
   - Never proceed with manual fixes without re-validating CI/CD

**Why This Matters:**
- CI/CD failures indicate code quality issues
- Releasing broken code to PyPI is irreversible
- Users depend on package quality
- Our automated tests are the last line of defense

---

## Current State

### What We Have ✅

- **release/RELEASE.md**: Complete documentation (680 lines)
- **GitHub Actions**: `release.yml` workflow with trusted publishing
- **PyPI**: Trusted publishing configured
- **Package**: Builds successfully, zero dependencies verified
- **Versioning**: `pyproject.toml` + `src/ascii_guard/__init__.py`

### What We Need ❌

- **release.sh**: The automation script (main deliverable)
- **.cursor/rules/ascii-guard-releases.mdc**: AI agent guidance
- **Testing**: Dry-run capability before real release

---

## Design: release.sh Script

### Architecture

The script will have **3 modes**:

1. **--prepare**: Analyze commits, generate release notes
2. **--set-version X.Y.Z**: Override auto-detected version
3. **--execute**: Publish the release

### File Flow

```
┌─────────────────────────────────────────────────────────┐
│ INPUTS                                                  │
├─────────────────────────────────────────────────────────┤
│ • release/AI_RELEASE_SUMMARY.md (AI-written)           │
│ • Git commits since last tag                            │
│ • pyproject.toml (current version)                      │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ PREPARE PHASE (./release/release.sh --prepare)         │
├─────────────────────────────────────────────────────────┤
│ • Parse commits (conventional commits format)           │
│ • Determine version bump (MAJOR/MINOR/PATCH)           │
│ • Read AI_RELEASE_SUMMARY.md                            │
│ • Generate release/RELEASE_NOTES.md                     │
│ • Save state to release/.prepare_state                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ REVIEW PHASE (HUMAN)                                    │
├─────────────────────────────────────────────────────────┤
│ • Edit release/RELEASE_NOTES.md                         │
│ • Optional: ./release/release.sh --set-version X.Y.Z   │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ EXECUTE PHASE (./release/release.sh --execute)         │
├─────────────────────────────────────────────────────────┤
│ • Update pyproject.toml version                         │
│ • Update src/ascii_guard/__init__.py version            │
│ • Build package (python -m build)                       │
│ • Commit version bump                                   │
│ • Create git tag                                        │
│ • Push to GitHub (triggers GitHub Actions)             │
│ • GitHub Actions: publish to PyPI                       │
│ • GitHub Actions: create GitHub release                 │
│ • Cleanup working files                                 │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ OUTPUTS                                                  │
├─────────────────────────────────────────────────────────┤
│ • PyPI: ascii-guard X.Y.Z published                     │
│ • GitHub: Release created with wheel/sdist              │
│ • Git: vX.Y.Z tag                                       │
│ • release/RELEASE_LOG.log (audit trail)                │
└─────────────────────────────────────────────────────────┘
```

---

## Key Design Features

### Core Features ✅

- Two-file architecture (AI_RELEASE_SUMMARY.md → RELEASE_NOTES.md)
- Three-step workflow (prepare → review → execute)
- Version override capability
- Commit categorization
- Audit logging

### Python Package Specifics 🔄

| Aspect | Implementation |
|--------|----------------|
| **Language** | Python package |
| **Version Files** | `pyproject.toml`, `src/ascii_guard/__init__.py` |
| **Build** | `python -m build` (wheel + sdist) |
| **Distribution** | PyPI + GitHub release |
| **Artifacts** | `*.whl`, `*.tar.gz` |
| **Publishing** | GitHub Actions trusted publishing |

---

## Implementation Plan

### Phase 1: release.sh Core

**Files to create**:
- `release/release.sh` (main script, ~500 lines)

**Functions needed**:
```bash
# Core functions
get_current_version()      # Read from pyproject.toml
get_last_release_tag()     # git describe --tags --abbrev=0
get_commits_since_tag()    # git log <tag>..HEAD
categorize_commit()        # Parse conventional commit format
determine_version_bump()   # Based on commit types
update_version_files()     # pyproject.toml + __init__.py

# Prepare mode
cmd_prepare()              # Main prepare orchestration
generate_release_notes()   # Combine AI summary + commits
save_prepare_state()       # Store metadata

# Set version mode
cmd_set_version()          # Override version number
validate_version_format()  # Ensure X.Y.Z format
validate_version_gt()      # Ensure new > current

# Execute mode
cmd_execute()              # Main execute orchestration
build_package()            # python -m build
create_git_tag()           # git tag -a vX.Y.Z
push_to_github()           # git push origin main && git push origin vX.Y.Z
cleanup_working_files()    # Remove temp files
log_release()              # Append to RELEASE_LOG.log
```

### Phase 2: Version File Updates

**pyproject.toml update**:
```bash
# Update version field
sed -i '' 's/^version = ".*"/version = "'"$NEW_VERSION"'"/' pyproject.toml
```

**__init__.py update**:
```bash
# Update __version__ constant
sed -i '' 's/^__version__ = ".*"/__version__ = "'"$NEW_VERSION"'"/' src/ascii_guard/__init__.py
```

### Phase 3: GitHub Actions Integration

**Key decision**: Release script does NOT publish to PyPI directly.

**Rationale**:
- GitHub Actions has trusted publishing configured
- Avoids storing PyPI tokens locally
- CI runs tests before publishing
- Consistent with our CI/CD strategy

**Workflow**:
1. `release.sh --execute` pushes tag to GitHub
2. GitHub Actions `release.yml` is triggered by tag push
3. GitHub Actions builds, tests, and publishes to PyPI
4. GitHub Actions creates GitHub release with artifacts

**Modification to release.sh**:
```bash
# Execute phase does NOT call twine directly
# Instead, it:
# 1. Pushes tag
# 2. Waits for GitHub Actions (optional monitoring)
# 3. Reports success/failure
```

### Phase 4: Cursor AI Rules

**File to create**:
- `.cursor/rules/ascii-guard-releases.mdc`

**Content structure**:
```markdown
# When user says "Release ascii-guard"

## Step 1: Generate AI Summary
- Write 2-3 paragraphs
- Save to release/AI_RELEASE_SUMMARY.md

## Step 2: Prepare
- Run: ./release/release.sh --prepare
- Show preview to user

## Step 3: Review
- Prompt user to review release/RELEASE_NOTES.md
- Handle version overrides if requested

## Step 4: Execute
- Run: ./release/release.sh --execute
- Monitor GitHub Actions
- Report success

## Safeguards
- Never modify release.sh logic
- Always wait for human approval before execute
- Never skip the review step
```

---

## Commit Parsing Strategy

### Conventional Commits Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Type Mapping

| Commit Type | Category | Version Bump |
|-------------|----------|--------------|
| `feat!:` | Breaking Changes | MAJOR |
| `fix!:` | Breaking Changes | MAJOR |
| `BREAKING CHANGE:` in body | Breaking Changes | MAJOR |
| `feat:` | Added | MINOR |
| `feature:` | Added | MINOR |
| `fix:` | Fixed | PATCH |
| `docs:` | Documentation | PATCH |
| `chore:` | Maintenance | PATCH |
| `refactor:` | Changed | PATCH |
| `test:` | Testing | (not shown) |
| `ci:` | CI/CD | (not shown) |

### Example Parsing

**Input commits**:
```
feat: Add config file support
fix: Correct corner detection
docs: Update README
chore: Bump dependencies
```

**Output categories**:
```markdown
### Added
- feat: Add config file support ([abc123](link))

### Fixed
- fix: Correct corner detection ([def456](link))

*Documentation and maintenance commits: 2*
```

---

## State Management

### .prepare_state File

**Purpose**: Store metadata between prepare and execute

**Format** (shell-sourceable):
```bash
NEW_VERSION="0.2.0"
CURRENT_VERSION="0.1.0"
BUMP_TYPE="minor"
LAST_TAG="v0.1.0"
COMMIT_COUNT="15"
PREPARE_TIMESTAMP="2025-11-16T16:45:00Z"
```

**Validation in execute**:
- Check file exists (prepare was run)
- Check timestamp is recent (<7 days)
- Verify current version hasn't changed

---

## Error Handling

### Prepare Phase

| Error | Detection | Resolution |
|-------|-----------|------------|
| No AI summary | File missing | Prompt user to create it |
| No commits | Empty log | Warn: "No changes to release" |
| Invalid commits | Parse failure | Skip and categorize as "Other" |

### Execute Phase

| Error | Detection | Resolution |
|-------|-----------|------------|
| No prepare state | File missing | Fail: "Run --prepare first" |
| Dirty working dir | `git status` | Fail: "Commit changes first" |
| Build failure | Exit code | Fail: Show build errors |
| Push failure | Exit code | Fail: Show git errors |

---

## Testing Strategy

### Manual Testing Checklist

Before final implementation:

- [ ] Test on clean repo clone
- [ ] Test with no commits (edge case)
- [ ] Test with breaking change commits
- [ ] Test version override (valid)
- [ ] Test version override (invalid format)
- [ ] Test version override (invalid progression)
- [ ] Test execute without prepare (should fail)
- [ ] Test execute with dirty working dir (should fail)
- [ ] Test GitHub Actions trigger after tag push

### Dry-Run Mode (Future Enhancement)

**Potential flag**: `--dry-run`

**Behavior**:
- Simulate all operations
- Show what would be done
- Don't modify files
- Don't push to GitHub

---

## Security Considerations

### What Gets Committed

- ✅ `release/AI_RELEASE_SUMMARY.md` (audit trail)
- ✅ `release/RELEASE_NOTES.md` (audit trail)
- ✅ `release/RELEASE_SUMMARY.md` (historical record)
- ✅ `release/RELEASE_LOG.log` (audit log)
- ❌ `release/.prepare_state` (temporary, gitignored)

### Sensitive Data

- ❌ No PyPI tokens in script (use GitHub Actions trusted publishing)
- ❌ No GitHub tokens in script (use `gh` CLI with user auth)
- ✅ All credentials via external auth systems

---

## Dependencies

### Required Tools

```bash
# Must be installed
git         # Version control
gh          # GitHub CLI (for release creation monitoring)
python3     # Package building
sed         # Text manipulation

# Python packages (dev dependencies)
build       # python -m build
twine       # Package validation (optional, for local testing)
```

### Environment Checks

Script will verify:
```bash
# Check git
command -v git >/dev/null || die "git not found"

# Check gh CLI
command -v gh >/dev/null || die "gh CLI not found"
gh auth status || die "gh not authenticated"

# Check Python
command -v python3 >/dev/null || die "python3 not found"

# Check build module
python3 -c "import build" 2>/dev/null || die "pip install build required"
```

---

## Rollback Strategy

### If Release Fails

**After prepare, before execute**:
- Just delete `release/.prepare_state`
- No changes have been made

**After execute starts, before push**:
- Changes are local only
- `git reset --hard HEAD^` to undo commit
- Delete local tag: `git tag -d vX.Y.Z`

**After push to GitHub**:
- ⚠️ Cannot undo PyPI publish (versions are immutable)
- Can delete GitHub release: `gh release delete vX.Y.Z`
- Can delete tag: `git push origin :refs/tags/vX.Y.Z`
- Must increment version and release again

---

## Future Enhancements

### Potential Additions

1. **--dry-run**: Simulate release without changes
2. **--changelog**: Generate CHANGELOG.md automatically
3. **--check**: Pre-flight checks before prepare
4. **Release candidates**: Support `vX.Y.Z-rc1` tags
5. **Hotfix workflow**: Fast-track patch releases
6. **Multi-branch**: Support release branches

---

## Success Criteria

This design will be considered complete when:

- [ ] `release.sh` script implements all 3 modes
- [ ] Script successfully prepares a release
- [ ] Script successfully executes a release
- [ ] PyPI publish works via GitHub Actions
- [ ] GitHub release is created automatically
- [ ] Cursor AI rule guides agent correctly
- [ ] Full audit trail in RELEASE_LOG.log
- [ ] Documentation matches implementation

---

## References

### Source Material

- **ascii-guard release docs**: `release/RELEASE.md`

### Related Tasks

- **#13**: Set up semantic versioning and release tagging workflow
- **#8**: Configure PyPI publishing workflow with GitHub Actions (DONE)

---

**Document Version**: 1.0
**Created**: 2025-11-16
**Status**: Ready for Review
**Next Step**: Review with user, then implement release.sh
