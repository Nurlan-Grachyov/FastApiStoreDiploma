from datetime import datetime
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(..., max_length=100)
    price: int = Field(..., ge=0)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
    is_active: bool = Field(True)
