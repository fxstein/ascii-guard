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

"""Tests for configuration file parsing."""

import sys
import tempfile
from pathlib import Path

import pytest

from ascii_guard.config import (
    DEFAULT_EXCLUDES,
    Config,
    find_config_file,
    load_config,
)


class TestVersionAwareImport:
    """Test that tomllib/tomli import works correctly based on Python version."""

    def test_toml_module_available(self) -> None:
        """Test that TOML parsing module is available."""
        # This should work on both Python 3.10 (tomli) and 3.11+ (tomllib)
        if sys.version_info >= (3, 11):
            import tomllib

            assert tomllib is not None
        else:
            import tomli as tomllib

            assert tomllib is not None

    def test_config_module_imports(self) -> None:
        """Test that config module imports without error."""
        import ascii_guard.config

        assert ascii_guard.config is not None


class TestConfigDefaults:
    """Test default configuration values."""

    def test_default_config(self) -> None:
        """Test that default Config object has expected values."""
        config = Config()

        assert config.extensions == []
        assert config.exclude == DEFAULT_EXCLUDES
        assert config.include == []
        assert config.follow_symlinks is False
        assert config.max_file_size == 10

    def test_default_excludes_present(self) -> None:
        """Test that default excludes contain common patterns."""
        assert ".git/" in DEFAULT_EXCLUDES
        assert "node_modules/" in DEFAULT_EXCLUDES
        assert "__pycache__/" in DEFAULT_EXCLUDES
        assert ".venv/" in DEFAULT_EXCLUDES
        assert "build/" in DEFAULT_EXCLUDES
        assert "dist/" in DEFAULT_EXCLUDES


class TestConfigFileDiscovery:
    """Test config file discovery logic."""

    def test_find_config_toml_preferred(self) -> None:
        """Test that .ascii-guard.toml is preferred over .ascii-guard."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create both files
            (tmppath / ".ascii-guard.toml").touch()
            (tmppath / ".ascii-guard").touch()

            found = find_config_file(tmppath)
            assert found is not None
            assert found.name == ".ascii-guard.toml"

    def test_find_config_fallback(self) -> None:
        """Test that .ascii-guard is found if .toml doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create only .ascii-guard
            (tmppath / ".ascii-guard").touch()

            found = find_config_file(tmppath)
            assert found is not None
            assert found.name == ".ascii-guard"

    def test_find_config_none(self) -> None:
        """Test that None is returned when no config file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            found = find_config_file(tmppath)
            assert found is None

    def test_find_config_walks_up(self) -> None:
        """Test that config file is found in parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir).resolve()

            # Create config in root
            (tmppath / ".ascii-guard.toml").touch()

            # Create nested directory
            nested = tmppath / "subdir" / "nested"
            nested.mkdir(parents=True)

            # Search from nested directory
            found = find_config_file(nested)
            assert found is not None
            assert found.resolve() == (tmppath / ".ascii-guard.toml").resolve()

    def test_find_config_stops_at_git_root(self) -> None:
        """Test that search stops at .git directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir).resolve()

            # Create git root with config
            git_root = tmppath / "repo"
            git_root.mkdir()
            (git_root / ".git").mkdir()
            (git_root / ".ascii-guard.toml").touch()

            # Create parent directory with different config
            (tmppath / ".ascii-guard.toml").write_text('[files]\nexclude = ["parent"]')

            # Create nested directory in repo
            nested = git_root / "subdir"
            nested.mkdir()

            # Search from nested should find repo config, not parent
            found = find_config_file(nested)
            assert found is not None
            assert found.resolve() == (git_root / ".ascii-guard.toml").resolve()


class TestConfigLoading:
    """Test configuration file loading and parsing."""

    def test_load_config_no_file_uses_defaults(self) -> None:
        """Test that load_config returns defaults when no file exists."""
        # Test without specifying path in empty directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory for testing
            import os

            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                config = load_config()
                assert config.extensions == []
                assert config.exclude == DEFAULT_EXCLUDES
            finally:
                os.chdir(old_cwd)

    def test_load_config_empty_file(self) -> None:
        """Test loading empty TOML config file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text("")

            config = load_config(config_file)
            assert config.extensions == []
            assert config.exclude == DEFAULT_EXCLUDES  # Defaults

    def test_load_config_with_extensions(self) -> None:
        """Test loading config with custom extensions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
extensions = [".md", ".txt", ".rst"]
"""
            )

            config = load_config(config_file)
            assert config.extensions == [".md", ".txt", ".rst"]

    def test_load_config_with_excludes(self) -> None:
        """Test loading config with custom excludes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
exclude = ["*.tmp", "cache/"]
"""
            )

            config = load_config(config_file)
            # User config overrides defaults
            assert config.exclude == ["*.tmp", "cache/"]

    def test_load_config_with_includes(self) -> None:
        """Test loading config with include patterns."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
include = ["!important.md", "!docs/keep.txt"]
"""
            )

            config = load_config(config_file)
            assert config.include == ["!important.md", "!docs/keep.txt"]

    def test_load_config_with_follow_symlinks(self) -> None:
        """Test loading config with follow_symlinks setting."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
follow_symlinks = true
"""
            )

            config = load_config(config_file)
            assert config.follow_symlinks is True

    def test_load_config_with_max_file_size(self) -> None:
        """Test loading config with max_file_size setting."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
max_file_size = 50
"""
            )

            config = load_config(config_file)
            assert config.max_file_size == 50

    def test_load_config_invalid_toml(self) -> None:
        """Test that invalid TOML raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text("invalid [[ toml")

            with pytest.raises(ValueError, match="Failed to parse config file"):
                load_config(config_file)

    def test_load_config_invalid_extensions_type(self) -> None:
        """Test that non-list extensions raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
