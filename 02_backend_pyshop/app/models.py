from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .db import Base


class Printer(Base):
    __tablename__ = "printers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    api_key = Column(String(64), unique=True, nullable=False, index=True)
    check_type = Column(String(20), nullable=False)
    point_id = Column(Integer, nullable=False)

    checks = relationship("Check", back_populates="printer")


class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True, index=True)
    printer_id = Column(Integer, ForeignKey("printers.id"), nullable=False)
    type = Column(String(20), nullable=False)
    order_payload = Column(Text, nullable=False)
    status = Column(String(20), default="new", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    printer = relationship("Printer", back_populates="checks")
