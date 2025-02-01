from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base


class VoteAnswer(Base):
     id = Column(Integer, primary_key=True, autoincrement=True)
     vote_id = Column(Integer, ForeignKey('vote.id', ondelete='CASCADE'))
     answer_text = Column(String(255), nullable=False)
     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
     vote = relationship("vote", back_populates="answer")
     selected_by = relationship("answer", back_populates="vote_answer")
