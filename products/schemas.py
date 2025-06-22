from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., max_length=100)
    price: int = Field(..., ge=0)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
    is_active: bool = Field(True)


class ProductRead(BaseModel):
    name: str = Field(..., max_length=100)
    price: int = Field(..., ge=0)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    price: Optional[int] = Field(None, ge=0)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    is_active: Optional[bool] = Field(default=True)
