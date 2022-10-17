from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import func


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column('user_id', Integer, primary_key=True, index=True)
    user = Column('username', String, unique=True, index=True)
    email = Column('user_email', String, unique=True, index=True)
    description = Column('user_description', String)
    password = Column('user_password', String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
