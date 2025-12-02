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

import sys
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


class TestCodeFenceDetection:
    """Test that boxes in markdown code fences are skipped."""

    def test_skip_boxes_in_code_fence(self, tmp_path: Path) -> None:
        """Test that boxes inside markdown code fences can be skipped with flag."""
        test_file = tmp_path / "code_fence.md"
        test_file.write_text(
            """Some text before
```python
# This box should be skipped
┌──────────┐
│ In code  │
└──────────┘
```

This box should be detected:
┌──────────┐
│ Outside  │
└──────────┘
"""
        )

        # Without flag: should detect both boxes
        boxes = detect_boxes(str(test_file))
        assert len(boxes) == 2

        # With exclude flag: should only find the box outside the code fence
        boxes = detect_boxes(str(test_file), exclude_code_blocks=True)
        assert len(boxes) == 1
        assert "Outside" in boxes[0].lines[1]

    def test_nested_code_fences(self, tmp_path: Path) -> None:
        """Test handling of multiple code fences with exclude flag."""
        test_file = tmp_path / "multi_fence.md"
        test_file.write_text(
            """First box (should be detected):
┌──────┐
│ Box1 │
└──────┘

```
Skip this:
┌──────┐
│ Skip │
└──────┘
```

Second box (should be detected):
┌──────┐
│ Box2 │
└──────┘

```
Skip this too:
┌──────┐
│ Skip │
└──────┘
```
"""
        )

        # Without flag: should detect all 4 boxes
        boxes = detect_boxes(str(test_file))
        assert len(boxes) == 4

        # With exclude flag: should only find boxes outside code fences
        boxes = detect_boxes(str(test_file), exclude_code_blocks=True)
        assert len(boxes) == 2
        assert "Box1" in boxes[0].lines[1]
        assert "Box2" in boxes[1].lines[1]


class TestMultipleBoxesPerLine:
    """Test detection of multiple boxes on the same line (flowcharts)."""

    def test_detect_two_boxes_side_by_side(self, tmp_path: Path) -> None:
        """Test detecting two boxes on the same line."""
        test_file = tmp_path / "side_by_side.txt"
        test_file.write_text(
            """┌──────────┐     ┌──────────┐
│ Box Left │     │ Box Right│
└──────────┘     └──────────┘
"""
        )

        boxes = detect_boxes(str(test_file))
        assert len(boxes) == 2
        assert boxes[0].left_col == 0
        assert boxes[1].left_col == 17  # Second box starts at column 17

    def test_flowchart_with_arrows(self, tmp_path: Path) -> None:
        """Test flowchart with boxes and arrows on same line."""
        test_file = tmp_path / "flowchart.txt"
        test_file.write_text(
            """        │ YES                   │ NO → Fail
        v                       │
┌──────────────────┐            v
│ Deploy to Target │     ┌──────────────┐
│   Environment    │     │ Report Error │
└──────────────────┘     └──────────────┘
"""
        )

        boxes = detect_boxes(str(test_file))
        # Should find both boxes despite flow indicators
        assert len(boxes) == 2

    def test_three_boxes_on_same_line(self, tmp_path: Path) -> None:
        """Test detecting three boxes on the same line."""
        test_file = tmp_path / "three_boxes.txt"
        test_file.write_text(
            """┌────┐   ┌────┐   ┌────┐
│ A  │   │ B  │   │ C  │
└────┘   └────┘   └────┘
"""
        )

        boxes = detect_boxes(str(test_file))
        assert len(boxes) == 3


