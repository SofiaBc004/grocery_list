from typing import Optional, List, Annotated
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .models import ItemCreate, ItemUpdate, ItemRead
from . import crud
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run at startup
    init_db()

    yield  # Application runs here


app = FastAPI(
    title="Grocery List API",
    version="1.0.0",
    lifespan=lifespan,
)

# allow the frontend to call the API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # only for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/items", response_model=ItemRead, status_code=200)
def create_item(item: ItemCreate):
    return crud.create_item(item.model_dump())

@app.get("/items", response_model=List[ItemRead])
def list_items(purchased: Optional[str] = None):
    # print("DEBUG: list_items was executed with raw value:", purchased)
    if purchased is not None:
        purchased = purchased.lower() in ("true", "1", "yes", "y")
    return crud.list_items(purchased)


@app.get("/items/{item_id}", response_model=ItemRead)
def read_item(item_id: int):
    item = crud.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.patch("/items/{item_id}", response_model=ItemRead)
def patch_item(item_id: int, patch: ItemUpdate):
    # Basic guard: at least one field provided
    if patch.model_dump(exclude_unset=True) == {}:
        raise HTTPException(status_code=422, detail="No fields to update")
    item = crud.update_item(item_id, patch.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.patch("/items/{item_id}/toggle", response_model=ItemRead, status_code=200)
def toggle_item(item_id: int):
    item = crud.toggle_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    ok = crud.delete_item(item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")
