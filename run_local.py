#!/usr/bin/env python
"""
Simple local runner for RapidApply v2.0
Run without Docker for development
"""

import os
import sys
import uvicorn

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ.setdefault("DATABASE_URL", "sqlite:///rapidapply.db")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
os.environ.setdefault("JWT_SECRET", "development-secret-change-this")

if __name__ == "__main__":
    print("Starting RapidApply v2.0...")
    print("Access the API at: http://localhost:8000")
    print("Access the docs at: http://localhost:8000/api/docs")
    print("Press CTRL+C to stop")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )