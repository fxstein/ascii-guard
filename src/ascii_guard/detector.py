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


def find_top_left_corner(line: str) -> int:
    """Find the first top-left corner character in a line."""
    top_left_corners = {"┌", "╔", "┏"}
    for i, char in enumerate(line):
        if char in top_left_corners:
            return i
    return -1


def find_bottom_left_corner(line: str) -> int:
    """Find the first bottom-left corner character in a line."""
    bottom_left_corners = {"└", "╚", "┗"}
    for i, char in enumerate(line):
        if char in bottom_left_corners:
            return i
    return -1


def detect_boxes(file_path: str) -> list[Box]:
    """Detect ASCII art boxes in a file.

    Args:
        file_path: Path to file to analyze

    Returns:
        List of detected Box objects

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as e:
        raise OSError(f"Cannot read file {file_path}: {e}") from e

    boxes: list[Box] = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip("\n")

        # Look for top-left corner
        left_col = find_top_left_corner(line)
        if left_col == -1:
            i += 1
            continue

        # Found a potential box start
        top_line = i

        # Find the bottom of the box
        bottom_line = -1
        for j in range(i + 1, len(lines)):
            bottom_left = find_bottom_left_corner(lines[j])
            if bottom_left == left_col:  # Same column as top-left
                bottom_line = j
                break

        if bottom_line == -1:
            # No matching bottom found, skip this potential box
            i += 1
            continue

        # Extract box lines
        box_lines = []
        for j in range(top_line, bottom_line + 1):
            box_lines.append(lines[j].rstrip("\n"))

        # Calculate right column (from top line)
        top_right_corners = {"┐", "╗", "┓"}
        right_col = -1
        for col_idx, char in enumerate(line):
            if char in top_right_corners and col_idx > left_col:
                right_col = col_idx
                break

        if right_col == -1:
            # No valid right corner found
            i += 1
            continue

        # Create box object
        box = Box(
            top_line=top_line,
            bottom_line=bottom_line,
            left_col=left_col,
            right_col=right_col,
            lines=box_lines,
            file_path=file_path,
        )
        boxes.append(box)

        # Move past this box
        i = bottom_line + 1

    return boxes
