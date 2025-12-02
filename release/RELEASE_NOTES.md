# ascii-guard v1.5.1

This release focuses on improving cross-platform compatibility and CI/CD reliability. The most significant improvements address scheduled test failures that were occurring on Python 3.10 and Windows platforms, ensuring ascii-guard works reliably across all supported environments.

Three critical compatibility issues have been resolved: Python 3.10 test failures due to conditional tomllib imports, Windows Unicode encoding errors when handling box-drawing characters, and Windows-specific file permission test behavior. These fixes ensure the test suite passes completely on Python 3.10, 3.11, and 3.12 across Ubuntu, macOS, and Windows environments.

The release process itself has been enhanced with GitHub Actions now correctly using detailed release notes from the repository instead of generic templates. This provides users with comprehensive changelog information for each release. Additionally, several GitHub Actions dependencies have been updated to their latest versions, including actions/checkout v6, actions/setup-python v6, and wait-on-check-action v1.4.1, ensuring the CI/CD pipeline benefits from the latest improvements and security updates.

---

### ✨ Added

- chore: prepare v1.5.1 release - add AI summary ([6aa1a68](https://github.com/fxstein/ascii-guard/commit/6aa1a685d5bde04e64f3a7928f734347520ab608))
- chore: close issue #11 (fixed in v1.5.0), archive task#58, create task#59 for ignore markers (task#57.5-57.7) ([96268c4](https://github.com/fxstein/ascii-guard/commit/96268c4055a303e14f486ec17d297696f7bdde4a))
- chore: review open issues and create task#58 to fix issue #11 (task#57.1-57.4) ([9a6db8a](https://github.com/fxstein/ascii-guard/commit/9a6db8a776d2c318d85e33a47b8fcd0d7c093346))
- chore: add task#57 for reviewing and fixing open GitHub issues ([dc4bc27](https://github.com/fxstein/ascii-guard/commit/dc4bc27f077b6b214e77d1b8c612e2796fccd4c9))
- chore: add task#56 for reviewing and merging Dependabot PRs ([9728891](https://github.com/fxstein/ascii-guard/commit/972889171613e81d1da7db0da547bfdd800d5f03))

### 🔄 Changed

- chore: update task#57 notes with investigation progress ([0db30e4](https://github.com/fxstein/ascii-guard/commit/0db30e4651defbb32cf97130013d0d86ff9e5196))
- chore: Update release log for 1.5.0 ([413acbd](https://github.com/fxstein/ascii-guard/commit/413acbdc63593ca818ae7c79834469d7ad8ce6a2))

### 🐛 Fixed

- chore: archive completed task#57 (GitHub issues review and fixes) ([ef55853](https://github.com/fxstein/ascii-guard/commit/ef558537eae81f206ca3afe7836c4fea08da660e))
- chore: complete task#57 - all scheduled test issues resolved ([fe2fa49](https://github.com/fxstein/ascii-guard/commit/fe2fa497cc6e979b9e9ddda08841ecd45e89b3ef))
- fix: skip chmod-based permission tests on Windows ([ee97c07](https://github.com/fxstein/ascii-guard/commit/ee97c07c16f776f85db1baab115d50f850dc0d4e))
- fix: force UTF-8 encoding on Windows for scheduled tests ([2a873eb](https://github.com/fxstein/ascii-guard/commit/2a873eb7311b731d0125094ef312e6a6da3b94fd))
- fix: allow tomllib in stdlib test for Python 3.10 compatibility ([8a1f62b](https://github.com/fxstein/ascii-guard/commit/8a1f62bba9ac9f3f04e1c6dffe20bc86808ed0c3))
- chore: complete task#57 (review and fix open GitHub issues) ([aaed37a](https://github.com/fxstein/ascii-guard/commit/aaed37a6a9e1147f587cec5f542cd0683f994628))
- fix: use RELEASE_SUMMARY.md for GitHub releases instead of generic template ([d559053](https://github.com/fxstein/ascii-guard/commit/d559053ef28dd7b5b4899bb6e1b485a499181bef))

*Documentation, maintenance, and other commits: 6*

*Total commits: 20*
