from sqlalchemy import UUID, Column, ForeignKey, TIMESTAMP, String, func
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base


class Answer(Base):
     vote_id = Column(UUID, ForeignKey('vote.id', ondelete='CASCADE'))
     answer_text = Column(String(255), nullable=False)
     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

     
     vote = relationship("Vote", back_populates="answers")
     user_answers = relationship("UserAnswers", back_populates="selected_answer")
