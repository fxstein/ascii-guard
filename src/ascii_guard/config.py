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

"""Configuration file parsing for ascii-guard.

Minimal dependencies:
- Python 3.11+: Uses stdlib tomllib (zero dependencies)
- Python 3.10: Uses tomli package (one dependency)
"""

import sys
from dataclasses import dataclass, field
from pathlib import Path

# Version-aware TOML import
# Python 3.11+ has tomllib in stdlib, Python 3.10 needs tomli package
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError as e:
        raise ImportError(
            "tomli package is required for Python 3.10. Install with: pip install ascii-guard"
        ) from e

# Default exclusion patterns (used when no config file exists)
DEFAULT_EXCLUDES = [
    ".git/",
    "node_modules/",
    "__pycache__/",
    ".venv/",
    "venv/",
    ".tox/",
    "build/",
    "dist/",
    ".mypy_cache/",
    ".pytest_cache/",
    ".ruff_cache/",
    "*.egg-info/",
]


@dataclass
class Config:
    """Configuration for ascii-guard linter.

    Attributes:
        extensions: File extensions to scan (empty = all text files)
        exclude: Exclude patterns (gitignore-style)
        include: Include patterns (negation - overrides excludes)
        follow_symlinks: Whether to follow symbolic links
        max_file_size: Maximum file size to scan in MB (0 = unlimited)
    """

    extensions: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=lambda: DEFAULT_EXCLUDES.copy())
    include: list[str] = field(default_factory=list)
    follow_symlinks: bool = False
    max_file_size: int = 10


def find_config_file(start_path: Path | None = None) -> Path | None:
    """Find .ascii-guard.toml or .ascii-guard config file.

    Searches from start_path upward to git root or filesystem root.

    Args:
        start_path: Directory to start search from (default: current directory)

    Returns:
        Path to config file if found, None otherwise
    """
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()

    # Walk up directory tree
    while True:
        # Check for .ascii-guard.toml (preferred)
        config_toml = current / ".ascii-guard.toml"
        if config_toml.exists() and config_toml.is_file():
            return config_toml

        # Check for .ascii-guard (fallback)
        config_plain = current / ".ascii-guard"
        if config_plain.exists() and config_plain.is_file():
            return config_plain

        # Stop at git root
        if (current / ".git").exists():
            break

        # Stop at filesystem root
        parent = current.parent
        if parent == current:
            break

        current = parent

    return None


def load_config(config_path: Path | str | None = None) -> Config:
    """Load configuration from file or use defaults.

    Args:
        config_path: Path to config file (default: auto-detect)

    Returns:
        Config object with loaded or default settings

    Raises:
        FileNotFoundError: If specified config_path doesn't exist
        TOMLDecodeError: If config file has invalid TOML syntax
        ValueError: If config contains invalid values
    """
    # If explicit path provided, use it
    if config_path is not None:
        config_file: Path = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
    else:
        # Auto-detect config file
        config_file_maybe = find_config_file()
        if config_file_maybe is None:
            # No config file found, use defaults
            return Config()
        config_file = config_file_maybe

    # Parse TOML file
    try:
        with open(config_file, "rb") as f:
            data = tomllib.load(f)
    except Exception as e:
        raise ValueError(f"Failed to parse config file {config_file}: {e}") from e

    # Extract [files] section
    files_config = data.get("files", {})

    # Validate known keys in [files] section
    valid_files_keys = {
        "extensions",
        "exclude",
        "include",
        "follow_symlinks",
        "max_file_size",
    }
    unknown_keys = set(files_config.keys()) - valid_files_keys
    if unknown_keys:
        print(f"Warning: Unknown keys in [files] section: {', '.join(unknown_keys)}")

    # Build Config object
    config = Config()

    # Extensions (list of strings)
    if "extensions" in files_config:
        extensions = files_config["extensions"]
        if not isinstance(extensions, list):
            raise ValueError(f"[files] extensions must be a list, got {type(extensions).__name__}")
        if not all(isinstance(ext, str) for ext in extensions):
            raise ValueError("[files] extensions must be a list of strings")
        config.extensions = extensions

    # Exclude patterns (list of strings)
    if "exclude" in files_config:
        exclude = files_config["exclude"]
        if not isinstance(exclude, list):
            raise ValueError(f"[files] exclude must be a list, got {type(exclude).__name__}")
        if not all(isinstance(pattern, str) for pattern in exclude):
            raise ValueError("[files] exclude must be a list of strings")
        # User config overrides defaults completely
        config.exclude = exclude

    # Include patterns (list of strings)
    if "include" in files_config:
        include = files_config["include"]
        if not isinstance(include, list):
            raise ValueError(f"[files] include must be a list, got {type(include).__name__}")
        if not all(isinstance(pattern, str) for pattern in include):
            raise ValueError("[files] include must be a list of strings")
        config.include = include

    # Follow symlinks (boolean)
    if "follow_symlinks" in files_config:
        follow_symlinks = files_config["follow_symlinks"]
        if not isinstance(follow_symlinks, bool):
            raise ValueError(
                f"[files] follow_symlinks must be a boolean, got {type(follow_symlinks).__name__}"
            )
        config.follow_symlinks = follow_symlinks

    # Max file size (integer)
    if "max_file_size" in files_config:
        max_file_size = files_config["max_file_size"]
        if not isinstance(max_file_size, int):
            raise ValueError(
                f"[files] max_file_size must be an integer, got {type(max_file_size).__name__}"
            )
        if max_file_size < 0:
            raise ValueError("[files] max_file_size must be non-negative")
        config.max_file_size = max_file_size

    # Warn about unknown sections (besides [files], [rules], [output])
    valid_sections = {"files", "rules", "output"}
    unknown_sections = set(data.keys()) - valid_sections
    if unknown_sections:
        print(f"Warning: Unknown config sections: {', '.join(unknown_sections)}")

    return config
