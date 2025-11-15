#!/usr/bin/env python3
"""
PALETTE-AI Development Server
Run this script to start the local development server
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("🎨 Starting PALETTE-AI development server...")
    print(f"📍 http://localhost:{settings.APP_PORT}")
    print(f"📚 API Docs: http://localhost:{settings.APP_PORT}/docs")
    print("\nPress CTRL+C to stop\n")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
