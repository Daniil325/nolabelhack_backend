from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base


class User(Base):
     id = Column(Integer, primary_key=True, autoincrement=True)
     first_name = Column(String(50), nullable=False)
     last_name = Column(String(50), nullable=False)
     email = Column(String(100), unique=True, nullable=False)
     hashed_password = Column(String(255), nullable=False)
     is_verified = Column(Boolean, default=False)
     role_id = Column(Integer, ForeignKey('role.id', ondelete='CASCADE'))
     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
     role = relationship("role", back_populates="user")
     answer = relationship("answer", back_populates="user")
