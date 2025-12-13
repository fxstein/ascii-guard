# UV Migration - Implementation Gap Analysis

**Date:** 2025-12-13
**Purpose:** Audit findings comparing the current implementation against the `UV_DESIGN.md` specification and best practices.

---

## 1. Documentation Gaps (High Priority)
The functional migration is complete, but documentation still references legacy tools, potentially confusing developers.

### 1.1 Developer Guide Updates
- **Gap:** `docs/DEVELOPMENT.md` and `docs/CI_CD.md` still reference `source .venv/bin/activate` and `pip install -e .`.
- **Recommendation:** Update all developer-facing instructions to use `uv sync` and `uv run`.
- **Status:** ⚠️ Needs Update

### 1.2 Usage Guide Mixed References
- **Gap:** `docs/USAGE.md` contains mixed references like `pip install -e .` (should be `uv sync` for devs) and `pip install pre-commit`.
- **Recommendation:** Clearly separate "User Installation" (pip) from "Developer Setup" (uv).
- **Status:** ⚠️ Needs Update

---

## 2. Workflow Standardization Gaps

### 2.1 Sync vs. Pip Install
- **Gap:** Multiple workflows (e.g., `ci.yml`, `release.yml`) use `uv pip install -e ".[dev]"` instead of the designed `uv sync --frozen`.
- **Risk:** `uv pip install` does not strictly enforce the `uv.lock` file in the same way `uv sync --frozen` does, potentially leading to less reproducible builds in CI.
- **Recommendation:** Standardize all CI steps to use `uv sync --frozen --dev` to strictly enforce the lockfile.
- **Status:** ⚠️ Diverges from Design

---

## 3. Legacy Artifacts

### 3.1 Legacy Config Files
- **Observation:** `.todo.ai/.todo.ai.log` and `TODO.md` contain historical references to "pip install".
- **Decision:** Keep for historical accuracy (audit trail). No action needed.

### 3.2 Cursor Rules
- **Gap:** `.cursor/rules/ascii-guard-releases.mdc` forbids `python3 -m venv` but doesn't explicitly mandate `uv sync`.
- **Recommendation:** Update rules to explicitly prefer `uv` patterns.
- **Status:** ℹ️ Minor Polish

---

## 4. Action Plan

1.  [ ] **Refactor CI Workflows:** Replace `uv pip install -e ...` with `uv sync --frozen --dev` in all GitHub Actions.
2.  [ ] **Update Documentation:** Rewrite `docs/DEVELOPMENT.md`, `docs/USAGE.md`, and `docs/CI_CD.md` to reflect the new `uv` workflow.
3.  [ ] **Update Cursor Rules:** Refresh `.cursor/rules` to align with the new tooling.
