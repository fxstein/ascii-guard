# ascii-guard v1.3.0

This release resolves the critical "fixer plateau" bug reported in Issue #10, where `ascii-guard fix` would stop making progress and leave persistent errors that could never be auto-fixed. The fix involved comprehensive enhancements across the detector, validator, and fixer modules to properly support advanced ASCII art structures commonly found in documentation.

The core problem was that ascii-guard didn't recognize several valid ASCII art patterns used in tables, flowcharts, and complex diagrams. This caused the validator to flag correct structures as errors, and the fixer would either fail to correct them or introduce new errors, creating a frustrating loop for users.

**Key Improvements:**

**Table Support:** Added full support for table column separators (`├─┬─┼─┤`) which are commonly used to divide table columns. The validator now recognizes these as valid structural elements rather than border misalignments. The fixer can also correct malformed table separators by removing extra characters and adding missing corners.

**Flowchart Junction Points:** Implemented proper handling of junction points (`┴`, `┬`) in flowchart borders. These characters connect boxes to flow lines above or below them. The validator now correctly counts junction points as part of the border width, fixing width mismatch errors that previously couldn't be resolved.

**Multi-Box Detection:** Enhanced the detector to find multiple boxes on the same line, enabling proper validation of side-by-side boxes in flowcharts. Previously, only the first box would be detected, and the second box would be flagged as "extra characters." The detector now uses `find_all_top_left_corners()` to discover all box starts on each line.

**Code Fence Handling:** Added markdown code fence detection to skip ASCII art examples within code blocks. This eliminates false positives when documentation includes ASCII art examples in markdown code fences.

**Malformed Line Fixing:** Improved the fixer's logic for handling lines with extra characters after table separators or missing bottom corners. The fixer now correctly truncates extra content and adds missing corners, ensuring tables can be automatically corrected.

**Testing & Validation:** Added 13 comprehensive test cases covering all new functionality. Created detailed validation report (`ISSUE_10_VALIDATION.md`) documenting that all 4 reported bug patterns are fixed. All 182 tests pass with 87% code coverage maintained.

This release transforms ascii-guard from a tool that could get stuck on complex ASCII art into one that handles real-world documentation patterns reliably. Users will no longer experience the frustrating plateau behavior where fixes never complete successfully.

---

### ✨ Added

- feat: Complete detector false positive fixes (task#34) ([3ad5b5c](https://github.com/fxstein/ascii-guard/commit/3ad5b5cf5ba31a240419134c48917d22b8999db6))
- feat: Add markdown code fence detection and multi-box line support (task#34.3, task#34.4, task#34.5) ([92c5a95](https://github.com/fxstein/ascii-guard/commit/92c5a95ed77407809332c298f9830f503d59961d))
- feat: Complete fixer plateau bug fix (Issue #10, task#35) ([08e1e76](https://github.com/fxstein/ascii-guard/commit/08e1e76627ba2e296e75d1a47990d1959903e859))
- test: Add comprehensive test cases for table separators and junction points (task#35.7) ([cb4a904](https://github.com/fxstein/ascii-guard/commit/cb4a904546829608f76860ecd9a3fe962b714f5f))
- feat: Improve fixer to handle malformed table separators and missing bottom corners (task#35.5) ([6b77c8d](https://github.com/fxstein/ascii-guard/commit/6b77c8ddcde85203a44fb27e87a7094928c421cd))
- feat: Add support for table column separators and junction points (task#35.3, task#35.4) ([6bbfcdf](https://github.com/fxstein/ascii-guard/commit/6bbfcdf993aeccf36de31197404ebcaa3e953034))
- feat: Add task list for fixing fixer plateau bug (Issue #10) ([56ccf64](https://github.com/fxstein/ascii-guard/commit/56ccf644090b65a498fe309784580c1f1f335466))
- docs: Add branch protection configuration guide ([7bce2c7](https://github.com/fxstein/ascii-guard/commit/7bce2c79da6acab3505b165bfaa38c08699f9742))
- fix: Add mandatory STOP after prepare in release process ([5d2d3ce](https://github.com/fxstein/ascii-guard/commit/5d2d3ce5c817300b8976c1774a4067c98d944d77))

### 🔄 Changed

- fix: Improve dependency check extraction logic ([6a2a192](https://github.com/fxstein/ascii-guard/commit/6a2a192676df231cd17a0b0ed628637ff41d62a8))
- fix: Update dependency check to allow conditional tomli dependency ([ae4152d](https://github.com/fxstein/ascii-guard/commit/ae4152dfe6e5ee9a015ff60d9b50890f5ee9efd5))

### 🐛 Fixed

- chore: Mark Issue #10 fix complete (task#35) - all 4 bug patterns resolved ([b06dd79](https://github.com/fxstein/ascii-guard/commit/b06dd79c6633fc3abfaaf9017b977c5e00182c12))
- fix: Support multiple boxes on same line in validator (completes Issue #10) ([2253403](https://github.com/fxstein/ascii-guard/commit/225340324560ff326b1d28cde24db3205afae146))
- fix: Configure auto-merge to ignore itself when waiting for checks ([c9c6987](https://github.com/fxstein/ascii-guard/commit/c9c6987df8843a1cd5ae1decdcf9f8c8ea7d1c30))
- fix: Remove check-regexp filter to wait for all CI checks ([7aae1ec](https://github.com/fxstein/ascii-guard/commit/7aae1ecf497b89261d82f3fad7218a8215579566))

*Documentation, maintenance, and other commits: 2*

*Total commits: 17*
