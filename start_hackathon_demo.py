#!/usr/bin/env python3
"""
JalRakshā AI - Hackathon Demo Startup Script
Simplified startup for hackathon presentation
"""

import subprocess
import time
import webbrowser
import sys
import os
from pathlib import Path

def print_banner():
    """Print startup banner."""
    print("🌊" + "="*60 + "🌊")
    print("    JalRakshā AI - Hackathon Demo Startup")
    print("🌊" + "="*60 + "🌊")
    print()

def check_services():
    """Check if required services are running."""
    print("🔍 Checking services...")
    
    try:
        import requests
        
        # Check FastAPI backend
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("✅ FastAPI Backend is running")
                return True
        except:
            pass
        
        print("❌ FastAPI Backend is not running")
        return False
        
    except ImportError:
        print("❌ requests library not found")
        return False

def start_fastapi():
    """Start FastAPI backend."""
    print("🚀 Starting FastAPI Backend...")
    
    try:
        # Start FastAPI in background
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for startup
        print("⏳ Waiting for FastAPI to start...")
        time.sleep(5)
        
        # Check if it's running
        if check_services():
            print("✅ FastAPI Backend started successfully")
            return process
        else:
            print("❌ FastAPI Backend failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting FastAPI: {e}")
        return None

def start_website():
    """Start website server."""
    print("🌐 Starting Website Server...")
    
    try:
        # Start simple HTTP server
        process = subprocess.Popen([
            sys.executable, "-m", "http.server", "8080"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(2)
        print("✅ Website server started on http://localhost:8080")
        return process
        
    except Exception as e:
        print(f"❌ Error starting website: {e}")
        return None

def start_iot_simulator():
    """Start IoT simulator."""
    print("📡 Starting IoT Simulator...")
    
    try:
        process = subprocess.Popen([
            sys.executable, "enhanced_iot_simulator.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(2)
        print("✅ IoT Simulator started")
        return process
        
    except Exception as e:
        print(f"❌ Error starting IoT simulator: {e}")
        return None

def open_demo():
    """Open demo in browser."""
    print("🌐 Opening demo in browser...")
    
    try:
        webbrowser.open("http://localhost:8080/index.html")
        print("✅ Demo opened in browser")
    except Exception as e:
        print(f"❌ Error opening browser: {e}")

def main():
    """Main startup function."""
    print_banner()
    
    print("🚀 Starting JalRakshā AI Hackathon Demo...")
    print()
    
    # Start services
    processes = {}
    
    # Start FastAPI
    processes['FastAPI'] = start_fastapi()
    if not processes['FastAPI']:
        print("❌ Cannot start demo without FastAPI backend")
        return
    
    # Start website
    processes['Website'] = start_website()
    
    # Start IoT simulator
    processes['IoT'] = start_iot_simulator()
    
    print()
    print("🎉 JalRakshā AI Demo Started Successfully!")
    print("=" * 50)
    print("📊 Demo URLs:")
    print("   • Main Website: http://localhost:8080/index.html")
    print("   • API Documentation: http://localhost:8000/docs")
    print("   • Backend API: http://localhost:8000")
    print()
    print("🔧 Features Available:")
    print("   • Real-time flood monitoring")
    print("   • AI risk prediction")
    print("   • Emergency SOS system")
    print("   • Interactive maps")
    print("   • IoT sensor simulation")
    print()
    
    # Open demo
    open_demo()
    
    print("🛑 Press Ctrl+C to stop all services")
    print()
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        
        # Stop all processes
        for name, process in processes.items():
            if process:
                try:
                    process.terminate()
                    print(f"✅ {name} stopped")
                except:
                    pass
        
        print("👋 Demo stopped")

if __name__ == "__main__":
    main()

