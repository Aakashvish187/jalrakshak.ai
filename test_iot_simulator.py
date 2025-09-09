#!/usr/bin/env python3
"""
Test script for IoT Simulator
Tests the fixed IoT simulator with correct API endpoints
"""

import requests
import json
import time

def test_api_endpoints():
    """Test the API endpoints that the IoT simulator uses."""
    print("🧪 Testing API Endpoints...")
    
    # Test prediction endpoint
    print("\n1. Testing Prediction Endpoint...")
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/predict",
            json={
                "water_level": 50.0,
                "rainfall": 80.0,
                "river_flow": 200.0
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction API working")
            print(f"   Response: {data}")
            print(f"   Risk Level: {data.get('risk_level', 'N/A')}")
            print(f"   Confidence: {data.get('confidence', 'N/A')}")
        else:
            print(f"❌ Prediction API failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Prediction API error: {e}")
    
    # Test monitoring endpoint
    print("\n2. Testing Monitoring Endpoint...")
    try:
        response = requests.get(
            "http://localhost:8000/api/v1/flood/monitoring",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Monitoring API working")
            print(f"   Response keys: {list(data.keys())}")
        else:
            print(f"❌ Monitoring API failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Monitoring API error: {e}")

def test_iot_simulator():
    """Test the IoT simulator with a single city."""
    print("\n🌊 Testing IoT Simulator...")
    
    # Import and test the simulator
    try:
        from enhanced_iot_simulator import simulate_city_monitoring, send_to_fastapi
        
        # Test with Mumbai
        print("Testing Mumbai simulation...")
        city = "Mumbai"
        sensor_data = {
            "water_level": 50.0,
            "rainfall": 80.0,
            "river_flow": 200.0,
            "timestamp": "2025-01-09T10:00:00"
        }
        
        # Test prediction
        prediction = send_to_fastapi(sensor_data)
        print(f"Prediction result: {prediction}")
        
        if prediction and 'risk_level' in prediction:
            print("✅ IoT Simulator working correctly")
            print(f"   Risk Level: {prediction['risk_level']}")
            print(f"   Confidence: {prediction['confidence']}")
        else:
            print("❌ IoT Simulator has issues")
            print(f"   Prediction: {prediction}")
            
    except Exception as e:
        print(f"❌ IoT Simulator error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 JalRakshā AI - IoT Simulator Test")
    print("=" * 50)
    
    # Test API endpoints first
    test_api_endpoints()
    
    # Test IoT simulator
    test_iot_simulator()
    
    print("\n✅ Test completed!")
