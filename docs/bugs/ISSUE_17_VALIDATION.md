# Issue #17 Validation Report

## Summary

Issue #17 reports that `ascii-guard fix` command does not fix all detected errors. After investigation, we found 2 distinct bug patterns that need to be addressed.

## Test Results

### Issue 1: Extra Characters in Nested Box Content Lines
**Status:** ✅ **FIXED**

**Problem:** Content lines inside nested boxes have extra `││` characters that should be removed
- Example: `│  │  - Task CRUD operations                          ││ │`
- Expected: `│  │  - Task CRUD operations                           │  │`
- Error: "Right border missing: line too short"

**Fix Implementation:**
- Updated `linter.py` to detect and fix duplicate borders (`││`) even when they occur just outside the detected box boundary.
- Updated `linter.py` merge logic to allow overwriting characters immediately outside the box (padding area) if they are not owned by another box.
- Updated `fixer.py` to be non-destructive to content trailing the box (preventing deletion of outer box borders).

**Verification:**
The test fixture `tests/fixtures/issue_17_nested_boxes.md` now fixes cleanly without errors or artifacts.

### Issue 2: Border Width Mismatch with Junction Characters
**Status:** ✅ **FIXED**

**Problem:** Boxes with junction characters in borders have width calculation issues
- Top border: `┌────▼────┐` (8 characters between corners: 4 dashes + ▼ + 3 dashes)
- Bottom border: `└┴────────┘` (9 characters between corners: ┴ + 8 dashes)
- Error: "Bottom border width (9) doesn't match top border width (8)"

**Fix Implementation:**
- Updated `validator.py` to correctly calculate effective border width (ignoring non-border characters like `▼`).
- Updated `validator.py` to strict column detection: only infer table columns from top junctions (`┬`) or middle separators (`┼`), NOT from vertical bars (`│`) in content lines. This prevents nested box borders from being misinterpreted as table columns, eliminating unwanted `┴` characters in bottom borders.

---

## Complete Test Run

```bash
$ ascii-guard lint tests/fixtures/issue_17_nested_boxes.md
# ... finds errors ...

$ ascii-guard fix tests/fixtures/issue_17_nested_boxes.md
✓ Fixed 9 box(es)

$ ascii-guard lint tests/fixtures/issue_17_nested_boxes.md
✓ No issues found
```

Visual inspection of the fixed file confirms:
1. No double borders (`││`).
2. No unwanted bottom junctions (`┴`) where there are no columns.
3. Outer box borders are preserved.
4. Spacing is correct.

## Conclusion

Issue #17 is **FULLY RESOLVED**. All identified sub-issues (border width, unwanted junctions, duplicate borders, destructive fixing) have been addressed with targeted fixes in `validator.py`, `linter.py`, and `fixer.py`.
