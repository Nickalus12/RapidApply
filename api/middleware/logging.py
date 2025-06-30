"""
Logging middleware for request/response tracking
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
import uuid
from typing import Dict

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging all requests and responses"""
    
    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Add request ID to request state
        request.state.request_id = request_id
        
        # Record start time
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else "unknown"
            }
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"Request completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration": f"{duration:.3f}s"
            }
        )
        
        # Add custom headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(duration)
        
        return response