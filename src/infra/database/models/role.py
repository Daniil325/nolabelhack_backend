from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base
 
 
class Role(Base):
     id = Column(Integer, primary_key=True, autoincrement=True)
     name = Column(String(50), unique=True, nullable=False)
     description = Column(Text)
     user = relationship("user", back_populates="role")
     role_permission = relationship("role_permission", back_populates="role")
