from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    point_id: int = Field(..., description="ID точки, для которой создаются чеки")
    payload: dict[str, Any] = Field(..., description="Данные заказа (JSON)")


class CheckBase(BaseModel):
    id: int
    printer_id: int
    type: str
    status: str
    created_at: datetime


class CheckResponse(CheckBase):
    class Config:
        from_attributes = True


class PrinterCreate(BaseModel):
    name: str
    api_key: str
    check_type: str
    point_id: int


class PrinterResponse(BaseModel):
    id: int
    name: str
    api_key: str
    check_type: str
    point_id: int

    class Config:
        from_attributes = True

