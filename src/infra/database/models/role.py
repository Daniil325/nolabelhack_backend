from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base
 
 
class Role(Base):
     name = Column(String(50), unique=True, nullable=False)
     description = Column(Text)

     
     user = relationship("User", back_populates="role")
     permission = relationship("RolePermission", back_populates="role")
