# Branch Protection Configuration

## Overview

The `main` branch uses **selective protection** that balances safety with workflow efficiency for solo development.

## Protection Rules

### Enabled ✅

1. **Lock branch** (prevent deletion)
   - Prevents accidental deletion of `main` branch
   - Can't run: `git push origin :main`

2. **Prevent force pushes** (optional)
   - Blocks: `git push --force origin main`
   - Protects against accidental history rewriting
   - Admin bypass available if needed

### Disabled ❌

1. **Require pull requests** - OFF
   - Reason: Solo project, direct commits are fine
   - Benefit: Release process works unchanged

2. **Require status checks** - OFF
   - Reason: Pre-commit hooks already enforce quality
   - Benefit: No waiting for GitHub Actions before push

3. **Require approvals** - OFF
   - Reason: No other reviewers on project
   - Benefit: No workflow friction

4. **Include administrators** - OFF
   - Reason: Admin (owner) needs direct push access
   - Benefit: Release script works unchanged

## Impact on Workflows

### ✅ What Still Works

- Direct push to `main` (you're admin)
- Release process: `./release/release.sh --execute`
- Tag pushes: `git push origin v1.2.1`
- Normal development workflow
- Pre-commit hooks enforce quality

### ❌ What's Blocked (Good!)

- Force push to `main`
- Deleting `main` branch
- Accidentally rewriting history

## Release Process Compatibility

**The release script works unchanged:**

```bash
# Step 1: Prepare
./release/release.sh --prepare
# Review notes, human gate

# Step 2: Execute
./release/release.sh --execute
# ✅ Pushes main + tag successfully
```

**Why it works:**
1. Admin bypass allows direct push to `main`
2. Tags aren't affected by branch protection
3. No PR workflow required
4. No status check delays

## Configuration Location

GitHub Settings → Branches → main → Edit rule

## Rationale

This configuration provides:
- **Safety**: Protects against common mistakes
- **Speed**: No workflow delays
- **Quality**: Pre-commit hooks enforce standards
- **Flexibility**: Easy to add stricter rules later

## Future Considerations

If adding collaborators:
1. Enable "Require pull requests"
2. Enable "Require status checks"
3. Keep admin bypass for releases
4. Consider modifying release script for PR workflow

## Verification

After enabling protection, test with:

```bash
# Should succeed (you're admin)
echo "test" >> README.md
git commit -am "test: verify branch protection"
git push origin main

# Should fail (protection working)
git push --force origin main
```

Then revert the test commit.

## References

- GitHub Branch Protection: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- Release Process: `docs/RELEASE_DESIGN.md`
