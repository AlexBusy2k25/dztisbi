from sqlalchemy import Column, Float, Integer, String

from .db import Base


class ExperimentAssignment(Base):
    __tablename__ = "experiment_assignments"

    id = Column(Integer, primary_key=True, index=True)
    device_token = Column(String(128), index=True, nullable=False)
    experiment_key = Column(String(64), nullable=False)
    option_value = Column(String(64), nullable=False)

