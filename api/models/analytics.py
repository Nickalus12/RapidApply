"""
Analytics database model
"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, JSON, ForeignKey, Float, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from api.utils.database import Base


class ApplicationAnalytics(Base):
    """Analytics model for tracking application performance"""
    __tablename__ = "application_analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"), unique=True, nullable=False)
    
    # Interaction metrics
    form_load_time = Column(Float)  # seconds
    form_completion_time = Column(Float)  # seconds
    mouse_movements = Column(Integer, default=0)
    keyboard_events = Column(Integer, default=0)
    page_scrolls = Column(Integer, default=0)
    
    # Field metrics
    fields_auto_filled = Column(Integer, default=0)
    fields_manually_filled = Column(Integer, default=0)
    fields_ai_assisted = Column(Integer, default=0)
    
    # AI usage
    ai_provider_used = Column(String(50))
    ai_tokens_consumed = Column(Integer, default=0)
    ai_response_time = Column(Float)  # seconds
    ai_retry_count = Column(Integer, default=0)
    
    # Browser metrics
    browser_name = Column(String(50))
    browser_version = Column(String(50))
    viewport_width = Column(Integer)
    viewport_height = Column(Integer)
    
    # Network metrics
    proxy_used = Column(Boolean, default=False)
    proxy_location = Column(String(100))
    request_count = Column(Integer, default=0)
    
    # Error tracking
    errors_encountered = Column(JSON, default=[])
    warnings = Column(JSON, default=[])
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    application = relationship("Application", back_populates="analytics")
    
    def __repr__(self):
        return f"<ApplicationAnalytics {self.application_id}>"


class DailyStats(Base):
    """Daily aggregated statistics"""
    __tablename__ = "daily_stats"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    
    # Application metrics
    applications_submitted = Column(Integer, default=0)
    applications_viewed = Column(Integer, default=0)
    applications_responded = Column(Integer, default=0)
    
    # Performance metrics
    average_completion_time = Column(Float)
    average_ai_confidence = Column(Float)
    success_rate = Column(Float)
    
    # Resource usage
    ai_tokens_used = Column(Integer, default=0)
    automation_minutes = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DailyStats user={self.user_id} date={self.date}>"