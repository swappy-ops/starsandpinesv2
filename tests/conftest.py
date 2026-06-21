"""Test configuration for Stars & Pines V2.

Uses an in-memory SQLite database for all tests.
"""

import os
import pytest
import tempfile
from pathlib import Path

# Set test database to in-memory before importing api modules
TEST_DB = tempfile.mktemp(suffix=".db")
os.environ["SP_DB_PATH"] = TEST_DB

from api.db import init_db, get_db, DB_PATH


@pytest.fixture(autouse=True)
def setup_test_db():
    """Initialize test database before each test, clean up after."""
    init_db()
    yield
    # Clean up
    if os.path.exists(TEST_DB):
        os.unlink(TEST_DB)


@pytest.fixture
def db():
    """Provide a database connection for tests."""
    with get_db() as conn:
        yield conn
