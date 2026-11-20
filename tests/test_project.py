
"""Foundation tests for the ODM project."""

import odm


def test_package_has_version() -> None:
    """The package exposes its version."""
    assert odm.__version__ == "0.1.0"


def test_package_version_is_a_string() -> None:
    """The package version can be represented as text."""
    assert isinstance(odm.__version__, str)

