from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base

 
class Permission(Base):
     name = Column(String(50), unique=True, nullable=False)
     description = Column(Text)

     
     roles = relationship("RolePermission", back_populates="permission")
