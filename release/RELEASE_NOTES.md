# ascii-guard v1.6.0

This release improves both user-facing documentation and the internal release workflow. Documentation has been updated to reflect the project's stable status, removing outdated alpha version references and correcting PyPI availability information. All pre-commit hook examples have been updated from v0.1.0 to v1.5.1, ensuring users reference the latest stable release with all bug fixes.

A new troubleshooting section addresses common user confusion about ignore marker syntax, clarifying that the correct marker is `<!-- ascii-guard-ignore -->` rather than the commonly mistaken `<!-- ascii-guard-ignore-start -->`. The FAQ has been updated to accurately document that file exclusion patterns are fully implemented via configuration files, correcting previous documentation that suggested this feature was still in development.

The release workflow itself has been significantly improved to eliminate recurring errors encountered during the release process. The AI release summary is now committed to version history before running the prepare script, maintaining diff capability across releases. Version files are automatically cleaned up from failed prepare attempts, and the freshness timeout has been increased from 30 to 60 seconds, creating a more reliable and maintainable release process.

---

### ✨ Added

- chore: add AI release summary ([f6b3256](https://github.com/fxstein/ascii-guard/commit/f6b325633a22e26ffe9edd33cf68054fc4424976))
- chore: add AI release summary ([a6c1f8c](https://github.com/fxstein/ascii-guard/commit/a6c1f8c57fb2a3c6ba01ce0016af0828a480937b))
- feat: improve release workflow - commit AI summary before prepare ([c565539](https://github.com/fxstein/ascii-guard/commit/c5655390dc7676ef0d5cc56970c181d70c5f4a6a))
- chore: prepare v1.5.2 release - add AI summary ([c8850f7](https://github.com/fxstein/ascii-guard/commit/c8850f7e694062a94c3aadc89daf30fcc2d9508b))
- docs: add troubleshooting section for ignore markers (task#59) ([3cab3e4](https://github.com/fxstein/ascii-guard/commit/3cab3e4ebaaf0102f3ad9e97412f9826c5c36b85))

### 🔄 Changed

- docs: update stale version info and development status ([d5dc6d7](https://github.com/fxstein/ascii-guard/commit/d5dc6d71c20090e412447b28f4aa9d0e221fa018))
- chore: Update release log for 1.5.1 ([77ef928](https://github.com/fxstein/ascii-guard/commit/77ef9283e2b927f9b189a5aa72f7e132e89abb1b))

### 🐛 Fixed

- fix: auto-cleanup version files from failed prepare attempts ([fee66fc](https://github.com/fxstein/ascii-guard/commit/fee66fc0d8535603c7ea96d1fba13266cf792742))
- fix: remove version number from AI summary commit message ([f639df9](https://github.com/fxstein/ascii-guard/commit/f639df99cdcc8849a4f33780064ff7ff34667f57))

*Documentation, maintenance, and other commits: 1*

*Total commits: 10*
