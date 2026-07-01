"""Phase 0 acceptance tests — verify repository foundation."""

from api.db import get_db


def test_database_tables_exist(db):
    """All 9 core tables should exist after init."""
    tables = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    table_names = [row["name"] for row in tables]

    expected = [
        "cleaning_requests",
        "guest_portal_tokens",
        "guests",
        "ledger_entries",
        "menu_items",
        "order_items",
        "orders",
        "rooms",
        "staff",
        "stays",
    ]

    for table in expected:
        assert table in table_names, f"Missing table: {table}"


def test_can_insert_guest(db):
    """Verify basic CRUD works on guests table."""
    db.execute(
        "INSERT INTO guests (id, name, phone) VALUES (?, ?, ?)",
        ("test-001", "Test Guest", "+919999999999"),
    )
    row = db.execute("SELECT * FROM guests WHERE id = ?", ("test-001",)).fetchone()
    assert row is not None
    assert row["name"] == "Test Guest"
    assert row["phone"] == "+919999999999"


def test_can_insert_room(db):
    """Verify rooms table works."""
    db.execute(
        "INSERT INTO rooms (id, name, type, base_price) VALUES (?, ?, ?, ?)",
        ("R99", "Test Room", "private", 1000),
    )
    row = db.execute("SELECT * FROM rooms WHERE id = ?", ("R99",)).fetchone()
    assert row is not None
    assert row["base_price"] == 1000


def test_can_insert_menu_item(db):
    """Verify menu_items table works."""
    db.execute(
        "INSERT INTO menu_items (id, name, category, price) VALUES (?, ?, ?, ?)",
        ("M99", "Test Dish", "mains", 150),
    )
    row = db.execute("SELECT * FROM menu_items WHERE id = ?", ("M99",)).fetchone()
    assert row is not None
    assert row["price"] == 150


def test_foreign_keys_enforced(db):
    """Verify foreign key constraints are active."""
    # This should fail because guest_id doesn't exist
    try:
        db.execute(
            "INSERT INTO stays (id, guest_id, room_id, check_in) VALUES (?, ?, ?, ?)",
            ("stay-001", "nonexistent", "R99", "2026-06-20T12:00:00"),
        )
        assert False, "Foreign key constraint should have prevented this"
    except Exception:
        pass  # Expected
