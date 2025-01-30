from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, relationship
 
Base = declarative_base()
 
class Role(Base):
     __tablename__ = 'roles'
     role_id = Column(Integer, primary_key=True, autoincrement=True)
     role_name = Column(String(50), unique=True, nullable=False)
     description = Column(Text)
     persons = relationship("Person", back_populates="role")
     permissions = relationship("RolePermission", back_populates="role")
 
class Person(Base):
     __tablename__ = 'persons'
     person_id = Column(Integer, primary_key=True, autoincrement=True)
     first_name = Column(String(50), nullable=False)
     last_name = Column(String(50), nullable=False)
     email = Column(String(100), unique=True, nullable=False)
     hashed_password = Column(String(255), nullable=False)
     is_verified = Column(Boolean, default=False)
     role_id = Column(Integer, ForeignKey('roles.role_id', ondelete='CASCADE'))
     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
     role = relationship("Role", back_populates="persons")
     answers = relationship("Answers", back_populates="person")
 
class Vote(Base):
     __tablename__ = 'votes'
     vote_id = Column(Integer, primary_key=True, autoincrement=True)
     title = Column(String(255), nullable=False)
     description = Column(Text)
     start_date = Column(TIMESTAMP, nullable=False)
     end_date = Column(TIMESTAMP)
     is_active = Column(Boolean, default=True)
     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
     answers = relationship("VoteAnswers", back_populates="vote")
 
class VoteAnswers(Base):
     __tablename__ = 'vote_answers'
     answer_id = Column(Integer, primary_key=True, autoincrement=True)
     vote_id = Column(Integer, ForeignKey('votes.vote_id', ondelete='CASCADE'))
     answer_text = Column(String(255), nullable=False)
     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
     vote = relationship("Vote", back_populates="answers")
     selected_by = relationship("Answers", back_populates="selected_answer")
 
class Answers(Base):
     __tablename__ = 'answers'
     answer_id = Column(Integer, primary_key=True, autoincrement=True)
     person_id = Column(Integer, ForeignKey('persons.person_id', ondelete='CASCADE'))
     selected_answer_id = Column(Integer, ForeignKey('vote_answers.answer_id', ondelete='CASCADE'))
     voted_at = Column(TIMESTAMP, server_default=func.current_timestamp())
     person = relationship("Person", back_populates="answers")
     selected_answer = relationship("VoteAnswers", back_populates="selected_by")
 
class Permission(Base):
     __tablename__ = 'permissions'
     permission_id = Column(Integer, primary_key=True, autoincrement=True)
     permission_name = Column(String(50), unique=True, nullable=False)
     description = Column(Text)
     roles = relationship("RolePermission", back_populates="permission")
 
class RolePermission(Base):
     __tablename__ = 'role_permissions'
     role_permission_id = Column(Integer, primary_key=True, autoincrement=True)
     role_id = Column(Integer, ForeignKey('roles.role_id', ondelete='CASCADE'))
     permission_id = Column(Integer, ForeignKey('permissions.permission_id', ondelete='CASCADE'))
     granted_at = Column(TIMESTAMP, server_default=func.current_timestamp())
     role = relationship("Role", back_populates="permissions")
     permission = relationship("Permission", back_populates="roles")
