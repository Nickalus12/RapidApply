"""
User database model
"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from api.utils.database import Base


class SubscriptionTier(str, enum.Enum):
    """Subscription tier enumeration"""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    company = Column(String(255))
    linkedin_url = Column(String(500))
    phone = Column(String(50))
    location = Column(String(255))
    bio = Column(String(1000))
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255))
    
    # Subscription
    subscription_tier = Column(
        Enum(SubscriptionTier),
        default=SubscriptionTier.FREE,
        nullable=False
    )
    credits_remaining = Column(Integer, default=50)
    subscription_expires_at = Column(DateTime)
    
    # LinkedIn credentials (encrypted)
    linkedin_email_encrypted = Column(String(500))
    linkedin_password_encrypted = Column(String(500))
    
    # Settings
    settings = Column(JSON, default={
        "email_notifications": True,
        "auto_apply": False,
        "preferred_job_types": [],
        "excluded_companies": [],
        "min_salary": None,
        "max_applications_per_day": 10
    })
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime)
    
    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")
    saved_jobs = relationship("SavedJob", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"