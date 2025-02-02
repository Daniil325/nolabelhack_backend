from sqlalchemy import TIMESTAMP, UUID, Boolean, Column, ForeignKey, String, func
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base


class User(Base):
     first_name = Column(String(50), nullable=False)
     last_name = Column(String(50), nullable=False)
     email = Column(String(100), unique=True, nullable=False)
     hashed_password = Column(String(255), nullable=False)
     is_verified = Column(Boolean, default=False)
     role_id = Column(UUID, ForeignKey('role.id', ondelete='CASCADE'))
     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())


     answers = relationship("UserAnswers", back_populates="user")
     role = relationship("Role", back_populates="user")
