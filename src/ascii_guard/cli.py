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

"""Command-line interface for ascii-guard.

ZERO dependencies - uses only Python stdlib (argparse).
"""

import argparse
import sys
from pathlib import Path
from typing import NoReturn

from ascii_guard import __version__
from ascii_guard.config import load_config
from ascii_guard.linter import fix_file, lint_file
from ascii_guard.scanner import scan_paths

# ANSI color codes (no colorama needed - stdlib only)
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"


def print_error(message: str) -> None:
    """Print error message in red."""
    print(f"{COLOR_RED}✗ {message}{COLOR_RESET}", file=sys.stderr)


def print_success(message: str) -> None:
    """Print success message in green."""
    print(f"{COLOR_GREEN}✓ {message}{COLOR_RESET}")


def print_warning(message: str) -> None:
    """Print warning message in yellow."""
    print(f"{COLOR_YELLOW}⚠ {message}{COLOR_RESET}")


def print_info(message: str) -> None:
    """Print info message in blue."""
    print(f"{COLOR_BLUE}ℹ {message}{COLOR_RESET}")


def cmd_lint(args: argparse.Namespace) -> int:
    """Execute lint command."""
    exit_code = 0
    total_errors = 0
    total_warnings = 0
    total_boxes = 0

    # Load config
    config = load_config(args.config) if hasattr(args, "config") and args.config else None

    # Show config if requested
    if hasattr(args, "show_config") and args.show_config:
        if config:
            print(f"{COLOR_BLUE}Config loaded from: {args.config}{COLOR_RESET}")
            print(f"  Extensions: {config.extensions or 'all text files'}")
            print(f"  Exclude: {config.exclude}")
            print(f"  Include: {config.include}")
            print(f"  Follow symlinks: {config.follow_symlinks}")
            print(f"  Max file size: {config.max_file_size}MB")
        else:
            print(f"{COLOR_BLUE}Using default config (no .ascii-guard.toml found){COLOR_RESET}")
        print()

    # Check that input paths exist
    for input_path in args.files:
        path = Path(input_path)
        if not path.exists():
            print_error(f"Path not found: {input_path}")
            exit_code = 1

    if exit_code != 0:
        return exit_code

    # Scan paths (handles both files and directories)
    file_paths = scan_paths(args.files, config)

    if not file_paths:
        print_warning("No files found to lint")
        return 0

    for file_path in file_paths:
        try:
            exclude_code_blocks = getattr(args, "exclude_code_blocks", False)
            result = lint_file(str(file_path), exclude_code_blocks=exclude_code_blocks)
            total_boxes += result.boxes_found

            if not args.quiet:
                print(f"\n{COLOR_BOLD}Checking {file_path}...{COLOR_RESET}")
                print(f"  Found {result.boxes_found} ASCII box(es)")

            if result.has_errors:
                total_errors += len(result.errors)
                exit_code = 1

                if not args.quiet:
                    for error in result.errors:
                        print_error(f"  {error}")

            if result.has_warnings:
                total_warnings += len(result.warnings)

                if not args.quiet:
                    for warning in result.warnings:
                        print_warning(f"  {warning}")

            if result.is_clean and not args.quiet:
                print_success("  No issues found")

        except Exception as e:
            print_error(f"Error processing {file_path}: {e}")
            exit_code = 1

    # Summary
    print(f"\n{COLOR_BOLD}Summary:{COLOR_RESET}")
    print(f"  Files checked: {len(file_paths)}")
    print(f"  Boxes found: {total_boxes}")

    if total_errors > 0:
        print_error(f"  Errors: {total_errors}")
    else:
        print_success("  Errors: 0")

    if total_warnings > 0:
        print_warning(f"  Warnings: {total_warnings}")

    return exit_code


def cmd_fix(args: argparse.Namespace) -> int:
    """Execute fix command."""
    exit_code = 0
    total_fixed = 0

    # Load config
    config = load_config(args.config) if hasattr(args, "config") and args.config else None

    # Check that input paths exist
    for input_path in args.files:
        path = Path(input_path)
        if not path.exists():
            print_error(f"Path not found: {input_path}")
            exit_code = 1

    if exit_code != 0:
        return exit_code

    # Scan paths (handles both files and directories)
    file_paths = scan_paths(args.files, config)

    if not file_paths:
        print_warning("No files found to fix")
        return 0

    for file_path in file_paths:
        try:
            exclude_code_blocks = getattr(args, "exclude_code_blocks", False)
            result = fix_file(
                str(file_path), dry_run=args.dry_run, exclude_code_blocks=exclude_code_blocks
            )
            total_fixed += result.boxes_fixed

            if result.boxes_fixed > 0:
                if args.dry_run:
                    print_info(f"{file_path}: Would fix {result.boxes_fixed} box(es)")
                else:
                    print_success(f"{file_path}: Fixed {result.boxes_fixed} box(es)")
            else:
                print_success(f"{file_path}: No fixes needed")

        except Exception as e:
            print_error(f"Error processing {file_path}: {e}")
            exit_code = 1

    # Summary
    print(f"\n{COLOR_BOLD}Summary:{COLOR_RESET}")
    print(f"  Files processed: {len(file_paths)}")

    if args.dry_run:
        print_info(f"  Boxes that would be fixed: {total_fixed}")
    else:
        print_success(f"  Boxes fixed: {total_fixed}")

    return exit_code


def main() -> NoReturn:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="ascii-guard",
        description="Lint and fix ASCII art boxes in documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Lint command
    lint_parser = subparsers.add_parser("lint", help="Check files for ASCII art issues")
    lint_parser.add_argument("files", nargs="+", help="Files or directories to lint")
    lint_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Only show errors, no detailed output",
    )
    lint_parser.add_argument(
        "--config",
        type=str,
        help="Path to config file (default: auto-detect .ascii-guard.toml)",
    )
    lint_parser.add_argument(
        "--show-config",
        action="store_true",
        help="Show effective configuration and exit",
    )
    lint_parser.add_argument(
        "--exclude-code-blocks",
        action="store_true",
        help="Skip ASCII boxes inside markdown code blocks (```)",
    )

    # Fix command
    fix_parser = subparsers.add_parser("fix", help="Auto-fix ASCII art issues")
    fix_parser.add_argument("files", nargs="+", help="Files or directories to fix")
    fix_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without making changes",
    )
    fix_parser.add_argument(
        "--config",
        type=str,
        help="Path to config file (default: auto-detect .ascii-guard.toml)",
    )
    fix_parser.add_argument(
        "--exclude-code-blocks",
        action="store_true",
        help="Skip ASCII boxes inside markdown code blocks (```)",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Execute command
    if args.command == "lint":
        exit_code = cmd_lint(args)
    elif args.command == "fix":
        exit_code = cmd_fix(args)
    else:
        parser.print_help()
        exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
