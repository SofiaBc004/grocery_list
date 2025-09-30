from typing import Optional, Dict, Any, List
from .db import get_conn

def _row_to_dict(row) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "name": row["name"],
        "quantity": row["quantity"],
        "category": row["category"],
        "purchased": bool(row["purchased"]),
    }

def create_item(data: Dict[str, Any]) -> Dict[str, Any]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO items (name, quantity, category, purchased) VALUES (?,?,?,?)",
            (data["name"], data.get("quantity", 1), data.get("category", ""), int(data.get("purchased", False))),
        )
        item_id = cur.lastrowid
        row = cur.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
        return _row_to_dict(row)

def list_items(purchased: Optional[bool] = None) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        cur = conn.cursor()
        if purchased is None:
            rows = cur.execute("SELECT * FROM items ORDER BY id").fetchall()
        else:
            rows = cur.execute("SELECT * FROM items WHERE purchased=? ORDER BY id", (int(purchased),)).fetchall()
        return [_row_to_dict(r) for r in rows]

def get_item(item_id: int) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
        return _row_to_dict(row) if row else None

def update_item(item_id: int, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not fields:
        return get_item(item_id)
    sets, vals = [], []
    if "name" in fields:      sets.append("name=?");      vals.append(fields["name"])
    if "quantity" in fields:  sets.append("quantity=?");  vals.append(fields["quantity"])
    if "category" in fields:  sets.append("category=?");  vals.append(fields["category"])
    if "purchased" in fields: sets.append("purchased=?"); vals.append(int(fields["purchased"]))
    if not sets:
        return get_item(item_id)

    with get_conn() as conn:
        cur = conn.cursor()
        vals.append(item_id)
        cur.execute(f"UPDATE items SET {', '.join(sets)} WHERE id=?", tuple(vals))
        if cur.rowcount == 0:
            return None
        row = cur.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
        return _row_to_dict(row)

def toggle_item(item_id: int) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        cur = conn.cursor()
        row = cur.execute("SELECT purchased FROM items WHERE id=?", (item_id,)).fetchone()
        if not row:
            return None
        new_val = 0 if row["purchased"] else 1
        cur.execute("UPDATE items SET purchased=? WHERE id=?", (new_val, item_id))
        row2 = cur.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
        return _row_to_dict(row2)

def delete_item(item_id: int) -> bool:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM items WHERE id=?", (item_id,))
        return cur.rowcount > 0
