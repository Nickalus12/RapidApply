"""
Job database model
"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, JSON, ForeignKey, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from api.utils.database import Base


class Job(Base):
    """Job model for storing LinkedIn job postings"""
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    linkedin_job_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Job details
    title = Column(String(500), nullable=False)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(500))
    description = Column(Text)
    requirements = Column(JSON, default=[])
    
    # Job metadata
    job_type = Column(String(50))  # full_time, part_time, contract, etc.
    experience_level = Column(String(50))  # entry, mid, senior, executive
    industry = Column(String(255))
    function = Column(String(255))
    
    # Salary information
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    salary_currency = Column(String(10), default="USD")
    
    # Application details
    linkedin_url = Column(String(1000), nullable=False)
    easy_apply = Column(Boolean, default=False)
    external_apply_url = Column(String(1000))
    
    # Tracking
    posted_date = Column(DateTime)
    expires_date = Column(DateTime)
    applicant_count = Column(Integer)
    view_count = Column(Integer)
    
    # Analysis
    skills_extracted = Column(JSON, default=[])
    keywords = Column(JSON, default=[])
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_checked_at = Column(DateTime)
    
    # Relationships
    applications = relationship("Application", back_populates="job")
    saved_by_users = relationship("SavedJob", back_populates="job")
    
    def __repr__(self):
        return f"<Job {self.title} at {self.company}>"


class SavedJob(Base):
    """Model for user's saved jobs"""
    __tablename__ = "saved_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    
    # Additional metadata
    notes = Column(Text)
    priority = Column(Integer, default=0)  # Higher number = higher priority
    reminder_date = Column(DateTime)
    
    # Timestamps
    saved_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="saved_jobs")
    job = relationship("Job", back_populates="saved_by_users")
    
    def __repr__(self):
        return f"<SavedJob user={self.user_id} job={self.job_id}>"