class TestDetectorEdgeCases:
    """Test edge cases to achieve 100% coverage."""

    def test_has_box_drawing_chars_false(self) -> None:
        """Test has_box_drawing_chars with no box characters."""
        from ascii_guard.detector import has_box_drawing_chars

        line = "This is just plain text"
        assert not has_box_drawing_chars(line)

    def test_detect_boxes_file_not_found(self, tmp_path: Path) -> None:
        """Test detecting boxes when file doesn't exist."""
        non_existent = tmp_path / "does_not_exist.txt"

        with pytest.raises(FileNotFoundError, match="File not found"):
            detect_boxes(str(non_existent))

    @pytest.mark.skipif(
        sys.platform == "win32", reason="chmod doesn't make files unreadable on Windows"
    )
    def test_detect_boxes_file_read_error(self, tmp_path: Path) -> None:
        """Test detecting boxes when file cannot be read (OSError)."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("┌────┐\n│Test│\n└────┘")
        # Make file unreadable
        import os

        os.chmod(test_file, 0o000)

        try:
            with pytest.raises(OSError, match="Cannot read file"):
                detect_boxes(str(test_file))
        finally:
            # Restore permissions for cleanup
            os.chmod(test_file, 0o644)

    def test_detect_boxes_with_incomplete_box(self, tmp_path: Path) -> None:
        """Test box detection with incomplete box (no bottom corner)."""
        test_file = tmp_path / "incomplete.txt"
        test_file.write_text(
            """┌──────────────┐
│ Has top      │
│ But no bottom
"""
        )

        boxes = detect_boxes(str(test_file))
        # Should not detect incomplete box
        assert len(boxes) == 0

    def test_detect_boxes_with_no_right_corner(self, tmp_path: Path) -> None:
        """Test box detection when top line has no right corner."""
        test_file = tmp_path / "no_right.txt"
        test_file.write_text(
            """┌──────────────
│ Content here │
└──────────────┘
"""
        )

        boxes = detect_boxes(str(test_file))
        # Should not detect box without right corner
        assert len(boxes) == 0

    def test_detect_boxes_exclude_code_blocks_with_bottom_in_fence(self, tmp_path: Path) -> None:
        """Test that bottom detection skips lines in code fence when exclude_code_blocks=True."""
        test_file = tmp_path / "fence_bottom.txt"
        test_file.write_text(
            """┌──────────────┐
│ Top part     │
```
└──────────────┘
```
"""
        )

        boxes = detect_boxes(str(test_file), exclude_code_blocks=True)
        # Bottom corner is in code fence, so box should not be detected
        assert len(boxes) == 0


class TestIgnoreMarkers:
    """Test suite for ascii-guard ignore markers."""

    def test_ignore_block_region(self, tmp_path: Path) -> None:
        """Test that boxes in block ignore regions are skipped."""
        test_file = tmp_path / "ignore_block.txt"
        test_file.write_text(
            """┌──────────────┐
│ Before       │
└──────────────┘

<!-- ascii-guard-ignore -->
┌──────────────┐
│ Ignored      │
└──────────────
<!-- ascii-guard-ignore-end -->

┌──────────────┐
│ After        │
└──────────────┘
"""
        )

        boxes = detect_boxes(str(test_file))
        # Should detect 2 boxes (before and after), skip the ignored one
        assert len(boxes) == 2
        assert boxes[0].lines[1] == "│ Before       │"
        assert boxes[1].lines[1] == "│ After        │"

    def test_ignore_next_marker(self, tmp_path: Path) -> None:
        """Test that ignore-next marker skips only the next box."""
        test_file = tmp_path / "ignore_next.txt"
        test_file.write_text(
            """┌──────────────┐
│ First box    │
└──────────────┘

<!-- ascii-guard-ignore-next -->
┌──────────────┐
│ Ignored box  │
└──────────────

┌──────────────┐
│ Third box    │
└──────────────┘
"""
        )

        boxes = detect_boxes(str(test_file))
        # Should detect 2 boxes (first and third), skip the ignored one
        assert len(boxes) == 2
        assert boxes[0].lines[1] == "│ First box    │"
        assert boxes[1].lines[1] == "│ Third box    │"

    def test_ignore_next_with_empty_lines(self, tmp_path: Path) -> None:
        """Test that ignore-next skips empty lines before finding box."""
        test_file = tmp_path / "ignore_next_empty.txt"
        test_file.write_text(
            """<!-- ascii-guard-ignore-next -->


┌──────────────┐
│ Should ignore│
└──────────────┘

