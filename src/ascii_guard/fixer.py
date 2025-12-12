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
    """Fix alignment issues in a single box.

    Args:
        box: Box object to fix

    Returns:
        List of fixed lines (replacement for box.lines)

    Example:
        >>> boxes = detect_boxes("README.md")
        >>> for box in boxes:
        ...     errors = validate_box(box)
        ...     if errors:
        ...         fixed_lines = fix_box(box)
        ...         # Apply fixed_lines to file
    """
    if not box.lines:
        return []

    fixed_lines = box.lines.copy()

    # Get top border to use as reference
    top_line = fixed_lines[0]

    # Fix bottom border to match top border width
    if len(fixed_lines) > 1:
        bottom_line = fixed_lines[-1]

        # Calculate actual top border width (counting only HORIZONTAL_CHARS and JUNCTION_CHARS)
        # This matches how the validator calculates width
        top_border_width = 0
        for i in range(box.left_col, min(len(top_line), box.right_col + 1)):
            if i < len(top_line):
                char = top_line[i]
                if char in HORIZONTAL_CHARS or char in JUNCTION_CHARS:
                    top_border_width += 1

        # Remember if we need to extend the line
        was_too_short = len(bottom_line) < box.right_col + 1

        # Ensure bottom line is at least as long as needed
        if was_too_short:
            bottom_line = bottom_line.ljust(box.right_col + 1)

        # Rebuild bottom border
        bottom_chars = list(bottom_line)

        # Determine corner characters
        # Use existing corner if valid, otherwise use default
        bottom_corner_chars = {"┘", "╝", "┙", "┛"}
        left_corner = (
            bottom_chars[box.left_col]
            if box.left_col < len(bottom_chars)
            and bottom_chars[box.left_col] in {"└", "╚", "┕", "┗"}
            else "└"
        )

        # For right corner, check if there's a valid corner at the expected position
        # If the original bottom border was misaligned, use default corner
        if box.right_col < len(bottom_chars) and bottom_chars[box.right_col] in bottom_corner_chars:
            right_corner = bottom_chars[box.right_col]
        else:
            right_corner = "┘"

        # Determine which horizontal character to use (preserve junction chars)
        horizontal_char = "─"
        for char in top_line[box.left_col : box.right_col + 1]:
            if char in HORIZONTAL_CHARS:
                horizontal_char = char
                break

        # Get column positions from the entire box (not just top border)
        column_positions = get_column_positions(box)
        column_positions_abs = {box.left_col + pos for pos in column_positions}

        # Build a continuous bottom border that matches top border WIDTH
        # The bottom border should be continuous (no gaps), with exactly top_border_width
        # horizontal/junction characters between the corners

        # Clear the border area first (from left_col to right_col)
        for i in range(box.left_col, min(len(bottom_chars), box.right_col + 1)):
            bottom_chars[i] = " "

        # Place left corner
        bottom_chars[box.left_col] = left_corner

        # Identify junction positions that need to be preserved
        junction_positions = set()
        if column_positions_abs:
            junction_positions.update(column_positions_abs)
        # Also check for junction chars in top border that should be converted
        for i in range(box.left_col + 1, box.right_col):
            if i < len(top_line) and top_line[i] in JUNCTION_CHARS:
                junction_positions.add(i)

        # Use box.right_col as the definitive right corner position
        # The box's structural width is determined by corner positions, NOT by counting
        # horizontal characters. Non-border chars like ▼ are visual indicators inside
        # the border but don't change the structural width.
        right_corner_pos = box.right_col

        # Ensure we have enough space in the array
        if right_corner_pos >= len(bottom_chars):
            bottom_chars.extend([" "] * (right_corner_pos - len(bottom_chars) + 1))

        # Identify which positions need junction characters
        # Only place junctions where the top border also has a junction
        junction_positions_to_place = []
        for i in sorted(junction_positions):
            if i > box.left_col and i < right_corner_pos:
                # Only include if top border has a junction at this position
                # OR if it's a column position and top border has some junction structure
                if i < len(top_line) and top_line[i] in JUNCTION_CHARS:
                    junction_positions_to_place.append(i)
                elif i in column_positions_abs:
                    # Column position from content rows - always add junction
                    # This ensures tables with column separators get proper ┴ in bottom border
                    junction_positions_to_place.append(i)

        # Place border characters continuously from left_col+1 to right_corner_pos-1
        # Fill ALL positions - the structural width is determined by corner positions
        for i in range(box.left_col + 1, right_corner_pos):
            if i in junction_positions_to_place:
                if i in column_positions_abs:
                    bottom_chars[i] = "┴"
                elif i < len(top_line) and top_line[i] in JUNCTION_CHARS:
                    junction_map = {"┬": "┴", "╦": "╩"}
                    bottom_chars[i] = junction_map.get(top_line[i], horizontal_char)
                else:
                    # Junction position but top border doesn't have junction - use horizontal
                    bottom_chars[i] = horizontal_char
            else:
                bottom_chars[i] = horizontal_char

        # Place right corner
        bottom_chars[right_corner_pos] = right_corner

        fixed_lines[-1] = "".join(bottom_chars).rstrip()

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

        # Only check for duplicate borders at THIS box's border positions
        # Don't touch content inside the box (could be nested boxes)
        # Check for duplicate at left_col (e.g., "││" at start)
        if (
            box.left_col < len(line_chars)
            and box.left_col + 1 < len(line_chars)
            and line_chars[box.left_col] in {"│", "║", "┃"}
            and line_chars[box.left_col + 1] in {"│", "║", "┃"}
        ):
            # Replace the duplicate after left border with space
            line_chars[box.left_col + 1] = " "

        # Check for duplicate immediately before left_col (e.g., "││" where second is at left_col)
        if (
            box.left_col > 0
            and box.left_col < len(line_chars)
            and box.left_col - 1 >= 0
            and line_chars[box.left_col] in {"│", "║", "┃"}
            and line_chars[box.left_col - 1] in {"│", "║", "┃"}
        ):
            # Replace the duplicate before left border with space
            line_chars[box.left_col - 1] = " "

        # Check for duplicate at right_col (e.g., "││" at right border)
        if (
            box.right_col < len(line_chars)
            and box.right_col + 1 < len(line_chars)
            and line_chars[box.right_col] in {"│", "║", "┃"}
            and line_chars[box.right_col + 1] in {"│", "║", "┃"}
        ):
            # Remove the duplicate after right border
            line_chars.pop(box.right_col + 1)

        # Check for duplicate before right_col (e.g., "││" where second is at right_col)
        if (
            box.right_col > 0
            and box.right_col < len(line_chars)
            and box.right_col - 1 >= 0
            and line_chars[box.right_col] in {"│", "║", "┃"}
            and line_chars[box.right_col - 1] in {"│", "║", "┃"}
        ):
            # Replace the duplicate before right border with space (keep position indices stable)
            line_chars[box.right_col - 1] = " "

        # Check for space-separated duplicate before right_col
        # e.g., "│ │" where second is at right_col
        if (
            box.right_col > box.left_col + 2
            and box.right_col < len(line_chars)
            and box.right_col - 2 >= 0
            and line_chars[box.right_col] in {"│", "║", "┃"}
            and line_chars[box.right_col - 1] == " "
            and line_chars[box.right_col - 2] in {"│", "║", "┃"}
        ):
            # Replace the inner duplicate with space
            line_chars[box.right_col - 2] = " "

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
            # Check for duplicate borders immediately after right_col
            if (
                box.right_col + 1 < len(line_chars)
                and line_chars[box.right_col] in {"│", "║", "┃"}
                and line_chars[box.right_col + 1] in {"│", "║", "┃"}
            ):
                # Double border detected - remove the duplicate
                # Find where the duplicate border ends
                dup_end = box.right_col + 1
                while dup_end < len(line_chars) and line_chars[dup_end] in {"│", "║", "┃"}:
                    dup_end += 1
                # Remove duplicate borders, keep only one at right_col
                line_chars = line_chars[: box.right_col + 1] + line_chars[dup_end:]
            # Check for duplicate borders before right_col (inside the box)
            # Handles cases like "││   CLI  │" with extra borders
            if (
                box.right_col > box.left_col + 1
                and box.right_col - 1 >= 0
                and box.right_col - 1 < len(line_chars)
                and line_chars[box.right_col - 1] in {"│", "║", "┃"}
                and line_chars[box.right_col] in {"│", "║", "┃"}
            ):
                # Remove the duplicate border before right_col
                line_chars = line_chars[: box.right_col - 1] + line_chars[box.right_col :]

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

        # Remove any duplicate borders immediately after right_col
        if box.right_col + 1 < len(line_chars):
            # Remove consecutive border chars after right_col
            while box.right_col + 1 < len(line_chars) and line_chars[box.right_col + 1] in {
                "│",
                "║",
                "┃",
            }:
                line_chars.pop(box.right_col + 1)

        # Safety check: ensure i is valid
        if i < len(fixed_lines):
            fixed_lines[i] = "".join(line_chars).rstrip()

    return fixed_lines
