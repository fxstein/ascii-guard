# ASCII Art Linter Implementation Plan

**Status**: Planning
**Priority**: Medium
**Estimated Effort**: 2-3 days
**Owner**: Engineering Team

---

## Problem Statement

AI-generated ASCII flowcharts and diagrams in documentation often have formatting errors where box borders are misaligned by 1-2 characters. This breaks the visual integrity of diagrams and makes them harder to read.

**Example of the problem:**
```
┌─────────────────────┐
│ Box Content         │
└────────────────────┘   ← Missing one character, doesn't align
```

**Should be:**
```
┌─────────────────────┐
│ Box Content         │
└─────────────────────┘  ← Perfect alignment
```

---

## Solution: Custom Pre-Commit Hook

Build a Python-based linter that:
1. Validates ASCII art box-drawing characters
2. Checks alignment of borders
3. Auto-fixes broken borders
4. Runs as a pre-commit hook
5. Works on markdown files with ASCII art code blocks

---

## Phase 1: Research and Design

### Task 1.1: Research ASCII Box-Drawing Characters

**Unicode Box-Drawing Characters to Support:**

| Type | Characters | Description |
|------|------------|-------------|
| **Horizontal** | `─` (U+2500) | Horizontal line |
| **Vertical** | `│` (U+2502) | Vertical line |
| **Corners** | `┌` `┐` `└` `┘` | Top-left, top-right, bottom-left, bottom-right |
| **T-junctions** | `├` `┤` `┬` `┴` | Left, right, top, bottom |
| **Cross** | `┼` | Four-way intersection |
| **Heavy lines** | `━` `┃` `┏` `┓` `┗` `┛` | Bold variants |
| **Double lines** | `═` `║` `╔` `╗` `╚` `╝` | Double-line variants |

**Validation Rules:**
1. All vertical lines in a column must align
2. All horizontal lines in a row must connect properly
3. Corner characters must match the adjacent lines
4. Box widths must be consistent (top, middle, bottom)
5. Content must fit within box borders

### Task 1.2: Design Linter Architecture

**Architecture:**

```
┌─────────────────────────────────────────────────────────┐
│                  lint-ascii-art.py                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Parse markdown files                                 │
│     └─ Extract code blocks with ASCII art               │
│                                                          │
│  2. Detect ASCII diagrams                                │
│     └─ Look for box-drawing characters                  │
│                                                          │
│  3. Validate structure                                   │
│     ├─ Check vertical alignment                         │
│     ├─ Check horizontal alignment                       │
│     ├─ Validate corner characters                       │
│     └─ Check box width consistency                      │
│                                                          │
│  4. Report or fix issues                                 │
│     ├─ --lint: Report issues with line numbers          │
│     └─ --fix: Auto-repair alignment issues              │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Data Structures:**

```python
class Box:
    def __init__(self):
        self.top_line: int = None      # Line number of top border
        self.bottom_line: int = None   # Line number of bottom border
        self.left_col: int = None      # Column of left border
        self.right_col: int = None     # Column of right border
        self.lines: List[str] = []     # All lines of the box

class ValidationError:
    def __init__(self, line: int, col: int, message: str, fix: str = None):
        self.line = line
        self.col = col
        self.message = message
        self.fix = fix  # Suggested fix
```

---

## Phase 2: Implementation

### Task 2.1: Implement Core Linter Script

**File**: `scripts/lint-ascii-art.py`

**Command-line interface:**
```bash
# Lint mode - report issues
./scripts/lint-ascii-art.py --lint <file>
./scripts/lint-ascii-art.py --lint release/RELEASE.md

# Fix mode - auto-repair
./scripts/lint-ascii-art.py --fix <file>
./scripts/lint-ascii-art.py --fix release/RELEASE.md