┌──────────────┐
│ Should detect│
└──────────────┘
"""
        )

        boxes = detect_boxes(str(test_file))
        # Should detect only the second box
        assert len(boxes) == 1
        assert boxes[0].lines[1] == "│ Should detect│"

    def test_nested_ignore_regions(self, tmp_path: Path) -> None:
        """Test multiple ignore blocks."""
        test_file = tmp_path / "nested_ignore.txt"
        test_file.write_text(
            """┌──────────────┐
│ Box 1        │
└──────────────┘

<!-- ascii-guard-ignore -->
┌──────────────┐
│ Ignored A    │
└──────────────┘
<!-- ascii-guard-ignore-end -->

┌──────────────┐
│ Box 2        │
└──────────────┘

<!-- ascii-guard-ignore -->
┌──────────────┐
│ Ignored B    │
└──────────────┘
<!-- ascii-guard-ignore-end -->

┌──────────────┐
│ Box 3        │
└──────────────┘
"""
        )

        boxes = detect_boxes(str(test_file))
        # Should detect 3 boxes, skip 2 ignored ones
        assert len(boxes) == 3
        assert boxes[0].lines[1] == "│ Box 1        │"
        assert boxes[1].lines[1] == "│ Box 2        │"
        assert boxes[2].lines[1] == "│ Box 3        │"

    def test_ignore_broken_box(self, tmp_path: Path) -> None:
        """Test that intentionally broken boxes in ignore regions are skipped."""
        test_file = tmp_path / "ignore_broken.txt"
        test_file.write_text(
            """<!-- ascii-guard-ignore -->
┌──────────────┐
│ Broken box││
└──────────────
<!-- ascii-guard-ignore-end -->
"""
        )

        boxes = detect_boxes(str(test_file))
        # Should not detect the broken box
        assert len(boxes) == 0

    def test_ignore_marker_inline_with_content(self, tmp_path: Path) -> None:
        """Test ignore markers on same line as other content."""
        test_file = tmp_path / "inline_marker.txt"
        test_file.write_text(
            """Some text <!-- ascii-guard-ignore --> more text
┌──────────────┐
│ Ignored      │
└──────────────┘
<!-- ascii-guard-ignore-end --> trailing content

┌──────────────┐
│ Detected     │
└──────────────┘
"""
        )

        boxes = detect_boxes(str(test_file))
        # Should detect only the second box
        assert len(boxes) == 1
        assert boxes[0].lines[1] == "│ Detected     │"

    def test_unclosed_ignore_block(self, tmp_path: Path) -> None:
        """Test that unclosed ignore block ignores all subsequent boxes."""
        test_file = tmp_path / "unclosed_ignore.txt"
        test_file.write_text(
            """┌──────────────┐
│ Before       │
└──────────────┘

<!-- ascii-guard-ignore -->
┌──────────────┐
│ Ignored 1    │
└──────────────┘

┌──────────────┐
│ Ignored 2    │
└──────────────┘
"""
        )

        boxes = detect_boxes(str(test_file))
        # Should detect only the first box (before ignore marker)
        assert len(boxes) == 1
        assert boxes[0].lines[1] == "│ Before       │"

    def test_ignore_with_code_blocks(self, tmp_path: Path) -> None:
        """Test ignore markers work independently of code block exclusion."""
        test_file = tmp_path / "ignore_and_fence.txt"
        test_file.write_text(
            """```
┌──────────────┐
│ In fence     │
└──────────────┘
```

<!-- ascii-guard-ignore -->
┌──────────────┐
│ Ignored      │
└──────────────┘
<!-- ascii-guard-ignore-end -->

┌──────────────┐
│ Detected     │
└──────────────┘
"""
        )

        # Without exclude_code_blocks: should detect fence box but not ignored box
        boxes = detect_boxes(str(test_file), exclude_code_blocks=False)
        assert len(boxes) == 2
        assert boxes[0].lines[1] == "│ In fence     │"
        assert boxes[1].lines[1] == "│ Detected     │"

        # With exclude_code_blocks: should detect only the last box
        boxes = detect_boxes(str(test_file), exclude_code_blocks=True)
        assert len(boxes) == 1
        assert boxes[0].lines[1] == "│ Detected     │"
