# ascii-guard Configuration Design

## Design Decisions

### 1. Config File Format: TOML

**Rationale**: Structured, extensible format for future rule configuration.

**Python Version Handling**:
- **Python 3.11+**: Use built-in `tomllib` (stdlib, read-only)
- **Python 3.10**: Use `tomli` package (external dependency, read-only)

This is a strategic exception to the "zero dependencies" principle:
- Python 3.10 requires ONE small dependency: `tomli`
- Python 3.11+ has ZERO dependencies (uses stdlib `tomllib`)
- `tomli` is the reference implementation that became stdlib
- Read-only is sufficient (we don't generate config files)

**Implementation**:
```python
import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib
```

### 2. Directory Scanning: Included in Task #17

**Scope**: Task #17 will include both config parsing AND directory scanning.

**Behavior**:
- CLI with **explicit file paths**: Process those files (bypass config filters)
- CLI with **directory path**: Recursively scan, apply config filters
- No directory arg: Current behavior (process explicit files only)

### 3. Config Location: Project-Only

**Location**: `.ascii-guard` in project root

**Discovery**:
1. Start from current directory
2. Walk up to find `.ascii-guard`
3. Stop at git root or filesystem root
4. CLI flag `--config <path>` overrides

**No user-level config** in Phase 1 (can add later if needed).

### 4. File Type Filtering: Configurable

**Default behavior** (no config):
- Scan all text files (encoding detection)
- Skip binary files automatically

**Config control**:
```toml
[files]
# File extensions to scan (if specified, only these are scanned)
extensions = [".md", ".txt", ".rst"]

# Exclude patterns (gitignore-style)
exclude = [
    "node_modules/",
    ".git/",
    "**/__pycache__/**",
    "*.tmp",
    "build/"
]

# Include patterns (override excludes)
include = [
    "!important.md"
]
```

---

## ✅ Design Decisions (Finalized)

### Q1: Zero-Dependency Messaging ✓

**Decision**: "Zero dependencies (Python 3.11+), one tiny dependency for Python 3.10 (`tomli`)"

Update README and docs to reflect this transparent messaging.

### Q2: Config File Name ✓

**Decision**: Support both `.ascii-guard.toml` and `.ascii-guard`

**Discovery order**:
1. Try `.ascii-guard.toml` (preferred)
2. Fallback to `.ascii-guard`

**Documentation**: Prefer `.ascii-guard.toml` in all examples and docs.

### Q3: Empty `extensions = []` Behavior ✓

**Decision**: Empty list means scan **all text files**

Auto-detect text files using encoding detection. Users can restrict by specifying extensions.

### Q4: Default Exclusions ✓

**Decision**: Built-in smart defaults when no config exists

```python
DEFAULT_EXCLUDES = [
    ".git/",
    "node_modules/",
    "__pycache__/",
    ".venv/",
    "venv/",
    ".tox/",
    "build/",
    "dist/",
    ".mypy_cache/",
    ".pytest_cache/",
    ".ruff_cache/",
    "*.egg-info/"
]
```

User config overrides these defaults completely.

### Q5: Pattern Matching Subset ✓

**Decision**: Support only stdlib-friendly patterns

**Supported**:
- `*.ext` - Glob patterns
- `dir/` - Directory matching
- `**/pattern/**` - Recursive matching
- `!pattern` - Negation (include override)
- `#` - Comments (line must start with `#`)

**Not supported**:
- `[a-z]` - Character ranges
- `\` - Escaping
- `*.{md,txt}` - Brace expansion

Document limitations clearly with examples.

### Q6: Config Validation ✓

**Decision**: Warn on unknown keys, error on bad values

- Unknown sections/keys: Print warning, continue
- Invalid values (wrong type): Error and exit
- Missing optional keys: Use defaults

### Q7: Dependency Declaration ✓

**Decision**: Conditional dependency (automatic)

```toml
dependencies = [
    "tomli>=2.0.0; python_version < '3.11'"
]
```

Most user-friendly - pip installs automatically only when needed.

---

## Final TOML Structure

```toml
# .ascii-guard.toml
# Configuration for ascii-guard linter

[files]
# File extensions to scan (empty = all text files)
extensions = []

# Exclude patterns (gitignore-style)
# Default excludes: .git/, node_modules/, __pycache__/, .venv/, venv/,
#                   .tox/, build/, dist/, .mypy_cache/, .pytest_cache/,
#                   .ruff_cache/, *.egg-info/
exclude = []

# Include patterns (negation - override excludes)
include = []

# Follow symbolic links when scanning directories
follow_symlinks = false

# Maximum file size to scan in MB (0 = unlimited)
max_file_size = 10

[rules]
# Phase 2: Enable/disable specific validation rules
# check_alignment = true
# check_corners = true
# check_width = true

[output]
# Phase 2: Output customization
# color = "auto"  # auto, always, never
# verbose = false
```

---

## Implementation Plan

### Phase 1: Task #17 (Config + Scanning)

**Detailed Subtasks**:

#### #17.1: Add tomli dependency and version-aware import
- Update `pyproject.toml` with conditional `tomli` dependency
- Create import wrapper in `ascii_guard/config.py`:
  ```python
  import sys
  if sys.version_info >= (3, 11):
      import tomllib
  else:
      import tomli as tomllib
  ```
- Update README.md and DESIGN.md about dependency
- Test on both Python 3.10 and 3.11+

#### #17.2: Config parser module
- Create `ascii_guard/config.py`
- Implement `load_config()` - discover and parse config file
- Config discovery: `.ascii-guard.toml` → `.ascii-guard` → defaults
- Parse `[files]` section with validation
- Warn on unknown keys, error on bad values
- Return config dataclass with defaults

#### #17.3: Path matcher with pattern support
- Create `ascii_guard/patterns.py`
- Implement `match_path()` using `fnmatch` + `pathlib`
- Support: `*.ext`, `dir/`, `**/pattern/**`, `!negation`, `#` comments
- Handle negation (include overrides)
- Test pattern matching edge cases

#### #17.4: Directory scanner
- Create `ascii_guard/scanner.py`
- Implement `scan_directory()` - recursive file discovery
- Apply exclude/include patterns
- Auto-detect text files vs binary
- Respect `max_file_size` and `follow_symlinks`
- Use built-in default excludes when no config

#### #17.5: CLI integration
- Update `cli.py` to detect directory vs file args
- Directory args: trigger scanning with config filters
- File args: process directly (bypass filters)
- Add `--config <path>` flag to override discovery
- Add `--show-config` flag to print effective config

#### #17.6: Tests
- Test config parsing (valid, invalid, missing)
- Test pattern matching (all supported patterns)
- Test directory scanning (with/without config)
- Test CLI integration (files vs directories)
- Test Python 3.10 and 3.11+ compatibility

### Phase 2: Future Enhancement

- Rule enable/disable configuration
- Output format customization
- User-level config (`~/.config/ascii-guard/config.toml`)
- Additional pattern features (if needed)

---

## Next Steps

1. ✅ Design decisions finalized
2. ⏭️  Update task #17 in TODO.md with detailed subtasks
3. ⏭️  Update `pyproject.toml` with conditional `tomli` dependency
4. ⏭️  Update documentation (README, DESIGN.md)
5. ⏭️  Begin implementation

---

**Status**: Design complete - ready for implementation
