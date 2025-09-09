from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import random
import math
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Database initialization
def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect('jalraksha_ai.db')
    cursor = conn.cursor()
    
    # Create reports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            severity TEXT DEFAULT 'medium',
            contact TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create rescue_teams table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rescue_teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT UNIQUE NOT NULL,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            status TEXT DEFAULT 'available',
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create flood_zones table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flood_zones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_name TEXT NOT NULL,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            radius REAL DEFAULT 1.0,
            risk_level TEXT DEFAULT 'medium'
        )
    ''')
    
    # Insert sample rescue teams
    sample_teams = [
        ('Team Alpha-1', 20.5937, 78.9629, 'available'),
        ('Team Beta-2', 22.5726, 88.3639, 'standby'),
        ('Team Gamma-3', 13.0827, 80.2707, 'available'),
        ('Team Delta-4', 12.9716, 77.5946, 'available'),
        ('Team Echo-5', 17.3850, 78.4867, 'standby')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO rescue_teams (team_name, lat, lng, status)
        VALUES (?, ?, ?, ?)
    ''', sample_teams)
    
    # Insert sample flood zones
    sample_zones = [
        ('Mumbai Coastal', 19.0760, 72.8777, 2.0, 'high'),
        ('Kolkata Riverside', 22.5726, 88.3639, 1.5, 'high'),
        ('Chennai Marina', 13.0827, 80.2707, 1.0, 'medium'),
        ('Bangalore Lakes', 12.9716, 77.5946, 0.8, 'low'),
        ('Hyderabad Tank', 17.3850, 78.4867, 1.2, 'medium')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO flood_zones (zone_name, lat, lng, radius, risk_level)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_zones)
    
    conn.commit()
    conn.close()

