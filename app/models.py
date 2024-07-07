
from sqlalchemy import Column,Integer,String,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__= 'users'

    
    userId = Column(Integer,primary_key=True,unique=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False,unique=True)
    password=Column(String, nullable=False)
    phone=Column(String)
    organisations=relationship('Organisation',secondary='user_organisations', back_populates='users' )

class Organisation(Base):
    __tablename__= 'organisations'

    orgId=Column(String,primary_key=True,index=True)
    name=Column(String, nullable=False)
    description=Column(String)
    users=relationship('User', secondary='user_organisations', back_populates='organisations')

class UserOrganisation(Base):
    __tablename__='user_organisations'

    user_id=Column(String,ForeignKey('users.userId'),primary_key=True)
    org_id=Column(String, ForeignKey('organisations.orgId'), primary_key=True)