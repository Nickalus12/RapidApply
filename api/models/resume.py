"""
Resume database model
"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, JSON, ForeignKey, Text, Float
from sqlalchemy.dialects.postgresql import UUID, ARRAY
# from pgvector.sqlalchemy import Vector  # Temporarily disabled
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from api.utils.database import Base


class Resume(Base):
    """Resume model for storing user resumes"""
    __tablename__ = "resumes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Resume metadata
    name = Column(String(255), nullable=False)
    version = Column(String(50), default="v1")
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    
    # Resume content (structured)
    content = Column(JSON, nullable=False, default={
        "personal": {
            "name": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "github": "",
            "website": ""
        },
        "summary": "",
        "experience": [],
        "education": [],
        "skills": [],
        "projects": [],
        "certifications": [],
        "languages": [],
        "awards": []
    })
    
    # Original file info
    original_filename = Column(String(500))
    file_format = Column(String(50))  # pdf, docx, txt
    file_size = Column(Integer)  # bytes
    file_path = Column(String(1000))  # S3 or local path
    
    # Extracted text for search
    full_text = Column(Text)
    
    # AI embeddings for semantic search
    # embedding = Column(Vector(1536))  # OpenAI embeddings dimension - temporarily disabled
    
    # Skills and keywords
    extracted_skills = Column(ARRAY(String), default=[])
    keywords = Column(ARRAY(String), default=[])
    
    # Performance metrics
    performance_score = Column(Float, default=0.0)  # 0.0 to 1.0
    application_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    
    # ATS optimization
    ats_score = Column(Float)  # 0.0 to 1.0
    ats_warnings = Column(JSON, default=[])
    
    # Tags for organization
    tags = Column(ARRAY(String), default=[])
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    applications = relationship("Application", back_populates="resume")
    
    def __repr__(self):
        return f"<Resume {self.name} v{self.version}>"