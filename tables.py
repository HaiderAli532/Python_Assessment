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
    role = Column(String, nullable=False)  # 'freelancer' or 'client'

# Organization Model
class Organization(Model):
    __tablename__ = 'organizations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=True)
    contact_info = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    owner = relationship('User', backref='organizations')

# Task Model
class Task(Model):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    budget = Column(Float, nullable=False)
    deadline = Column(DateTime, nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    
    organization = relationship('Organization', backref='tasks')

# Proposal Model
class Proposal(Model):
    __tablename__ = 'proposals'
    
    id = Column(Integer, primary_key=True)
    freelancer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    bid_amount = Column(Float, nullable=False)
    message = Column(String, nullable=True)
    status = Column(String, nullable=False)  # 'pending', 'accepted', 'rejected'
    
    freelancer = relationship('User', backref='proposals')
    task = relationship('Task', backref='proposals')

# Profile Model
class Profile(Model):
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True)
    freelancer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    freelancer = relationship('User', backref='profiles')
    organization = relationship('Organization', backref='profiles')

# Notification Model
class Notification(Model):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    type = Column(String, nullable=False)
    content = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    profile = relationship('Profile', backref='notifications')

# Notification Preferences Model
class NotificationPreference(Model):
    __tablename__ = 'notification_preferences'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    notification_type = Column(String, nullable=False)
    preference = Column(String, nullable=False)  # 'immediate', 'weekly', 'none'
    
    profile = relationship('Profile', backref='preferences')