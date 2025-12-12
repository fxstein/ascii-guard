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

"""Validator for ASCII art box alignment.

ZERO dependencies - uses only Python stdlib.
"""

from ascii_guard.models import (
    CORNER_CHARS,
    HORIZONTAL_CHARS,
    LEFT_DIVIDER_CHARS,
    RIGHT_DIVIDER_CHARS,
    TABLE_COLUMN_JUNCTION_CHARS,
    VERTICAL_CHARS,
    Box,
    ValidationError,
)


def is_divider_line(line: str, left_col: int, right_col: int) -> bool:
    """Check if a line is a horizontal divider within a box.

    A divider line has left divider char (├, ╠), horizontal chars, and right divider char (┤, ╣).

    Args:
        line: The line to check
        left_col: Column index of the left border
        right_col: Column index of the right border

    Returns:
        True if the line is a divider line
    """
    if left_col >= len(line) or right_col >= len(line):
        return False

    left_char = line[left_col]
    right_char = line[right_col]

    # Check if both ends have divider characters
    if left_char not in LEFT_DIVIDER_CHARS or right_char not in RIGHT_DIVIDER_CHARS:
        return False

    # Check that the middle portion contains only horizontal chars (and optional spaces)
    for i in range(left_col + 1, right_col):
        if i < len(line):
            char = line[i]
            if char not in HORIZONTAL_CHARS and char != " ":
                return False

    return True


def is_table_separator_line(line: str, left_col: int, right_col: int) -> bool:
    """Check if a line is a table column separator within a box.

    A table separator line has left divider char (├, ╠), horizontal chars with
    column junction chars (┬, ┼, ╦, ╬), and right divider char (┤, ╣).

    This function is tolerant of extra characters after the right border.

    Args:
        line: The line to check
        left_col: Column index of the left border
        right_col: Column index of the right border

    Returns:
        True if the line is a table separator line
    """
    if left_col >= len(line):
        return False

    left_char = line[left_col]

    # Check if left end has divider character
    if left_char not in LEFT_DIVIDER_CHARS:
        return False

    # Find the right divider character (might be at right_col or right_col-1)
    # This handles cases where there's an extra character after the divider
    actual_right_col = -1
    for offset in [0, -1]:  # Check right_col, then right_col-1
        check_col = right_col + offset
        if 0 <= check_col < len(line) and line[check_col] in RIGHT_DIVIDER_CHARS:
            actual_right_col = check_col
            break

    if actual_right_col == -1:
        return False

    # Check that the middle portion contains horizontal chars and/or table junction chars
    has_junction = False
    for i in range(left_col + 1, actual_right_col):
        if i < len(line):
            char = line[i]
            if char in TABLE_COLUMN_JUNCTION_CHARS:
                has_junction = True
            elif char not in HORIZONTAL_CHARS and char != " ":
                return False

    # Table separator must have at least one junction character
    return has_junction


def get_column_positions(box: Box) -> list[int]:
    """Detect column separator positions in a table box.

    Scans the box to find consistent vertical column separator positions by
    looking for ┬ in top border, │ in content rows, and ┼ in middle separators.

    Args:
        box: Box to analyze

    Returns:
        List of column positions (relative to box left_col) where separators exist
    """
    from ascii_guard.models import TOP_JUNCTION_CHARS

    column_positions = set()

    # Check top border for ┬ junction points
    if box.lines:
        top_line = box.lines[0]
        for i, char in enumerate(top_line):
            if char in TOP_JUNCTION_CHARS:
                column_positions.add(i)

    # Note: We intentionally DO NOT check content lines for │ separators
    # because that causes false positives for nested boxes (inner box borders
    # interpreted as columns of outer box). We only trust top junctions (┬)
    # and middle separators (┼) for defining table columns.

    # Check for ┼ in middle separator lines
    for line in box.lines[1:-1]:
        for i, char in enumerate(line):
            if char in TABLE_COLUMN_JUNCTION_CHARS:
                column_positions.add(i)

    # Return sorted list of column positions (relative to left edge)
    return sorted(
        [
            pos - box.left_col
            for pos in column_positions
            if pos > box.left_col and pos < box.right_col
        ]
    )


