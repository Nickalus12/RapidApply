"""
Application database model
"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, JSON, ForeignKey, Text, Float, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from api.utils.database import Base


class ApplicationStatus(str, enum.Enum):
    """Application status enumeration"""
    DRAFT = "draft"
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    FAILED = "failed"
    VIEWED = "viewed"
    IN_REVIEW = "in_review"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class Application(Base):
    """Application model for tracking job applications"""
    __tablename__ = "applications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    
    # Application status
    status = Column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.DRAFT,
        nullable=False,
        index=True
    )
    
    # Application details
    cover_letter = Column(Text)
    answers = Column(JSON, default={})  # Stores Q&A responses
    
    # AI metrics
    ai_confidence_score = Column(Float)  # 0.0 to 1.0
    ai_suggestions_used = Column(JSON, default=[])
    personalization_score = Column(Float)
    
    # Tracking
    submitted_at = Column(DateTime)
    viewed_at = Column(DateTime)
    responded_at = Column(DateTime)
    
    # Response tracking
    recruiter_viewed = Column(Boolean, default=False)
    recruiter_response = Column(Text)
    interview_scheduled = Column(Boolean, default=False)
    
    # Error tracking
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    
    # Performance metrics
    time_to_complete = Column(Integer)  # seconds
    form_fields_count = Column(Integer)
    
    # Metadata
    application_method = Column(String(50))  # easy_apply, external, email
    external_reference = Column(String(255))  # External application ID if any
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
    analytics = relationship("ApplicationAnalytics", back_populates="application", uselist=False)
    
    def __repr__(self):
        return f"<Application {self.id} status={self.status}>"