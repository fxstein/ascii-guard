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

"""Pattern matching for file filtering (gitignore-style patterns).

ZERO dependencies - uses only Python stdlib (fnmatch + pathlib).
"""

import fnmatch
from pathlib import Path, PurePosixPath


def match_path(
    path: Path | str,
    patterns: list[str],
    base_path: Path | str | None = None,
) -> bool:
    """Check if a path matches any of the given patterns.

    Supports gitignore-style patterns (subset):
    - `*.ext` - Match files with extension
    - `dir/` - Match directory
    - `**/pattern/**` - Match anywhere in tree
    - `!pattern` - Negation (include override)

    Args:
        path: Path to check
        patterns: List of patterns to match against
        base_path: Base path for relative pattern matching (default: current dir)

    Returns:
        True if path should be excluded (matches pattern), False if included
    """
    if not patterns:
        return False

    path_obj = Path(path).resolve()
    base_obj = Path(base_path).resolve() if base_path is not None else Path.cwd().resolve()

    # Make path relative to base for pattern matching
    try:
        rel_path = path_obj.relative_to(base_obj)
    except ValueError:
        # Path is not relative to base, use absolute path
        rel_path = path_obj

    # Convert to POSIX path for consistent pattern matching
    posix_path = PurePosixPath(rel_path)
    path_str = str(posix_path)
    path_parts = posix_path.parts

    # Check if path is a directory (check original path object)
    is_directory = path_obj.is_dir()

    # Process patterns in order (later patterns override earlier ones)
    excluded = False

    for pattern in patterns:
        # Skip empty patterns and comments
        if not pattern or pattern.startswith("#"):
            continue

        # Check for negation (include override)
        is_negation = pattern.startswith("!")
        if is_negation:
            pattern = pattern[1:]  # Remove ! prefix

        # Match the pattern
        matched = _match_single_pattern(pattern, path_str, path_parts, is_directory)

        if matched:
            # If negation, include (not excluded)
            # If not negation, exclude
            excluded = not is_negation

    return excluded


def _match_single_pattern(
    pattern: str,
    path_str: str,
    path_parts: tuple[str, ...],
    is_directory: bool,
) -> bool:
    """Match a single pattern against a path.

    Args:
        pattern: Pattern to match (without negation prefix)
        path_str: Path as string (POSIX format)
        path_parts: Path components as tuple
        is_directory: Whether the path is a directory

    Returns:
        True if pattern matches, False otherwise
    """
    # Directory-specific pattern (ends with /)
    # This matches the directory itself AND all contents
    if pattern.endswith("/"):
        dir_pattern = pattern.rstrip("/")

        # Check if path IS the directory
        if is_directory:
            # Match against directory itself
            if fnmatch.fnmatch(path_str, dir_pattern):
                return True
            for part in path_parts:
                if fnmatch.fnmatch(part, dir_pattern):
                    return True

        # Check if path is INSIDE the matched directory
        # E.g., docs/file.txt matches pattern docs/
        for i in range(len(path_parts)):
            parent_path = "/".join(path_parts[: i + 1])
            if fnmatch.fnmatch(parent_path, dir_pattern):
                # Path is inside this directory
                return True

        return False

    # Pattern with ** matches anywhere in tree
    if "**" in pattern:
        # Convert ** pattern to regex-like matching
        # E.g., "**/node_modules/**" matches any path containing "node_modules"

        # Simple case: **/pattern matches if pattern is anywhere in path
        if pattern.startswith("**/"):
            sub_pattern = pattern[3:]  # Remove **/
            # Match any path component
            for part in path_parts:
                if fnmatch.fnmatch(part, sub_pattern):
                    return True
            # Also try matching full path from any level
            for i in range(len(path_parts)):
                sub_path = "/".join(path_parts[i:])
                if fnmatch.fnmatch(sub_path, sub_pattern):
                    return True
            return False

        # Pattern ending with /** matches directory and all contents
        if pattern.endswith("/**"):
            dir_pattern = pattern[:-3]  # Remove /**
            # Match if directory is in path
            for i in range(len(path_parts)):
                sub_path = "/".join(path_parts[: i + 1])
                if fnmatch.fnmatch(sub_path, dir_pattern):
                    return True
            return False

        # Complex ** pattern in middle
        # For simplicity, convert ** to * for fnmatch
        # This is not perfect but covers most cases
        simplified = pattern.replace("**/", "*/").replace("/**", "/*")
        return bool(fnmatch.fnmatch(path_str, simplified))

    # Simple pattern matching
    # Try matching against full path
    if fnmatch.fnmatch(path_str, pattern):
        return True

    # Try matching against just the filename
    if path_parts:
        filename = path_parts[-1]
        if fnmatch.fnmatch(filename, pattern):
            return True

    # Try matching against any path component
    return any(fnmatch.fnmatch(part, pattern) for part in path_parts)


def filter_paths(
    paths: list[Path | str],
    exclude_patterns: list[str],
    include_patterns: list[str] | None = None,
    base_path: Path | str | None = None,
) -> list[Path]:
    """Filter a list of paths based on exclude/include patterns.

    Args:
        paths: List of paths to filter
        exclude_patterns: Patterns for exclusion
        include_patterns: Patterns for inclusion (override excludes)
        base_path: Base path for relative pattern matching

    Returns:
        List of Path objects that should be included
    """
    if include_patterns is None:
        include_patterns = []

    # Combine patterns: excludes first, then includes (for negation)
    all_patterns = exclude_patterns + include_patterns

    filtered = []
    for path in paths:
        path_obj = Path(path)
        if not match_path(path_obj, all_patterns, base_path):
            filtered.append(path_obj)

    return filtered
