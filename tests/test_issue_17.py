# Copyright 2025 Oliver Ratzesberger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Regression tests for Issue #17 (nested boxes and junction artifacts)."""

import shutil
from pathlib import Path

import pytest

from ascii_guard.linter import fix_file, lint_file


class TestIssue17:
    """Test suite for Issue #17 regression verification."""

    @pytest.fixture
    def fixtures_dir(self) -> Path:
        """Return the path to test fixtures directory."""
        return Path(__file__).parent / "fixtures"

    def test_fix_issue_17_broken_fixture(self, fixtures_dir: Path, tmp_path: Path) -> None:
        """Verify that the broken fixture for Issue 17 can be fixed correctly.

        This test:
        1. Takes the intentionally broken fixture file (which must remain broken in repo)
        2. Copies it to a temp directory
        3. Runs the fixer on the copy
        4. Verifies the result is clean and has no artifacts
        """
        source_fixture = fixtures_dir / "issue_17_nested_boxes.md"
        assert source_fixture.exists(), "Fixture file missing"

        # 1. Verify source is indeed broken (sanity check)
        # This ensures we don't accidentally commit a fixed version
        lint_result_source = lint_file(str(source_fixture))
        assert lint_result_source.has_errors, "Source fixture should be broken but has no errors"

        # 2. Copy to temp for fixing
        test_file = tmp_path / "test_fix.md"
        shutil.copy(source_fixture, test_file)

        # 3. Run fix
        fix_result = fix_file(str(test_file))
        assert fix_result.boxes_fixed > 0
        assert fix_result.was_modified

        # 4. Verify fixed content
        # Check linting first
        lint_result_fixed = lint_file(str(test_file))
        assert not lint_result_fixed.has_errors, (
            f"Fixed file still has errors: {lint_result_fixed.errors}"
        )
        assert not lint_result_fixed.has_warnings, (
            f"Fixed file has warnings: {lint_result_fixed.warnings}"
        )

        # Check content explicitly for known artifacts
        content = test_file.read_text(encoding="utf-8")

        # Check for adjacent duplicate borders (original issue)
        assert "││" not in content

        # Check for space-separated duplicate borders (artifacts like "│ │")
        # We check specific known problem lines from the fixture
        lines = content.splitlines()

        # Line ~35: "│  │  - Execution tracking                           │ │  │" -> should be fixed
        for line in lines:
            if "Execution tracking" in line:
                assert "│ │" not in line.replace("│  │", "││")  # inner duplicates only
                assert line.strip().endswith("│  │")
            if "Version management" in line:
                assert "│ │" not in line.replace("│  │", "││")
                assert line.strip().endswith("│  │")

        # Check for unwanted bottom junctions (┴) where there are no columns
        # The inner boxes (File Operations, etc.) should have clean bottom borders
        # like "│  └───────────────────────────────────────────────────┘  │"
        # NOT "│  └───────────────────────────────────────────────────┴┘  │"
        assert "──┴┘" not in content
        assert "───┘" in content
