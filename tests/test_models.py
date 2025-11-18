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

"""Tests for data models.

Tests the Box, ValidationError, and LintResult models.
"""

from ascii_guard.models import (
    ALL_BOX_CHARS,
    CORNER_CHARS,
    Box,
    LintResult,
    ValidationError,
)


class TestBox:
    """Test suite for Box model."""

    def test_box_creation(self) -> None:
        """Test creating a Box instance."""
        box = Box(
            top_line=0,
            bottom_line=2,
            left_col=0,
            right_col=10,
            lines=["┌──────────┐", "│ Content  │", "└──────────┘"],
            file_path="test.txt",
        )

        assert box.top_line == 0
        assert box.bottom_line == 2
        assert box.left_col == 0
        assert box.right_col == 10
        assert len(box.lines) == 3
        assert box.file_path == "test.txt"

    def test_box_attributes_types(self) -> None:
        """Test that Box attributes have correct types."""
        box = Box(
            top_line=1,
            bottom_line=3,
            left_col=5,
            right_col=15,
            lines=["line1", "line2"],
            file_path="/path/to/file.txt",
        )

        assert isinstance(box.top_line, int)
        assert isinstance(box.bottom_line, int)
        assert isinstance(box.left_col, int)
        assert isinstance(box.right_col, int)
        assert isinstance(box.lines, list)
        assert isinstance(box.file_path, str)

    def test_box_width_property(self) -> None:
        """Test Box.width property calculation."""
        box = Box(
            top_line=0,
            bottom_line=2,
            left_col=5,
            right_col=15,
            lines=["test"],
            file_path="test.txt",
        )

        # Width is right_col - left_col + 1
        assert box.width == 11

    def test_box_height_property(self) -> None:
        """Test Box.height property calculation."""
        box = Box(
            top_line=10,
            bottom_line=15,
            left_col=0,
            right_col=10,
            lines=["test"],
            file_path="test.txt",
        )

        # Height is bottom_line - top_line + 1
        assert box.height == 6


class TestValidationError:
    """Test suite for ValidationError model."""

    def test_validation_error_creation(self) -> None:
        """Test creating a ValidationError instance."""
        error = ValidationError(
            line=5,
            column=10,
            message="Test error message",
            severity="error",
            fix="Suggested fix",
        )

        assert error.line == 5
        assert error.column == 10
        assert error.message == "Test error message"
        assert error.severity == "error"
        assert error.fix == "Suggested fix"

    def test_validation_error_without_fix(self) -> None:
        """Test ValidationError without a suggested fix."""
        error = ValidationError(
            line=1,
            column=0,
            message="Error without fix",
            severity="warning",
        )

        assert error.fix is None

    def test_validation_error_str(self) -> None:
        """Test string representation of ValidationError."""
        error = ValidationError(
            line=5,
            column=10,
            message="Test error",
            severity="error",
        )

        error_str = str(error)
        # Line 5 becomes "Line 6" (1-indexed for display)
        assert "6" in error_str
        # Column 10 becomes "Col 11" (1-indexed for display)
        assert "11" in error_str
        assert "Test error" in error_str

    def test_validation_error_severities(self) -> None:
        """Test different severity levels."""
        error = ValidationError(
            line=1,
            column=0,
            message="Error severity",
            severity="error",
        )

        warning = ValidationError(
            line=1,
            column=0,
            message="Warning severity",
            severity="warning",
        )

        assert error.severity == "error"
        assert warning.severity == "warning"


class TestLintResult:
    """Test suite for LintResult model."""

    def test_lint_result_creation(self) -> None:
        """Test creating a LintResult instance."""
        result = LintResult(
            file_path="test.txt",
            boxes_found=2,
            errors=[],
            warnings=[],
        )

        assert result.file_path == "test.txt"
        assert result.boxes_found == 2
        assert len(result.errors) == 0
        assert len(result.warnings) == 0

    def test_lint_result_is_clean(self) -> None:
        """Test is_clean property."""
        # Clean result
        clean_result = LintResult(
            file_path="test.txt",
            boxes_found=1,
            errors=[],
            warnings=[],
        )
        assert clean_result.is_clean

        # Result with errors
        error_result = LintResult(
            file_path="test.txt",
            boxes_found=1,
            errors=[ValidationError(line=1, column=0, message="Error", severity="error")],
            warnings=[],
        )
        assert not error_result.is_clean

        # Result with warnings only (not clean - implementation considers warnings as not clean)
        warning_result = LintResult(
            file_path="test.txt",
            boxes_found=1,
            errors=[],
            warnings=[ValidationError(line=1, column=0, message="Warning", severity="warning")],
        )
        assert not warning_result.is_clean  # Warnings also make file not clean

    def test_lint_result_has_errors(self) -> None:
        """Test has_errors property."""
        result_no_errors = LintResult(
            file_path="test.txt",
            boxes_found=1,
            errors=[],
            warnings=[],
        )
        assert not result_no_errors.has_errors

        result_with_errors = LintResult(
            file_path="test.txt",
            boxes_found=1,
            errors=[ValidationError(line=1, column=0, message="Error", severity="error")],
            warnings=[],
        )
        assert result_with_errors.has_errors

    def test_lint_result_has_warnings(self) -> None:
        """Test has_warnings property."""
        result_no_warnings = LintResult(
            file_path="test.txt",
            boxes_found=1,
            errors=[],
            warnings=[],
        )
        assert not result_no_warnings.has_warnings

        result_with_warnings = LintResult(
            file_path="test.txt",
            boxes_found=1,
            errors=[],
            warnings=[ValidationError(line=1, column=0, message="Warning", severity="warning")],
        )
        assert result_with_warnings.has_warnings


class TestBoxCharacterConstants:
    """Test suite for box character constants."""

    def test_corner_chars_defined(self) -> None:
        """Test that corner characters are defined."""
        assert len(CORNER_CHARS) > 0
        assert isinstance(CORNER_CHARS, set)

        # Check for common corners (not including ASCII + style)
        expected_corners = {"┌", "┐", "└", "┘", "╔", "╗", "╚", "╝", "┏", "┓", "┗", "┛"}
        assert expected_corners.issubset(CORNER_CHARS)

    def test_all_box_chars_defined(self) -> None:
        """Test that all box characters are defined."""
        assert len(ALL_BOX_CHARS) > 0
        assert isinstance(ALL_BOX_CHARS, set)

        # Should include corners
        assert CORNER_CHARS.issubset(ALL_BOX_CHARS)

        # Should include common box-drawing chars (not including ASCII - and | style)
        expected_chars = {"─", "│", "═", "║", "━", "┃"}
        assert expected_chars.issubset(ALL_BOX_CHARS)

    def test_corner_chars_in_all_box_chars(self) -> None:
        """Test that corner characters are subset of all box characters."""
        assert CORNER_CHARS.issubset(ALL_BOX_CHARS)
