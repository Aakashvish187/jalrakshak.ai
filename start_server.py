#!/usr/bin/env python3
"""
JalRakshā AI Backend Server Startup Script
This script provides an easy way to start the Flask server with proper configuration
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False

def start_server():
    """Start the Flask server"""
    print("🌊 JalRakshā AI Backend Server")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Cannot start server due to missing dependencies")
        return
    
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("❌ app.py not found in current directory")
        return
    
    print("🚀 Starting Flask server...")
    print("📊 Server will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the Flask app
        os.system("python app.py")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    start_server()