extensions = ".md"  # Should be a list
"""
            )

            with pytest.raises(ValueError, match="extensions must be a list"):
                load_config(config_file)

    def test_load_config_invalid_max_file_size(self) -> None:
        """Test that negative max_file_size raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
max_file_size = -1
"""
            )

            with pytest.raises(ValueError, match="max_file_size must be non-negative"):
                load_config(config_file)

    def test_load_config_file_not_found(self) -> None:
        """Test that specifying non-existent config file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Config file not found"):
            load_config("/nonexistent/path/.ascii-guard.toml")

    def test_load_config_warns_unknown_keys(self, capsys) -> None:  # type: ignore[no-untyped-def]
        """Test that unknown keys in [files] section produce warnings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
extensions = []
unknown_key = "value"
"""
            )

            config = load_config(config_file)
            assert config is not None

            captured = capsys.readouterr()
            assert "Warning" in captured.out
            assert "unknown_key" in captured.out

    def test_load_config_warns_unknown_sections(self, capsys) -> None:  # type: ignore[no-untyped-def]
        """Test that unknown sections produce warnings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
extensions = []

[unknown_section]
key = "value"
"""
            )

            config = load_config(config_file)
            assert config is not None

            captured = capsys.readouterr()
            assert "Warning" in captured.out
            assert "unknown_section" in captured.out


class TestConfigEdgeCases:
    """Test edge cases to achieve 100% coverage."""

    def test_load_config_extensions_not_all_strings(self) -> None:
        """Test that extensions with non-string values raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
extensions = [".txt", 123, ".md"]
"""
            )

            with pytest.raises(ValueError, match="extensions must be a list of strings"):
                load_config(config_file)

    def test_load_config_exclude_not_list(self) -> None:
        """Test that exclude must be a list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
exclude = "not_a_list"
"""
            )

            with pytest.raises(ValueError, match="exclude must be a list, got str"):
                load_config(config_file)

    def test_load_config_exclude_not_all_strings(self) -> None:
        """Test that exclude with non-string values raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
exclude = ["*.txt", 456]
"""
            )

            with pytest.raises(ValueError, match="exclude must be a list of strings"):
                load_config(config_file)

    def test_load_config_include_not_list(self) -> None:
        """Test that include must be a list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
include = "not_a_list"
"""
            )

            with pytest.raises(ValueError, match="include must be a list, got str"):
                load_config(config_file)

    def test_load_config_include_not_all_strings(self) -> None:
        """Test that include with non-string values raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
include = ["!*.md", 789]
"""
            )

            with pytest.raises(ValueError, match="include must be a list of strings"):
                load_config(config_file)

    def test_load_config_follow_symlinks_not_bool(self) -> None:
        """Test that follow_symlinks with non-bool value raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
follow_symlinks = "yes"
"""
            )

            with pytest.raises(ValueError, match="follow_symlinks must be a boolean"):
                load_config(config_file)

    def test_load_config_max_file_size_not_int(self) -> None:
        """Test that max_file_size with non-int value raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            config_file = tmppath / ".ascii-guard.toml"
            config_file.write_text(
                """
[files]
max_file_size = "10"
"""
            )

            with pytest.raises(ValueError, match="max_file_size must be an integer"):
                load_config(config_file)

    def test_find_config_stops_at_git_root(self) -> None:
        """Test that config search stops at git root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            # Create a git root
            git_dir = tmppath / ".git"
            git_dir.mkdir()

            # Create a nested directory below git root
            nested = tmppath / "src" / "deep" / "nested"
            nested.mkdir(parents=True)

            # No config file exists, but search should stop at git root
            config_file = find_config_file(nested)
            # Should return None (no config found)
            assert config_file is None
