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

"""Directory scanner for finding text files to lint.

ZERO dependencies - uses only Python stdlib.
"""

import os
from pathlib import Path

from ascii_guard.config import Config
from ascii_guard.patterns import match_path


def is_text_file(file_path: Path, max_size_mb: int = 10) -> bool:
    """Check if a file is likely a text file.

    Uses simple heuristics:
    - Check file size (skip huge files)
    - Try to read as UTF-8 (most text files)
    - Check for NULL bytes (binary indicator)

    Args:
        file_path: Path to file to check
        max_size_mb: Maximum file size in MB (0 = unlimited)

    Returns:
        True if file appears to be text, False otherwise
    """
    try:
        # Check size
        if max_size_mb > 0:
            size_mb = file_path.stat().st_size / (1024 * 1024)
            if size_mb > max_size_mb:
                return False

        # Try to read first 8KB as text
        with open(file_path, "rb") as f:
            chunk = f.read(8192)

        # Empty file is considered text
        if not chunk:
            return True

        # Check for NULL bytes (common in binary files)
        if b"\x00" in chunk:
            return False

        # Try to decode as UTF-8
        try:
            chunk.decode("utf-8")
            return True
        except UnicodeDecodeError:
            # Try other common encodings
            try:
                chunk.decode("latin-1")
                return True
            except UnicodeDecodeError:
                return False

    except (OSError, PermissionError):
        return False


def scan_directory(
    directory: Path | str,
    config: Config,
) -> list[Path]:
    """Recursively scan directory for text files matching config filters.

    Args:
        directory: Directory to scan
        config: Config object with file filtering settings

    Returns:
        List of text file paths that should be linted

    Raises:
        FileNotFoundError: If directory doesn't exist
        NotADirectoryError: If path is not a directory
    """
    dir_path = Path(directory).resolve()

    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not dir_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    # Collect all patterns for filtering
    exclude_patterns = config.exclude
    include_patterns = config.include

    # Combine into single list (excludes first, then includes)
    all_patterns = exclude_patterns + include_patterns

    found_files: list[Path] = []

    # Walk directory tree
    for root, dirs, files in os.walk(dir_path, followlinks=config.follow_symlinks):
        root_path = Path(root)

        # Filter out excluded directories (modify dirs in-place to prevent descent)
        filtered_dirs = []
        for dirname in dirs:
            dir_full_path = root_path / dirname
            if not match_path(dir_full_path, all_patterns, dir_path):
                filtered_dirs.append(dirname)

        # Update dirs list to only include non-excluded directories
        dirs[:] = filtered_dirs

        # Process files in this directory
        for filename in files:
            file_path = root_path / filename

            # Check if file matches exclude/include patterns
            if match_path(file_path, all_patterns, dir_path):
                continue  # File is excluded

            # Check file extension if configured
            if config.extensions and not any(filename.endswith(ext) for ext in config.extensions):
                continue  # File extension not in allowed list

            # Check if file is text
            if not is_text_file(file_path, config.max_file_size):
                continue  # Not a text file or too large

            found_files.append(file_path)

    return found_files


def scan_paths(
    paths: list[Path | str],
    config: Config | None = None,
) -> list[Path]:
    """Scan a list of paths (files or directories).

    For files: include them directly if they pass filters
    For directories: recursively scan them

    Args:
        paths: List of file or directory paths
        config: Config object (uses default if None)

    Returns:
        List of file paths to lint
    """
    if config is None:
        config = Config()

    result_files: list[Path] = []

    for path in paths:
        path_obj = Path(path).resolve()

        if not path_obj.exists():
            continue  # Skip non-existent paths

        if path_obj.is_file():
            # Explicit file paths bypass config filters
            result_files.append(path_obj)
        elif path_obj.is_dir():
            # Directory: scan recursively with filters
            dir_files = scan_directory(path_obj, config)
            result_files.extend(dir_files)

    return result_files
