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

"""Integration tests for end-to-end workflows."""

import tempfile
from pathlib import Path

from ascii_guard.cli import cmd_fix, cmd_lint
from ascii_guard.config import load_config
from ascii_guard.scanner import scan_paths


class TestEndToEndWorkflow:
    """Test complete workflows from config to CLI."""

    def test_config_to_scanner_to_linter(self) -> None:
        """Test full workflow: config → scanner → linter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create config file
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
extensions = [".md"]
exclude = ["temp/"]
"""
            )

            # Create test files
            (tmppath / "good.md").write_text(
                """
┌─────────┐
│ Content │
└─────────┘
"""
            )

            (tmppath / "bad.txt").write_text("This should be excluded by extension filter")

            temp_dir = tmppath / "temp"
            temp_dir.mkdir()
            (temp_dir / "excluded.md").write_text("This should be excluded by pattern")

            # Load config
            config = load_config(config_file)
            assert config.extensions == [".md"]

            # Scan paths
            files = scan_paths([tmppath], config)

            # Should only find good.md
            assert len(files) == 1
            assert files[0].name == "good.md"

    def test_cli_with_config_file(self) -> None:
        """Test CLI with explicit config file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create config
            config_file = tmppath / "my-config.toml"
            config_file.write_text(
                """
[files]
exclude = ["*.tmp"]
"""
            )

            # Create files
            (tmppath / "keep.md").write_text(
                """
┌─────┐
│ Box │
└─────┘
"""
            )
            (tmppath / "exclude.tmp").write_text("temp file")

            # Mock args
            class Args:
                files = [str(tmppath)]
                quiet = True
                config = str(config_file)
                show_config = False

            exit_code = cmd_lint(Args())
            assert exit_code == 0  # Should succeed

    def test_cli_directory_scanning(self) -> None:
        """Test CLI scanning entire directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create directory structure
            (tmppath / "docs").mkdir()
            (tmppath / "docs" / "file1.md").write_text(
                """
┌────────┐
│ Test 1 │
└────────┘
"""
            )
            (tmppath / "docs" / "file2.md").write_text(
                """
┌────────┐
│ Test 2 │
└────────┘
"""
            )

            class Args:
                files = [str(tmppath / "docs")]
                quiet = True

            exit_code = cmd_lint(Args())
            assert exit_code == 0

    def test_cli_mixed_files_and_directories(self) -> None:
        """Test CLI with mixed file and directory inputs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create single file
            file1 = tmppath / "single.md"
            file1.write_text(
                """
┌─────┐
│ One │
└─────┘
"""
            )

            # Create directory with files
            dir1 = tmppath / "multiple"
            dir1.mkdir()
            (dir1 / "file1.md").write_text(
                """
┌─────┐
│ Two │
└─────┘
"""
            )
            (dir1 / "file2.md").write_text(
                """
┌───────┐
│ Three │
└───────┘
"""
            )

            class Args:
                files = [str(file1), str(dir1)]
                quiet = True

            exit_code = cmd_lint(Args())
            assert exit_code == 0

    def test_cli_fix_with_directory(self) -> None:
        """Test CLI fix command with directory scanning."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create broken box
            broken_file = tmppath / "broken.md"
            broken_file.write_text(
                """
┌────────┐
│ Broken │
└───────┘
"""
            )  # Bottom line is too short

            class Args:
                files = [str(tmppath)]
                dry_run = False

            exit_code = cmd_fix(Args())
            assert exit_code == 0

            # Verify file was fixed (check that bottom line was modified)
            content = broken_file.read_text()
            lines = [line for line in content.split("\n") if line.strip()]
            # Bottom line should now have 8 dashes (matching top line)
            bottom_line = lines[-1]
            assert len(bottom_line) >= 10  # Should be properly sized now

    def test_default_excludes_work(self) -> None:
        """Test that default excludes prevent scanning common directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create files that should be scanned
            (tmppath / "README.md").write_text(
                """
┌──────┐
│ Docs │
└──────┘
"""
            )

            # Create files in default excluded directories
            git_dir = tmppath / ".git"
            git_dir.mkdir()
            (git_dir / "config").write_text("git config")

            node_modules = tmppath / "node_modules"
            node_modules.mkdir()
            (node_modules / "package.json").write_text("{}")

            # Scan without config (should use defaults)
            files = scan_paths([tmppath])

            # Should only find README.md, not .git or node_modules contents
            assert len(files) == 1
            assert files[0].name == "README.md"

    def test_explicit_files_bypass_filters(self) -> None:
        """Test that explicit file paths bypass config filters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create config that excludes .txt
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
exclude = ["*.txt"]
"""
            )

            # Create a .txt file
            txt_file = tmppath / "excluded.txt"
            txt_file.write_text(
                """
┌──────┐
│ Text │
└──────┘
"""
            )

            config = load_config(config_file)

            # Explicit file path should bypass filters
            files = scan_paths([txt_file], config)
            assert len(files) == 1
            assert files[0] == txt_file.resolve()

    def test_negation_patterns_work(self) -> None:
        """Test that negation patterns (include overrides) work."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create config with exclusion and negation
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
exclude = ["*.tmp"]
include = ["!important.tmp"]
"""
            )

            # Create files
            (tmppath / "normal.md").write_text(
                """
┌────────┐
│ Normal │
└────────┘
"""
            )
            (tmppath / "excluded.tmp").write_text("excluded")
            (tmppath / "important.tmp").write_text(
                """
┌───────────┐
│ Important │
└───────────┘
"""
            )

            config = load_config(config_file)
            files = scan_paths([tmppath], config)

            # Filter out the config file itself
            files = [f for f in files if not f.name.endswith(".toml")]

            # Should find normal.md and important.tmp, but not excluded.tmp
            assert len(files) == 2
            filenames = {f.name for f in files}
            assert "normal.md" in filenames
            assert "important.tmp" in filenames
            assert "excluded.tmp" not in filenames

    def test_python_310_311_compatibility(self) -> None:
        """Test that TOML import works on different Python versions."""
        import sys

        # This test verifies the version-aware import works
        if sys.version_info >= (3, 11):
            import tomllib

            assert tomllib is not None
        else:
            import tomli as tomllib

            assert tomllib is not None

        # Test that config loading works
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
extensions = [".md"]
"""
            )

            config = load_config(config_file)
            assert config.extensions == [".md"]
