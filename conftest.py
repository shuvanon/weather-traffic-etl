"""Shared pytest fixtures.

Placing conftest.py at the repository root also puts the root on sys.path, so
`import data_pipeline` resolves when running pytest from the project root.
"""
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir():
    """Directory holding the committed CSV fixtures used by the offline tests."""
    return Path(__file__).parent / "tests" / "fixtures"
