## Release 0.2.0

This is a test release to validate the dry-run functionality of the release process. The improvements include better error handling, process invalidation detection, and a simulation mode that allows testing the entire release workflow without actually pushing to GitHub or PyPI.

Key enhancements focus on reliability and safety, ensuring that the release process can be thoroughly tested before executing a real release. The dry-run mode provides visibility into exactly what operations would be performed.

This test validates that all release steps can be simulated successfully, building confidence in the release automation before using it for actual package distribution.

---

### ✨ Added

- fix: Force-add ignored release files for audit trail ([c29e26f](https://github.com/fxstein/ascii-guard/commit/c29e26f6edb1cf2454764d1c9a83edf9b15f1c32))
- chore: Complete task#16 (release process implementation) ([37c3102](https://github.com/fxstein/ascii-guard/commit/37c3102a0fd347520eb8841c13be415a2f36bbfe))
- feat: Implement automated release process (task#16) ([745fe73](https://github.com/fxstein/ascii-guard/commit/745fe731b2749588a2a7a04df7446a31b0080b66))
- docs: Add release process design document (task#16) ([c3dc194](https://github.com/fxstein/ascii-guard/commit/c3dc1945e6475e2d1a1cb066962d8a9c5ca83364))
- Add comprehensive user documentation ([0cf9cff](https://github.com/fxstein/ascii-guard/commit/0cf9cfff2c8704fc9eff6f84a92494eedd3f96be))
- Add CONTRIBUTING.md and CODE_OF_CONDUCT.md ([5f07ff7](https://github.com/fxstein/ascii-guard/commit/5f07ff7a4f6d06d6e3b3401b3b1f1151919accc9))
- Complete rewrite of DESIGN.md to reflect actual implementation ([08d43f5](https://github.com/fxstein/ascii-guard/commit/08d43f5acd9c9a704e57014d45de9feecaf731ae))
- Fix additional GitHub Actions workflow issues ([73449e8](https://github.com/fxstein/ascii-guard/commit/73449e865885e28c0b410ee8981a915446b55a4f))
- Implement comprehensive CI/CD workflows (task#7) ([60af282](https://github.com/fxstein/ascii-guard/commit/60af28265a92fb6c54c9a1253ab8b5bbd1ac947a))
- Complete task#6: Add comprehensive test suite ([5e410b5](https://github.com/fxstein/ascii-guard/commit/5e410b5a5f4ab60f0adef0f0b1b52047a9f9a176))
- Implement comprehensive test suite (task#6) ([d253fdc](https://github.com/fxstein/ascii-guard/commit/d253fdc52be8133933801dbd6eec1a096a50db69))
- Add task#17: Implement .ascii-guard config file with exclusion patterns ([a187d8e](https://github.com/fxstein/ascii-guard/commit/a187d8e017ce73ef0b737ff116df846d43422d11))
- feat: Implement core linter and CLI functionality (task#4, task#5) ([77eab82](https://github.com/fxstein/ascii-guard/commit/77eab822bc44e4fe1e63e46e5edec54f1a1817fc))
- docs: Add comprehensive README with zero-dependency focus (task#10) ([75498c4](https://github.com/fxstein/ascii-guard/commit/75498c4500a92248cd015721939a643785295d9c))

### 🔄 Changed

- fix: Improve release process reliability ([f637eb9](https://github.com/fxstein/ascii-guard/commit/f637eb9b9b09b4573c2541159bcb0d0ef808d398))
- Update pre-commit hooks and fix code formatting ([c25e7d3](https://github.com/fxstein/ascii-guard/commit/c25e7d3cc2c64c71a95b800d29c01e830e5458f8))

### 🐛 Fixed

- fix: Properly mark task#16 subtasks as complete using todo.ai ([0e68186](https://github.com/fxstein/ascii-guard/commit/0e68186ce00e985d50a74a943a157fbd3ef4786d))
- Fix license format in pyproject.toml for modern packaging ([045ecf0](https://github.com/fxstein/ascii-guard/commit/045ecf0099cf420329ccad6e3888d03ab7187ea0))
- Fix PR checks workflow and code formatting issues ([cbc1dbe](https://github.com/fxstein/ascii-guard/commit/cbc1dbed61b0c7420283af2fd0c9715eebf065a4))
- Fix Dependabot configuration ([c005d0a](https://github.com/fxstein/ascii-guard/commit/c005d0a4f163332ac79a3005e0d2d404b2a1a2b9))
- Fix GitHub Actions workflows ([6d20e04](https://github.com/fxstein/ascii-guard/commit/6d20e04eb63ad99b230e854ca1164ef064db92d2))

*Documentation, maintenance, and other commits: 9*

*Total commits: 30*
