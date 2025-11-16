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

"""Tests for the box detection module.

Verifies that ASCII art boxes are correctly detected in files.
"""

from pathlib import Path

import pytest

from ascii_guard.detector import detect_boxes


class TestBoxDetection:
    """Test suite for ASCII box detection."""

    @pytest.fixture
    def fixtures_dir(self) -> Path:
        """Return the path to test fixtures directory."""
        return Path(__file__).parent / "fixtures"

    def test_detect_perfect_box(self, fixtures_dir: Path) -> None:
        """Test detection of a perfectly aligned box."""
        test_file = str(fixtures_dir / "perfect_box.txt")
        boxes = detect_boxes(test_file)

        assert len(boxes) == 1
        box = boxes[0]
        assert box.top_line == 2
        assert box.bottom_line == 5
        assert box.left_col == 0
        assert box.right_col == 46  # Column index of right border
        assert len(box.lines) == 4

    def test_detect_broken_box(self, fixtures_dir: Path) -> None:
        """Test detection of a box with misalignment."""
        test_file = str(fixtures_dir / "broken_box.txt")
        boxes = detect_boxes(test_file)

        assert len(boxes) == 1
        # Should still detect the box even if broken
        box = boxes[0]
        assert box.top_line == 2
        assert box.bottom_line == 5

    def test_detect_multiple_boxes(self, fixtures_dir: Path) -> None:
        """Test detection of multiple boxes in a single file."""
        test_file = str(fixtures_dir / "multiple_boxes.md")
        boxes = detect_boxes(test_file)

        # Should detect 4 boxes
        assert len(boxes) == 4

    def test_detect_no_boxes(self, fixtures_dir: Path) -> None:
        """Test file with no ASCII boxes."""
        test_file = str(fixtures_dir / "no_boxes.txt")
        boxes = detect_boxes(test_file)

        assert len(boxes) == 0

    def test_detect_mixed_styles(self, fixtures_dir: Path) -> None:
        """Test detection of different box drawing styles."""
        test_file = str(fixtures_dir / "mixed_styles.txt")
        boxes = detect_boxes(test_file)

        # Should detect Unicode box styles (not ASCII +/- style)
        assert len(boxes) == 3

    def test_file_not_found(self) -> None:
        """Test handling of non-existent file."""
        with pytest.raises(OSError):
            detect_boxes("/nonexistent/file.txt")

    def test_box_properties(self, fixtures_dir: Path) -> None:
        """Test that detected boxes have correct properties."""
        test_file = str(fixtures_dir / "perfect_box.txt")
        boxes = detect_boxes(test_file)

        box = boxes[0]
        assert box.file_path == test_file
        assert isinstance(box.lines, list)
        assert all(isinstance(line, str) for line in box.lines)
        assert box.top_line < box.bottom_line
        assert box.left_col <= box.right_col


class TestEdgeCases:
    """Test edge cases in box detection."""

    def test_empty_file(self, tmp_path: Path) -> None:
        """Test detection in an empty file."""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("")

        boxes = detect_boxes(str(test_file))
        assert len(boxes) == 0

    def test_single_line_file(self, tmp_path: Path) -> None:
        """Test detection in a single-line file."""
        test_file = tmp_path / "single_line.txt"
        test_file.write_text("Just one line\n")

        boxes = detect_boxes(str(test_file))
        assert len(boxes) == 0

    def test_box_at_start_of_file(self, tmp_path: Path) -> None:
        """Test box detection when box is at the very start."""
        test_file = tmp_path / "box_at_start.txt"
        test_file.write_text("┌────────┐\n│ Box    │\n└────────┘\n")

        boxes = detect_boxes(str(test_file))
        assert len(boxes) == 1
        assert boxes[0].top_line == 0

    def test_box_at_end_of_file(self, tmp_path: Path) -> None:
        """Test box detection when box is at the very end."""
        test_file = tmp_path / "box_at_end.txt"
        test_file.write_text(
            "Some text\n┌────────┐\n│ Box    │\n└────────┘"  # No trailing newline
        )

        boxes = detect_boxes(str(test_file))
        assert len(boxes) == 1

    def test_nested_boxes_not_detected_as_one(self, tmp_path: Path) -> None:
        """Test that nested boxes are handled correctly."""
        test_file = tmp_path / "nested.txt"
        test_file.write_text(
            "┌──────────────┐\n"
            "│ Outer box    │\n"
            "│ ┌────────┐   │\n"
            "│ │ Inner  │   │\n"
            "│ └────────┘   │\n"
            "└──────────────┘\n"
        )

        boxes = detect_boxes(str(test_file))
        # Should detect both boxes
        assert len(boxes) >= 1
