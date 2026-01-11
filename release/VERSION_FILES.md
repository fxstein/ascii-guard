# Version Files Reference

This document lists all files that contain version numbers for ascii-guard.

## Files Containing Version Numbers

### 1. pyproject.toml
**Location**: `pyproject.toml`
**Field**: `version = "X.Y.Z"`
**Line Range**: ~7
**Format**: String in quotes
**Purpose**: Package version for PyPI and pip installation

### 2. src/ascii_guard/__init__.py
**Location**: `src/ascii_guard/__init__.py`
**Field**: `__version__ = "X.Y.Z"`
**Line Range**: ~21
**Format**: String assignment
**Purpose**: Runtime version accessible via `ascii_guard.__version__`

### 3. uv.lock
**Location**: `uv.lock`
**Field**: `version = "X.Y.Z"` (within `[[package]]` section for `name = "ascii-guard"`)
**Line Range**: Variable (within package section)
**Format**: TOML string in quotes
**Purpose**: Lock file version for reproducible builds and dependency resolution

## Update Process

All version files MUST be updated together atomically during the release process to maintain consistency.

### When to Update

1. **During PREPARE phase**: All version files are updated immediately after determining new version
2. **During SET-VERSION**: All version files are updated if version is overridden
3. **NOT during EXECUTE**: Execute only commits the already-updated files

### How to Update

The `release.sh` script contains an `update_version()` function that updates all files in this list.

**Update function location**: `release/release.sh` lines ~212-229

```bash
update_version() {
    local new_version="$1"

    # Update pyproject.toml
    sed -i '' 's/^version = ".*"/version = "'"$new_version"'"/' pyproject.toml

    # Update __init__.py
    sed -i '' 's/^__version__ = ".*"/__version__ = "'"$new_version"'"/' src/ascii_guard/__init__.py

    # Update uv.lock (package version in lock file)
    if [[ -f uv.lock ]]; then
        sed -i '' '/^name = "ascii-guard"$/,/^version = / {
            s/^version = ".*"/version = "'"$new_version"'"/
        }' uv.lock
    fi
}
```

## Verification

After updating versions, verify consistency:

```bash
# Check pyproject.toml
grep '^version = ' pyproject.toml

# Check __init__.py
grep '^__version__ = ' src/ascii_guard/__init__.py

# Check uv.lock
grep -A 2 'name = "ascii-guard"' uv.lock | grep '^version = '

# All should show the same version
```

## Version Source of Truth

**GitHub Releases** is the source of truth for the current version.

Use `gh release list --limit 1` to get the latest released version.

**DO NOT** trust version numbers in source files as they may be modified during development or testing.

## Adding New Version Files

If additional files need to track versions (e.g., documentation, CI/CD configs):

1. Add file to this document with location and format
2. Update `update_version()` function in `release.sh`
3. Test with `./release/release.sh --execute --dry-run`

---

**Last Updated**: 2025-11-16
**Maintained by**: Release automation process
