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

"""Data models for ASCII art boxes and validation errors.

ZERO dependencies - uses only Python stdlib.
"""

from dataclasses import dataclass

# Box-drawing character sets
HORIZONTAL_CHARS = {"─", "═", "━"}
VERTICAL_CHARS = {"│", "║", "┃"}
CORNER_CHARS = {"┌", "┐", "└", "┘", "╔", "╗", "╚", "╝", "┏", "┓", "┗", "┛"}
JUNCTION_CHARS = {"├", "┤", "┬", "┴", "╠", "╣", "╦", "╩", "┼", "╬"}

# Divider characters (for horizontal divider lines within boxes)
LEFT_DIVIDER_CHARS = {"├", "╠"}
RIGHT_DIVIDER_CHARS = {"┤", "╣"}

# Table junction characters (for table column/row separators)
TABLE_COLUMN_JUNCTION_CHARS = {"┬", "┼", "╦", "╬"}  # Used in horizontal separator lines
TOP_JUNCTION_CHARS = {"┬", "╦"}  # Junction pointing down from top border
BOTTOM_JUNCTION_CHARS = {"┴", "╩"}  # Junction pointing up from bottom border

# All box-drawing characters
ALL_BOX_CHARS = HORIZONTAL_CHARS | VERTICAL_CHARS | CORNER_CHARS | JUNCTION_CHARS


@dataclass
class Box:
    """Represents an ASCII art box structure."""

    top_line: int  # Line number of top border (0-indexed)
    bottom_line: int  # Line number of bottom border (0-indexed)
    left_col: int  # Column of left border (0-indexed)
    right_col: int  # Column of right border (0-indexed)
    lines: list[str]  # All lines of the box
    file_path: str  # Source file path

    @property
    def width(self) -> int:
        """Calculate box width."""
        return self.right_col - self.left_col + 1

    @property
    def height(self) -> int:
        """Calculate box height."""
        return self.bottom_line - self.top_line + 1


@dataclass
class ValidationError:
    """Represents a validation error in an ASCII art box."""

    line: int  # Line number (0-indexed)
    column: int  # Column number (0-indexed)
    message: str  # Error description
    severity: str  # 'error' or 'warning'
    fix: str | None = None  # Suggested fix

    def __str__(self) -> str:
        """Format error for display."""
        return f"Line {self.line + 1}, Col {self.column + 1}: {self.message}"


@dataclass
class LintResult:
    """Results from linting a file."""

    file_path: str
    boxes_found: int
    errors: list[ValidationError]
    warnings: list[ValidationError]

    @property
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0

    @property
    def is_clean(self) -> bool:
        """Check if file is clean (no errors or warnings)."""
        return not self.has_errors and not self.has_warnings


@dataclass
class FixResult:
    """Results from fixing a file."""

    file_path: str
    boxes_fixed: int
    lines: list[str]
    modified: bool  # True if file was actually modified

    @property
    def was_modified(self) -> bool:
        """Check if file was modified."""
        return self.modified
