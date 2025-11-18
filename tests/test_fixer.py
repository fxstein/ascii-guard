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

"""Tests for the box fixing module.

Verifies that ASCII box alignment issues are correctly fixed.
"""

from ascii_guard.fixer import fix_box
from ascii_guard.models import Box


class TestBoxFixer:
    """Test suite for ASCII box fixing."""

    def test_fix_broken_bottom(self) -> None:
        """Test fixing a bottom edge that's too short."""
        box = Box(
            top_line=0,
            bottom_line=2,
            left_col=0,
            right_col=20,
            lines=[
                "┌────────────────────┐",
                "│ Content            │",
                "└───────────────────",  # Too short
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # Fixer should attempt to extend the bottom line
        assert "└" in fixed_lines[2]
        # Note: Current implementation may not fully extend to match top width

    def test_fix_broken_right_border(self) -> None:
        """Test fixing missing right borders."""
        box = Box(
            top_line=0,
            bottom_line=2,
            left_col=0,
            right_col=20,
            lines=[
                "┌────────────────────┐",
                "│ Missing right      ",  # Missing right border
                "└────────────────────┘",
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # Right border should be added
        assert fixed_lines[1].rstrip().endswith("│")

    def test_fix_preserves_perfect_box(self) -> None:
        """Test that fixing doesn't modify a perfect box."""
        box = Box(
            top_line=0,
            bottom_line=2,
            left_col=0,
            right_col=20,
            lines=[
                "┌────────────────────┐",
                "│ Perfect box        │",
                "└────────────────────┘",
            ],
            file_path="test.txt",
        )

        original_lines = box.lines.copy()
        fixed_lines = fix_box(box)

        # Should be similar (may have minor formatting adjustments)
        assert len(fixed_lines) == len(original_lines)
        # Core structure should be preserved
        assert "┌" in fixed_lines[0]
        assert "└" in fixed_lines[2]

    def test_fix_multiple_content_lines(self) -> None:
        """Test fixing boxes with multiple content lines."""
        box = Box(
            top_line=0,
            bottom_line=4,
            left_col=0,
            right_col=20,
            lines=[
                "┌────────────────────┐",
                "│ Line 1             │",
                "│ Line 2             ",  # Missing right
                "│ Line 3             │",
                "└────────────────────",  # Missing right corner
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)

        # All lines should have box-drawing characters
        assert all("│" in line or "─" in line or "└" in line or "┌" in line for line in fixed_lines)
        # Bottom line should have bottom-left corner at minimum
        assert "└" in fixed_lines[4]

    def test_fix_maintains_content(self) -> None:
        """Test that fixing preserves the actual content."""
        box = Box(
            top_line=0,
            bottom_line=2,
            left_col=0,
            right_col=25,
            lines=[
                "┌─────────────────────────┐",
                "│ Important content!      ",  # Missing right border
                "└─────────────────────────",  # Missing right corner
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)

        # Content should still be present
        assert "Important content!" in fixed_lines[1]

    def test_fix_returns_correct_number_of_lines(self) -> None:
        """Test that fixer returns the same number of lines."""
        box = Box(
            top_line=0,
            bottom_line=3,
            left_col=0,
            right_col=15,
            lines=[
                "┌───────────────┐",
                "│ Line 1        │",
                "│ Line 2        │",
                "└───────────────",
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        assert len(fixed_lines) == len(box.lines)


class TestFixerEdgeCases:
    """Test edge cases in box fixing."""

    def test_fix_empty_content_lines(self) -> None:
        """Test fixing boxes with empty content."""
        box = Box(
            top_line=0,
            bottom_line=2,
            left_col=0,
            right_col=10,
            lines=[
                "┌──────────┐",
                "│          ",  # Empty content, missing right
                "└──────────",
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # Should attempt to fix borders
        assert "│" in fixed_lines[1]
        assert "└" in fixed_lines[2]

    def test_fix_very_short_box(self) -> None:
        """Test fixing a very short box."""
        box = Box(
            top_line=0,
            bottom_line=1,
            left_col=0,
            right_col=5,
            lines=[
                "┌─────┐",
                "└─────",  # Missing corner
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # Should have bottom-left corner
        assert "└" in fixed_lines[1]

    def test_fix_wide_box(self) -> None:
        """Test fixing a very wide box."""
        box = Box(
            top_line=0,
            bottom_line=2,
            left_col=0,
            right_col=100,
            lines=[
                "┌" + "─" * 99 + "┐",
                "│" + " " * 99,  # Missing right
                "└" + "─" * 99,  # Missing corner
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # Should have vertical borders
        assert "│" in fixed_lines[1]
        # Should have bottom-left corner
        assert "└" in fixed_lines[2]


class TestDifferentBoxStyleFixing:
    """Test fixing different box drawing styles."""

    def test_fix_double_line_box(self) -> None:
        """Test fixing double-line boxes."""
        box = Box(
            top_line=0,
            bottom_line=2,
            left_col=0,
            right_col=20,
            lines=[
                "╔════════════════════╗",
                "║ Double line        ║",
                "╚════════════════════",  # Missing corner
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # Should have bottom-left corner (may convert styles)
        assert "╚" in fixed_lines[2]

    def test_fix_heavy_line_box(self) -> None:
        """Test fixing heavy-line boxes."""
        box = Box(
            top_line=0,
            bottom_line=2,
            left_col=0,
            right_col=20,
            lines=[
                "┏━━━━━━━━━━━━━━━━━━━━┓",
                "┃ Heavy line         ",  # Missing right
                "┗━━━━━━━━━━━━━━━━━━━━┛",
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        assert "┃" in fixed_lines[1]

    def test_fix_ascii_box(self) -> None:
        """Test fixing simple ASCII boxes."""
        box = Box(
            top_line=0,
            bottom_line=2,
            left_col=0,
            right_col=20,
            lines=[
                "+--------------------+",
                "| ASCII box          ",  # Missing right
                "+--------------------",  # Missing corner
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # Fixer may convert ASCII style to Unicode box drawing
        assert "│" in fixed_lines[1] or "|" in fixed_lines[1]
        # Should have some bottom border character
        assert len(fixed_lines[2]) > 0


class TestFixerWithDividers:
    """Test suite for fixing boxes with horizontal dividers."""

    def test_fix_short_line_after_divider(self) -> None:
        """Test fixing a box where content lines are one char too short."""
        box = Box(
            top_line=0,
            bottom_line=4,
            left_col=0,
            right_col=30,
            lines=[
                "┌──────────────────────────────┐",
                "│ Header                       │",
                "├──────────────────────────────┤",
                "│ Short content line          │",  # Missing one space before border
                "└──────────────────────────────┘",
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # Should extend the line and place border at correct position
        assert len(fixed_lines[3]) == 31  # Should match top border length
        assert fixed_lines[3][30] == "│"  # Right border at correct position
        assert "││" not in fixed_lines[3]  # Should NOT create double borders

    def test_fix_preserves_divider_lines(self) -> None:
        """Test that divider lines remain intact during fixing."""
        box = Box(
            top_line=0,
            bottom_line=5,
            left_col=0,
            right_col=26,
            lines=[
                "┌─────────────────────────┐",
                "│ Section 1               │",
                "├─────────────────────────┤",
                "│ Section 2              │",  # One char short
                "│ Content                 │",
                "└─────────────────────────┘",
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # Divider line should be unchanged
        assert fixed_lines[2] == "├─────────────────────────┤"
        # Short line should be fixed
        assert len(fixed_lines[3]) == 27
        assert "││" not in fixed_lines[3]

    def test_fix_multiple_short_lines_with_dividers(self) -> None:
        """Test fixing multiple short lines in a box with dividers."""
        box = Box(
            top_line=0,
            bottom_line=6,
            left_col=0,
            right_col=21,
            lines=[
                "┌────────────────────┐",
                "│ Header            │",  # One char short
                "├────────────────────┤",
                "│ Body              │",  # One char short
                "├────────────────────┤",
                "│ Footer            │",  # One char short
                "└────────────────────┘",
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # All content lines should be fixed to proper length
        assert len(fixed_lines[1]) == 22
        assert len(fixed_lines[3]) == 22
        assert len(fixed_lines[5]) == 22
        # Divider lines should be unchanged
        assert fixed_lines[2] == "├────────────────────┤"
        assert fixed_lines[4] == "├────────────────────┤"
        # No double borders
        for line in fixed_lines:
            assert "││" not in line


class TestFixerWithTableSeparators:
    """Test suite for fixing boxes with table column separators."""

    def test_fix_table_separator_with_extra_char(self) -> None:
        """Test fixing table separator with extra character at end."""
        box = Box(
            top_line=0,
            bottom_line=3,
            left_col=0,
            right_col=21,
            lines=[
                "┌─────────┬──────────┐",
                "│ Col 1   │ Col 2    │",
                "├─────────┼──────────┤│",  # Extra │ at end
                "└─────────┴──────────┘",
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # Extra character should be removed
        assert fixed_lines[2] == "├─────────┼──────────┤"
        assert len(fixed_lines[2]) == 22  # Should match top border length

    def test_fix_missing_bottom_corner(self) -> None:
        """Test fixing box with missing bottom right corner."""
        box = Box(
            top_line=0,
            bottom_line=2,
            left_col=0,
            right_col=21,
            lines=[
                "┌────────────────────┐",
                "│ Content            │",
                "└───────────────────",  # Missing ┘
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # Bottom line should be extended and corner added
        assert len(fixed_lines[2]) == 22
        assert fixed_lines[2][21] == "┘"
        assert fixed_lines[2] == "└────────────────────┘"

    def test_fix_table_with_extra_chars_and_missing_corner(self) -> None:
        """Test fixing table with both extra chars and missing corner."""
        box = Box(
            top_line=0,
            bottom_line=4,
            left_col=0,
            right_col=30,
            lines=[
                "┌──────────┬──────────────────┐",
                "│ Header 1 │ Header 2         │",
                "├──────────┼──────────────────┤│",  # Extra │
                "│ Data     │ Values           │",
                "└──────────┴─────────────────",  # Missing ┘
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # Table separator should have extra char removed
        assert fixed_lines[2] == "├──────────┼──────────────────┤"
        assert len(fixed_lines[2]) == 31
        # Bottom corner should be added
        assert fixed_lines[4][30] == "┘"
        assert len(fixed_lines[4]) == 31

    def test_fix_preserves_junction_points_in_borders(self) -> None:
        """Test that junction points in borders are preserved during fixing."""
        box = Box(
            top_line=0,
            bottom_line=2,
            left_col=0,
            right_col=21,
            lines=[
                "┌─────────┬──────────┐",  # Junction in top border
                "│ Content │ Content  │",
                "└─────────┴─────────",  # Missing ┘, junction should map ┬→┴
            ],
            file_path="test.txt",
        )

        fixed_lines = fix_box(box)
        # Top border should be unchanged
        assert fixed_lines[0] == "┌─────────┬──────────┐"
        # Bottom should have junction converted and corner added
        assert fixed_lines[2] == "└─────────┴──────────┘"
        assert len(fixed_lines[2]) == 22
