"""
Rate limiting middleware
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import time
from typing import Dict
import asyncio

from api.config import settings
from api.utils.redis_client import get_redis


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using Redis"""
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks and docs
        if request.url.path in ["/health", "/api/docs", "/api/openapi.json", "/api/redoc"]:
            return await call_next(request)
        
        # Get client identifier (IP or user ID from token)
        client_id = self.get_client_id(request)
        
        # Check rate limit
        if not await self.check_rate_limit(client_id):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )
        
        # Process request
        response = await call_next(request)
        return response
    
    def get_client_id(self, request: Request) -> str:
        """Get client identifier from request"""
        # Try to get user ID from authorization header
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            # In production, decode JWT to get user ID
            return f"user:{auth_header[7:][:20]}"  # Simplified for now
        
        # Fall back to IP address
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"
    
    async def check_rate_limit(self, client_id: str) -> bool:
        """Check if client has exceeded rate limit"""
        try:
            redis_client = await get_redis()
            key = f"rate_limit:{client_id}"
            
            # Get current count
            current = await redis_client.get(key)
            
            if current is None:
                # First request, set counter
                await redis_client.setex(
                    key,
                    settings.RATE_LIMIT_PERIOD,
                    1
                )
                return True
            
            current_count = int(current)
            
            if current_count >= settings.RATE_LIMIT_REQUESTS:
                return False
            
            # Increment counter
            await redis_client.incr(key)
            return True
            
        except Exception as e:
            # If Redis is down, allow request
            print(f"Rate limit check failed: {e}")
            return True