"""Conftest file for pytest fixtures."""

import pytest


@pytest.fixture
def sample_fixture():
    """A sample fixture for testing."""
    return "This is a sample fixture"
