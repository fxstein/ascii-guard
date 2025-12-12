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

"""Detector for ASCII art boxes in files.

ZERO dependencies - uses only Python stdlib.
"""

from pathlib import Path

from ascii_guard.models import ALL_BOX_CHARS, Box


def has_box_drawing_chars(line: str) -> bool:
    """Check if a line contains box-drawing characters."""
    return any(char in ALL_BOX_CHARS for char in line)


def is_in_code_fence(line_idx: int, lines: list[str]) -> bool:
    """Check if a line is within a markdown code fence (```).

    Args:
        line_idx: The line index to check
        lines: All lines in the file

    Returns:
        True if the line is within a code fence
    """
    fence_count = 0
    for i in range(line_idx):
        line = lines[i].strip()
        if line.startswith("```"):
            fence_count += 1

    # Odd fence_count means we're inside a code fence
    return fence_count % 2 == 1


def is_ignore_marker(line: str) -> tuple[str, bool]:
    """Check if a line contains an ascii-guard ignore marker.

    Args:
        line: The line to check

    Returns:
        Tuple of (marker_type, is_marker) where marker_type is one of:
        - "start": <!-- ascii-guard-ignore -->
        - "end": <!-- ascii-guard-ignore-end -->
        - "next": <!-- ascii-guard-ignore-next -->
        - "": not a marker
    """
    stripped = line.strip()

    if "<!-- ascii-guard-ignore-next -->" in stripped:
        return ("next", True)
    if "<!-- ascii-guard-ignore -->" in stripped:
        return ("start", True)
    if "<!-- ascii-guard-ignore-end -->" in stripped:
        return ("end", True)

    return ("", False)


def is_in_ignore_region(line_idx: int, lines: list[str]) -> bool:
    """Check if a line is within an ascii-guard ignore region.

    Ignore regions are marked with:
    - Block: <!-- ascii-guard-ignore --> ... <!-- ascii-guard-ignore-end -->
    - Single: <!-- ascii-guard-ignore-next --> (ignores next box only)

    Args:
        line_idx: The line index to check
        lines: All lines in the file

    Returns:
        True if the line is within an ignore region or is the next line after ignore-next
    """
    # Check for block ignore regions (start/end pairs)
    in_block_ignore = False
    for i in range(line_idx):
        marker_type, is_marker = is_ignore_marker(lines[i])
        if is_marker:
            if marker_type == "start":
                in_block_ignore = True
            elif marker_type == "end":
                in_block_ignore = False

    if in_block_ignore:
        return True

    # Check for single-line ignore-next marker
    # Look at previous non-empty lines to find ignore-next
    for i in range(line_idx - 1, -1, -1):
        line = lines[i].strip()
        if not line:  # Skip empty lines
            continue

        marker_type, is_marker = is_ignore_marker(lines[i])
        if is_marker and marker_type == "next":
            # This is the first non-empty line after ignore-next
            return True

        # Found a non-empty, non-marker line - stop looking
        break

    return False


def find_top_left_corner(line: str, start_col: int = 0) -> int:
    """Find the first top-left corner character in a line after start_col.

    Args:
        line: The line to search
        start_col: Column to start searching from (default: 0)

    Returns:
        Column index of the top-left corner, or -1 if not found
    """
    top_left_corners = {"┌", "╔", "┏"}
    for i in range(start_col, len(line)):
        if line[i] in top_left_corners:
            return i
    return -1


def find_bottom_left_corner(line: str, column: int) -> int:
    """Find a bottom-left corner character at a specific column.

    Args:
        line: The line to search
        column: The column to check

    Returns:
        Column index if bottom-left corner found at that column, otherwise -1
    """
    bottom_left_corners = {"└", "╚", "┗"}
    if column < len(line) and line[column] in bottom_left_corners:
        return column
    return -1


def find_all_top_left_corners(line: str) -> list[int]:
    """Find all top-left corner characters in a line.

    Args:
        line: The line to search

    Returns:
        List of column indices where top-left corners are found
    """
    corners = []
    col = 0
    while col < len(line):
        corner_col = find_top_left_corner(line, col)
        if corner_col == -1:
            break
        corners.append(corner_col)
        col = corner_col + 1
    return corners


def detect_boxes(file_path: str | Path, exclude_code_blocks: bool = False) -> list[Box]:
    """Detect ASCII art boxes in a file.

    This function only detects boxes; it does not validate them.
    Use lint_file() for validation or validate_box() for individual boxes.

    By default, detects boxes everywhere including markdown code fences.
    Optionally skips code blocks if exclude_code_blocks=True.

    Args:
        file_path: Path to file to analyze (str or Path)
        exclude_code_blocks: If True, skip ASCII boxes inside markdown code blocks (```)

    Returns:
        List of detected Box objects

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file cannot be read
        ValueError: If file_path is invalid

    Example:
        >>> boxes = detect_boxes("README.md")
        >>> print(f"Found {len(boxes)} ASCII art boxes")
        >>> for box in boxes:
        ...     print(f"Box at line {box.top_line + 1}: {box.width}x{box.height}")
    """
    file_path_str = str(file_path)
    path = Path(file_path_str)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path_str}")

    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as e:
        raise OSError(f"Cannot read file {file_path_str}: {e}") from e

    # Strip newlines from all lines
    stripped_lines = [line.rstrip("\n") for line in lines]

    boxes: list[Box] = []
    i = 0

    while i < len(stripped_lines):
        line = stripped_lines[i]

        # Skip lines in markdown code fences (if requested)
        if exclude_code_blocks and is_in_code_fence(i, stripped_lines):
            i += 1
            continue

        # ALWAYS skip lines in ignore regions (regardless of exclude_code_blocks setting)
        if is_in_ignore_region(i, stripped_lines):
            i += 1
            continue

        # Find all potential box starts on this line
        left_cols = find_all_top_left_corners(line)
        if not left_cols:
            i += 1
            continue

        # Try to detect a box for each top-left corner found
        for left_col in left_cols:
            # Found a potential box start
            top_line = i

            # Find the bottom of the box
            bottom_line = -1
            for j in range(i + 1, len(stripped_lines)):
                # Skip if bottom line would be in code fence (if requested)
                if exclude_code_blocks and is_in_code_fence(j, stripped_lines):
                    continue

                # ALWAYS skip if bottom line would be in ignore region
                if is_in_ignore_region(j, stripped_lines):
                    continue

                bottom_left = find_bottom_left_corner(stripped_lines[j], left_col)
                if bottom_left == left_col:  # Same column as top-left
                    bottom_line = j
                    break

            if bottom_line == -1:
                # No matching bottom found, skip this potential box
                continue

            # Extract box lines
            box_lines = []
            for j in range(top_line, bottom_line + 1):
                box_lines.append(stripped_lines[j])

            # Calculate right column (from top line)
            top_right_corners = {"┐", "╗", "┓"}
            right_col = -1
            for col_idx in range(left_col + 1, len(line)):
                if line[col_idx] in top_right_corners:
                    right_col = col_idx
                    break

            if right_col == -1:
                # No valid right corner found
                continue

            # Create box object
            box = Box(
                top_line=top_line,
                bottom_line=bottom_line,
                left_col=left_col,
                right_col=right_col,
                lines=box_lines,
                file_path=file_path_str,
            )
            boxes.append(box)

        # Move to next line
        i += 1

    return boxes
