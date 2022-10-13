from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column('user_id', Integer, primary_key=True, index=True)
    user = Column('username', String, unique=True, index=True)
    email = Column('user_email', String, unique=True, index=True)
    password = Column('user_password', String)
