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

"""Tests for the CLI module.

Tests command-line interface functionality.
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from ascii_guard.cli import cmd_fix, cmd_lint, main


class TestCLILintCommand:
    """Test suite for the lint command."""

    @pytest.fixture
    def fixtures_dir(self) -> Path:
        """Return the path to test fixtures directory."""
        return Path(__file__).parent / "fixtures"

    def test_lint_command_perfect_file(
        self, fixtures_dir: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test lint command on a perfect file."""
        test_file = str(fixtures_dir / "perfect_box.txt")

        # Mock argparse.Namespace
        class Args:
            files = [test_file]
            quiet = False

        exit_code = cmd_lint(Args())

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "No issues found" in captured.out or "Errors: 0" in captured.out

    def test_lint_command_broken_file(
        self, fixtures_dir: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test lint command on a broken file."""
        test_file = str(fixtures_dir / "broken_box.txt")

        class Args:
            files = [test_file]
            quiet = False

        exit_code = cmd_lint(Args())

        assert exit_code == 1  # Should return error code
        captured = capsys.readouterr()
        # Error messages go to stderr
        assert "Errors:" in captured.err or "✗" in captured.err or "Errors:" in captured.out

    def test_lint_command_quiet_mode(
        self, fixtures_dir: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test lint command in quiet mode."""
        test_file = str(fixtures_dir / "perfect_box.txt")

        class Args:
            files = [test_file]
            quiet = True

        exit_code = cmd_lint(Args())

        assert exit_code == 0
        captured = capsys.readouterr()
        # Quiet mode should still show summary but not detailed output
        assert "Summary" in captured.out

    def test_lint_command_multiple_files(self, fixtures_dir: Path) -> None:
        """Test lint command with multiple files."""
        test_files = [
            str(fixtures_dir / "perfect_box.txt"),
            str(fixtures_dir / "broken_box.txt"),
        ]

        class Args:
            files = test_files
            quiet = False

        exit_code = cmd_lint(Args())

        # Should fail because one file has errors
        assert exit_code == 1

    def test_lint_command_nonexistent_file(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test lint command with non-existent file."""

        class Args:
            files = ["/nonexistent/file.txt"]
            quiet = False

        exit_code = cmd_lint(Args())

        assert exit_code == 1
        captured = capsys.readouterr()
        # Error messages go to stderr
        assert "not found" in captured.err.lower() or "✗" in captured.err


class TestCLIFixCommand:
    """Test suite for the fix command."""

    def test_fix_command_broken_file(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test fix command on a broken file."""
        test_file = tmp_path / "broken.txt"
        test_file.write_text("┌────────────┐\n│ Content    │\n└────────────\n")

        class Args:
            files = [str(test_file)]
            dry_run = False

        exit_code = cmd_fix(Args())

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Fixed" in captured.out or "✓" in captured.out

    def test_fix_command_dry_run(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test fix command with dry-run mode."""
        test_file = tmp_path / "broken.txt"
        original_content = "┌────────────┐\n│ Content    │\n└────────────\n"
        test_file.write_text(original_content)

        class Args:
            files = [str(test_file)]
            dry_run = True

        exit_code = cmd_fix(Args())

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Would fix" in captured.out or "ℹ" in captured.out

        # File should be unchanged
        assert test_file.read_text() == original_content

    def test_fix_command_perfect_file(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test fix command on a perfect file."""
        test_file = tmp_path / "perfect.txt"
        test_file.write_text("┌────────────┐\n│ Content    │\n└────────────┘\n")

        class Args:
            files = [str(test_file)]
            dry_run = False

        exit_code = cmd_fix(Args())

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "No fixes needed" in captured.out or "0" in captured.out

    def test_fix_command_multiple_files(self, tmp_path: Path) -> None:
        """Test fix command with multiple files."""
        file1 = tmp_path / "file1.txt"
        file1.write_text("┌────┐\n│ 1  │\n└────\n")

        file2 = tmp_path / "file2.txt"
        file2.write_text("┌────┐\n│ 2  │\n└────\n")

        class Args:
            files = [str(file1), str(file2)]
            dry_run = False

        exit_code = cmd_fix(Args())
        assert exit_code == 0

    def test_fix_command_nonexistent_file(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test fix command with non-existent file."""

        class Args:
            files = ["/nonexistent/file.txt"]
            dry_run = False

        exit_code = cmd_fix(Args())

        assert exit_code == 1
        captured = capsys.readouterr()
        # Error messages go to stderr
        assert "not found" in captured.err.lower() or "✗" in captured.err


class TestCLIMain:
    """Test suite for main CLI entry point."""

    def test_main_no_args(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test main with no arguments shows help."""
        with patch.object(sys, "argv", ["ascii-guard"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0
            captured = capsys.readouterr()
            # Should show help message
            assert "usage:" in captured.out.lower() or "ascii-guard" in captured.out

    def test_main_version(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test --version flag."""
        with patch.object(sys, "argv", ["ascii-guard", "--version"]):
            with pytest.raises(SystemExit):
                main()

            captured = capsys.readouterr()
            assert "ascii-guard" in captured.out or "0.1.0" in captured.out

    def test_main_lint_command(self, tmp_path: Path) -> None:
        """Test main with lint command."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("┌────┐\n│ OK │\n└────┘\n")

        with patch.object(sys, "argv", ["ascii-guard", "lint", str(test_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

    def test_main_fix_command(self, tmp_path: Path) -> None:
        """Test main with fix command."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("┌────┐\n│ OK │\n└────\n")

        with patch.object(sys, "argv", ["ascii-guard", "fix", str(test_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            # Should succeed
            assert exc_info.value.code == 0

    def test_main_unknown_command(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test main with unknown command."""
        with patch.object(sys, "argv", ["ascii-guard", "unknown"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            # Should show error
            assert exc_info.value.code != 0 or capsys.readouterr().err


class TestCLIColors:
    """Test colored output functionality."""

    def test_colored_output_functions_exist(self) -> None:
        """Test that color output functions are available."""
        from ascii_guard.cli import (
            print_error,
            print_info,
            print_success,
            print_warning,
        )

        # Should not raise
        assert callable(print_error)
        assert callable(print_success)
        assert callable(print_warning)
        assert callable(print_info)

    def test_color_constants_defined(self) -> None:
        """Test that ANSI color constants are defined."""
        from ascii_guard.cli import (
            COLOR_BLUE,
            COLOR_BOLD,
            COLOR_GREEN,
            COLOR_RED,
            COLOR_RESET,
            COLOR_YELLOW,
        )

        # Should be non-empty strings
        assert isinstance(COLOR_RED, str) and len(COLOR_RED) > 0
        assert isinstance(COLOR_GREEN, str) and len(COLOR_GREEN) > 0
        assert isinstance(COLOR_YELLOW, str) and len(COLOR_YELLOW) > 0
        assert isinstance(COLOR_BLUE, str) and len(COLOR_BLUE) > 0
        assert isinstance(COLOR_BOLD, str) and len(COLOR_BOLD) > 0
        assert isinstance(COLOR_RESET, str) and len(COLOR_RESET) > 0


class TestCLIEdgeCases:
    """Test CLI edge cases to achieve better coverage."""

    def test_lint_no_files_found(self, tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
        """Test linting when no files match."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        class Args:
            files = [str(empty_dir)]
            quiet = False

        result = cmd_lint(Args())
        # Should return 0 (warning, not error)
        assert result == 0

        # Should show warning about no files
        captured = capsys.readouterr()
        assert "No files found" in captured.out

    def test_fix_no_files_found(self, tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
        """Test fix when no files match."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        class Args:
            files = [str(empty_dir)]
            dry_run = False

        result = cmd_fix(Args())
        # Should return 0 (warning, not error)
        assert result == 0

        # Should show warning
        captured = capsys.readouterr()
        assert "No files found" in captured.out

    def test_fix_dry_run_mode(self, tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
        """Test fix in dry-run mode."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("┌────┐\n│Test│\n└───")  # Short bottom

        class Args:
            files = [str(test_file)]
            dry_run = True

        result = cmd_fix(Args())

        # Should succeed
        assert result == 0

        # Output should mention "Would fix"
        captured = capsys.readouterr()
        assert "Would fix" in captured.out

    def test_lint_displays_warnings_non_quiet(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test lint displays warnings in non-quiet mode."""
        # Create a file with a table missing bottom junctions (warning)
        test_file = tmp_path / "mixed.txt"
        test_file.write_text(
            "┌───┬───┐\n"
            "│ A │ B │\n"
            "├───┼───┤\n"
            "│ 1 │ 2 │\n"
            "└───────┘\n"  # Missing bottom junction (warning)
        )

        class Args:
            files = [str(test_file)]
            quiet = False

        exit_code = cmd_lint(Args())

        # Warnings don't cause error exit code
        assert exit_code == 0

        captured = capsys.readouterr()
        # Should display warnings (⚠ symbol or "Warnings:" text)
        assert "⚠" in captured.out or "Warning" in captured.out

    def test_lint_exception_handling(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test lint exception handling when file cannot be processed."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("┌────┐\n│ OK │\n└────┘\n")

        class Args:
            files = [str(test_file)]
            quiet = False

        # Mock lint_file to raise an exception
        from ascii_guard import cli

        def mock_lint_file(*args, **kwargs):  # type: ignore[no-untyped-def]
            raise ValueError("Simulated processing error")

        with patch.object(cli, "lint_file", side_effect=mock_lint_file):
            exit_code = cmd_lint(Args())

        # Should return error code
        assert exit_code == 1

        captured = capsys.readouterr()
        # Should show error message
        assert "Error processing" in captured.err or "Simulated processing error" in captured.err

    def test_fix_exception_handling(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test fix exception handling when file cannot be processed."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("┌────┐\n│ OK │\n└────\n")

        class Args:
            files = [str(test_file)]
            dry_run = False

        # Mock fix_file to raise an exception
        from ascii_guard import cli

        def mock_fix_file(*args, **kwargs):  # type: ignore[no-untyped-def]
            raise OSError("Permission denied")

        with patch.object(cli, "fix_file", side_effect=mock_fix_file):
            exit_code = cmd_fix(Args())

        # Should return error code
        assert exit_code == 1

        captured = capsys.readouterr()
        # Should show error message
        assert "Error processing" in captured.err or "Permission denied" in captured.err

    def test_show_config_with_config_file(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test --show-config flag with config file present."""
        # Create a config file
        config_file = tmp_path / ".ascii-guard.toml"
        config_file.write_text(
            "[ascii-guard]\n"
            'extensions = [".txt", ".md"]\n'
            'exclude = ["node_modules/**"]\n'
            'include = ["docs/**"]\n'
            "follow_symlinks = true\n"
            "max_file_size = 5\n"
        )

        # Create a test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("┌────┐\n│ OK │\n└────┘\n")

        class Args:
            files = [str(test_file)]
            quiet = False
            show_config = True
            config = str(config_file)

        # Mock load_config to return the config
        from ascii_guard.config import Config

        config_obj = Config(
            extensions=[".txt", ".md"],
            exclude=["node_modules/**"],
            include=["docs/**"],
            follow_symlinks=True,
            max_file_size=5,
        )

        from ascii_guard import cli

        with patch.object(cli, "load_config", return_value=config_obj):
            exit_code = cmd_lint(Args())

        assert exit_code == 0

        captured = capsys.readouterr()
        # Should display config info
        assert "Config loaded from:" in captured.out
        assert ".txt" in captured.out
        assert "node_modules" in captured.out

    def test_show_config_without_config_file(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test --show-config flag without config file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("┌────┐\n│ OK │\n└────┘\n")

        class Args:
            files = [str(test_file)]
            quiet = False
            show_config = True
            config = None

        # Mock load_config to return None
        from ascii_guard import cli

        with patch.object(cli, "load_config", return_value=None):
            exit_code = cmd_lint(Args())

        assert exit_code == 0

        captured = capsys.readouterr()
        # Should display default config message
        assert (
            "Using default config" in captured.out or "no .ascii-guard.toml found" in captured.out
        )

    def test_main_no_command_shows_help(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that running without a subcommand shows help."""
        with patch.object(sys, "argv", ["ascii-guard"]), pytest.raises(SystemExit):
            main()

        captured = capsys.readouterr()
        # Should show help/usage
        assert "usage:" in captured.out.lower() or "ascii-guard" in captured.out
