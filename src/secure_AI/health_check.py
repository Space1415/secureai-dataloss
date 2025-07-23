#!/usr/bin/env python3
"""
Health Check Endpoint for SecureAI MCP
"""

import json
import psutil
import time
from datetime import datetime

def health_check():
    """Perform health check and return status."""
    try:
        # Check system resources
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Check if SecureAI modules can be imported
        try:
            import masquerade
            secureai_status = "healthy"
        except ImportError:
            secureai_status = "unhealthy"
        
        # Check API key (if available)
        api_key_status = "unknown"
        try:
            import os
            if os.getenv("TINFOIL_API_KEY"):
                api_key_status = "configured"
            else:
                api_key_status = "missing"
        except:
            pass
        
        health_data = {
            "status": "healthy" if secureai_status == "healthy" else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "components": {
                "secureai": secureai_status,
                "api_key": api_key_status
            },
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent
            }
        }
        
        return health_data
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

if __name__ == "__main__":
    health = health_check()
    print(json.dumps(health, indent=2))
