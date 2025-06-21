"""
Users router
Handles user profile management and settings
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

from api.routers.auth import oauth2_scheme

router = APIRouter()


class UserProfile(BaseModel):
    """User profile schema"""
    email: EmailStr
    full_name: str
    company: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None


class UserSettings(BaseModel):
    """User settings schema"""
    email_notifications: bool = True
    auto_apply: bool = False
    preferred_job_types: list[str] = []
    excluded_companies: list[str] = []
    min_salary: Optional[int] = None
    max_applications_per_day: int = 10


class UserStats(BaseModel):
    """User statistics schema"""
    total_applications: int
    successful_applications: int
    pending_applications: int
    rejected_applications: int
    average_response_time: float
    success_rate: float


@router.get("/profile", response_model=UserProfile)
async def get_profile(current_token: str = Depends(oauth2_scheme)):
    """Get user profile"""
    # TODO: Fetch user profile from database
    return UserProfile(
        email="user@example.com",
        full_name="Test User",
        company="Tech Corp",
        linkedin_url="https://linkedin.com/in/testuser"
    )


@router.put("/profile", response_model=UserProfile)
async def update_profile(
    profile_data: UserProfile,
    current_token: str = Depends(oauth2_scheme)
):
    """Update user profile"""
    # TODO: Update user profile in database
    return profile_data


@router.get("/settings", response_model=UserSettings)
async def get_settings(current_token: str = Depends(oauth2_scheme)):
    """Get user settings"""
    # TODO: Fetch user settings from database
    return UserSettings()


@router.put("/settings", response_model=UserSettings)
async def update_settings(
    settings_data: UserSettings,
    current_token: str = Depends(oauth2_scheme)
):
    """Update user settings"""
    # TODO: Update user settings in database
    return settings_data


@router.get("/stats", response_model=UserStats)
async def get_stats(current_token: str = Depends(oauth2_scheme)):
    """Get user statistics"""
    # TODO: Calculate stats from database
    return UserStats(
        total_applications=150,
        successful_applications=45,
        pending_applications=30,
        rejected_applications=75,
        average_response_time=3.5,
        success_rate=0.3
    )


@router.post("/linkedin/connect")
async def connect_linkedin(
    linkedin_email: str,
    linkedin_password: str,
    current_token: str = Depends(oauth2_scheme)
):
    """Connect LinkedIn account"""
    # TODO: Securely store LinkedIn credentials
    # TODO: Verify LinkedIn connection
    return {"message": "LinkedIn account connected successfully"}


@router.delete("/linkedin/disconnect")
async def disconnect_linkedin(current_token: str = Depends(oauth2_scheme)):
    """Disconnect LinkedIn account"""
    # TODO: Remove LinkedIn credentials
    return {"message": "LinkedIn account disconnected"}


@router.get("/subscription")
async def get_subscription(current_token: str = Depends(oauth2_scheme)):
    """Get user subscription details"""
    # TODO: Fetch subscription from database
    return {
        "plan": "free",
        "applications_used": 25,
        "applications_limit": 50,
        "expires_at": None
    }


@router.post("/subscription/upgrade")
async def upgrade_subscription(
    plan: str,
    current_token: str = Depends(oauth2_scheme)
):
    """Upgrade subscription plan"""
    if plan not in ["pro", "enterprise"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan. Choose 'pro' or 'enterprise'"
        )
    
    # TODO: Process payment
    # TODO: Update subscription in database
    return {
        "message": f"Successfully upgraded to {plan} plan",
        "plan": plan
    }