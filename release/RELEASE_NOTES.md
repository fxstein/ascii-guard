# ascii-guard v2.1.0

This release officially adds support for Python 3.13 and 3.14, ensuring compatibility with the latest Python environments. We have updated our CI/CD pipelines to test against these versions and refined our development tooling to support the latest Python releases.

Additionally, this release includes stability improvements to our release process and CI workflows, resolving deprecated configuration warnings and ensuring smoother future updates.

---

### ✨ Added

- feat: Official Python 3.13 support ([c2fe020](https://github.com/fxstein/ascii-guard/commit/c2fe0203889227f3bf4b559f1d555c76c2f4186d))
- feat: Official Python 3.14 support ([9ba2658](https://github.com/fxstein/ascii-guard/commit/9ba26581572e82f2de20fe0d8394edc8fa340756), [c7720f8](https://github.com/fxstein/ascii-guard/commit/c7720f81dab5bfe17226059038b5e06616e4060d))

### 🔄 Changed

- chore: Update .python-version to 3.14.2 to match venv ([f992830](https://github.com/fxstein/ascii-guard/commit/f9928305863626bae91f39a8856c880fe2bb1da1))
- fix: Update Codecov action input from 'file' to 'files' ([048d3e8](https://github.com/fxstein/ascii-guard/commit/048d3e8f4af0016db3c8612689b64fcf8c30378b))

### 🐛 Fixed

- fix: Ensure release script validates venv python, not system python ([0761704](https://github.com/fxstein/ascii-guard/commit/076170486f8aa743530be5fe17039351fe34e0a0))

*Total commits: 11*
