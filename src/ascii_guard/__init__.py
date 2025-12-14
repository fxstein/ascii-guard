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

"""ascii-guard: A zero-dependency Python linter for ASCII art boxes.

This package provides tools for detecting and fixing misaligned ASCII art
boxes in documentation and markdown files.

Public API:
    - lint_file: Lint a file for ASCII art alignment issues
    - fix_file: Fix ASCII art alignment issues in a file
    - detect_boxes: Detect ASCII art boxes in a file
    - validate_box: Validate a single Box object
    - fix_box: Fix a single Box object
    - Box: ASCII art box data structure
    - ValidationError: Validation error representation
    - LintResult: Results from linting a file
    - FixResult: Results from fixing a file
"""

from ascii_guard.detector import detect_boxes
from ascii_guard.fixer import fix_box
from ascii_guard.linter import fix_file, lint_file
from ascii_guard.models import Box, FixResult, LintResult, ValidationError
from ascii_guard.validator import validate_box

__version__ = "2.2.1"
__all__ = [
    "__version__",
    # High-level functions
    "lint_file",
    "fix_file",
    "detect_boxes",
    # Programmatic functions
    "validate_box",
    "fix_box",
    # Data models
    "Box",
    "ValidationError",
    "LintResult",
    "FixResult",
]
