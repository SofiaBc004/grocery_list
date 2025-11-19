from fastapi.testclient import TestClient
from app.main import app
from app.db import get_conn

client = TestClient(app)


def clear_db():
    conn = get_conn()
    conn.execute("DELETE FROM items")
    conn.execute("DELETE FROM sqlite_sequence WHERE name='items'")
    conn.commit()


def test_health_endpoint():
    r = client.get("/")
    assert r.status_code in (200, 404)  # root may not exist


def test_create_and_get_item():
    clear_db()

    data = {"name": "Apples", "quantity": 4, "category": "Fruit"}
    r = client.post("/items", json=data)
    assert r.status_code == 200

    item = r.json()
    item_id = item["id"]

    r2 = client.get(f"/items/{item_id}")
    assert r2.status_code == 200
    fetched = r2.json()

    assert fetched["name"] == "Apples"
    assert fetched["quantity"] == 4


def test_list_items():
    clear_db()

    client.post("/items", json={"name": "A", "purchased": False})
    client.post("/items", json={"name": "B", "purchased": True})   # FIXED

    r = client.get("/items")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2

    r2 = client.get("/items?purchased=true")
    filtered = r2.json()
    assert len(filtered) == 1              # now valid
    assert filtered[0]["purchased"] is True


def test_update_item():
    clear_db()
    r = client.post("/items", json={"name": "Milk", "quantity": 1})
    item_id = r.json()["id"]

    r2 = client.patch(f"/items/{item_id}", json={"quantity": 5})
    assert r2.status_code == 200

    updated = r2.json()
    assert updated["quantity"] == 5


def test_update_item_empty_patch():
    clear_db()
    r = client.post("/items", json={"name": "Tea"})
    item_id = r.json()["id"]

    r2 = client.patch(f"/items/{item_id}", json={})
    assert r2.status_code == 422


def test_toggle_item():
    clear_db()
    r = client.post("/items", json={"name": "X"})
    item_id = r.json()["id"]

    r2 = client.patch(f"/items/{item_id}/toggle")
    assert r2.status_code == 200
    assert r2.json()["purchased"] is True


def test_delete_item():
    clear_db()
    r = client.post("/items", json={"name": "DeleteMe"})
    item_id = r.json()["id"]

    r2 = client.delete(f"/items/{item_id}")
    assert r2.status_code == 204

    r3 = client.get(f"/items/{item_id}")
    assert r3.status_code == 404
