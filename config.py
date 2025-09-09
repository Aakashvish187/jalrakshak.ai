"""
Configuration file for JalRakshā AI Backend
Modify these settings to customize the system behavior
"""

# Server Configuration
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
DEBUG_MODE = True

# Database Configuration
DATABASE_NAME = 'jalraksha_ai.db'

# Risk Assessment Thresholds
RISK_THRESHOLDS = {
    'water_level': {
        'low': 40,      # cm
        'medium': 80,   # cm
        'high': 120     # cm
    },
    'rainfall': {
        'low': 40,      # mm
        'medium': 100,  # mm
        'high': 150     # mm
    },
    'river_flow': {
        'low': 100,     # m³/s
        'medium': 300,  # m³/s
        'high': 500     # m³/s
    }
}

# Rescue Team Configuration
RESCUE_TEAMS = [
    {'name': 'Team Alpha-1', 'lat': 20.5937, 'lng': 78.9629, 'status': 'available'},
    {'name': 'Team Beta-2', 'lat': 22.5726, 'lng': 88.3639, 'status': 'standby'},
    {'name': 'Team Gamma-3', 'lat': 13.0827, 'lng': 80.2707, 'status': 'available'},
    {'name': 'Team Delta-4', 'lat': 12.9716, 'lng': 77.5946, 'status': 'available'},
    {'name': 'Team Echo-5', 'lat': 17.3850, 'lng': 78.4867, 'status': 'standby'}
]

# Flood Zones Configuration
FLOOD_ZONES = [
    {'name': 'Mumbai Coastal', 'lat': 19.0760, 'lng': 72.8777, 'radius': 2.0, 'risk_level': 'high'},
    {'name': 'Kolkata Riverside', 'lat': 22.5726, 'lng': 88.3639, 'radius': 1.5, 'risk_level': 'high'},
    {'name': 'Chennai Marina', 'lat': 13.0827, 'lng': 80.2707, 'radius': 1.0, 'risk_level': 'medium'},
    {'name': 'Bangalore Lakes', 'lat': 12.9716, 'lng': 77.5946, 'radius': 0.8, 'risk_level': 'low'},
    {'name': 'Hyderabad Tank', 'lat': 17.3850, 'lng': 78.4867, 'radius': 1.2, 'risk_level': 'medium'}
]

# API Configuration
API_CONFIG = {
    'max_reports_per_request': 50,
    'default_reports_limit': 5,
    'eta_calculation_factor': 1.2,  # km per minute with buffer
    'max_route_alternatives': 3
}

# CORS Configuration
CORS_ORIGINS = [
    'http://localhost:3000',  # React development server
    'http://localhost:8080',  # Static file server
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8080'
]

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Security Configuration (for future use)
SECRET_KEY = 'jalraksha-ai-secret-key-change-in-production'
JWT_EXPIRATION_DELTA = 3600  # 1 hour

# External API Configuration (for future integrations)
EXTERNAL_APIS = {
    'google_maps': {
        'enabled': False,
        'api_key': None,
        'base_url': 'https://maps.googleapis.com/maps/api'
    },
    'weather_api': {
        'enabled': False,
        'api_key': None,
        'base_url': 'https://api.openweathermap.org/data/2.5'
    }
}
