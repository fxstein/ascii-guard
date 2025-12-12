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

"""Main linter interface for ASCII art validation and fixing.

ZERO dependencies - uses only Python stdlib.
"""

from pathlib import Path

from ascii_guard.detector import detect_boxes
from ascii_guard.fixer import fix_box
from ascii_guard.models import FixResult, LintResult, ValidationError
from ascii_guard.validator import validate_box


def lint_file(file_path: str | Path, exclude_code_blocks: bool = False) -> LintResult:
    """Lint a file for ASCII art alignment issues.

    Args:
        file_path: Path to file to lint (str or Path)
        exclude_code_blocks: If True, skip ASCII boxes inside markdown code blocks

    Returns:
        LintResult with errors and warnings

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file cannot be read
        ValueError: If file_path is invalid

    Example:
        >>> result = lint_file("README.md")
        >>> if result.has_errors:
        ...     print(f"Found {len(result.errors)} errors")
    """
    file_path_str = str(file_path)
    boxes = detect_boxes(file_path_str, exclude_code_blocks=exclude_code_blocks)

    all_errors: list[ValidationError] = []
    all_warnings: list[ValidationError] = []

    for box in boxes:
        validation_errors = validate_box(box)

        for error in validation_errors:
            if error.severity == "error":
                all_errors.append(error)
            elif error.severity == "warning":
                all_warnings.append(error)

    return LintResult(
        file_path=file_path_str,
        boxes_found=len(boxes),
        errors=all_errors,
        warnings=all_warnings,
    )


