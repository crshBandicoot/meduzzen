from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship
from db import Base


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'), index=True)
    owner = relationship('User', back_populates='companies')
    description = Column(String)
    visible = Column(Boolean, default=True)
    requests = relationship('Request', back_populates='company')
    members = relationship('Member')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Member(Base):
    __tablename__ = 'members'
    company = Column(Integer, ForeignKey('companies.id'), primary_key=True)
    user = Column(ForeignKey('users.id'), primary_key=True)
    admin = Column(Boolean, default=False)


class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    user = relationship('User', back_populates='requests')
    company_id = Column(Integer, ForeignKey('companies.id'), index=True)
    company = relationship('Company', back_populates='requests')
    side = Column(Boolean)
