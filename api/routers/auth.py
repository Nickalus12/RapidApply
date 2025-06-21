"""
Authentication router
Handles user registration, login, and token management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
import jwt

from api.config import settings
from api.utils.security import verify_password, hash_password, create_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


class UserRegister(BaseModel):
    """User registration schema"""
    email: EmailStr
    password: str
    full_name: str
    company: Optional[str] = None


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token data schema"""
    email: Optional[str] = None
    user_id: Optional[str] = None


@router.post("/register", response_model=Token)
async def register(user_data: UserRegister):
    """Register a new user"""
    # TODO: Check if user exists in database
    # TODO: Create user in database
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user_data.email, "user_id": "temp-user-id"}
    )
    
    return {
        "access_token": access_token,
        "expires_in": settings.JWT_EXPIRATION_MINUTES * 60
    }


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user with email and password"""
    # TODO: Verify user credentials from database
    # TODO: Check if user is active
    
    # Create access token
    access_token = create_access_token(
        data={"sub": form_data.username, "user_id": "temp-user-id"}
    )
    
    return {
        "access_token": access_token,
        "expires_in": settings.JWT_EXPIRATION_MINUTES * 60
    }


@router.post("/token", response_model=Token)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 compatible token endpoint"""
    return await login(form_data)


@router.post("/refresh", response_model=Token)
async def refresh_token(current_token: str = Depends(oauth2_scheme)):
    """Refresh access token"""
    try:
        # Decode current token
        payload = jwt.decode(
            current_token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        
        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Create new token
        access_token = create_access_token(
            data={"sub": email, "user_id": user_id}
        )
        
        return {
            "access_token": access_token,
            "expires_in": settings.JWT_EXPIRATION_MINUTES * 60
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


@router.post("/logout")
async def logout(current_token: str = Depends(oauth2_scheme)):
    """Logout user (invalidate token)"""
    # TODO: Add token to blacklist in Redis
    return {"message": "Successfully logged out"}


@router.get("/me")
async def get_current_user(current_token: str = Depends(oauth2_scheme)):
    """Get current user information"""
    try:
        # Decode token
        payload = jwt.decode(
            current_token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        
        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # TODO: Fetch user from database
        return {
            "id": user_id,
            "email": email,
            "full_name": "Test User",
            "is_active": True
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )