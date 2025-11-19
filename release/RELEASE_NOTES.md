# ascii-guard v1.5.0

This release introduces selective linting control through ignore markers, giving users fine-grained control over which ASCII art boxes should be excluded from validation. Users can now wrap specific boxes with `<!-- ascii-guard-ignore-start -->` and `<!-- ascii-guard-ignore-end -->` markers to preserve intentionally unconventional formatting while maintaining strict validation for the rest of their documentation. This feature is particularly valuable for documentation that includes examples of broken boxes or stylistic variations.

The project documentation has been significantly reorganized to improve accessibility for both end users and contributors. The main README now focuses exclusively on quick start and usage information, while all development setup, testing procedures, and contribution guidelines have been consolidated into a dedicated DEVELOPMENT.md guide. Additional README files have been added to the docs/, release/, and tests/ directories to improve navigation and context.

Developer experience has been streamlined with a comprehensive one-step setup script that handles Python environment configuration, dependency installation, and pre-commit hook setup automatically. The setup process has been standardized on bash for maximum cross-platform compatibility, replacing the previous zsh-specific scripts to ensure consistent behavior across Linux, macOS, and Windows WSL environments.

---

### ✨ Added

- docs: add README.md to release/ and tests/ directories ([ac0d813](https://github.com/fxstein/ascii-guard/commit/ac0d813a8188e5c0ed876c101192fb6b79c31ccc))
- docs: add README.md to docs/ directory for navigation ([80464c4](https://github.com/fxstein/ascii-guard/commit/80464c445f7160075bcb10516286a5231d62c5e0))
- docs: create dedicated DEVELOPMENT.md and simplify README ([5206c46](https://github.com/fxstein/ascii-guard/commit/5206c46d34dbd3a347e53ffbe3b9e79a276f0136))
- feat: add comprehensive one-step setup script for developers ([baee263](https://github.com/fxstein/ascii-guard/commit/baee263dd051a82259048eed67515c029be2d97c))
- feat: add ignore markers for ASCII boxes (task#55) ([eb97ebc](https://github.com/fxstein/ascii-guard/commit/eb97ebcf0ba342389c064200b95af11c4cee2f1d))
- chore: add task list for ignore markers feature (task#55) ([c047784](https://github.com/fxstein/ascii-guard/commit/c0477842412e208d601420e01ff6b5ea8a39e9e8))
- feat: add AI release summary validation to enforce cursor rules ([9f6f85b](https://github.com/fxstein/ascii-guard/commit/9f6f85be00a6677f9b2c4964929bf9074d135c57))

### 🔄 Changed

- refactor: remove setup-venv.sh and standardize on setup.sh ([ddf5fff](https://github.com/fxstein/ascii-guard/commit/ddf5fffd3e6b4d044ac657a5bef646394b50a4d0))
- refactor: standardize on bash for cross-platform setup scripts ([0cf5a6f](https://github.com/fxstein/ascii-guard/commit/0cf5a6f407eb084f32e8acdcb7603d3d39e5565f))
- chore: Update release log for 1.4.0 ([d57e094](https://github.com/fxstein/ascii-guard/commit/d57e094c8668b0cb82a6f02ca25446349ff4d8ff))

*Documentation, maintenance, and other commits: 3*

*Total commits: 13*
