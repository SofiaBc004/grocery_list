from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .models import ItemCreate, ItemUpdate, ItemRead
from . import crud
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from pathlib import Path
from fastapi.responses import FileResponse


# LIFESPAN - only for initializing the database
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

# FASTAPI APP
app = FastAPI(
    title="Grocery List API",
    version="1.0.0",
    lifespan=lifespan,
)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

@app.get("/", include_in_schema=False)
def serve_frontend():
    """Serve the single-page grocery list frontend."""
    index_path = FRONTEND_DIR / "index.html"
    return FileResponse(index_path)


# PROMETHEUS INSTRUMENTATION 
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=False,
    should_instrument_requests_inprogress=True,
)

instrumentator.instrument(app).expose(app)


# CORS MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/items", response_model=ItemRead, status_code=200)
def create_item(item: ItemCreate):
    return crud.create_item(item.model_dump())


@app.get("/items", response_model=List[ItemRead])
def list_items(purchased: Optional[str] = None):
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
