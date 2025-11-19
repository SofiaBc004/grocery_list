from app import crud
from app.db import get_conn


def clear_db():
    """Utility to reset the DB before each test."""
    conn = get_conn()
    conn.execute("DELETE FROM items")
    conn.commit()


def test_create_item():
    clear_db()

    item = {"name": "Bananas", "quantity": 3, "category": "Fruit"}
    created = crud.create_item(item)

    assert created["id"] > 0
    assert created["name"] == "Bananas"
    assert created["quantity"] == 3
    assert created["category"] == "Fruit"
    assert created["purchased"] is False


def test_list_items_all():
    clear_db()
    crud.create_item({"name": "Milk", "quantity": 1})
    crud.create_item({"name": "Bread", "quantity": 2})

    items = crud.list_items()
    assert len(items) == 2


def test_list_items_filtered():
    clear_db()
    crud.create_item({"name": "A", "purchased": True})
    crud.create_item({"name": "B", "purchased": False})

    purchased_items = crud.list_items(True)
    not_purchased_items = crud.list_items(False)

    assert len(purchased_items) == 1
    assert purchased_items[0]["purchased"] is True

    assert len(not_purchased_items) == 1
    assert not_purchased_items[0]["purchased"] is False


def test_get_item_found():
    clear_db()
    created = crud.create_item({"name": "Juice"})
    item = crud.get_item(created["id"])

    assert item is not None
    assert item["name"] == "Juice"


def test_get_item_not_found():
    clear_db()
    assert crud.get_item(9999) is None


def test_update_item_full():
    clear_db()
    created = crud.create_item({"name": "Pasta", "quantity": 1})

    updated = crud.update_item(created["id"], {
        "name": "Spaghetti",
        "quantity": 5,
        "category": "Food",
        "purchased": True
    })

    assert updated["name"] == "Spaghetti"
    assert updated["quantity"] == 5
    assert updated["category"] == "Food"
    assert updated["purchased"] is True


def test_update_item_partial():
    clear_db()
    created = crud.create_item({"name": "Water", "quantity": 2})

    updated = crud.update_item(created["id"], {"quantity": 10})

    assert updated["quantity"] == 10
    assert updated["name"] == "Water"  # unchanged


def test_update_item_invalid_id():
    clear_db()
    updated = crud.update_item(123456, {"name": "X"})
    assert updated is None


def test_update_item_empty_fields_returns_original():
    clear_db()
    created = crud.create_item({"name": "Tea", "quantity": 1})

    updated = crud.update_item(created["id"], {})

    assert updated["name"] == "Tea"
    assert updated["quantity"] == 1


def test_toggle_item():
    clear_db()
    created = crud.create_item({"name": "Eggs", "purchased": False})

    toggled = crud.toggle_item(created["id"])
    assert toggled["purchased"] is True

    toggled_again = crud.toggle_item(created["id"])
    assert toggled_again["purchased"] is False


def test_toggle_item_invalid_id():
    clear_db()
    assert crud.toggle_item(9999) is None


def test_delete_item_success():
    clear_db()
    created = crud.create_item({"name": "Sugar"})

    deleted = crud.delete_item(created["id"])
    assert deleted is True

    assert crud.get_item(created["id"]) is None


def test_delete_item_invalid():
    clear_db()
    deleted = crud.delete_item(4444)
    assert deleted is False
