# ascii-guard v2.2.0

This release completes the comprehensive migration from traditional Python package management (venv, pip, pyenv) to uv, a modern and fast package manager. The migration eliminates all manual virtual environment management and pip installations in favor of uv's unified toolchain, significantly improving developer experience and CI/CD reliability.

Key improvements include comprehensive updates to all CI/CD workflows using uv's native caching and frozen lock file support, complete migration of local development scripts (setup.sh, release.sh) to use uv commands, and thorough documentation updates across all developer-facing guides. The migration maintains full backward compatibility while providing faster dependency resolution, better reproducibility through uv.lock, and simplified developer workflows.

Developers can now set up the project with a single command using uv, and all CI/CD pipelines benefit from faster builds and more reliable dependency management. The zero-dependency promise of ascii-guard remains intact, with verification tests confirming the package works standalone without external runtime dependencies.

---

### ✨ Added

- chore: add AI release summary for uv migration release ([d129004](https://github.com/fxstein/ascii-guard/commit/d1290044c85d7a37691c1c0c72d03ab2722be409))
- chore: add AI release summary for uv migration test ([5b977bf](https://github.com/fxstein/ascii-guard/commit/5b977bf8a030904ddfa45af962dd86e7d7ba7a2c))
- docs: Add test-setup.sh script and documentation (task#79.4) ([4e731be](https://github.com/fxstein/ascii-guard/commit/4e731bea6ffdd8368985d7c2c1ed91d35c05f91f))
- feat: Complete Phase 4 - Update scripts and documentation to use uv (task#79.4) ([74c660e](https://github.com/fxstein/ascii-guard/commit/74c660e4d1319108e6fefd23ee3a6aea0bc40497))
- feat: Complete Phase 2 - Local Development with uv (task#79) ([f1a19ab](https://github.com/fxstein/ascii-guard/commit/f1a19ab63225f59c67fa130cdb3ee860c62b6832))
- docs: Add UV migration analysis, design, and gap analysis documents (task#79) ([d480752](https://github.com/fxstein/ascii-guard/commit/d480752bb3f95718425f2ae884c3ca10c6add11d))

### 🔄 Changed

- chore: Update TODO.md and commit pending changes for release test ([a19a387](https://github.com/fxstein/ascii-guard/commit/a19a3871755c331b46e7d046d15d2926441d064b))
- refactor: Replace ALL venv activations with uv run (task#79.3) ([7cdd9e2](https://github.com/fxstein/ascii-guard/commit/7cdd9e2ca86bb8aa04cba5f2c0e28a2367350aa6))
- docs: Update TODO.md - defer task#79.3.7 SHA pinning (task#79) ([2838459](https://github.com/fxstein/ascii-guard/commit/28384590b12f4788b0ddb5a4b9f4051905e3f6ca))
- docs: Update UV gap analysis status (task#79) ([f907fb3](https://github.com/fxstein/ascii-guard/commit/f907fb31ed62c8be7b7033b99d7e197e15d4d6ff))
- chore: Update release log for 2.1.0 ([5ff8ea6](https://github.com/fxstein/ascii-guard/commit/5ff8ea6ea91a2e60ad181dd7610db636ba863410))

### 🐛 Fixed

- fix: Keep set -e disabled for entire verification section (test-setup.sh) ([93a607a](https://github.com/fxstein/ascii-guard/commit/93a607a3751aed14b64e5d57e292f2325c179843))
- fix: Allow verification to run even if setup.sh fails (test-setup.sh) ([de73164](https://github.com/fxstein/ascii-guard/commit/de7316470bb7377a52651c024a7ddac4ad74c3cc))
- fix: Suppress coverage module-not-measured warning (task#79.3) ([cda0d9b](https://github.com/fxstein/ascii-guard/commit/cda0d9bc4ef53310d5dcfcf300c3f313726c1ce0))
- fix: Use uv run instead of manual venv activation (task#79.3) ([4a681ba](https://github.com/fxstein/ascii-guard/commit/4a681babdb8ee8b7bea8c715da5740322db6a103))
- fix: Configure mypy to ignore missing tomli imports ([885b570](https://github.com/fxstein/ascii-guard/commit/885b570b7bda2b58f0aa7d7f449e5ef6a425e02d))
- chore: Clean up TODO.md - remove duplicate notes and fix references (task#79) ([3b85abf](https://github.com/fxstein/ascii-guard/commit/3b85abff48810736b2111ad469a87d14917606d5))

*Documentation, maintenance, and other commits: 6*

*Total commits: 23*
