import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Something(Base):
    __tablename__ = "something"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    description = Column(String)
