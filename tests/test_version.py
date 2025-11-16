"""Test version information."""

import ascii_guard


def test_version() -> None:
    """Test that version is defined."""
    assert hasattr(ascii_guard, "__version__")
    assert isinstance(ascii_guard.__version__, str)
    assert ascii_guard.__version__ == "0.1.0"