# Check all markdown files
./scripts/lint-ascii-art.py --lint **/*.md

# Dry-run mode (show what would be fixed)
./scripts/lint-ascii-art.py --fix --dry-run <file>
```

**Core Functions:**

```python
def extract_ascii_blocks(markdown_file: str) -> List[Tuple[int, str]]:
    """Extract code blocks that contain ASCII art."""
    # Find ``` blocks with box-drawing characters
    pass

def detect_boxes(block: str) -> List[Box]:
    """Detect box structures in ASCII art."""
    # Find ┌┐└┘ patterns
    pass

def validate_box(box: Box) -> List[ValidationError]:
    """Validate a single box for alignment issues."""
    # Check vertical alignment of │ characters
    # Check horizontal alignment of ─ characters
    # Check corner character correctness
    # Check width consistency
    pass

def fix_box(box: Box, errors: List[ValidationError]) -> Box:
    """Auto-fix alignment issues in a box."""
    # Adjust character positions
    # Extend/shrink lines to match width
    pass

def report_errors(errors: List[ValidationError], file: str):
    """Pretty-print validation errors."""
    # Format: file.md:line:col: error message
    pass
```

**Exit Codes:**
- `0`: No issues found or all fixed
- `1`: Issues found (--lint mode)
- `2`: Invalid arguments
- `3`: File not found

### Task 2.2: Add Pre-Commit Hook Configuration

**File**: `templates/.pre-commit-config.yaml`

Add ASCII art linting hook:

```yaml
  - repo: local
    hooks:
      - id: ascii-art-linter
        name: ASCII Art Linter
        entry: scripts/lint-ascii-art.py --lint
        language: python
        types: [markdown]
        additional_dependencies:
          - markdown
        description: Validate ASCII art diagrams in markdown files
```

---

## Phase 3: Testing

### Task 3.1: Create Test Suite

**File**: `tests/unit/test_ascii_art_linter.py`

**Test cases:**

```python
def test_detect_single_box():
    """Test detection of a simple box."""
    pass

def test_detect_misaligned_vertical_border():
    """Test detection of misaligned │ character."""
    pass

def test_detect_misaligned_horizontal_border():
    """Test detection of misaligned ─ character."""
    pass

def test_detect_wrong_corner_character():
    """Test detection of incorrect corner character."""
    pass

def test_detect_inconsistent_width():
    """Test detection of boxes with inconsistent widths."""
    pass

def test_fix_vertical_misalignment():
    """Test auto-fixing vertical alignment."""
    pass

def test_fix_horizontal_misalignment():
    """Test auto-fixing horizontal alignment."""
    pass

def test_fix_preserves_content():
    """Test that fixing preserves box content."""
    pass

def test_multiple_boxes():
    """Test handling multiple boxes in one file."""
    pass

def test_nested_boxes():
    """Test handling nested box structures."""
    pass
```

### Task 3.2: Test on Existing Flowcharts

**Files to test:**
- `release/RELEASE.md` (contains large flowchart)
- Any other markdown files with ASCII art

**Process:**
1. Run `--lint` mode on existing files
2. Document any issues found
3. Run `--fix` mode
4. Verify fixes are correct
5. Commit fixed files if changes needed

### Task 3.3: Integration Testing

**Scenarios:**
1. Pre-commit hook triggers on markdown file with broken ASCII art
2. Pre-commit hook passes on markdown file with correct ASCII art
3. Fix mode corrects issues and allows commit
4. Multiple files with ASCII art in one commit

---

## Phase 4: Documentation

### Task 4.1: Create Cursor Rule

**File**: `.cursor/rules/ascii-guard.mdc`

**Content:**

```markdown
# ASCII Art Linter - AI Agent Guidance

When creating or editing ASCII flowcharts in markdown files:

## Rules for AI Agents

1. **Always use Unicode box-drawing characters**
   - Use `┌─┐` not `+--+`
   - Use `│` not `|`
   - Use `└─┘` not `+--+`

2. **Ensure alignment**
   - All vertical borders must align
   - All horizontal borders must have equal width
   - Corners must connect properly

3. **Before committing**
   - The ASCII art linter will run automatically
   - Fix any reported alignment issues
   - Use: `./scripts/lint-ascii-art.py --fix <file>`

4. **Common mistakes**
   - Missing characters in horizontal lines
   - Misaligned vertical borders
   - Inconsistent box widths
   - Wrong corner characters

## Commands

**Check for issues:**
```bash
./scripts/lint-ascii-art.py --lint release/RELEASE.md
```

**Auto-fix issues:**
```bash
./scripts/lint-ascii-art.py --fix release/RELEASE.md
```

**Preview fixes (dry-run):**
```bash
./scripts/lint-ascii-art.py --fix --dry-run release/RELEASE.md
```

## When to Use

- Creating new flowcharts in documentation
- Editing existing ASCII diagrams
- Before committing markdown files with ASCII art
- After AI generates a flowchart

## What Gets Validated

- Box border alignment (vertical and horizontal)
- Corner character correctness (┌┐└┘)
- Width consistency (top, middle, bottom borders match)
- Proper use of T-junctions (├┤┬┴)
- Cross intersections (┼)

## Examples

**Valid box:**
```
┌─────────────────────┐
│ Content here        │
└─────────────────────┘
```

**Invalid box (will be flagged):**
```
┌─────────────────────┐
│ Content here        │
└────────────────────┘   ← Too short!
```

## Pre-Commit Hook

The linter runs automatically on `git commit` for all `.md` files.
If issues are found, the commit will be blocked until fixed.
```

### Task 4.2: Update Repository README

Add section to `README.md`:

```markdown
### ASCII Art Linting

Documentation with ASCII flowcharts is automatically validated for alignment issues.

**Check diagrams:**
```bash
./scripts/lint-ascii-art.py --lint release/RELEASE.md
```

**Auto-fix issues:**
```bash
./scripts/lint-ascii-art.py --fix release/RELEASE.md
```

The linter runs automatically on commit for all markdown files.
```

---

## Implementation Checklist

### Phase 1: Research and Design ✅
- [ ] **Task 1.1**: Research ASCII box-drawing characters
- [ ] **Task 1.2**: Design linter architecture

### Phase 2: Implementation
- [ ] **Task 2.1**: Implement `scripts/lint-ascii-art.py`
  - [ ] Parse markdown files
  - [ ] Extract ASCII code blocks
  - [ ] Detect box structures
  - [ ] Validate alignment
  - [ ] Implement `--lint` mode
  - [ ] Implement `--fix` mode
  - [ ] Implement `--dry-run` mode
  - [ ] Add exit codes
  - [ ] Add color output for errors
- [ ] **Task 2.2**: Add to `templates/.pre-commit-config.yaml`
- [ ] **Task 2.3**: Add to `.pre-commit-config.yaml` (root)

### Phase 3: Testing
- [ ] **Task 3.1**: Create test suite
  - [ ] Write 10+ unit tests
  - [ ] Test detection logic
  - [ ] Test fixing logic
  - [ ] Test edge cases
- [ ] **Task 3.2**: Test on existing flowcharts
  - [ ] Run on `release/RELEASE.md`
  - [ ] Fix any issues found
  - [ ] Verify fixes are correct
- [ ] **Task 3.3**: Integration testing
  - [ ] Test pre-commit hook
  - [ ] Test with multiple files
  - [ ] Test fix workflow

### Phase 4: Documentation
- [ ] **Task 4.1**: Create `.cursor/rules/asciss-guard.mdc`
- [ ] **Task 4.2**: Update `README.md`


---

## Success Criteria

1. ✅ Linter correctly detects misaligned ASCII art
2. ✅ Linter can auto-fix alignment issues
3. ✅ Pre-commit hook blocks commits with broken ASCII art
4. ✅ `--lint` mode provides clear error messages
5. ✅ `--fix` mode preserves content while fixing alignment
8. ✅ Documented for AI agents and humans

---

## Future Enhancements

**Not in scope for initial release, but could be added later:**

1. **Support for different box styles**
   - Heavy lines (`━┃┏┓┗┛`)
   - Double lines (`═║╔╗╚╝`)
   - Rounded corners (`╭╮╰╯`)

2. **Detect and fix other issues**
   - Arrows (`→ ← ↑ ↓`)
   - Flowchart shapes (diamonds, circles)
   - Line intersections beyond simple boxes

3. **Generate ASCII art from descriptions**
   - AI-powered flowchart generation
   - Convert mermaid diagrams to ASCII
   - Template-based box generation

4. **Performance optimizations**
   - Cache validation results
   - Parallel processing for multiple files
   - Incremental validation (only changed blocks)

5. **IDE integration**
   - VS Code extension
   - Real-time validation
   - Quick-fix suggestions

---

## Dependencies

**Python Packages:**
- `markdown` - Parse markdown files
- `click` or `argparse` - Command-line interface
- `colorama` - Colored terminal output

**System Requirements:**
- Python 3.8+ # Lets make sure we validate this
- UTF-8 terminal support for box-drawing characters

**No external linters needed** - this is a custom solution specific to our needs.

---

## Notes

- This is a **custom solution** because no existing linter handles ASCII art validation
- Focus on **common cases** (boxes, simple flowcharts) initially
- **Idempotent** - running `--fix` multiple times should be safe
- **Non-destructive** - content must always be preserved
- **Fast** - must run in < 2 seconds for typical documentation files

---

**Document Version**: 1.0
**Created**: 2025-11-16
**Status**: Planning Phase
