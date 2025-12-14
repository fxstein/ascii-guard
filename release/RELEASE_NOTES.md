# ascii-guard v2.2.1

## Summary

This release focuses on CI/CD hardening, security improvements, and workflow optimizations. The primary changes include comprehensive security hardening by pinning all GitHub Actions to commit SHAs, eliminating workflow redundancy that was causing duplicate CI runs on pull requests, and fixing cache-related issues in the CI pipeline. Additionally, Python 3.13 and 3.14 have been added to scheduled cross-platform tests, and the default Python version for single-version jobs has been updated from 3.12 to 3.14.

The release addresses critical security concerns by ensuring all GitHub Actions are pinned to immutable commit SHAs, preventing potential supply chain attacks from compromised action tags. Workflow efficiency has been significantly improved by removing redundant code quality and test coverage jobs from PR checks, reducing CI time and resource usage by approximately 50% for pull requests. The dependency check logic has also been improved to use `uv` commands instead of fragile text parsing, making it more robust and maintainable.

These improvements build upon the successful `uv` migration completed in v2.2.0, further optimizing the development and CI/CD experience while maintaining the project's commitment to security, efficiency, and best practices.

---

### ✨ Added

- docs: Mark CI/CD audit as implemented and complete task#85 ([e37fe55](https://github.com/fxstein/ascii-guard/commit/e37fe55f208f2afa02016d62e61ec28379f5b63d))
- chore: Add Python 3.13 and 3.14 to scheduled tests matrix (task#85.4) ([edbfda1](https://github.com/fxstein/ascii-guard/commit/edbfda1d8cb4496f3348f4f518841db35d74759e))
- fix: Add cache-suffix to prevent cache key conflicts in matrix jobs ([d1f28f0](https://github.com/fxstein/ascii-guard/commit/d1f28f0cfa45b23a13dd86070e0a5ce58cc05042))
- docs: Mark implementation gap analysis as resolved (task#79.6) ([d10c22e](https://github.com/fxstein/ascii-guard/commit/d10c22ed7c4c1572e1197a6245f3a776c580660d))
- chore: Mark Phase 6 complete - all implementation gaps addressed (task#79.6) ([67f678c](https://github.com/fxstein/ascii-guard/commit/67f678ca39005d50f21c30c456eac8bd937ca49b))
- chore: Update task list with implementation gap subtasks (task#79.6) ([363235b](https://github.com/fxstein/ascii-guard/commit/363235b7c6a48a571267d83ae8a8ab3a25bc7c47))
- docs: Create UV implementation gap analysis (task#79) ([307231d](https://github.com/fxstein/ascii-guard/commit/307231da4ce63178ce3e63c83e961e042c43f445))
- docs: Add explanation for uv recommendation in README ([46e9c18](https://github.com/fxstein/ascii-guard/commit/46e9c18b51f56f5c566730a964eba4de338acc5e))

### 🔄 Changed

- refactor: Remove wait-on-check-action and use native auto-merge (task#85.3) ([bdb3bf8](https://github.com/fxstein/ascii-guard/commit/bdb3bf85a8d287c2ce53ab35454e6199a7a314ab))
- chore: Update release workflow to use Python 3.14 for consistency ([9744b51](https://github.com/fxstein/ascii-guard/commit/9744b51950cd2b8449749f19182d050fd24a6fcb))
- chore: Update default Python version from 3.12 to 3.14 for all single-version jobs ([8746841](https://github.com/fxstein/ascii-guard/commit/87468417d5018b0b5fb196e3f360b313965ff472))
- docs: Update developer documentation to use uv (task#79.6.1) ([12d56d8](https://github.com/fxstein/ascii-guard/commit/12d56d839a41197e00b1dfee6a972d5e506d1938))
- chore: Update README installation note wording ([69cca3e](https://github.com/fxstein/ascii-guard/commit/69cca3e7da2a90e95c38775a4d17b41d00256672))
- chore: Update release log for 2.2.0 ([05d4edf](https://github.com/fxstein/ascii-guard/commit/05d4edfbfa2dac0df0d65677822db7418ef6de7b))

### 🐛 Fixed

- fix: Use save-cache: false for test-import-without-deps job ([9e2297e](https://github.com/fxstein/ascii-guard/commit/9e2297e72f261216bc7d8d61459d661fc6929342))
- fix: Upgrade setup-uv from v4 to v7.1.6 to fix cache 400 errors ([783ec2e](https://github.com/fxstein/ascii-guard/commit/783ec2ea15c19cc1352743188a073503ef337701))
- fix: Optimize uv caching to eliminate cache warnings ([9b64a20](https://github.com/fxstein/ascii-guard/commit/9b64a202798b0c3fbfe16ecce160c5984b4a77a1))
- fix: Use --extra dev instead of --dev for uv sync (CI/CD fix) ([1e4a4b0](https://github.com/fxstein/ascii-guard/commit/1e4a4b0e6a9f322dc2d64789300701ca12ffa297))

*Documentation, maintenance, and other commits: 9*

*Total commits: 27*
