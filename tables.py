from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float, func, types
import sqlalchemy as sa


class Base(DeclarativeBase):
    pass

class Model(Base):
    __abstract__ = True
    
    is_active = sa.Column(sa.Boolean, nullable=False, server_default="1")
    is_deleted = sa.Column(sa.Boolean, nullable=False, server_default="0")
    created_by = sa.Column(sa.String(), nullable=True)
    updated_by = sa.Column(sa.String(), nullable=True)
    deleted_at = sa.Column(types.TIMESTAMP, nullable=True)
    deleted_by = sa.Column(sa.String(), nullable=True)

class User(Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Organization(Model):
    __tablename__ = 'organizations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='organizations')

class Job(Model):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    budget = Column(Float, nullable=False)
    deadline = Column(DateTime, nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)  
    organization = relationship('Organization', backref='jobs')


class Proposal(Model):
    __tablename__ = 'proposals'
    
    id = Column(Integer, primary_key=True)
    freelancer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    bid_amount = Column(Float, nullable=False)
    message = Column(String, nullable=True)
    status = Column(String, nullable=False)
    freelancer = relationship('User', backref='proposals')
    task = relationship('Task', backref='proposals')


class Profile(Model):
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True)
    freelancer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    freelancer = relationship('User', backref='profiles')
    organization = relationship('Organization', backref='profiles')


class Notification(Model):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    content = Column(String, nullable=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)  
    organization = relationship('Organization', backref='notifications')

class NotificationPreference(Model):
    __tablename__ = 'notification_preferences'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    notification_type = Column(String, nullable=False)
    preference = Column(String, nullable=False)
    profile = relationship('Profile', backref='preferences')