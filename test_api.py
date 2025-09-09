#!/usr/bin/env python3
"""
Test script for JalRakshā AI Flask API
Run this after starting the Flask server to test all endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_endpoint(method, endpoint, data=None, params=None):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, json=data)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        print(f"🔍 {method} {endpoint}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Success")
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"   ❌ Error: {response.text}")
        
        print()
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed. Make sure Flask server is running on {BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all API tests"""
    print("🌊 JalRakshā AI API Test Suite")
    print("=" * 50)
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    test_endpoint("GET", "/health")
    
    # Test 2: Get Live Data
    print("2. Testing Live Sensor Data...")
    test_endpoint("GET", "/get_live_data")
    
    # Test 3: Predict Risk
    print("3. Testing Risk Prediction...")
    risk_data = {
        "water_level": 75,
        "rainfall": 85,
        "river_flow": 250
    }
    test_endpoint("POST", "/predict_risk", data=risk_data)
    
    # Test 4: Safe Route Finder
    print("4. Testing Safe Route Finder...")
    test_endpoint("GET", "/get_safe_route", params={"from": "Mumbai", "to": "Pune"})
    
    # Test 5: Assign Rescue Team
    print("5. Testing Rescue Team Assignment...")
    rescue_data = {
        "lat": 20.5937,
        "lng": 78.9629
    }
    test_endpoint("POST", "/assign_rescue", data=rescue_data)
    
    # Test 6: Report Issue
    print("6. Testing Issue Reporting...")
    report_data = {
        "location": "Riverside District",
        "description": "Severe flooding, roads blocked",
        "severity": "critical",
        "contact": "+91-9876543210"
    }
    test_endpoint("POST", "/report_issue", data=report_data)
    
    # Test 7: Get Reports
    print("7. Testing Get Reports...")
    test_endpoint("GET", "/get_reports")
    
    # Test 8: Get Rescue Status
    print("8. Testing Rescue Team Status...")
    test_endpoint("GET", "/get_rescue_status")
    
    # Test 9: Get Flood Zones
    print("9. Testing Flood Zones...")
    test_endpoint("GET", "/get_flood_zones")
    
    print("🎉 API Testing Complete!")
    print("\n💡 Tips:")
    print("   - Check the database file 'jalraksha_ai.db' for stored data")
    print("   - Use the reset endpoint to reset team statuses for testing")
    print("   - All endpoints return JSON responses with proper error handling")

if __name__ == "__main__":
    main()