def fix_file(
    file_path: str | Path, dry_run: bool = False, exclude_code_blocks: bool = False
) -> FixResult:
    """Fix ASCII art alignment issues in a file.

    Args:
        file_path: Path to file to fix (str or Path)
        dry_run: If True, don't write changes to file (returns fixed lines)
        exclude_code_blocks: If True, skip ASCII boxes inside markdown code blocks

    Returns:
        FixResult with fixed lines and metadata

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file cannot be read/written
        ValueError: If file_path is invalid

    Example:
        >>> result = fix_file("README.md", dry_run=True)
        >>> print(f"Would fix {result.boxes_fixed} boxes")
        >>> if not result.dry_run:
        ...     print(f"Fixed {result.boxes_fixed} boxes in {result.file_path}")
    """
    file_path_str = str(file_path)
    path = Path(file_path_str)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path_str}")

    # Read original file
    try:
        with open(path, encoding="utf-8") as f:
            original_lines = f.readlines()
    except OSError as e:
        raise OSError(f"Cannot read file {file_path_str}: {e}") from e

    # Detect boxes
    boxes = detect_boxes(file_path_str, exclude_code_blocks=exclude_code_blocks)

    if not boxes:
        # No boxes to fix
        return FixResult(
            file_path=file_path_str,
            boxes_fixed=0,
            lines=[line.rstrip("\n") for line in original_lines],
            modified=False,
        )

    # Start with original lines
    result_lines = [line.rstrip("\n") for line in original_lines]

    # Fix each box
    boxes_fixed = 0
    # Track which lines have been modified and by which boxes
    modified_lines: dict[int, str] = {}  # line_idx -> fixed_line

    for box in boxes:
        # Check if box needs fixing
        errors = validate_box(box)

        # Also check if bottom border is non-continuous (has spaces in middle)
        # or if there are duplicate borders in middle lines
        # This should be fixed even if validator doesn't complain
        needs_fixing = bool(errors)
        if not needs_fixing and len(box.lines) > 1:
            bottom_line = box.lines[-1]
            # Check if bottom border has spaces between left_col and right_col
            # that are not at the edges
            has_gap = False
            for i in range(box.left_col + 1, min(len(bottom_line), box.right_col)):
                if i < len(bottom_line):
                    char = bottom_line[i]
                    # If we find a space that's not at the very end, it's a gap
                    if char == " ":
                        # Check if there are border chars before and after
                        has_before = False
                        has_after = False
                        for j in range(box.left_col + 1, i):
                            if j < len(bottom_line) and bottom_line[j] not in {" ", "│", "║", "┃"}:
                                has_before = True
                                break
                        for j in range(i + 1, box.right_col):
                            if j < len(bottom_line) and bottom_line[j] not in {" ", "│", "║", "┃"}:
                                has_after = True
                                break
                        if has_before and has_after:
                            has_gap = True
                            break
            needs_fixing = has_gap

            # Also check for duplicate borders in middle lines and at boundaries
            if not needs_fixing:
                for i in range(1, len(box.lines) - 1):
                    line = box.lines[i]
                    # Check for consecutive border chars at boundaries
                    # Start checking from left_col - 1 to catch duplicates before the box
                    for j in range(box.left_col - 1, min(len(line), box.right_col + 2)):
                        if j < 0:
                            continue

                        # Check for duplicate borders (││)
                        has_dup = (
                            j < len(line)
                            and line[j] in {"│", "║", "┃"}
                            and j + 1 < len(line)
                            and line[j + 1] in {"│", "║", "┃"}
                        )
                        # Check position validity
                        is_at_border = (
                            j == box.left_col - 1  # Before left border
                            or j == box.left_col  # At left border (dup inside)
                            or j == box.right_col  # At right border (dup outside)
                            or j == box.right_col - 1  # Inside right border (dup at border)
                        )
                        if has_dup and is_at_border:
                            needs_fixing = True
                            break

                    # Check for "│ │" pattern at right border (space separated duplicate)
                    # This handles artifacts like "...│ │" where the inner │ is a leftover
                    if (
                        not needs_fixing
                        and box.right_col > box.left_col + 2
                        and box.right_col < len(line)
                        and line[box.right_col] in {"│", "║", "┃"}
                        and line[box.right_col - 1] == " "
                        and line[box.right_col - 2] in {"│", "║", "┃"}
                    ):
                        needs_fixing = True

                    if needs_fixing:
                        break

        if not needs_fixing:
            continue  # Box is already correct

        # Fix the box
        fixed_box_lines = fix_box(box)

        # Replace lines in result, merging fixes for boxes on the same line
        for i, fixed_line in enumerate(fixed_box_lines):
            line_idx = box.top_line + i
            if line_idx < len(result_lines):
                if line_idx in modified_lines:
                    # This line was already modified by another box - merge the fixes
                    # Take the maximum length and merge character by character
                    existing_line = modified_lines[line_idx]
                    merged_line = list(existing_line)

                    # Extend merged_line if fixed_line is longer
                    if len(fixed_line) > len(merged_line):
                        merged_line.extend([" "] * (len(fixed_line) - len(merged_line)))

                    # Merge: use fixed_line characters ONLY in the box's column range
                    # Each box should only update its own boundaries, not touch other boxes' areas
                    # We expand range slightly to allow fixing duplicates near borders
                    start_col = max(0, box.left_col - 1)
                    end_col = min(box.right_col + 2, len(fixed_line))

                    for col in range(start_col, end_col):
                        if col < len(fixed_line) and col < len(merged_line):
                            # Only write if this column is not owned by another box
                            # (unless it's inside THIS box)
                            is_owned_by_other = False
                            if col < box.left_col or col > box.right_col:
                                for other_box in boxes:
                                    if other_box is box:
                                        continue
                                    if (
                                        other_box.top_line <= line_idx <= other_box.bottom_line
                                        and other_box.left_col <= col <= other_box.right_col
                                    ):
                                        is_owned_by_other = True
                                        break

                            if is_owned_by_other:
                                continue

                            char = fixed_line[col]
                            existing_char = merged_line[col]
                            # Check if this is a corner character
                            if char in {"┌", "┐", "└", "┘", "╔", "╗", "╚", "╝"}:
                                # Only overwrite if the existing char is not a corner
                                # or if this is the right corner for this box
                                if (
                                    existing_char not in {"┌", "┐", "└", "┘", "╔", "╗", "╚", "╝"}
                                    or col == box.right_col
                                ):
                                    merged_line[col] = char
                            else:
                                # Non-corner character - use the fixed_line character
                                merged_line[col] = char

                    # Remove any duplicate corners that might have been created
                    # Look for corner chars immediately after any box's right_col on this line
                    # We need to check all boxes that affect this line
                    max_right_col = box.right_col
                    for other_box in boxes:
                        if other_box.top_line <= line_idx <= other_box.bottom_line:
                            max_right_col = max(max_right_col, other_box.right_col)

                    # Remove duplicate corners after the maximum right_col
                    for col in range(max_right_col + 1, min(len(merged_line), max_right_col + 10)):
                        if col < len(merged_line) and merged_line[col] in {
                            "┌",
                            "┐",
                            "└",
                            "┘",
                            "╔",
                            "╗",
                            "╚",
                            "╝",
                        }:
                            # Remove duplicate corner
                            merged_line[col] = " "

                    modified_lines[line_idx] = "".join(merged_line)
                else:
                    # First box to modify this line
                    modified_lines[line_idx] = fixed_line

        boxes_fixed += 1

    # Apply all modifications to result_lines
    for line_idx, fixed_line in modified_lines.items():
        if line_idx < len(result_lines):
            result_lines[line_idx] = fixed_line

    # Write back to file if not dry-run
    if not dry_run and boxes_fixed > 0:
        try:
            with open(path, "w", encoding="utf-8") as f:
                for line in result_lines:
                    f.write(line + "\n")
        except OSError as e:
            raise OSError(f"Cannot write file {file_path_str}: {e}") from e

    return FixResult(
        file_path=file_path_str,
        boxes_fixed=boxes_fixed,
        lines=result_lines,
        modified=not dry_run and boxes_fixed > 0,
    )
