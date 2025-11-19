# Documentation

Complete documentation for ascii-guard.

## 📖 User Documentation

Essential guides for using ascii-guard:

### [USAGE.md](USAGE.md)
Complete user guide covering all features and options.
- Command-line usage (`lint`, `fix`, `show-config`)
- Configuration files (`.ascii-guard.toml`)
- Ignore markers for documentation examples
- Advanced usage patterns

### [FAQ.md](FAQ.md)
Frequently asked questions and troubleshooting.
- Installation and requirements
- Common issues and solutions
- Platform-specific notes
- Performance tips

---

## 👨‍💻 Developer Documentation

Guides for contributing to ascii-guard:

### [DEVELOPMENT.md](DEVELOPMENT.md)
**Start here for development!** Comprehensive guide for contributors.
- Prerequisites and quick setup (`./setup.sh`)
- Development workflow (branching, commits, PRs)
- Coding standards (zero dependencies, type hints, style)
- Testing guide (running tests, coverage, writing tests)
- Common tasks (features, bugs, docs)
- Project structure and architecture
- Troubleshooting

### [TESTING.md](TESTING.md)
Testing strategy and patterns.
- Test organization and structure
- Testing best practices
- Coverage requirements
- CI/CD integration

---

## 🏗️ Architecture & Design

Technical design documentation:

### [DESIGN.md](DESIGN.md)
Architecture and design decisions.
- System architecture overview
- Core components (scanner, detector, validator, fixer)
- Data flow and algorithms
- Design principles and rationale

### [CONFIG_DESIGN.md](CONFIG_DESIGN.md)
Configuration system design.
- Configuration file format (TOML)
- File discovery and precedence
- Configuration options and defaults
- Future extensibility

---

## 🚀 Release & Infrastructure

Documentation for maintainers:

### [RELEASE_DESIGN.md](RELEASE_DESIGN.md)
Release process and automation.
- Release workflow steps
- Version management (semantic versioning)
- Changelog generation
- PyPI publishing with Trusted Publishing

### [CI_CD.md](CI_CD.md)
Continuous integration and deployment.
- GitHub Actions workflows
- Automated testing
- Code quality checks
- Deployment pipeline

### [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md)
Branch protection and repository settings.
- Branch protection rules
- Required status checks
- Code review requirements
- Merge strategies

---

## 📂 Document Categories

### Quick Reference

| Document | Category | Audience | Purpose |
|----------|----------|----------|---------|
| [USAGE.md](USAGE.md) | User | All users | How to use ascii-guard |
| [FAQ.md](FAQ.md) | User | All users | Common questions |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Developer | Contributors | How to develop |
| [TESTING.md](TESTING.md) | Developer | Contributors | Testing guide |
| [DESIGN.md](DESIGN.md) | Architecture | Contributors | System design |
| [CONFIG_DESIGN.md](CONFIG_DESIGN.md) | Architecture | Contributors | Config system |
| [RELEASE_DESIGN.md](RELEASE_DESIGN.md) | Maintainer | Maintainers | Release process |
| [CI_CD.md](CI_CD.md) | Maintainer | Maintainers | CI/CD setup |
| [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md) | Maintainer | Maintainers | Repo settings |

---

## 🚀 Getting Started

**New users?** Start with [USAGE.md](USAGE.md) and [FAQ.md](FAQ.md)

**New contributors?** Start with [DEVELOPMENT.md](DEVELOPMENT.md)

**Want to understand the internals?** Read [DESIGN.md](DESIGN.md)

---

## 🔗 Other Resources

- [Main README](../README.md) - Project overview
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) - Community guidelines
- [LICENSE](../LICENSE) - Apache 2.0 License

---

## 📝 Documentation Standards

When updating documentation:
- Use clear, concise language
- Include code examples where helpful
- Keep table of contents updated for long docs
- Cross-link related documentation
- Test all code examples before committing
- No timestamps (Git tracks history)

---

**Questions?** [Open a discussion](https://github.com/fxstein/ascii-guard/discussions) or [issue](https://github.com/fxstein/ascii-guard/issues)
