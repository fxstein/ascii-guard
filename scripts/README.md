# Scripts Directory

Utility scripts for `ascii-guard` development and CI/CD.

## CI/CD Monitoring

### `wait-for-ci.sh`

Wait for all active CI/CD workflows to complete.

**Usage:**
```bash
./scripts/wait-for-ci.sh
```

**Returns:**
- `0` - All workflows completed successfully
- `1` - One or more workflows failed
- `4` - Timeout (10 minutes)

**Example:**
```bash
git push origin main
./scripts/wait-for-ci.sh
```

---

### `monitor-ci.sh`

Monitor a specific workflow by name.

**Usage:**
```bash
./scripts/monitor-ci.sh [workflow-name] [timeout-minutes]
```

**Parameters:**
- `workflow-name` - Name of workflow to monitor (default: "CI")
- `timeout-minutes` - Maximum time to wait (default: 10)

**Returns:**
- `0` - Workflow completed successfully
- `1` - Workflow failed
- `2` - Workflow was cancelled
- `3` - Workflow completed with other status
- `4` - Timeout

**Examples:**
```bash
# Monitor CI workflow (default)
./scripts/monitor-ci.sh

# Monitor Release workflow with 15 minute timeout
./scripts/monitor-ci.sh Release 15

# Monitor specific workflow
./scripts/monitor-ci.sh "PR Checks" 5
```

---

## Python Environment

### `check-python-env.sh`

Validates the Python environment setup (see task #30).

**Usage:**
```bash
./scripts/check-python-env.sh
```

Checks:
- `.venv` exists and has `ascii-guard`
- pyenv global is pristine (only `pip`)
- `PIP_REQUIRE_VIRTUALENV` protection is active

---

## Usage in Cursor Rules

These scripts can be referenced in `.cursor/rules/` for AI agents:

```bash
# Wait for CI before proceeding
./scripts/wait-for-ci.sh || exit 1

# Monitor specific workflow
./scripts/monitor-ci.sh Release 15
```

Clean output, reliable completion detection, no stuck loops.
