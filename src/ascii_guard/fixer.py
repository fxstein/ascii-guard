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


from ascii_guard.models import HORIZONTAL_CHARS, Box


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

        # Ensure bottom line is at least as long as needed
        if len(bottom_line) < box.right_col + 1:
            bottom_line = bottom_line.ljust(box.right_col + 1)

        # Rebuild bottom border
        bottom_chars = list(bottom_line)

        # Keep the corner characters
        left_corner = bottom_chars[box.left_col] if box.left_col < len(bottom_chars) else "└"
        right_corner = bottom_chars[box.right_col] if box.right_col < len(bottom_chars) else "┘"

        # Determine which horizontal character to use
        horizontal_char = "─"
        for char in top_line[box.left_col : box.right_col + 1]:
            if char in HORIZONTAL_CHARS:
                horizontal_char = char
                break

        # Build the bottom border
        for i in range(box.left_col, box.right_col + 1):
            if i == box.left_col:
                bottom_chars[i] = left_corner
            elif i == box.right_col:
                bottom_chars[i] = right_corner
            else:
                bottom_chars[i] = horizontal_char

        fixed_lines[-1] = "".join(bottom_chars)

    # Fix middle lines (ensure they have proper vertical borders)
    for i in range(1, len(fixed_lines) - 1):
        line = fixed_lines[i]

        # Ensure line is long enough
        if len(line) < box.right_col + 1:
            line = line.ljust(box.right_col + 1)

        line_chars = list(line)

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
