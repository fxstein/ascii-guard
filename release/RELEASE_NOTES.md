# ascii-guard v2.2.2

This release focuses on infrastructure hardening and reliability improvements that ensure consistent development environments across all platforms. The most significant change is the complete isolation of Python environments through uv-managed Python versions, preventing issues with corrupted or mismatched system Python installations that could break development workflows.

Key improvements include fixing the scheduled CI test failures that were occurring due to module import errors in the Performance Benchmark job, and updating all GitHub Actions dependencies to their latest versions for improved security and compatibility. The uv setup now enforces the use of managed Python versions with explicit validation, ensuring that virtual environments always use the correct Python interpreter regardless of system configuration.

These changes are primarily internal improvements that enhance developer experience and CI/CD reliability. Users will benefit from more stable releases and faster CI/CD pipelines, while developers working on the project will have a more robust and isolated development environment that works consistently across different systems and Python installations.

---

### ✨ Added

- chore: add AI release summary ([8f4f5cd](https://github.com/fxstein/ascii-guard/commit/8f4f5cd45bbdd6284f8c90c95703f70e341b598b))
- feat: harden uv setup to use managed Python only (task#93) ([40ba545](https://github.com/fxstein/ascii-guard/commit/40ba545864f497a92668096cf66f8594700ee052))
- chore: add task list for uv hardening (task#93) ([d4f784c](https://github.com/fxstein/ascii-guard/commit/d4f784cc016e19c9f7bcbbce357fcd3de7eeb711))
- chore: create task list for fixing scheduled CI failures and Dependabot PRs (task#86) ([9be7b3d](https://github.com/fxstein/ascii-guard/commit/9be7b3dde22f5828b574e3dccc52b3104ebd175f))

### 🔄 Changed

- chore: Archive completed tasks #79 and #85, update uv.lock for v2.2.1 ([6e6afdd](https://github.com/fxstein/ascii-guard/commit/6e6afddac3171435d24cb8f8d88fb5952f82e92a))
- chore: Update release log for 2.2.1 ([d19e93f](https://github.com/fxstein/ascii-guard/commit/d19e93fa1de07a5dac2029f19832d241e10b172e))

### 🐛 Fixed

- fix: use uv run in Performance Benchmark job (task#86.1) ([5d849b0](https://github.com/fxstein/ascii-guard/commit/5d849b0c193b384f94993b6224c25bad007d8a8e))

*Documentation, maintenance, and other commits: 6*

*Total commits: 13*
