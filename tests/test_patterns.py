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

"""Tests for pattern matching."""

import tempfile
from pathlib import Path

from ascii_guard.patterns import filter_paths, match_path


class TestSimplePatterns:
    """Test simple glob patterns."""

    def test_wildcard_extension(self) -> None:
        """Test *.ext pattern matches files with extension."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "test.txt").touch()
            (tmppath / "other.md").touch()

            assert match_path(tmppath / "test.txt", ["*.txt"], tmppath) is True
            assert match_path(tmppath / "other.md", ["*.txt"], tmppath) is False

    def test_wildcard_filename(self) -> None:
        """Test wildcard in filename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "test_file.txt").touch()
            (tmppath / "test_other.txt").touch()
            (tmppath / "other.txt").touch()

            assert match_path(tmppath / "test_file.txt", ["test_*.txt"], tmppath) is True
            assert match_path(tmppath / "test_other.txt", ["test_*.txt"], tmppath) is True
            assert match_path(tmppath / "other.txt", ["test_*.txt"], tmppath) is False

    def test_directory_pattern(self) -> None:
        """Test directory-specific patterns (ending with /)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            dir_path = tmppath / "node_modules"
            dir_path.mkdir()
            (tmppath / "node_modules.txt").touch()

            # Directory pattern should match directories only
            assert match_path(dir_path, ["node_modules/"], tmppath) is True
            assert match_path(tmppath / "node_modules.txt", ["node_modules/"], tmppath) is False

    def test_specific_file(self) -> None:
        """Test exact filename match."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "README.md").touch()
            (tmppath / "OTHER.md").touch()

            assert match_path(tmppath / "README.md", ["README.md"], tmppath) is True
            assert match_path(tmppath / "OTHER.md", ["README.md"], tmppath) is False


class TestRecursivePatterns:
    """Test ** recursive patterns."""

    def test_recursive_prefix(self) -> None:
        """Test **/pattern matches pattern anywhere in tree."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create nested structure
            (tmppath / "level1").mkdir()
            (tmppath / "level1" / "test.txt").touch()
            (tmppath / "level1" / "level2").mkdir()
            (tmppath / "level1" / "level2" / "test.txt").touch()

            # Should match test.txt at any level
            assert match_path(tmppath / "level1" / "test.txt", ["**/test.txt"], tmppath) is True
            assert (
                match_path(tmppath / "level1" / "level2" / "test.txt", ["**/test.txt"], tmppath)
                is True
            )

    def test_recursive_suffix(self) -> None:
        """Test pattern/** matches directory and all contents."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create directory structure
            cache_dir = tmppath / "__pycache__"
            cache_dir.mkdir()
            (cache_dir / "file.pyc").touch()

            # Should match __pycache__ directory and contents
            assert match_path(cache_dir, ["__pycache__/**"], tmppath) is True
            assert match_path(cache_dir / "file.pyc", ["__pycache__/**"], tmppath) is True

    def test_recursive_middle(self) -> None:
        """Test pattern with ** in middle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create nested structure
            (tmppath / "src").mkdir()
            (tmppath / "src" / "test").mkdir()
            (tmppath / "src" / "test" / "file.py").touch()

            # Match src/**/file.py
            assert (
                match_path(tmppath / "src" / "file.py", ["src/**/*.py"], tmppath) is False
            )  # Not nested enough
            assert (
                match_path(tmppath / "src" / "test" / "file.py", ["src/**/*.py"], tmppath) is True
            )


class TestNegationPatterns:
    """Test negation (include override) patterns."""

    def test_simple_negation(self) -> None:
        """Test !pattern includes files that would be excluded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "important.txt").touch()
            (tmppath / "other.txt").touch()

            # Exclude all .txt, but include important.txt
            patterns = ["*.txt", "!important.txt"]

            assert match_path(tmppath / "other.txt", patterns, tmppath) is True  # Excluded
            assert match_path(tmppath / "important.txt", patterns, tmppath) is False  # Included

    def test_negation_overrides_earlier(self) -> None:
        """Test that negation patterns override earlier excludes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            docs_dir = tmppath / "docs"
            docs_dir.mkdir()
            (docs_dir / "keep.md").touch()
            (docs_dir / "remove.md").touch()

            # Exclude docs/, but include docs/keep.md
            patterns = ["docs/", "!docs/keep.md"]

            assert match_path(docs_dir, patterns, tmppath) is True  # Directory excluded
            assert match_path(docs_dir / "remove.md", patterns, tmppath) is True  # Excluded
            assert match_path(docs_dir / "keep.md", patterns, tmppath) is False  # Included


class TestCommentPatterns:
    """Test that comments are ignored."""

    def test_comment_ignored(self) -> None:
        """Test that lines starting with # are ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "test.txt").touch()

            patterns = [
                "# This is a comment",
                "*.txt",
            ]

            assert match_path(tmppath / "test.txt", patterns, tmppath) is True


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_patterns(self) -> None:
        """Test that empty pattern list matches nothing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "file.txt").touch()

            assert match_path(tmppath / "file.txt", [], tmppath) is False

    def test_empty_pattern_strings(self) -> None:
        """Test that empty strings in patterns are ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "file.txt").touch()

            patterns = ["", "*.txt", ""]
            assert match_path(tmppath / "file.txt", patterns, tmppath) is True

    def test_path_outside_base(self) -> None:
        """Test matching paths outside base directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "file.txt").touch()

            # Use different base path
            other_base = Path(tmpdir).parent

            # Should still work with absolute paths
            result = match_path(tmppath / "file.txt", ["*.txt"], other_base)
            assert isinstance(result, bool)  # Just verify it doesn't crash


class TestFilterPaths:
    """Test filter_paths utility function."""

    def test_filter_with_excludes(self) -> None:
        """Test filtering paths with exclude patterns."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            file1 = tmppath / "keep.md"
            file2 = tmppath / "remove.txt"
            file3 = tmppath / "also_keep.md"
            file1.touch()
            file2.touch()
            file3.touch()

            paths = [file1, file2, file3]
            filtered = filter_paths(paths, ["*.txt"], base_path=tmppath)

            assert len(filtered) == 2
            assert file1 in filtered
            assert file3 in filtered
            assert file2 not in filtered

    def test_filter_with_includes(self) -> None:
        """Test filtering with both exclude and include patterns."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            file1 = tmppath / "temp1.txt"
            file2 = tmppath / "temp2.txt"
            file3 = tmppath / "important.txt"
            file1.touch()
            file2.touch()
            file3.touch()

            paths = [file1, file2, file3]

            # Exclude all .txt, but include important.txt
            filtered = filter_paths(
                paths,
                exclude_patterns=["*.txt"],
                include_patterns=["!important.txt"],
                base_path=tmppath,
            )

            assert len(filtered) == 1
            assert file3 in filtered

    def test_filter_empty_list(self) -> None:
        """Test filtering empty path list."""
        filtered = filter_paths([], ["*.txt"])
        assert filtered == []
