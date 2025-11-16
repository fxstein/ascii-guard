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
from typing import NoReturn

from ascii_guard import __version__


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
    lint_parser.add_argument("files", nargs="+", help="Files to lint")
    lint_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Only show errors, no detailed output",
    )

    # Fix command
    fix_parser = subparsers.add_parser("fix", help="Auto-fix ASCII art issues")
    fix_parser.add_argument("files", nargs="+", help="Files to fix")
    fix_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without making changes",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # TODO: Implement lint and fix logic
    print(f"Command '{args.command}' not yet implemented")
    sys.exit(1)


if __name__ == "__main__":
    main()
