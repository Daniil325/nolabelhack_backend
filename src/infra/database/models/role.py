from sqlalchemy import UUID, Column, String, Text
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base
 
 
class Role(Base):
     name = Column(String(50), unique=True)
     description = Column(Text)
     resource_id = Column(UUID)


     users = relationship("UserRole", back_populates="role")
     permission = relationship("RolePermission", back_populates="role")
