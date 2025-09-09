# 🌊 JalRakshā AI Backend

A Flask-based REST API backend for the JalRakshā AI flood monitoring and emergency response system.

## 🚀 Features

- **Live Sensor Data Simulation**: Real-time IoT sensor data with risk assessment
- **Risk Prediction**: AI-powered flood risk prediction from sensor inputs
- **Safe Route Planning**: Route optimization avoiding flood zones
- **Rescue Team Management**: Automatic team assignment and tracking
- **Citizen Reporting**: Crowdsourced flood issue reporting system
- **Real-time Status Updates**: Live rescue team and report status

## 📋 API Endpoints

### 1. Live Sensor Data
```
GET /get_live_data
```
Returns simulated IoT sensor data with risk assessment.

**Response:**
```json
{
  "water_level": 55,
  "rainfall": 90,
  "river_flow": 220,
  "risk": "Medium",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 2. Risk Prediction
```
POST /predict_risk
```
Predicts flood risk from sensor data.

**Request:**
```json
{
  "water_level": 50,
  "rainfall": 80,
  "river_flow": 200
}
```

**Response:**
```json
{
  "risk": "Low",
  "confidence": 0.85,
  "factors": {
    "water_level_impact": "Low",
    "rainfall_impact": "Medium",
    "river_flow_impact": "Medium"
  }
}
```

### 3. Safe Route Finder
```
GET /get_safe_route?from=Mumbai&to=Pune
```
Finds the safest route between two locations.

**Response:**
```json
{
  "best_route": "Via Highway 101 - Mumbai → Pune",
  "eta": "25 min",
  "safety_score": "Low Risk",
  "distance": "12.5 km",
  "steps": ["Start from Mumbai", "Take Highway 101 North", "Continue to Pune"],
  "warnings": ["⚠️ Mumbai Coastal - High Risk Zone"]
}
```

### 4. Rescue Team Assignment
```
POST /assign_rescue
```
Assigns the nearest available rescue team.

**Request:**
```json
{
  "lat": 23.03,
  "lng": 72.58
}
```

**Response:**
```json
{
  "team": "Team Alpha-1",
  "eta": "12 min",
  "status": "Dispatched",
  "distance": "8.5 km"
}
```

### 5. Report Issue
```
POST /report_issue
```
Submits a citizen report.

**Request:**
```json
{
  "location": "Riverside District",
  "description": "Severe flooding, roads blocked",
  "severity": "critical",
  "contact": "+91-9876543210"
}
```

**Response:**
```json
{
  "message": "Report submitted successfully",
  "report_id": 1,
  "timestamp": "2024-01-15T10:30:00"
}
```

### 6. Get Reports
```
GET /get_reports?limit=5
```
Retrieves latest citizen reports.

**Response:**
```json
[
    {
      "id": 1,
    "location": "Riverside District",
    "description": "Severe flooding, roads blocked",
    "severity": "critical",
    "timestamp": "2024-01-15T10:30:00"
  }
]
```

### 7. Rescue Team Status
```
GET /get_rescue_status
```
Gets current status of all rescue teams.

**Response:**
```json
[
  {
    "team": "Team Alpha-1",
    "lat": 20.5937,
    "lng": 78.9629,
    "status": "dispatched",
    "last_updated": "2024-01-15T10:30:00"
  }
]
```

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.7+
- pip

### Installation

1. **Clone or download the project files**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the Flask server:**
```bash
python app.py
```

4. **Test the API:**
```bash
python test_api.py
```

The server will start on `http://localhost:5000`

## 🗄️ Database Schema

The system uses SQLite with the following tables:

### `reports`
- `id` (INTEGER PRIMARY KEY)
- `location` (TEXT)
- `description` (TEXT)
- `severity` (TEXT)
- `contact` (TEXT)
- `timestamp` (DATETIME)

### `rescue_teams`
- `id` (INTEGER PRIMARY KEY)
- `team_name` (TEXT UNIQUE)
- `lat` (REAL)
- `lng` (REAL)
- `status` (TEXT)
- `last_updated` (DATETIME)

### `flood_zones`
- `id` (INTEGER PRIMARY KEY)
- `zone_name` (TEXT)
- `lat` (REAL)
- `lng` (REAL)
- `radius` (REAL)
- `risk_level` (TEXT)

## 🔧 Configuration

### Risk Assessment Thresholds

The system uses the following thresholds for risk assessment:

**Water Level (cm):**
- Low Risk: < 40cm
- Medium Risk: 40-80cm
- High Risk: > 80cm

**Rainfall (mm):**
- Low Risk: < 40mm
- Medium Risk: 40-100mm
- High Risk: > 100mm

**River Flow (m³/s):**
- Low Risk: < 100m³/s
- Medium Risk: 100-300m³/s
- High Risk: > 300m³/s

## 🧪 Testing

Run the test suite to verify all endpoints:

   ```bash
python test_api.py
```

This will test all API endpoints and show response examples.

## 🌐 Frontend Integration

The backend is designed to work with the JalRakshā AI frontend. Update the frontend API calls to use:

```javascript
const API_BASE = 'http://localhost:5000';

// Example: Get live data
fetch(`${API_BASE}/get_live_data`)
  .then(response => response.json())
  .then(data => console.log(data));
```

## 📱 Telegram Bot Integration

The backend can be integrated with Telegram bots by calling the same endpoints:

```python
import requests

# Get live data for bot alerts
response = requests.get('http://localhost:5000/get_live_data')
data = response.json()

if data['risk'] == 'High':
    # Send alert to Telegram
    send_telegram_alert(data)
```

## 🚨 Error Handling

All endpoints return proper HTTP status codes:

- `200` - Success
- `201` - Created (for POST requests)
- `400` - Bad Request (invalid input)
- `404` - Not Found
- `500` - Internal Server Error

Error responses include descriptive messages:

```json
{
  "error": "Location and description are required"
}
```

## 🔄 Real-time Updates

The system supports real-time updates through:

1. **Live sensor data** - Updates every API call
2. **Rescue team status** - Updates when teams are dispatched
3. **Citizen reports** - Real-time submission and retrieval

## 🛡️ CORS Support

CORS is enabled for frontend integration. The API accepts requests from any origin during development.

## 📊 Sample Data

The system comes pre-loaded with:

- 5 rescue teams across different Indian cities
- 5 flood zones with risk assessments
- Sample reports and team statuses

## 🔧 Development

### Adding New Endpoints

1. Add the route function in `app.py`
2. Update the test suite in `test_api.py`
3. Update this README with endpoint documentation

### Database Modifications

Use the `init_db()` function to modify database schema and add sample data.

## 📞 Support

For issues or questions:
1. Check the test suite output
2. Verify database file `jalraksha_ai.db` is created
3. Ensure Flask server is running on port 5000
4. Check console output for error messages

---

**🌊 JalRakshā AI - Protecting Lives Through Technology**