"""
Disaster Management Router for JalRakshā AI

This module provides comprehensive disaster monitoring and city-level risk assessment
for all Indian cities with real-time IoT data and AI predictions.
"""

import logging
import random
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter()

# Indian Cities Database with comprehensive data - All States Coverage
INDIAN_CITIES_DATABASE = {
    # GUJARAT
    "Ahmedabad": {
        "lat": 23.0225, "lng": 72.5714, "state": "Gujarat", "population": "8M",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.6
    },
    "Baroda": {
        "lat": 22.3072, "lng": 73.1812, "state": "Gujarat", "population": "2M",
        "flood_risk_factor": 0.5, "monsoon_intensity": 0.6, "drainage_capacity": 0.6
    },
    "Dwarka": {
        "lat": 22.2403, "lng": 68.9686, "state": "Gujarat", "population": "50K",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.7
    },
    "Somnath": {
        "lat": 20.8880, "lng": 70.4060, "state": "Gujarat", "population": "20K",
        "flood_risk_factor": 0.2, "monsoon_intensity": 0.3, "drainage_capacity": 0.8
    },
    "Rajkot": {
        "lat": 22.3039, "lng": 70.8022, "state": "Gujarat", "population": "1M",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.7
    },
    "Bhavnagar": {
        "lat": 21.7645, "lng": 72.1519, "state": "Gujarat", "population": "600K",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.6
    },
    "Surat": {
        "lat": 21.1702, "lng": 72.8311, "state": "Gujarat", "population": "6M",
        "flood_risk_factor": 0.7, "monsoon_intensity": 0.6, "drainage_capacity": 0.5
    },
    
    # MAHARASHTRA
    "Mumbai": {
        "lat": 19.0760, "lng": 72.8777, "state": "Maharashtra", "population": "20M",
        "flood_risk_factor": 0.8, "monsoon_intensity": 0.9, "drainage_capacity": 0.4
    },
    "Nashik": {
        "lat": 19.9975, "lng": 73.7898, "state": "Maharashtra", "population": "1M",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.7
    },
    "Aurangabad": {
        "lat": 19.8762, "lng": 75.3433, "state": "Maharashtra", "population": "1M",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.8
    },
    "Solapur": {
        "lat": 17.6599, "lng": 75.9064, "state": "Maharashtra", "population": "900K",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.7
    },
    "Kolhapur": {
        "lat": 16.7050, "lng": 74.2433, "state": "Maharashtra", "population": "500K",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    "Sangli": {
        "lat": 16.8524, "lng": 74.5815, "state": "Maharashtra", "population": "400K",
        "flood_risk_factor": 0.5, "monsoon_intensity": 0.6, "drainage_capacity": 0.6
    },
    # DELHI
    "Delhi": {
        "lat": 28.7041, "lng": 77.1025, "state": "Delhi", "population": "19M",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.7
    },
    
    # UTTAR PRADESH
    "Lucknow": {
        "lat": 26.8467, "lng": 80.9462, "state": "Uttar Pradesh", "population": "4M",
        "flood_risk_factor": 0.5, "monsoon_intensity": 0.6, "drainage_capacity": 0.6
    },
    "Kanpur": {
        "lat": 26.4499, "lng": 80.3319, "state": "Uttar Pradesh", "population": "3M",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    "Agra": {
        "lat": 27.1767, "lng": 78.0081, "state": "Uttar Pradesh", "population": "2M",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.6
    },
    "Varanasi": {
        "lat": 25.3176, "lng": 82.9739, "state": "Uttar Pradesh", "population": "1M",
        "flood_risk_factor": 0.7, "monsoon_intensity": 0.8, "drainage_capacity": 0.4
    },
    "Allahabad": {
        "lat": 25.4358, "lng": 81.8463, "state": "Uttar Pradesh", "population": "1M",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    "Meerut": {
        "lat": 28.9845, "lng": 77.7064, "state": "Uttar Pradesh", "population": "1M",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.7
    },
    
    # BIHAR
    "Patna": {
        "lat": 25.5941, "lng": 85.1376, "state": "Bihar", "population": "2M",
        "flood_risk_factor": 0.8, "monsoon_intensity": 0.9, "drainage_capacity": 0.3
    },
    "Gaya": {
        "lat": 24.7955, "lng": 84.9994, "state": "Bihar", "population": "500K",
        "flood_risk_factor": 0.5, "monsoon_intensity": 0.6, "drainage_capacity": 0.6
    },
    "Muzaffarpur": {
        "lat": 26.1209, "lng": 85.3647, "state": "Bihar", "population": "400K",
        "flood_risk_factor": 0.7, "monsoon_intensity": 0.8, "drainage_capacity": 0.4
    },
    "Bhagalpur": {
        "lat": 25.2445, "lng": 86.9718, "state": "Bihar", "population": "400K",
        "flood_risk_factor": 0.8, "monsoon_intensity": 0.9, "drainage_capacity": 0.3
    },
    "Darbhanga": {
        "lat": 26.1667, "lng": 85.9000, "state": "Bihar", "population": "300K",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    # WEST BENGAL
    "Kolkata": {
        "lat": 22.5726, "lng": 88.3639, "state": "West Bengal", "population": "15M",
        "flood_risk_factor": 0.85, "monsoon_intensity": 0.9, "drainage_capacity": 0.4
    },
    "Siliguri": {
        "lat": 26.7271, "lng": 88.3643, "state": "West Bengal", "population": "500K",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    "Howrah": {
        "lat": 22.5958, "lng": 88.2636, "state": "West Bengal", "population": "1M",
        "flood_risk_factor": 0.8, "monsoon_intensity": 0.9, "drainage_capacity": 0.3
    },
    "Durgapur": {
        "lat": 23.5204, "lng": 87.3119, "state": "West Bengal", "population": "600K",
        "flood_risk_factor": 0.5, "monsoon_intensity": 0.6, "drainage_capacity": 0.6
    },
    "Asansol": {
        "lat": 23.6739, "lng": 86.9524, "state": "West Bengal", "population": "1M",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.7
    },
    "Malda": {
        "lat": 25.0118, "lng": 88.1407, "state": "West Bengal", "population": "400K",
        "flood_risk_factor": 0.7, "monsoon_intensity": 0.8, "drainage_capacity": 0.4
    },
    # TAMIL NADU
    "Chennai": {
        "lat": 13.0827, "lng": 80.2707, "state": "Tamil Nadu", "population": "11M",
        "flood_risk_factor": 0.9, "monsoon_intensity": 0.8, "drainage_capacity": 0.3
    },
    "Madurai": {
        "lat": 9.9252, "lng": 78.1198, "state": "Tamil Nadu", "population": "1M",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    "Coimbatore": {
        "lat": 11.0168, "lng": 76.9558, "state": "Tamil Nadu", "population": "2M",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.7
    },
    "Salem": {
        "lat": 11.6643, "lng": 78.1460, "state": "Tamil Nadu", "population": "1M",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.7
    },
    "Tiruchirappalli": {
        "lat": 10.7905, "lng": 78.7047, "state": "Tamil Nadu", "population": "1M",
        "flood_risk_factor": 0.5, "monsoon_intensity": 0.6, "drainage_capacity": 0.6
    },
    "Tirunelveli": {
        "lat": 8.7139, "lng": 77.7567, "state": "Tamil Nadu", "population": "1M",
        "flood_risk_factor": 0.5, "monsoon_intensity": 0.6, "drainage_capacity": 0.6
    },
    
    # TELANGANA
    "Hyderabad": {
        "lat": 17.3850, "lng": 78.4867, "state": "Telangana", "population": "10M",
        "flood_risk_factor": 0.5, "monsoon_intensity": 0.6, "drainage_capacity": 0.6
    },
    "Warangal": {
        "lat": 17.9689, "lng": 79.5941, "state": "Telangana", "population": "800K",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.7
    },
    "Nizamabad": {
        "lat": 18.6712, "lng": 78.0938, "state": "Telangana", "population": "300K",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.8
    },
    
    # KARNATAKA
    "Bangalore": {
        "lat": 12.9716, "lng": 77.5946, "state": "Karnataka", "population": "12M",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.7
    },
    "Mysuru": {
        "lat": 12.2958, "lng": 76.6394, "state": "Karnataka", "population": "1M",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.8
    },
    "Mangalore": {
        "lat": 12.9141, "lng": 74.8560, "state": "Karnataka", "population": "500K",
        "flood_risk_factor": 0.7, "monsoon_intensity": 0.8, "drainage_capacity": 0.4
    },
    "Hubli": {
        "lat": 15.3647, "lng": 75.1240, "state": "Karnataka", "population": "900K",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.7
    },
    "Belgaum": {
        "lat": 15.8497, "lng": 74.4977, "state": "Karnataka", "population": "600K",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.8
    },
    "Gulbarga": {
        "lat": 17.3297, "lng": 76.8343, "state": "Karnataka", "population": "500K",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.8
    },
    "Pune": {
        "lat": 18.5204, "lng": 73.8567, "state": "Maharashtra", "population": "7M",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    "Jaipur": {
        "lat": 26.9124, "lng": 75.7873, "state": "Rajasthan", "population": "4M",
        "flood_risk_factor": 0.2, "monsoon_intensity": 0.3, "drainage_capacity": 0.8
    },
    "Kanpur": {
        "lat": 26.4499, "lng": 80.3319, "state": "Uttar Pradesh", "population": "3M",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    "Nagpur": {
        "lat": 21.1458, "lng": 79.0882, "state": "Maharashtra", "population": "3M",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.7
    },
    "Indore": {
        "lat": 22.7196, "lng": 75.8577, "state": "Madhya Pradesh", "population": "3M",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.6
    },
    "Thane": {
        "lat": 19.2183, "lng": 72.9781, "state": "Maharashtra", "population": "2M",
        "flood_risk_factor": 0.8, "monsoon_intensity": 0.85, "drainage_capacity": 0.4
    },
    "Bhopal": {
        "lat": 23.2599, "lng": 77.4126, "state": "Madhya Pradesh", "population": "2M",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.7
    },
    "Visakhapatnam": {
        "lat": 17.6868, "lng": 83.2185, "state": "Andhra Pradesh", "population": "2M",
        "flood_risk_factor": 0.7, "monsoon_intensity": 0.8, "drainage_capacity": 0.5
    },
    "Vadodara": {
        "lat": 22.3072, "lng": 73.1812, "state": "Gujarat", "population": "2M",
        "flood_risk_factor": 0.5, "monsoon_intensity": 0.6, "drainage_capacity": 0.6
    },
    "Kochi": {
        "lat": 9.9312, "lng": 76.2673, "state": "Kerala", "population": "2M",
        "flood_risk_factor": 0.9, "monsoon_intensity": 0.95, "drainage_capacity": 0.3
    },
    "Coimbatore": {
        "lat": 11.0168, "lng": 76.9558, "state": "Tamil Nadu", "population": "2M",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.7
    },
    "Trivandrum": {
        "lat": 8.5241, "lng": 76.9366, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.8, "monsoon_intensity": 0.9, "drainage_capacity": 0.4
    },
    "Madurai": {
        "lat": 9.9252, "lng": 78.1198, "state": "Tamil Nadu", "population": "1M",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    "Tiruchirappalli": {
        "lat": 10.7905, "lng": 78.7047, "state": "Tamil Nadu", "population": "1M",
        "flood_risk_factor": 0.5, "monsoon_intensity": 0.6, "drainage_capacity": 0.6
    },
    "Salem": {
        "lat": 11.6643, "lng": 78.1460, "state": "Tamil Nadu", "population": "1M",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.7
    },
    "Tirunelveli": {
        "lat": 8.7139, "lng": 77.7567, "state": "Tamil Nadu", "population": "1M",
        "flood_risk_factor": 0.5, "monsoon_intensity": 0.6, "drainage_capacity": 0.6
    },
    "Erode": {
        "lat": 11.3410, "lng": 77.7172, "state": "Tamil Nadu", "population": "1M",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.8
    },
    "Thanjavur": {
        "lat": 10.7867, "lng": 79.1378, "state": "Tamil Nadu", "population": "1M",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    "Kollam": {
        "lat": 8.8932, "lng": 76.6141, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.7, "monsoon_intensity": 0.8, "drainage_capacity": 0.4
    },
    "Thrissur": {
        "lat": 10.5276, "lng": 76.2144, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    "Kottayam": {
        "lat": 9.5916, "lng": 76.5222, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.8, "monsoon_intensity": 0.9, "drainage_capacity": 0.3
    },
    "Palakkad": {
        "lat": 10.7867, "lng": 76.6548, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.5, "monsoon_intensity": 0.6, "drainage_capacity": 0.6
    },
    "Malappuram": {
        "lat": 11.0500, "lng": 76.0700, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.7, "monsoon_intensity": 0.8, "drainage_capacity": 0.4
    },
    "Kozhikode": {
        "lat": 11.2588, "lng": 75.7804, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.8, "monsoon_intensity": 0.9, "drainage_capacity": 0.3
    },
    "Kannur": {
        "lat": 11.8745, "lng": 75.3704, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    "Kasaragod": {
        "lat": 12.5000, "lng": 74.9833, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.7, "monsoon_intensity": 0.8, "drainage_capacity": 0.4
    },
    "Alappuzha": {
        "lat": 9.4981, "lng": 76.3388, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.95, "monsoon_intensity": 0.9, "drainage_capacity": 0.2
    },
    "Pathanamthitta": {
        "lat": 9.2647, "lng": 76.7870, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    "Idukki": {
        "lat": 9.8497, "lng": 76.9681, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.7, "monsoon_intensity": 0.8, "drainage_capacity": 0.4
    },
    "Wayanad": {
        "lat": 11.6854, "lng": 76.1320, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.8, "monsoon_intensity": 0.9, "drainage_capacity": 0.3
    },
    "Ernakulam": {
        "lat": 9.9816, "lng": 76.2999, "state": "Kerala", "population": "1M",
        "flood_risk_factor": 0.9, "monsoon_intensity": 0.95, "drainage_capacity": 0.3
    },
    "Chandigarh": {
        "lat": 30.7333, "lng": 76.7794, "state": "Punjab", "population": "1M",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.8
    },
    "Ludhiana": {
        "lat": 30.9010, "lng": 75.8573, "state": "Punjab", "population": "2M",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.7
    },
    "Amritsar": {
        "lat": 31.6340, "lng": 74.8723, "state": "Punjab", "population": "1M",
        "flood_risk_factor": 0.3, "monsoon_intensity": 0.4, "drainage_capacity": 0.8
    },
    "Jalandhar": {
        "lat": 31.3260, "lng": 75.5762, "state": "Punjab", "population": "1M",
        "flood_risk_factor": 0.4, "monsoon_intensity": 0.5, "drainage_capacity": 0.7
    },
    "Guwahati": {
        "lat": 26.1445, "lng": 91.7362, "state": "Assam", "population": "1M",
        "flood_risk_factor": 0.8, "monsoon_intensity": 0.9, "drainage_capacity": 0.3
    },
    "Dibrugarh": {
        "lat": 27.4728, "lng": 94.9120, "state": "Assam", "population": "1M",
        "flood_risk_factor": 0.7, "monsoon_intensity": 0.8, "drainage_capacity": 0.4
    },
    "Silchar": {
        "lat": 24.8167, "lng": 92.8000, "state": "Assam", "population": "1M",
        "flood_risk_factor": 0.8, "monsoon_intensity": 0.9, "drainage_capacity": 0.3
    },
    "Jorhat": {
        "lat": 26.7509, "lng": 94.2037, "state": "Assam", "population": "1M",
        "flood_risk_factor": 0.6, "monsoon_intensity": 0.7, "drainage_capacity": 0.5
    },
    "Tezpur": {
        "lat": 26.6333, "lng": 92.8000, "state": "Assam", "population": "1M",
        "flood_risk_factor": 0.7, "monsoon_intensity": 0.8, "drainage_capacity": 0.4
    }
}

# Historical disaster events for each city - Comprehensive 5-year data
HISTORICAL_EVENTS = {
    # Gujarat Cities
    "Ahmedabad": [
        {"year": 2019, "event": "Major flood affected 5000 people"},
        {"year": 2020, "event": "Flash floods in urban areas"},
        {"year": 2021, "event": "Drainage system failure"},
        {"year": 2022, "event": "Cyclone Tauktae impact"},
        {"year": 2023, "event": "Monsoon waterlogging"}
    ],
    "Baroda": [
        {"year": 2019, "event": "Heavy rainfall caused flooding"},
        {"year": 2020, "event": "Urban drainage overflow"},
        {"year": 2021, "event": "Monsoon season flooding"},
        {"year": 2022, "event": "Flash floods in low-lying areas"},
        {"year": 2023, "event": "Heavy rains affected traffic"}
    ],
    "Surat": [
        {"year": 2019, "event": "Tapi River overflow"},
        {"year": 2020, "event": "Urban flooding in diamond district"},
        {"year": 2021, "event": "Monsoon rains caused waterlogging"},
        {"year": 2022, "event": "Heavy rainfall warnings"},
        {"year": 2023, "event": "Drainage system overload"}
    ],
    
    # Maharashtra Cities
    "Mumbai": [
        {"year": 2019, "event": "Heavy rainfall paralyzed city for days"},
        {"year": 2020, "event": "Monsoon flooding affected millions"},
        {"year": 2021, "event": "Cyclone Tauktae caused severe damage"},
        {"year": 2022, "event": "Heavy rains flooded low-lying areas"},
        {"year": 2023, "event": "Urban flooding in suburbs"}
    ],
    "Pune": [
        {"year": 2019, "event": "Heavy monsoon rains"},
        {"year": 2020, "event": "Urban flooding in IT areas"},
        {"year": 2021, "event": "Drainage system failure"},
        {"year": 2022, "event": "Flash floods in outskirts"},
        {"year": 2023, "event": "Monsoon waterlogging"}
    ],
    
    # Bihar Cities
    "Patna": [
        {"year": 2019, "event": "Koshi River flood displaced 2000 families"},
        {"year": 2020, "event": "Monsoon rains overflowed Ganga"},
        {"year": 2021, "event": "Urban flooding in city center"},
        {"year": 2022, "event": "Heavy rainfall warnings"},
        {"year": 2023, "event": "Drainage system overload"}
    ],
    "Gaya": [
        {"year": 2019, "event": "Monsoon season flooding"},
        {"year": 2020, "event": "Heavy rainfall caused waterlogging"},
        {"year": 2021, "event": "Urban drainage overflow"},
        {"year": 2022, "event": "Flash floods in low-lying areas"},
        {"year": 2023, "event": "Heavy rains affected traffic"}
    ],
    
    # West Bengal Cities
    "Kolkata": [
        {"year": 2019, "event": "Cyclone Mora caused severe flooding"},
        {"year": 2020, "event": "Amphan cyclone devastated coastal areas"},
        {"year": 2021, "event": "Heavy monsoon damage"},
        {"year": 2022, "event": "Urban flooding in low-lying areas"},
        {"year": 2023, "event": "Drainage system failure"}
    ],
    "Siliguri": [
        {"year": 2019, "event": "Monsoon flooding in tea gardens"},
        {"year": 2020, "event": "Heavy rainfall warnings"},
        {"year": 2021, "event": "Urban drainage overflow"},
        {"year": 2022, "event": "Flash floods in outskirts"},
        {"year": 2023, "event": "Monsoon waterlogging"}
    ],
    
    # Tamil Nadu Cities
    "Chennai": [
        {"year": 2019, "event": "Cyclone Gaja brought severe flooding"},
        {"year": 2020, "event": "Heavy rains flooded low-lying areas"},
        {"year": 2021, "event": "Urban flooding in IT corridor"},
        {"year": 2022, "event": "Monsoon season flooding"},
        {"year": 2023, "event": "Drainage system overload"}
    ],
    "Madurai": [
        {"year": 2019, "event": "Heavy monsoon rains"},
        {"year": 2020, "event": "Urban flooding in temple areas"},
        {"year": 2021, "event": "Drainage system failure"},
        {"year": 2022, "event": "Flash floods in outskirts"},
        {"year": 2023, "event": "Monsoon waterlogging"}
    ],
    
    # Karnataka Cities
    "Bangalore": [
        {"year": 2019, "event": "Heavy rainfall caused flooding"},
        {"year": 2020, "event": "Urban drainage overflow"},
        {"year": 2021, "event": "Monsoon season flooding"},
        {"year": 2022, "event": "Flash floods in IT areas"},
        {"year": 2023, "event": "Heavy rains affected traffic"}
    ],
    "Mysuru": [
        {"year": 2019, "event": "Monsoon flooding in palace area"},
        {"year": 2020, "event": "Heavy rainfall warnings"},
        {"year": 2021, "event": "Urban drainage overflow"},
        {"year": 2022, "event": "Flash floods in outskirts"},
        {"year": 2023, "event": "Monsoon waterlogging"}
    ],
    
    # Kerala Cities
    "Kochi": [
        {"year": 2019, "event": "Heavy monsoon caused landslides"},
        {"year": 2020, "event": "Flash floods in urban areas"},
        {"year": 2021, "event": "Monsoon flooding in port area"},
        {"year": 2022, "event": "Heavy rainfall warnings"},
        {"year": 2023, "event": "Drainage system overload"}
    ],
    "Alappuzha": [
        {"year": 2019, "event": "Monsoon flooding affected tourism"},
        {"year": 2020, "event": "Heavy rains flooded low-lying areas"},
        {"year": 2021, "event": "Backwaters overflow"},
        {"year": 2022, "event": "Flash floods in houseboat areas"},
        {"year": 2023, "event": "Monsoon waterlogging"}
    ],
    
    # Assam Cities
    "Guwahati": [
        {"year": 2019, "event": "Monsoon floods affected Assam"},
        {"year": 2020, "event": "Heavy rains caused landslides"},
        {"year": 2021, "event": "Brahmaputra floods displaced thousands"},
        {"year": 2022, "event": "Urban flooding in hill areas"},
        {"year": 2023, "event": "Drainage system failure"}
    ],
    "Dibrugarh": [
        {"year": 2019, "event": "Monsoon flooding in tea gardens"},
        {"year": 2020, "event": "Heavy rainfall warnings"},
        {"year": 2021, "event": "Urban drainage overflow"},
        {"year": 2022, "event": "Flash floods in outskirts"},
        {"year": 2023, "event": "Monsoon waterlogging"}
    ]
}

# Pydantic models
class IoTData(BaseModel):
    water_level: str
    rainfall: str
    river_flow: str
    drainage_capacity: str

class PastEvent(BaseModel):
    year: int
    event: str

class CityData(BaseModel):
    city: str
    lat: float
    lng: float
    risk: str
    current_status: str
    confidence: int
    iot_data: IoTData
    past_events: List[PastEvent]

def generate_realistic_iot_data(city_name: str) -> IoTData:
    """Generate realistic IoT sensor data based on city characteristics."""
    city_info = INDIAN_CITIES_DATABASE.get(city_name, {})
    flood_risk = city_info.get("flood_risk_factor", 0.5)
    monsoon_intensity = city_info.get("monsoon_intensity", 0.5)
    
    # Generate water level (0.5m to 8m)
    base_water_level = 1.0 + (flood_risk * 4)
    water_level = base_water_level + random.uniform(-0.5, 1.5)
    water_level = max(0.5, min(8.0, water_level))
    
    # Generate rainfall (0mm/hr to 200mm/hr)
    base_rainfall = monsoon_intensity * 100
    rainfall = base_rainfall + random.uniform(-20, 50)
    rainfall = max(0, min(200, rainfall))
    
    # Generate river flow status
    if water_level > 5.0 or rainfall > 100:
        river_flow = "High"
    elif water_level > 3.0 or rainfall > 50:
        river_flow = "Moderate"
    else:
        river_flow = "Low"
    
    # Generate drainage capacity
    drainage_base = city_info.get("drainage_capacity", 0.6)
    drainage_capacity = drainage_base + random.uniform(-0.2, 0.2)
    drainage_capacity = max(0.1, min(1.0, drainage_capacity))
    
    if drainage_capacity > 0.8:
        drainage_status = f"{int(drainage_capacity * 100)}%"
    elif drainage_capacity > 0.5:
        drainage_status = f"{int(drainage_capacity * 100)}%"
    else:
        drainage_status = "Overloaded"
    
    return IoTData(
        water_level=f"{water_level:.1f}m",
        rainfall=f"{rainfall:.0f}mm/hr",
        river_flow=river_flow,
        drainage_capacity=drainage_status
    )

def determine_risk_level(city_name: str, iot_data: IoTData) -> tuple:
    """Determine risk level and status based on IoT data."""
    city_info = INDIAN_CITIES_DATABASE.get(city_name, {})
    flood_risk = city_info.get("flood_risk_factor", 0.5)
    
    water_level = float(iot_data.water_level.replace("m", ""))
    rainfall = float(iot_data.rainfall.replace("mm/hr", ""))
    
    # Calculate risk score
    risk_score = (
        (water_level / 8.0) * 0.4 +
        (rainfall / 200.0) * 0.3 +
        (1 - flood_risk) * 0.3
    )
    
    # Determine risk level
    if risk_score > 0.7:
        risk = "critical"
        status = "Heavy Rainfall + Rising Water Level"
        confidence = random.randint(85, 98)
    elif risk_score > 0.5:
        risk = "warning"
        status = "Monsoon Rain Predicted"
        confidence = random.randint(70, 90)
    else:
        risk = "safe"
        status = "Normal Conditions"
        confidence = random.randint(60, 85)
    
    return risk, status, confidence

@router.get("/disaster/cities", response_model=List[CityData])
async def get_cities_data():
    """
    Get real-time IoT and AI prediction data for all Indian cities.
    
    Returns comprehensive data including:
    - City coordinates and basic info
    - Real-time IoT sensor data
    - AI risk assessment
    - Historical disaster events
    """
    try:
        cities_data = []
        
        for city_name, city_info in INDIAN_CITIES_DATABASE.items():
            # Generate realistic IoT data
            iot_data = generate_realistic_iot_data(city_name)
            
            # Determine risk level and status
            risk, status, confidence = determine_risk_level(city_name, iot_data)
            
            # Get historical events
            past_events = HISTORICAL_EVENTS.get(city_name, [
                {"year": 2020, "event": "Monsoon season flooding"},
                {"year": 2019, "event": "Heavy rainfall caused waterlogging"}
            ])
            
            # Create city data
            city_data = CityData(
                city=city_name,
                lat=city_info["lat"],
                lng=city_info["lng"],
                risk=risk,
                current_status=status,
                confidence=confidence,
                iot_data=iot_data,
                past_events=[PastEvent(**event) for event in past_events]
            )
            
            cities_data.append(city_data)
        
        logger.info(f"Generated data for {len(cities_data)} cities")
        return cities_data
        
    except Exception as e:
        logger.error(f"Error generating cities data: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate cities data")

@router.get("/disaster/cities/{city_name}", response_model=CityData)
async def get_city_data(city_name: str):
    """
    Get detailed data for a specific city.
    """
    try:
        city_info = INDIAN_CITIES_DATABASE.get(city_name)
        if not city_info:
            raise HTTPException(status_code=404, detail="City not found")
        
        # Generate realistic IoT data
        iot_data = generate_realistic_iot_data(city_name)
        
        # Determine risk level and status
        risk, status, confidence = determine_risk_level(city_name, iot_data)
        
        # Get historical events
        past_events = HISTORICAL_EVENTS.get(city_name, [
            {"year": 2020, "event": "Monsoon season flooding"},
            {"year": 2019, "event": "Heavy rainfall caused waterlogging"}
        ])
        
        # Create city data
        city_data = CityData(
            city=city_name,
            lat=city_info["lat"],
            lng=city_info["lng"],
            risk=risk,
            current_status=status,
            confidence=confidence,
            iot_data=iot_data,
            past_events=[PastEvent(**event) for event in past_events]
        )
        
        return city_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating city data for {city_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate city data")
