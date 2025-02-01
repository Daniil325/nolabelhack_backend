from sqlalchemy import UUID, Column, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base

 
class RolePermission(Base):
     role_id = Column(UUID, ForeignKey('role.id', ondelete='CASCADE'))
     permission_id = Column(UUID, ForeignKey('permission.id', ondelete='CASCADE'))
     granted_at = Column(TIMESTAMP, server_default=func.current_timestamp())

     
     role = relationship("Role", back_populates="permission")
     permission = relationship("Permission", back_populates="roles")
