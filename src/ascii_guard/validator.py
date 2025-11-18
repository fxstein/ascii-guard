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
    HORIZONTAL_CHARS,
    LEFT_DIVIDER_CHARS,
    RIGHT_DIVIDER_CHARS,
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


def validate_box(box: Box) -> list[ValidationError]:
    """Validate a box for alignment issues.

    Args:
        box: Box to validate

    Returns:
        List of validation errors found
    """
    errors: list[ValidationError] = []

    # Validate top and bottom border widths match
    top_line = box.lines[0] if box.lines else ""
    bottom_line = box.lines[-1] if len(box.lines) > 1 else ""

    # Count horizontal characters in top border
    top_width = 0
    for i in range(box.left_col, min(len(top_line), box.right_col + 1)):
        if i < len(top_line) and top_line[i] in HORIZONTAL_CHARS:
            top_width += 1

    # Count horizontal characters in bottom border
    bottom_width = 0
    for i in range(box.left_col, min(len(bottom_line), box.right_col + 1)):
        if i < len(bottom_line) and bottom_line[i] in HORIZONTAL_CHARS:
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

        # Skip validation for divider lines (├───┤)
        if is_divider_line(line, box.left_col, box.right_col):
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

    return errors
