from typing import List, Optional

from pydantic import BaseModel


class MenuItemCreate(BaseModel):
    name: str
    url: Optional[str] = None
    menu_name: str
    parent_id: Optional[int] = None


class MenuItemNode(BaseModel):
    id: int
    name: str
    url: Optional[str] = None
    children: List["MenuItemNode"] = []

    class Config:
        from_attributes = True


MenuItemNode.model_rebuild()

