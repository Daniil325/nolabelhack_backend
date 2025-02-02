from sqlalchemy import TIMESTAMP, UUID, Boolean, Column, String, func
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base


class User(Base):
     first_name = Column(String(50))
     last_name = Column(String(50))
     email = Column(String(100), unique=True, nullable=False)
     hashed_password = Column(String(255), nullable=False)
     is_verified = Column(Boolean, default=False)
     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())


     answers = relationship("UserAnswers", back_populates="user")
     roles = relationship("UserRole", back_populates="user")
