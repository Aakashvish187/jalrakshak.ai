#!/usr/bin/env python3
"""
JalRakshā AI - Complete System Startup Script
Starts all components: FastAPI backend, Telegram bot, IoT simulator, and serves the website
"""

import subprocess
import threading
import time
import webbrowser
import os
import sys
from pathlib import Path

def print_banner():
    """Print startup banner."""
    print("🌊" + "="*60 + "🌊")
    print("    JalRakshā AI - Complete Flood Management System")
    print("🌊" + "="*60 + "🌊")
    print()

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_files = [
        "app/main.py",
        "telegram_bot_with_api.py", 
        "enhanced_iot_simulator.py",
        "index.html"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def start_fastapi_backend():
    """Start FastAPI backend server."""
    print("🚀 Starting FastAPI backend...")
    try:
        # Change to the project directory
        os.chdir(Path(__file__).parent)
        
        # Start FastAPI server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ FastAPI backend started on http://localhost:8000")
            return process
        else:
            print("❌ Failed to start FastAPI backend")
            return None
            
    except Exception as e:
        print(f"❌ Error starting FastAPI: {e}")
        return None

def start_telegram_bot():
    """Start Telegram bot with API."""
    print("📱 Starting Telegram bot...")
    try:
        process = subprocess.Popen([
            sys.executable, "telegram_bot_with_api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for bot to start
        time.sleep(2)
        
        if process.poll() is None:
            print("✅ Telegram bot started on http://localhost:5000")
            return process
        else:
            print("❌ Failed to start Telegram bot")
            return None
            
    except Exception as e:
        print(f"❌ Error starting Telegram bot: {e}")
        return None

def start_iot_simulator():
    """Start IoT sensor simulator."""
    print("📡 Starting IoT sensor simulator...")
    try:
        process = subprocess.Popen([
            sys.executable, "enhanced_iot_simulator.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for simulator to start
        time.sleep(2)
        
        if process.poll() is None:
            print("✅ IoT simulator started")
            return process
        else:
            print("❌ Failed to start IoT simulator")
            return None
            
    except Exception as e:
        print(f"❌ Error starting IoT simulator: {e}")
        return None

def serve_website():
    """Serve the website using Python's built-in server."""
    print("🌐 Starting website server...")
    try:
        # Start simple HTTP server for the website
        process = subprocess.Popen([
            sys.executable, "-m", "http.server", "8080"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(1)
        
        if process.poll() is None:
            print("✅ Website server started on http://localhost:8080")
            return process
        else:
            print("❌ Failed to start website server")
            return None
            
    except Exception as e:
        print(f"❌ Error starting website server: {e}")
        return None

def open_browser():
    """Open browser to the website."""
    print("🌐 Opening website in browser...")
    try:
        webbrowser.open("http://localhost:8080/index.html")
        print("✅ Website opened in browser")
    except Exception as e:
        print(f"❌ Error opening browser: {e}")

def monitor_processes(processes):
    """Monitor all processes and restart if needed."""
    print("👀 Monitoring system processes...")
    
    while True:
        try:
            for name, process in processes.items():
                if process and process.poll() is not None:
                    print(f"⚠️ {name} stopped unexpectedly")
            
            time.sleep(10)  # Check every 10 seconds
            
        except KeyboardInterrupt:
            print("\n🛑 Shutting down all services...")
            break

def main():
    """Main function to start the complete system."""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Please ensure all required files are present")
        return
    
    print("🚀 Starting JalRakshā AI Complete System...")
    print()
    
    # Start all services
    processes = {}
    
    # Start FastAPI backend
    processes['FastAPI'] = start_fastapi_backend()
    time.sleep(2)
    
    # Start Telegram bot
    processes['Telegram Bot'] = start_telegram_bot()
    time.sleep(2)
    
    # Start IoT simulator
    processes['IoT Simulator'] = start_iot_simulator()
    time.sleep(2)
    
    # Start website server
    processes['Website'] = serve_website()
    time.sleep(2)
    
    # Check if all services started successfully
    failed_services = [name for name, process in processes.items() if process is None]
    
    if failed_services:
        print(f"❌ Failed to start: {', '.join(failed_services)}")
        print("🛑 Please check the error messages above and try again")
        return
    
    print()
    print("🎉 JalRakshā AI System Started Successfully!")
    print("="*50)
    print("📊 Services Running:")
    print("   • FastAPI Backend: http://localhost:8000")
    print("   • API Documentation: http://localhost:8000/docs")
    print("   • Telegram Bot API: http://localhost:5000")
    print("   • Website: http://localhost:8080/index.html")
    print("   • IoT Simulator: Running in background")
    print()
    print("🔗 Key Features:")
    print("   • Real-time flood monitoring")
    print("   • AI-powered risk assessment")
    print("   • Telegram emergency alerts")
    print("   • SOS request handling")
    print("   • IoT sensor data integration")
    print()
    print("📱 Telegram Bot Commands:")
    print("   • /start - Start the bot")
    print("   • /help - Get help information")
    print("   • Send 'SOS' or 'HELP' for emergency")
    print()
    print("🌐 Website Features:")
    print("   • Real-time dashboard")
    print("   • Interactive flood maps")
    print("   • Emergency SOS requests")
    print("   • Team management")
    print("   • Analytics and reports")
    print()
    print("🛑 Press Ctrl+C to stop all services")
    print()
    
    # Open browser
    open_browser()
    
    try:
        # Monitor processes
        monitor_processes(processes)
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all services...")
        
        # Stop all processes
        for name, process in processes.items():
            if process:
                try:
                    process.terminate()
                    print(f"✅ {name} stopped")
                except:
                    pass
        
        print("👋 JalRakshā AI system stopped")

if __name__ == "__main__":
    main()
