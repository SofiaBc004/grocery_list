from typing import Optional
from pydantic import BaseModel, Field, constr, conint

class ItemCreate(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=80)
    quantity: conint(ge=1) = 1
    category: constr(max_length=40) = ""

class ItemUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=80)] = None
    quantity: Optional[conint(ge=1)] = None
    category: Optional[constr(max_length=40)] = None
    purchased: Optional[bool] = None

class ItemRead(BaseModel):
    id: int
    name: str
    quantity: int
    category: str
    purchased: bool
