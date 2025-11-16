# Release Process Testing Guide

This document describes how to test the release process without actually publishing to GitHub or PyPI.

## Prerequisites: CI/CD Status Check

**BEFORE TESTING OR EXECUTING ANY RELEASE:**

### Check CI/CD Status

```bash
# Check latest workflow status
gh run list --limit 1

# View more details if needed
gh run list --limit 5
```

### Required Status

**Must show:**
- Status: `completed`
- Conclusion: `success`
- No workflows `in_progress`

**If CI/CD is failing:**
1. STOP - Do not proceed with release testing
2. Identify failing workflows: `gh run view <run-id>`
3. Fix the issues causing failures
4. Wait for CI/CD to pass
5. Only then proceed with release testing

### Why This Matters

- Release process testing validates the automation
- But if CI/CD is already failing, you're testing a broken state
- Always start from a clean, passing CI/CD state
- This ensures test results are meaningful

---

## Dry-Run Mode

The release script supports a `--dry-run` flag that simulates the entire release process without performing any actual git operations.

### Usage

```bash
# 1. Create AI release summary
cat > release/AI_RELEASE_SUMMARY.md << 'EOF'
This is a test release to validate the release process.
All functionality works as expected without publishing.
EOF

# 2. Prepare release
./release/release.sh --prepare

# 3. Review release notes
vim release/RELEASE_NOTES.md

# 4. Test execute with dry-run
./release/release.sh --execute --dry-run
```

### What Dry-Run Does

**Simulates:**
- ✅ Version file updates (pyproject.toml, __init__.py)
- ✅ Package build (python -m build)
- ✅ Git commit creation
- ✅ Git tag creation
- ✅ Git push operations
- ✅ Release log updates

**Actually Performs:**
- Version files ARE updated (so you can verify the changes)
- Release notes ARE copied to RELEASE_SUMMARY.md
- Working files remain for inspection

**Does NOT Perform:**
- Git commit (files staged but not committed)
- Git tag creation
- Git push to GitHub
- GitHub Actions trigger
- PyPI publishing

### Expected Output

Dry-run mode shows yellow `[DRY-RUN]` prefixes for all simulated operations:

```
🧪 DRY-RUN MODE ENABLED
No actual git operations will be performed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Executing release 0.2.0...

📝 Copying release notes to summary...
📝 Updating version in pyproject.toml and __init__.py...
📦 Building Python package...
[DRY-RUN] Would clean previous builds
[DRY-RUN] Would run: python3 -m build
[DRY-RUN] Package build simulated successfully
💾 Committing version change and release notes...
[DRY-RUN] Would commit with message: 'release: Version 0.2.0'
🏷️  Creating tag v0.2.0...
[DRY-RUN] Would create tag: v0.2.0
[DRY-RUN] Would push main branch to origin
[DRY-RUN] Would push tag v0.2.0 to origin

✅ DRY-RUN COMPLETE - No actual release was performed

📋 What would have happened:
   • Version files updated to 0.2.0
   • Package built successfully
   • Changes committed
   • Tag v0.2.0 created and pushed
   • GitHub Actions triggered for PyPI publish
```

### Cleanup After Dry-Run

After testing with dry-run, clean up the modified files:

```bash
# Restore version files
git checkout pyproject.toml src/ascii_guard/__init__.py

# Remove working files
rm -f release/AI_RELEASE_SUMMARY.md release/RELEASE_NOTES.md release/.prepare_state release/RELEASE_SUMMARY.md

# Clean build artifacts
rm -rf dist/ build/ src/*.egg-info
```

## Testing Checklist

Use this checklist to validate the release process:

### Prepare Mode Tests

- [ ] Run prepare with no commits (should warn)
- [ ] Run prepare with feat: commits (should detect minor)
- [ ] Run prepare with fix: commits (should detect patch)
- [ ] Run prepare with feat!: commits (should detect major)
- [ ] Verify AI_RELEASE_SUMMARY.md is included in output
- [ ] Verify RELEASE_NOTES.md is generated with all sections
- [ ] Verify commit categorization is correct

### Set-Version Mode Tests

- [ ] Override to valid version (should succeed)
- [ ] Override to invalid format like "v1.0.0" (should fail)
- [ ] Override to invalid format like "1.0" (should fail)
- [ ] Override to lower version (should fail)
- [ ] Override to same version (should fail)
- [ ] Verify RELEASE_NOTES.md header is updated

### Execute Mode Tests (Dry-Run)

- [ ] Run execute without prepare (should fail)
- [ ] Run execute after committing changes (should fail with invalidation message)
- [ ] Run execute --dry-run successfully
- [ ] Verify version files are updated
- [ ] Verify RELEASE_SUMMARY.md is created
- [ ] Verify all [DRY-RUN] messages appear
- [ ] Verify no actual commits/tags/pushes occur

### Process Invalidation Tests

- [ ] Prepare → commit something → execute (should fail)
- [ ] Verify clear error message about invalidation
- [ ] Verify instructions to restart process

### Version Override Tests

- [ ] Prepare (auto-detects 0.2.0) → set-version 1.0.0 → execute
- [ ] Verify RELEASE_NOTES.md shows 1.0.0
- [ ] Verify prepare state is updated

## Testing Without pyenv/venv

If you don't have the Python environment set up (pyenv, venv, etc), dry-run mode will still work for most operations. The only issue is that pre-commit hooks may fail during commits.

To test without a full environment:

```bash
# Use --no-verify to skip pre-commit hooks
git commit --no-verify -m "test"

# Or test with dry-run (doesn't actually commit)
./release/release.sh --execute --dry-run
```

## Continuous Testing

The release process should be tested:

1. **Before Each Release**: Run dry-run to validate
2. **After Process Changes**: Full checklist
3. **In CI/CD**: Consider adding dry-run tests to GitHub Actions

## Known Limitations

### Dry-Run Limitations

- **Version files are actually modified**: Dry-run updates pyproject.toml and __init__.py for real (so you can verify), but doesn't commit them
- **Working files are created**: RELEASE_SUMMARY.md is created but not committed
- **Pre-commit hooks don't run**: Since no actual commit happens, pre-commit validation is skipped

### Environment Requirements

For real releases (not dry-run):
- Python 3.12+ installed via pyenv
- `python -m build` package installed
- `gh` CLI authenticated
- PyPI trusted publishing configured

## Troubleshooting

### "Release process invalidated"

**Cause**: Commits were made after running `--prepare`

**Solution**: Restart the process:
```bash
rm -f release/.prepare_state release/AI_RELEASE_SUMMARY.md release/RELEASE_NOTES.md
./release/release.sh --prepare
# Review, then execute
```

### "Package build failed" in Dry-Run

**Cause**: Shouldn't happen in dry-run (it's simulated)

**Solution**: Update to latest release.sh version

### Version files not restored after dry-run

**Cause**: Manual cleanup needed

**Solution**:
```bash
git checkout pyproject.toml src/ascii_guard/__init__.py
```

## Best Practices

1. **Always test with dry-run first** before real releases
2. **Review RELEASE_NOTES.md** carefully during testing
3. **Test version override** to ensure it works
4. **Verify process invalidation** catches stale prepares
5. **Clean up after testing** to avoid confusion

## Future Improvements

Potential enhancements for testing:

- [ ] Automated test script that runs full checklist
- [ ] Mock GitHub/PyPI endpoints for full integration testing
- [ ] CI job that runs dry-run on every commit to release.sh
- [ ] Test fixtures with various commit patterns

---

**Last Updated**: 2025-11-16
**Version**: 1.0
