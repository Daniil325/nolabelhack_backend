from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base
 
 
class UserRole(Base):
    user_id = Column(UUID, ForeignKey('user.id', ondelete='CASCADE'))
    role_id = Column(UUID, ForeignKey('role.id', ondelete='CASCADE'))


    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")
