from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base


class Vote(Base):
     id = Column(Integer, primary_key=True, autoincrement=True)
     title = Column(String(255), nullable=False)
     description = Column(Text)
     start_date = Column(TIMESTAMP, nullable=False)
     end_date = Column(TIMESTAMP)
     is_active = Column(Boolean, default=True)
     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
     answer = relationship("vote_answer", back_populates="vote")
