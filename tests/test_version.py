"""Test version information."""

import re

import ascii_guard


def test_version() -> None:
    """Test that version is defined and follows semantic versioning."""
    assert hasattr(ascii_guard, "__version__")
    assert isinstance(ascii_guard.__version__, str)
    # Check that version follows semantic versioning (X.Y.Z format)
    assert re.match(r"^\d+\.\d+\.\d+$", ascii_guard.__version__), (
        f"Version must be in X.Y.Z format, got: {ascii_guard.__version__}"
    )
