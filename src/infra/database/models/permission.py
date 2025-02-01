from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base

 
class Permission(Base):
     id = Column(Integer, primary_key=True, autoincrement=True)
     name = Column(String(50), unique=True, nullable=False)
     description = Column(Text)
     roles = relationship("role_permission", back_populates="permission")
