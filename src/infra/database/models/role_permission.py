from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base

 
class RolePermission(Base):
     id = Column(Integer, primary_key=True, autoincrement=True)
     role_id = Column(Integer, ForeignKey('role.id', ondelete='CASCADE'))
     permission_id = Column(Integer, ForeignKey('permission.id', ondelete='CASCADE'))
     granted_at = Column(TIMESTAMP, server_default=func.current_timestamp())
     role = relationship("role", back_populates="permission")
     permission = relationship("permission", back_populates="role")
