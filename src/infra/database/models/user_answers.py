from sqlalchemy import UUID, Column, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base


class UserAnswers(Base):
     selected_answer_id = Column(UUID, ForeignKey('answer.id', ondelete='CASCADE'))
     user_id = Column(UUID, ForeignKey('user.id', ondelete='CASCADE'))
     voted_at = Column(TIMESTAMP, server_default=func.current_timestamp())

     
     user = relationship("User", back_populates="answers")
     selected_answer = relationship("Answer", back_populates="user_answers")
