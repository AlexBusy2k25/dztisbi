from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    url = Column(String(255), nullable=True)
    menu_name = Column(String(50), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("menu_items.id"), nullable=True)

    children = relationship("MenuItem")

