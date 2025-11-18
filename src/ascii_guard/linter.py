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
from ascii_guard.models import LintResult, ValidationError
from ascii_guard.validator import validate_box


def lint_file(file_path: str, exclude_code_blocks: bool = False) -> LintResult:
    """Lint a file for ASCII art alignment issues.

    Args:
        file_path: Path to file to lint
        exclude_code_blocks: If True, skip ASCII boxes inside markdown code blocks

    Returns:
        LintResult with errors and warnings

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    boxes = detect_boxes(file_path, exclude_code_blocks=exclude_code_blocks)

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
        file_path=file_path,
        boxes_found=len(boxes),
        errors=all_errors,
        warnings=all_warnings,
    )


def fix_file(
    file_path: str, dry_run: bool = False, exclude_code_blocks: bool = False
) -> tuple[int, list[str]]:
    """Fix ASCII art alignment issues in a file.

    Args:
        file_path: Path to file to fix
        dry_run: If True, don't write changes to file
        exclude_code_blocks: If True, skip ASCII boxes inside markdown code blocks

    Returns:
        Tuple of (number of boxes fixed, fixed file lines)

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read/written
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read original file
    try:
        with open(path, encoding="utf-8") as f:
            original_lines = f.readlines()
    except OSError as e:
        raise OSError(f"Cannot read file {file_path}: {e}") from e

    # Detect boxes
    boxes = detect_boxes(file_path, exclude_code_blocks=exclude_code_blocks)

    if not boxes:
        # No boxes to fix
        return 0, [line.rstrip("\n") for line in original_lines]

    # Start with original lines
    result_lines = [line.rstrip("\n") for line in original_lines]

    # Fix each box
    boxes_fixed = 0
    for box in boxes:
        # Check if box needs fixing
        errors = validate_box(box)
        if not errors:
            continue  # Box is already correct

        # Fix the box
        fixed_box_lines = fix_box(box)

        # Replace lines in result
        for i, fixed_line in enumerate(fixed_box_lines):
            line_idx = box.top_line + i
            if line_idx < len(result_lines):
                result_lines[line_idx] = fixed_line

        boxes_fixed += 1

    # Write back to file if not dry-run
    if not dry_run and boxes_fixed > 0:
        try:
            with open(path, "w", encoding="utf-8") as f:
                for line in result_lines:
                    f.write(line + "\n")
        except OSError as e:
            raise OSError(f"Cannot write file {file_path}: {e}") from e

    return boxes_fixed, result_lines
