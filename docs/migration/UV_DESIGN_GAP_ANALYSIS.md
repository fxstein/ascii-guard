# UV Migration - Design Gap Analysis

**Date:** 2025-12-13
**Status:** All gaps identified in this document have been addressed in the updated [UV_DESIGN.md](./UV_DESIGN.md).
**Purpose:** Supplement to `UV_DESIGN.md`, identifying critical gaps in security, reliability, and efficiency based on industry best practices.

---

## 1. Security Gaps (Critical)

The current design replicates the existing security posture but misses opportunities to harden the pipeline during the migration.

### 1.1 Action Pinning
- **Gap:** The design uses mutable tags (e.g., `uses: actions/checkout@v4`).
- **Risk:** Tags can be overwritten or hijacked, leading to supply chain attacks.
- **Recommendation:** Pin all Actions to full commit SHAs for immutable security.
  ```yaml
  uses: actions/checkout@b4ffde... # v4.1.1
  ```
- **Mitigation:** Configure **Dependabot** to manage these SHA updates automatically.

### 1.2 Workflow Permissions (Least Privilege)
- **Gap:** Workflows currently run with default permissions, which are often too permissive (Read/Write).
- **Risk:** Compromised steps could modify the repository.
- **Recommendation:** Define strict top-level permissions in every workflow file.
  ```yaml
  permissions:
    contents: read  # minimal default
  ```
- **Grant Write Access Explicitly:** Only add `contents: write` or `id-token: write` to specific jobs that require it (e.g., releases).

---

## 2. Reliability & Reproducibility Gaps

### 2.1 Lock File Strategy
- **Gap:** `UV_DESIGN.md` lists `uv.lock` as "optional."
- **Risk:** "It works on my machine" bugs. Without a lock file, `uv sync` resolves dependencies based on `pyproject.toml` ranges, meaning different developers (or CI runs) could get different transitive dependency versions.
- **Recommendation:** **Mandate and commit `uv.lock`**.
  - Ensures 100% deterministic builds across all environments.
  - CI should run `uv sync --frozen` to fail if the lock file is out of sync with `pyproject.toml`.

---

## 3. Efficiency Gaps

### 3.1 Caching Strategy
- **Gap:** The design proposes manually configuring `actions/cache` for `~/.cache/uv`.
- **Inefficiency:** This is verbose and prone to configuration errors (e.g., suboptimal cache keys).
- **Recommendation:** Leverage the native caching built into `astral-sh/setup-uv`.
  ```yaml
  - name: Install uv
    uses: astral-sh/setup-uv@v4
    with:
      enable-cache: true
      cache-dependency-glob: "uv.lock"
  ```
  - This automatically handles save/restore logic correctly.

---

## 4. Developer Experience Gaps

### 4.1 Python Version Pinning
- **Gap:** The design relies on the legacy `.python-version` file without enforcing usage.
- **Risk:** Inconsistent local environments. Some developers might accidentally use system Python.
- **Recommendation:** Use `uv python pin` to explicitly manage the project's Python version.
  - This ensures `uv run` always uses the exact interpreter version defined for the project, regardless of what is installed globally on the developer's machine.

---

## 5. Recommended Actions

1. **Update Migration Plan:** Incorporate these security and reliability improvements into the Phase 3 (CI/CD) and Phase 4 (Scripts) tasks.
2. **Add Todo Items:**
   - [ ] Configure `uv.lock` generation and commit to repo.
   - [ ] Update workflows to use SHA pinning.
   - [ ] Add `permissions: contents: read` to all workflows.
   - [ ] Switch to `enable-cache: true` in `setup-uv` steps.
