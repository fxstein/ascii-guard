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

"""Fixer for ASCII art box alignment issues.

ZERO dependencies - uses only Python stdlib.
"""

from ascii_guard.models import HORIZONTAL_CHARS, JUNCTION_CHARS, RIGHT_DIVIDER_CHARS, Box
from ascii_guard.validator import get_column_positions, is_divider_line, is_table_separator_line


def fix_box(box: Box) -> list[str]:
    """Fix alignment issues in a box.

    Args:
        box: Box to fix

    Returns:
        List of fixed lines
    """
    if not box.lines:
        return []

    fixed_lines = box.lines.copy()

    # Get top border to use as reference
    top_line = fixed_lines[0]

    # Fix bottom border to match top border width
    if len(fixed_lines) > 1:
        bottom_line = fixed_lines[-1]

        # Remember if we need to extend the line
        was_too_short = len(bottom_line) < box.right_col + 1

        # Ensure bottom line is at least as long as needed
        if was_too_short:
            bottom_line = bottom_line.ljust(box.right_col + 1)

        # Rebuild bottom border
        bottom_chars = list(bottom_line)

        # Determine corner characters (use defaults if line was extended)
        left_corner = bottom_chars[box.left_col] if box.left_col < len(bottom_chars) else "└"
        if was_too_short:
            # Line was extended with spaces, so use default right corner
            right_corner = "┘"
        else:
            # Keep the existing right corner character
            right_corner = bottom_chars[box.right_col] if box.right_col < len(bottom_chars) else "┘"

        # Determine which horizontal character to use (preserve junction chars)
        horizontal_char = "─"
        for char in top_line[box.left_col : box.right_col + 1]:
            if char in HORIZONTAL_CHARS:
                horizontal_char = char
                break

        # Get column positions from the entire box (not just top border)
        column_positions = get_column_positions(box)
        column_positions_abs = {box.left_col + pos for pos in column_positions}

        # Build the bottom border with junction points at column positions
        for i in range(box.left_col, box.right_col + 1):
            if i == box.left_col:
                bottom_chars[i] = left_corner
            elif i == box.right_col:
                bottom_chars[i] = right_corner
            elif i in column_positions_abs:
                # Add bottom junction at column position
                bottom_chars[i] = "┴"  # Use standard bottom junction
            elif i < len(top_line) and top_line[i] in JUNCTION_CHARS:
                # Preserve other junction characters from top border
                # Convert top junction to bottom junction
                junction_map = {"┬": "┴", "╦": "╩"}
                bottom_chars[i] = junction_map.get(top_line[i], horizontal_char)
            else:
                bottom_chars[i] = horizontal_char

        fixed_lines[-1] = "".join(bottom_chars)

    # Fix middle lines (ensure they have proper vertical borders)
    for i in range(1, len(fixed_lines) - 1):
        line = fixed_lines[i].rstrip()

        # Skip divider lines and table separator lines - they're valid structural elements
        if is_divider_line(line, box.left_col, box.right_col):
            continue
        if is_table_separator_line(line, box.left_col, box.right_col):
            # Fix malformed table separator lines (extra chars at end)
            # Find where the actual right divider character is
            actual_right_col = -1
            for offset in [0, -1]:  # Check right_col, then right_col-1
                check_col = box.right_col + offset
                if 0 <= check_col < len(line) and line[check_col] in RIGHT_DIVIDER_CHARS:
                    actual_right_col = check_col
                    break

            if actual_right_col != -1 and len(line) > actual_right_col + 1:
                # Remove extra characters after the right divider
                line = line[: actual_right_col + 1]
                fixed_lines[i] = line.rstrip()
            continue

        line_chars = list(line)

        # Check if this line is too short and needs the right border moved/added
        if len(line_chars) <= box.right_col:
            # If line has a border character at the end that should be at right_col
            if line_chars and line_chars[-1] in {"│", "║", "┃"}:
                # Remove the misplaced border and extend the line
                line_chars = line_chars[:-1]

            # Extend line to proper length with spaces
            while len(line_chars) < box.right_col + 1:
                line_chars.append(" ")
        elif len(line_chars) > box.right_col + 1:
            # Line is too long - check for double borders or trailing content
            if (
                box.right_col + 1 < len(line_chars)
                and line_chars[box.right_col] in {"│", "║", "┃"}
                and line_chars[box.right_col + 1] in {"│", "║", "┃"}
            ):
                # Double border detected - truncate after the correct position
                line_chars = line_chars[: box.right_col + 1]
            # Note: We don't truncate lines with extra content after the border
            # as they might be part of flowcharts with multiple boxes per line
            # This is addressed in task#35.6

        # Fix left border if needed
        if box.left_col < len(line_chars) and line_chars[box.left_col] not in {
            "│",
            "║",
            "┃",
            "├",
            "┤",
            "┼",
        }:
            line_chars[box.left_col] = "│"

        # Fix right border if needed
        if box.right_col < len(line_chars) and line_chars[box.right_col] not in {
            "│",
            "║",
            "┃",
            "├",
            "┤",
            "┼",
        }:
            line_chars[box.right_col] = "│"

        fixed_lines[i] = "".join(line_chars).rstrip()

    return fixed_lines