# Helper functions
def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('jalraksha_ai.db')
    conn.row_factory = sqlite3.Row
    return conn

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two coordinates using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    
    a = (math.sin(dlat/2) * math.sin(dlat/2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlng/2) * math.sin(dlng/2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    return distance

def determine_risk_level(water_level, rainfall, river_flow):
    """Determine risk level based on sensor values"""
    risk_score = 0
    
    # Water level thresholds (in cm)
    if water_level > 80:
        risk_score += 3
    elif water_level > 60:
        risk_score += 2
    elif water_level > 40:
        risk_score += 1
    
    # Rainfall thresholds (in mm)
    if rainfall > 100:
        risk_score += 3
    elif rainfall > 70:
        risk_score += 2
    elif rainfall > 40:
        risk_score += 1
    
    # River flow thresholds (in m³/s)
    if river_flow > 300:
        risk_score += 3
    elif river_flow > 200:
        risk_score += 2
    elif river_flow > 100:
        risk_score += 1
    
    # Determine risk level
    if risk_score >= 6:
        return "High"
    elif risk_score >= 3:
        return "Medium"
    else:
        return "Low"

# API Endpoints

@app.route('/get_live_data', methods=['GET'])
def get_live_data():
    """Get simulated live sensor data"""
    try:
        # Generate random sensor values
        water_level = random.randint(20, 120)  # cm
        rainfall = random.randint(10, 150)      # mm
        river_flow = random.randint(50, 400)   # m³/s
        
        # Determine risk level
        risk = determine_risk_level(water_level, rainfall, river_flow)
        
        response = {
            "water_level": water_level,
            "rainfall": rainfall,
            "river_flow": river_flow,
            "risk": risk,
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict_risk', methods=['POST'])
def predict_risk():
    """Predict risk level from input sensor data"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Extract sensor values
        water_level = data.get('water_level', 0)
        rainfall = data.get('rainfall', 0)
        river_flow = data.get('river_flow', 0)
        
        # Validate inputs
        if not all(isinstance(x, (int, float)) for x in [water_level, rainfall, river_flow]):
            return jsonify({"error": "Invalid sensor values"}), 400
        
        # Determine risk level
        risk = determine_risk_level(water_level, rainfall, river_flow)
        
        response = {
            "risk": risk,
            "confidence": random.uniform(0.75, 0.95),  # Mock confidence score
            "factors": {
                "water_level_impact": "High" if water_level > 80 else "Medium" if water_level > 60 else "Low",
                "rainfall_impact": "High" if rainfall > 100 else "Medium" if rainfall > 70 else "Low",
                "river_flow_impact": "High" if river_flow > 300 else "Medium" if river_flow > 200 else "Low"
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_safe_route', methods=['GET'])
def get_safe_route():
    """Get safe route between two locations"""
    try:
        from_location = request.args.get('from', '')
        to_location = request.args.get('to', '')
        
        if not from_location or not to_location:
            return jsonify({"error": "Both 'from' and 'to' parameters are required"}), 400
        
        # Mock route data (in real implementation, use Google Maps API)
        routes = [
            {
                "best_route": f"Via Highway 101 - {from_location} → {to_location}",
                "eta": f"{random.randint(15, 45)} min",
                "safety_score": random.choice(["Low Risk", "Medium Risk", "High Risk"]),
                "distance": f"{random.uniform(5.0, 25.0):.1f} km",
                "steps": [
                    f"Start from {from_location}",
                    "Take Highway 101 North",
                    "Avoid flooded areas near Riverside District",
                    f"Continue to {to_location}"
                ],
                "alternatives": [
                    f"Alternative Route: Via Coastal Road - {random.randint(20, 50)} min",
                    f"Emergency Route: Via Mountain Pass - {random.randint(30, 60)} min"
                ]
            }
        ]
        
        # Check for flood zones along the route
        conn = get_db_connection()
        flood_zones = conn.execute('SELECT * FROM flood_zones').fetchall()
        conn.close()
        
        # Add flood zone warnings
        warnings = []
        for zone in flood_zones:
            if zone['risk_level'] in ['high', 'medium']:
                warnings.append(f"⚠️ {zone['zone_name']} - {zone['risk_level'].title()} Risk Zone")
        
        response = routes[0]
        response['warnings'] = warnings
        response['route_id'] = f"route_{random.randint(1000, 9999)}"
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/assign_rescue', methods=['POST'])
def assign_rescue():
    """Assign nearest available rescue team"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        lat = data.get('lat')
        lng = data.get('lng')
        
        if lat is None or lng is None:
            return jsonify({"error": "Latitude and longitude are required"}), 400
        
        # Find nearest available team
        conn = get_db_connection()
        teams = conn.execute('SELECT * FROM rescue_teams WHERE status = "available"').fetchall()
        
        if not teams:
            conn.close()
            return jsonify({"error": "No available rescue teams"}), 404
        
        # Calculate distances and find nearest team
        nearest_team = None
        min_distance = float('inf')
        
        for team in teams:
            distance = calculate_distance(lat, lng, team['lat'], team['lng'])
            if distance < min_distance:
                min_distance = distance
                nearest_team = team
        
        if nearest_team:
            # Update team status to dispatched
            conn.execute('''
                UPDATE rescue_teams 
                SET status = 'dispatched', last_updated = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (nearest_team['id'],))
            conn.commit()
            
            # Calculate ETA (rough estimate: 1 km per minute)
            eta_minutes = int(min_distance * 1.2)  # Add 20% buffer
            
            response = {
                "team": nearest_team['team_name'],
                "eta": f"{eta_minutes} min",
                "status": "Dispatched",
                "distance": f"{min_distance:.1f} km",
                "team_id": nearest_team['id'],
                "dispatch_time": datetime.now().isoformat()
            }
            
            conn.close()
            return jsonify(response), 200
        else:
            conn.close()
            return jsonify({"error": "No suitable team found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/report_issue', methods=['POST'])
def report_issue():
    """Submit citizen report"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        location = data.get('location', '').strip()
        description = data.get('description', '').strip()
        severity = data.get('severity', 'medium')
        contact = data.get('contact', '')
        
        if not location or not description:
            return jsonify({"error": "Location and description are required"}), 400
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.execute('''
            INSERT INTO reports (location, description, severity, contact)
            VALUES (?, ?, ?, ?)
        ''', (location, description, severity, contact))
        
        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        response = {
            "message": "Report submitted successfully",
            "report_id": report_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_reports', methods=['GET'])
def get_reports():
    """Get latest reports"""
    try:
        limit = request.args.get('limit', 5, type=int)
        
        conn = get_db_connection()
        reports = conn.execute('''
            SELECT * FROM reports 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,)).fetchall()
        conn.close()
        
        response = []
        for report in reports:
            response.append({
                "id": report['id'],
                "location": report['location'],
                "description": report['description'],
                "severity": report['severity'],
                "contact": report['contact'],
                "timestamp": report['timestamp']
            })
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_rescue_status', methods=['GET'])
def get_rescue_status():
    """Get rescue team status for frontend map"""
    try:
        conn = get_db_connection()
        teams = conn.execute('SELECT * FROM rescue_teams ORDER BY team_name').fetchall()
        conn.close()
        
        response = []
        for team in teams:
            response.append({
                "team": team['team_name'],
                "lat": team['lat'],
                "lng": team['lng'],
                "status": team['status'],
                "last_updated": team['last_updated']
            })
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Additional utility endpoints

@app.route('/get_flood_zones', methods=['GET'])
def get_flood_zones():
    """Get flood zones for route planning"""
    try:
        conn = get_db_connection()
        zones = conn.execute('SELECT * FROM flood_zones').fetchall()
        conn.close()
        
        response = []
        for zone in zones:
            response.append({
                "zone_name": zone['zone_name'],
                "lat": zone['lat'],
                "lng": zone['lng'],
                "radius": zone['radius'],
                "risk_level": zone['risk_level']
            })
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reset_team_status', methods=['POST'])
def reset_team_status():
    """Reset team status (for testing)"""
    try:
        conn = get_db_connection()
        conn.execute('UPDATE rescue_teams SET status = "available"')
        conn.commit()
        conn.close()
        
        return jsonify({"message": "All team statuses reset to available"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "JalRakshā AI Backend",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run Flask app
    print("🌊 JalRakshā AI Backend Server Starting...")
    print("📊 Database initialized with sample data")
    print("🚀 Server running on http://localhost:5000")
    print("📋 Available endpoints:")
    print("   GET  /get_live_data")
    print("   POST /predict_risk")
    print("   GET  /get_safe_route")
    print("   POST /assign_rescue")
    print("   POST /report_issue")
    print("   GET  /get_reports")
    print("   GET  /get_rescue_status")
    print("   GET  /health")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