def validate_box(box: Box) -> list[ValidationError]:
    """Validate a single ASCII art box.

    Args:
        box: Box object to validate

    Returns:
        List of ValidationError objects (empty if box is valid)

    Example:
        >>> boxes = detect_boxes("README.md")
        >>> for box in boxes:
        ...     errors = validate_box(box)
        ...     if errors:
        ...         print(f"Box has {len(errors)} validation errors")
    """
    errors: list[ValidationError] = []

    # Validate top and bottom border widths match
    top_line = box.lines[0] if box.lines else ""
    bottom_line = box.lines[-1] if len(box.lines) > 1 else ""

    # Count horizontal characters in top border (including junction points and any non-space chars)
    # This ensures we handle boxes with labels or arrows (like ▼) correctly
    top_width = 0
    for i in range(box.left_col, min(len(top_line), box.right_col + 1)):
        if i < len(top_line):
            char = top_line[i]
            # Count effectively solid parts of the border (not spaces, not corners)
            # We include JUNCTION_CHARS because they are part of the border length
            # We exclude CORNER_CHARS because they define the endpoints
            if char != " " and char not in CORNER_CHARS:
                top_width += 1

    # Count horizontal characters in bottom border
    bottom_width = 0
    for i in range(box.left_col, min(len(bottom_line), box.right_col + 1)):
        if i < len(bottom_line):
            char = bottom_line[i]
            if char != " " and char not in CORNER_CHARS:
                bottom_width += 1

    # Check if widths match
    if top_width != bottom_width and top_width > 0 and bottom_width > 0:
        errors.append(
            ValidationError(
                line=box.bottom_line,
                column=box.left_col,
                message=(
                    f"Bottom border width ({bottom_width}) doesn't match "
                    f"top border width ({top_width})"
                ),
                severity="error",
                fix="Adjust bottom border to match top border width",
            )
        )

    # Validate vertical alignment of left and right borders
    for i, line in enumerate(box.lines[1:-1], start=1):  # Skip top and bottom
        actual_line_num = box.top_line + i

        # Skip validation for divider lines (├───┤) and table separator lines (├─┬─┤)
        if is_divider_line(line, box.left_col, box.right_col):
            continue
        if is_table_separator_line(line, box.left_col, box.right_col):
            # Check for extra characters after table separator
            # Find where the actual right divider is
            actual_right_col = -1
            for offset in [0, -1]:
                check_col = box.right_col + offset
                if 0 <= check_col < len(line) and line[check_col] in RIGHT_DIVIDER_CHARS:
                    actual_right_col = check_col
                    break

            if actual_right_col != -1:
                line_stripped = line.rstrip()
                if len(line_stripped) > actual_right_col + 1:
                    errors.append(
                        ValidationError(
                            line=actual_line_num,
                            column=actual_right_col + 1,
                            message=(
                                f"Table separator has extra characters after right border "
                                f"(length {len(line_stripped)}, expected {actual_right_col + 1})"
                            ),
                            severity="error",
                            fix="Remove extra characters after right border",
                        )
                    )
            continue

        # Check left border
        if box.left_col < len(line):
            char = line[box.left_col]
            if char not in VERTICAL_CHARS and char != " ":
                errors.append(
                    ValidationError(
                        line=actual_line_num,
                        column=box.left_col,
                        message=(
                            f"Left border misaligned: expected vertical character, got '{char}'"
                        ),
                        severity="error",
                        fix="Replace with vertical border character │",
                    )
                )
        else:
            errors.append(
                ValidationError(
                    line=actual_line_num,
                    column=box.left_col,
                    message="Left border missing: line too short",
                    severity="error",
                    fix="Extend line to include left border",
                )
            )

        # Check right border
        if box.right_col < len(line):
            char = line[box.right_col]
            if char not in VERTICAL_CHARS and char != " ":
                errors.append(
                    ValidationError(
                        line=actual_line_num,
                        column=box.right_col,
                        message=(
                            f"Right border misaligned: expected vertical character, got '{char}'"
                        ),
                        severity="error",
                        fix="Replace with vertical border character │",
                    )
                )

            # Check if line has extra content/borders after right_col
            # Only validate the slice of the line that belongs to this box
            # (handles multiple boxes on same line)
            line_stripped = line.rstrip()
            if len(line_stripped) > box.right_col + 1:
                # Check if extra characters are outside this box's range
                # (could be another box on the same line)
                extra_content = line_stripped[box.right_col + 1 :].lstrip()
                # If extra content starts with a box character (corner or vertical),
                # it's likely another box on the same line
                box_chars = {"┌", "└", "╔", "╚", "┏", "┗"} | VERTICAL_CHARS
                if not any(extra_content.startswith(c) for c in box_chars):
                    errors.append(
                        ValidationError(
                            line=actual_line_num,
                            column=box.right_col + 1,
                            message=(
                                f"Line has extra characters after right border "
                                f"(length {len(line_stripped)}, expected {box.right_col + 1})"
                            ),
                            severity="error",
                            fix="Remove extra characters after right border",
                        )
                    )
        else:
            errors.append(
                ValidationError(
                    line=actual_line_num,
                    column=box.right_col,
                    message="Right border missing: line too short",
                    severity="error",
                    fix="Extend line to include right border",
                )
            )

    # Check for missing bottom junction points in tables
    column_positions = get_column_positions(box)
    if column_positions and len(box.lines) >= 2:
        from ascii_guard.models import BOTTOM_JUNCTION_CHARS

        bottom_line = box.lines[-1]
        for col_pos in column_positions:
            # col_pos is relative to box, convert to absolute position
            abs_col = box.left_col + col_pos
            if abs_col < len(bottom_line):
                char_at_pos = bottom_line[abs_col]
                # Check if bottom junction is missing
                if char_at_pos not in BOTTOM_JUNCTION_CHARS and char_at_pos in HORIZONTAL_CHARS:
                    msg = (
                        f"Bottom border missing junction point at column {abs_col + 1} "
                        f"(expected ┴, got '{char_at_pos}')"
                    )
                    errors.append(
                        ValidationError(
                            line=box.bottom_line + 1,  # 1-indexed
                            column=abs_col + 1,  # 1-indexed
                            message=msg,
                            severity="warning",
                            fix="Replace horizontal line with bottom junction (┴)",
                        )
                    )

    return errors
