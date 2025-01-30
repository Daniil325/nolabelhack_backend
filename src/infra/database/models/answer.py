from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from src.infra.database.models.base import Base

 
class Answer(Base):
     id = Column(Integer, primary_key=True, autoincrement=True)
     user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
     selected_answer_id = Column(Integer, ForeignKey('vote_answer.id', ondelete='CASCADE'))
     voted_at = Column(TIMESTAMP, server_default=func.current_timestamp())
     user = relationship("user", back_populates="answer")
     selected_answer = relationship("vote_answer", back_populates="selected_by")
