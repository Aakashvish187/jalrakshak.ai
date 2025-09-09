#!/usr/bin/env python3
"""
JalRakshā AI - Quick Demo Test Script
Tests all major components before hackathon presentation
"""

import requests
import time
import webbrowser
import subprocess
import sys
from pathlib import Path

def print_banner():
    """Print demo test banner."""
    print("🌊" + "="*50 + "🌊")
    print("    JalRakshā AI - Demo Test Script")
    print("🌊" + "="*50 + "🌊")
    print()

def test_fastapi_backend():
    """Test FastAPI backend endpoints."""
    print("🔧 Testing FastAPI Backend...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ FastAPI Backend is running")
            return True
        else:
            print("❌ FastAPI Backend health check failed")
            return False
    except requests.exceptions.RequestException:
        print("❌ FastAPI Backend is not running")
        return False

def test_website():
    """Test website accessibility."""
    print("🌐 Testing Website...")
    
    try:
        response = requests.get("http://localhost:8080/index.html", timeout=5)
        if response.status_code == 200:
            print("✅ Website is accessible")
            return True
        else:
            print("❌ Website is not accessible")
            return False
    except requests.exceptions.RequestException:
        print("❌ Website is not running")
        return False

def test_api_endpoints():
    """Test key API endpoints."""
    print("📡 Testing API Endpoints...")
    
    base_url = "http://localhost:8000"
    endpoints = [
        "/get_live_data",
        "/get_reports",
        "/get_rescue_status"
    ]
    
    success_count = 0
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint} - Working")
                success_count += 1
            else:
                print(f"❌ {endpoint} - Failed ({response.status_code})")
        except requests.exceptions.RequestException:
            print(f"❌ {endpoint} - Connection failed")
    
    return success_count == len(endpoints)

def test_risk_prediction():
    """Test risk prediction endpoint."""
    print("🤖 Testing AI Risk Prediction...")
    
    base_url = "http://localhost:8000"
    
    test_data = {
        "water_level": 50,
        "rainfall": 80,
        "river_flow": 200
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict_risk",
            json=test_data,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Risk Prediction - Working (Risk: {data.get('risk', 'Unknown')})")
            return True
        else:
            print(f"❌ Risk Prediction - Failed ({response.status_code})")
            return False
    except requests.exceptions.RequestException:
        print("❌ Risk Prediction - Connection failed")
        return False

def test_sos_system():
    """Test SOS reporting system."""
    print("🚨 Testing SOS System...")
    
    base_url = "http://localhost:8000"
    
    test_report = {
        "location": "Test Location",
        "description": "Demo test report",
        "severity": "medium",
        "contact": "+91-9999999999"
    }
    
    try:
        response = requests.post(
            f"{base_url}/report_issue",
            json=test_report,
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ SOS System - Working")
            return True
        else:
            print(f"❌ SOS System - Failed ({response.status_code})")
            return False
    except requests.exceptions.RequestException:
        print("❌ SOS System - Connection failed")
        return False

def open_demo_urls():
    """Open demo URLs in browser."""
    print("🌐 Opening Demo URLs...")
    
    urls = [
        "http://localhost:8080/index.html",
        "http://localhost:8000/docs"
    ]
    
    for url in urls:
        try:
            webbrowser.open(url)
            print(f"✅ Opened: {url}")
        except Exception as e:
            print(f"❌ Failed to open {url}: {e}")

def main():
    """Main demo test function."""
    print_banner()
    
    print("🚀 Starting JalRakshā AI Demo Test...")
    print()
    
    # Test all components
    tests = [
        ("FastAPI Backend", test_fastapi_backend),
        ("Website", test_website),
        ("API Endpoints", test_api_endpoints),
        ("Risk Prediction", test_risk_prediction),
        ("SOS System", test_sos_system)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # Summary
    print("📊 Test Results Summary:")
    print("="*30)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print()
    print(f"Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All systems ready for hackathon demo!")
        print()
        print("🌐 Opening demo URLs...")
        open_demo_urls()
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        print("💡 Try running: python start_complete_system.py")
    
    print()
    print("🛑 Press Enter to exit...")
    input()

if __name__ == "__main__":
    main()

