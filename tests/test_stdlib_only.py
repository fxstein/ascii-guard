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

"""Tests to verify ZERO runtime dependencies.

This is a critical test suite that ensures ascii-guard only uses Python stdlib.
NO external packages should be imported at runtime.
"""

import ast
import sys
from pathlib import Path


class TestStdlibOnly:
    """Verify that ascii-guard only uses Python standard library."""

    def test_no_external_imports_in_package(self) -> None:
        """Test that no external packages are imported in runtime code.

        Allowed minimal dependencies:
        - tomli: For TOML config support on Python 3.10 (stdlib tomllib in 3.11+)
        """
        # List of allowed stdlib modules
        stdlib_modules = set(sys.stdlib_module_names)

        # Add modules that are always available
        always_available = {
            "ascii_guard",  # Our own package
            "__future__",
            "typing",
            "dataclasses",
            "pathlib",
            "argparse",
            "sys",
            "os",
            "re",
            "io",
            "collections",
        }

        # Allowed minimal external dependencies
        # tomli is only needed for Python 3.10 (3.11+ uses stdlib tomllib)
        allowed_external = {
            "tomli",  # TOML config support for Python 3.10
            "tomllib",  # Stdlib in 3.11+, appears in source but won't execute on 3.10
        }

        stdlib_modules.update(always_available)
        stdlib_modules.update(allowed_external)

        # Get all Python files in src/ascii_guard
        src_dir = Path(__file__).parent.parent / "src" / "ascii_guard"
        python_files = list(src_dir.glob("*.py"))

        assert len(python_files) > 0, "No Python files found in src/ascii_guard"

        violations = []

        for py_file in python_files:
            if py_file.name == "__pycache__":
                continue

            with open(py_file, encoding="utf-8") as f:
                try:
                    tree = ast.parse(f.read(), filename=str(py_file))
                except SyntaxError:
                    violations.append(f"{py_file.name}: Syntax error")
                    continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module = alias.name.split(".")[0]
                        if module not in stdlib_modules:
                            violations.append(f"{py_file.name}: imports external module '{module}'")

                elif isinstance(node, ast.ImportFrom) and node.module:
                    module = node.module.split(".")[0]
                    if module not in stdlib_modules:
                        violations.append(
                            f"{py_file.name}: imports from external module '{module}'"
                        )

        if violations:
            violation_msg = "\n".join(violations)
            raise AssertionError(
                f"CRITICAL: Unexpected external dependencies detected!\n"
                f"ascii-guard must use only stdlib + minimal essential dependencies.\n"
                f"Allowed: tomli (for Python 3.10 TOML support).\n"
                f"Violations:\n{violation_msg}"
            )

    def test_no_click_or_typer(self) -> None:
        """Specifically test that click/typer are NOT used."""
        src_dir = Path(__file__).parent.parent / "src" / "ascii_guard"
        cli_file = src_dir / "cli.py"

        assert cli_file.exists(), "cli.py not found"

        content = cli_file.read_text()

        # Should use argparse, not click/typer
        assert "import click" not in content.lower()
        assert "import typer" not in content.lower()
        assert "from click" not in content.lower()
        assert "from typer" not in content.lower()

        # Should use argparse
        assert "import argparse" in content or "from argparse" in content

    def test_no_colorama(self) -> None:
        """Specifically test that colorama is NOT used."""
        src_dir = Path(__file__).parent.parent / "src" / "ascii_guard"
        cli_file = src_dir / "cli.py"

        content = cli_file.read_text()

        # Should NOT use colorama
        assert "import colorama" not in content.lower()
        assert "from colorama" not in content.lower()

        # Should use ANSI escape codes directly
        assert "\\033[" in content or "033[" in content

    def test_no_markdown_parser(self) -> None:
        """Test that no markdown parsing library is used."""
        src_dir = Path(__file__).parent.parent / "src" / "ascii_guard"

        for py_file in src_dir.glob("*.py"):
            content = py_file.read_text()

            # Should NOT use external markdown libraries
            assert "import markdown" not in content.lower()
            assert "from markdown" not in content.lower()
            assert "import mistune" not in content.lower()
            assert "import commonmark" not in content.lower()

    def test_only_stdlib_in_imports(self) -> None:
        """Test that all imports are from stdlib."""
        src_dir = Path(__file__).parent.parent / "src" / "ascii_guard"

        # Expected stdlib imports we should see
        expected_imports = {
            "dataclasses",
            "pathlib",
            "typing",
            "argparse",
            "sys",
            "os",  # For directory walking
            "fnmatch",  # For pattern matching
        }

        found_imports = set()

        for py_file in src_dir.glob("*.py"):
            content = py_file.read_text()
            for line in content.split("\n"):
                if line.startswith("import ") or line.startswith("from "):
                    # Extract module name
                    if line.startswith("import "):
                        module = line.split()[1].split(".")[0]
                    else:  # from ... import
                        module = line.split()[1].split(".")[0]

                    if not module.startswith("ascii_guard"):
                        found_imports.add(module)

        # All found imports should be in expected
        unexpected = found_imports - expected_imports
        # Filter out __future__ and typing_extensions if present
        unexpected = {m for m in unexpected if m not in {"__future__"}}

        assert len(unexpected) == 0, f"Unexpected stdlib imports: {unexpected}"

    def test_pyproject_minimal_dependencies(self) -> None:
        """Test that pyproject.toml declares only minimal runtime dependencies.

        Allowed dependencies:
        - tomli>=2.0.0; python_version < '3.11' (for TOML config on Python 3.10)
        """
        pyproject_file = Path(__file__).parent.parent / "pyproject.toml"
        assert pyproject_file.exists(), "pyproject.toml not found"

        content = pyproject_file.read_text()

        # Find the dependencies array in [project] section
        in_project = False
        in_dependencies = False
        dependencies: list[str] = []

        for line in content.split("\n"):
            if line.strip() == "[project]":
                in_project = True
            elif line.strip().startswith("[") and in_project:
                # Exited project section
                break
            elif in_project and line.strip().startswith("dependencies"):
                in_dependencies = True
                # Check if it's a single-line empty array
                if "= []" in line:
                    dependencies = []
                    break
            elif in_dependencies:
                # Collect dependency lines until we hit a closing bracket or new section
                stripped = line.strip()
                if stripped.startswith("]"):
                    break
                elif stripped and not stripped.startswith("#"):
                    # Remove quotes and whitespace
                    dep = stripped.strip('",')
                    if dep:
                        dependencies.append(dep)

        # Verify only tomli for Python 3.10 is allowed
        assert len(dependencies) <= 1, (
            f"Too many runtime dependencies! Expected only tomli (conditional), got: {dependencies}"
        )

        if dependencies:
            dep = dependencies[0]
            assert dep.startswith("tomli>="), (
                f"Unexpected dependency: {dep}. "
                f"Only 'tomli' is allowed for Python 3.10 TOML support."
            )
            assert "python_version < '3.11'" in dep or 'python_version < "3.11"' in dep, (
                f"tomli must be conditional on python_version < '3.11', got: {dep}"
            )


class TestPackageCanRunStandalone:
    """Test that the package can run without any external dependencies."""

    def test_can_import_all_modules(self) -> None:
        """Test that all modules can be imported without external deps."""
        try:
            import ascii_guard  # noqa: F401
            import ascii_guard.cli  # noqa: F401
            import ascii_guard.detector  # noqa: F401
            import ascii_guard.fixer  # noqa: F401
            import ascii_guard.linter  # noqa: F401
            import ascii_guard.models  # noqa: F401
            import ascii_guard.validator  # noqa: F401
        except ImportError as e:
            raise AssertionError(
                f"Failed to import module (missing external dependency?): {e}"
            ) from e

    def test_version_is_set(self) -> None:
        """Test that package version is defined."""
        import ascii_guard

        assert hasattr(ascii_guard, "__version__")
        assert len(ascii_guard.__version__) > 0
        assert "." in ascii_guard.__version__  # Semantic versioning

    def test_main_entry_point_exists(self) -> None:
        """Test that CLI main entry point exists."""
        from ascii_guard.cli import main

        assert callable(main)
