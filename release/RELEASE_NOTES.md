# ascii-guard v2.0.1

This release focuses on critical stability improvements for complex ASCII art structures. We have resolved significant issues with nested boxes and non-standard border characters, ensuring that `ascii-guard` correctly handles diagrams with internal components, arrows, and junction points without triggering false positives or creating duplicate border artifacts.

Key improvements include a smarter border width validation algorithm that correctly accounts for visual width including arrows (e.g., `▼`) and junctions, as well as an enhanced fixer that can surgically repair inner boxes without damaging surrounding structures. These changes make the tool much more reliable for verifying sophisticated architectural diagrams and technical documentation.

---

### ✨ Added

- test: Add regression test for Issue #17 using broken fixture ([8ad8590](https://github.com/fxstein/ascii-guard/commit/8ad8590c54500cc4e4da79c185f415c96730ed37))

### 🔄 Changed

- fix: Improve fixer for border width mismatches and duplicate borders (task#78.1) ([9a213de](https://github.com/fxstein/ascii-guard/commit/9a213dec5749242e7c3686dade578ac5d8b69464))

### 🐛 Fixed

- fix: Resolve Issue #17 - persistent errors and artifacts in nested boxes (task#78) ([7ca2768](https://github.com/fxstein/ascii-guard/commit/7ca2768c0daf93b266daf5554d62ecb45196e598))

*Total commits: 9*
