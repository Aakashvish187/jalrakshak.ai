"""
🌊 JalRakshā AI - Live Sensor Map Component
Real-time visualization of IoT sensor network across India
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
import requests
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SensorNodeData:
    """Sensor node data structure"""
    node_id: str
    name: str
    lat: float
    lng: float
    sensor_type: str
    protocol: str
    status: str
    health_score: int
    last_seen: str
    data: Dict[str, Any]

class SensorMapAPI:
    """API for sensor map data"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.sensor_endpoint = f"{base_url}/iot/sensors"
        self.health_endpoint = f"{base_url}/iot/sensor-health"
    
    async def get_all_sensors(self) -> List[SensorNodeData]:
        """Get all sensor nodes data"""
        try:
            response = requests.get(self.sensor_endpoint, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                sensors = []
                
                for sensor_data in data.get("sensors", []):
                    sensor = SensorNodeData(
                        node_id=sensor_data["node_id"],
                        name=sensor_data["name"],
                        lat=sensor_data["lat"],
                        lng=sensor_data["lng"],
                        sensor_type=sensor_data["sensor_type"],
                        protocol=sensor_data["protocol"],
                        status=sensor_data["status"],
                        health_score=sensor_data["health_score"],
                        last_seen=sensor_data["last_seen"],
                        data=sensor_data.get("data", {})
                    )
                    sensors.append(sensor)
                
                logger.info(f"✅ Retrieved {len(sensors)} sensor nodes")
                return sensors
                
            else:
                logger.error(f"❌ Failed to get sensors: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Get sensors error: {str(e)}")
            return []
    
    async def get_sensor_health(self) -> Dict[str, Any]:
        """Get overall sensor network health"""
        try:
            response = requests.get(self.health_endpoint, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"❌ Failed to get sensor health: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Get sensor health error: {str(e)}")
            return {}

class SensorMapVisualizer:
    """Sensor map visualization generator"""
    
    def __init__(self):
        self.api = SensorMapAPI()
        self.sensor_icons = {
            "water_level": "💧",
            "rainfall": "🌧️",
            "river_flow": "🌊",
            "drainage": "🏗️"
        }
        self.status_colors = {
            "online": "#10B981",  # Green
            "offline": "#EF4444",  # Red
            "error": "#F59E0B",   # Yellow
            "warning": "#F97316"  # Orange
        }
    
    def generate_map_html(self, sensors: List[SensorNodeData], health_data: Dict[str, Any]) -> str:
        """Generate HTML for sensor map visualization"""
        try:
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌊 JalRakshā AI - Live Sensor Network Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .sensor-marker {{
            background: white;
            border-radius: 50%;
            border: 3px solid;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
        .sensor-popup {{
            background: #1f2937;
            color: white;
            border-radius: 8px;
            padding: 12px;
            min-width: 250px;
        }}
        .health-indicator {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }}
        .online {{ background: #10B981; }}
        .offline {{ background: #EF4444; }}
        .error {{ background: #F59E0B; }}
        .warning {{ background: #F97316; }}
    </style>
</head>
<body class="bg-gray-900 text-white">
    <div class="container mx-auto p-4">
        <header class="mb-6">
            <h1 class="text-3xl font-bold text-cyan-400 mb-2">
                🌊 JalRakshā AI - Live Sensor Network Map
            </h1>
            <p class="text-gray-300">
                Real-time IoT sensor monitoring across India • Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </p>
        </header>
        
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
            <!-- Network Health Stats -->
            <div class="bg-gray-800 rounded-lg p-4">
                <h3 class="text-lg font-semibold text-cyan-400 mb-3">Network Health</h3>
                <div class="space-y-2">
                    <div class="flex justify-between">
                        <span>Online Sensors:</span>
                        <span class="text-green-400 font-bold">{health_data.get('online_count', 0)}</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Offline Sensors:</span>
                        <span class="text-red-400 font-bold">{health_data.get('offline_count', 0)}</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Error Sensors:</span>
                        <span class="text-yellow-400 font-bold">{health_data.get('error_count', 0)}</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Avg Health Score:</span>
                        <span class="text-blue-400 font-bold">{health_data.get('avg_health_score', 0)}%</span>
                    </div>
                </div>
            </div>
            
            <!-- Sensor Types -->
            <div class="bg-gray-800 rounded-lg p-4">
                <h3 class="text-lg font-semibold text-cyan-400 mb-3">Sensor Types</h3>
                <div class="space-y-2">
                    <div class="flex items-center">
                        <span class="text-2xl mr-2">💧</span>
                        <span>Water Level: {len([s for s in sensors if s.sensor_type == 'water_level'])}</span>
                    </div>
                    <div class="flex items-center">
                        <span class="text-2xl mr-2">🌧️</span>
                        <span>Rainfall: {len([s for s in sensors if s.sensor_type == 'rainfall'])}</span>
                    </div>
                    <div class="flex items-center">
                        <span class="text-2xl mr-2">🌊</span>
                        <span>River Flow: {len([s for s in sensors if s.sensor_type == 'river_flow'])}</span>
                    </div>
                    <div class="flex items-center">
                        <span class="text-2xl mr-2">🏗️</span>
                        <span>Drainage: {len([s for s in sensors if s.sensor_type == 'drainage'])}</span>
                    </div>
                </div>
            </div>
            
            <!-- Protocols -->
            <div class="bg-gray-800 rounded-lg p-4">
                <h3 class="text-lg font-semibold text-cyan-400 mb-3">Protocols</h3>
                <div class="space-y-2">
                    <div class="flex justify-between">
                        <span>MQTT:</span>
                        <span class="text-blue-400 font-bold">{len([s for s in sensors if s.protocol == 'mqtt'])}</span>
                    </div>
                    <div class="flex justify-between">
                        <span>LoRaWAN:</span>
                        <span class="text-purple-400 font-bold">{len([s for s in sensors if s.protocol == 'lorawan'])}</span>
                    </div>
                    <div class="flex justify-between">
                        <span>HTTP:</span>
                        <span class="text-green-400 font-bold">{len([s for s in sensors if s.protocol == 'http'])}</span>
                    </div>
                </div>
            </div>
            
            <!-- Quick Actions -->
            <div class="bg-gray-800 rounded-lg p-4">
                <h3 class="text-lg font-semibold text-cyan-400 mb-3">Quick Actions</h3>
                <div class="space-y-2">
                    <button onclick="refreshMap()" class="w-full bg-cyan-600 hover:bg-cyan-700 text-white px-4 py-2 rounded transition">
                        🔄 Refresh Map
                    </button>
                    <button onclick="exportData()" class="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded transition">
                        📊 Export Data
                    </button>
                    <button onclick="showHealthReport()" class="w-full bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded transition">
                        📋 Health Report
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Map Container -->
        <div class="bg-gray-800 rounded-lg overflow-hidden">
            <div id="sensorMap" style="height: 600px; width: 100%;"></div>
        </div>
        
        <!-- Legend -->
        <div class="mt-6 bg-gray-800 rounded-lg p-4">
            <h3 class="text-lg font-semibold text-cyan-400 mb-3">Map Legend</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="flex items-center">
                    <div class="health-indicator online"></div>
                    <span>Online Sensor</span>
                </div>
                <div class="flex items-center">
                    <div class="health-indicator offline"></div>
                    <span>Offline Sensor</span>
                </div>
                <div class="flex items-center">
                    <div class="health-indicator error"></div>
                    <span>Error Sensor</span>
                </div>
                <div class="flex items-center">
                    <div class="health-indicator warning"></div>
                    <span>Warning Sensor</span>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Initialize map
        const map = L.map('sensorMap').setView([20.5937, 78.9629], 6);
        
        // Add dark tile layer
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            attribution: '© JalRakshā AI Sensor Network',
            subdomains: 'abcd',
            maxZoom: 18
        }}).addTo(map);
        
        // Sensor data
        const sensors = {json.dumps([{
            'node_id': s.node_id,
            'name': s.name,
            'lat': s.lat,
            'lng': s.lng,
            'sensor_type': s.sensor_type,
            'protocol': s.protocol,
            'status': s.status,
            'health_score': s.health_score,
            'last_seen': s.last_seen,
            'data': s.data
        } for s in sensors])};
        
        // Add sensor markers
        sensors.forEach(sensor => {{
            const icon = getSensorIcon(sensor.sensor_type, sensor.status);
            const marker = L.marker([sensor.lat, sensor.lng], {{ icon: icon }}).addTo(map);
            
            const popupContent = `
                <div class="sensor-popup">
                    <h3 class="text-lg font-semibold text-cyan-400 mb-2">${{sensor.name}}</h3>
                    <div class="space-y-1 text-sm">
                        <div class="flex justify-between">
                            <span>Status:</span>
                            <span class="font-bold ${{getStatusColor(sensor.status)}}">${{sensor.status.toUpperCase()}}</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Type:</span>
                            <span>${{sensor.sensor_type.replace('_', ' ').toUpperCase()}}</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Protocol:</span>
                            <span>${{sensor.protocol.toUpperCase()}}</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Health Score:</span>
                            <span class="font-bold">${{sensor.health_score}}%</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Last Seen:</span>
                            <span>${{new Date(sensor.last_seen).toLocaleString()}}</span>
                        </div>
                        ${{sensor.data ? `
                        <div class="mt-2 pt-2 border-t border-gray-600">
                            <h4 class="text-cyan-400 font-semibold mb-1">Live Data:</h4>
                            ${{Object.entries(sensor.data).map(([key, value]) => `
                                <div class="flex justify-between text-xs">
                                    <span>${{key.replace('_', ' ').toUpperCase()}}:</span>
                                    <span>${{value}}</span>
                                </div>
                            `).join('')}}
                        </div>
                        ` : ''}}
                    </div>
                </div>
            `;
            
            marker.bindPopup(popupContent);
        }});
        
        function getSensorIcon(sensorType, status) {{
            const icons = {{
                'water_level': '💧',
                'rainfall': '🌧️',
                'river_flow': '🌊',
                'drainage': '🏗️'
            }};
            
            const colors = {{
                'online': '#10B981',
                'offline': '#EF4444',
                'error': '#F59E0B',
                'warning': '#F97316'
            }};
            
            return L.divIcon({{
                className: 'sensor-marker',
                html: `<div style="border-color: ${{colors[status]}}; color: ${{colors[status]}}">${{icons[sensorType]}}</div>`,
                iconSize: [40, 40],
                iconAnchor: [20, 20],
                popupAnchor: [0, -20]
            }});
        }}
        
        function getStatusColor(status) {{
            const colors = {{
                'online': 'text-green-400',
                'offline': 'text-red-400',
                'error': 'text-yellow-400',
                'warning': 'text-orange-400'
            }};
            return colors[status] || 'text-gray-400';
        }}
        
        function refreshMap() {{
            location.reload();
        }}
        
        function exportData() {{
            const dataStr = JSON.stringify(sensors, null, 2);
            const dataBlob = new Blob([dataStr], {{type: 'application/json'}});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'sensor_network_data.json';
            link.click();
        }}
        
        function showHealthReport() {{
            const report = {{
                total_sensors: sensors.length,
                online_sensors: sensors.filter(s => s.status === 'online').length,
                offline_sensors: sensors.filter(s => s.status === 'offline').length,
                error_sensors: sensors.filter(s => s.status === 'error').length,
                avg_health_score: Math.round(sensors.reduce((sum, s) => sum + s.health_score, 0) / sensors.length),
                sensor_types: {{
                    water_level: sensors.filter(s => s.sensor_type === 'water_level').length,
                    rainfall: sensors.filter(s => s.sensor_type === 'rainfall').length,
                    river_flow: sensors.filter(s => s.sensor_type === 'river_flow').length,
                    drainage: sensors.filter(s => s.sensor_type === 'drainage').length
                }},
                protocols: {{
                    mqtt: sensors.filter(s => s.protocol === 'mqtt').length,
                    lorawan: sensors.filter(s => s.protocol === 'lorawan').length,
                    http: sensors.filter(s => s.protocol === 'http').length
                }}
            }};
            
            alert('Sensor Network Health Report:\\n\\n' + JSON.stringify(report, null, 2));
        }}
        
        // Auto-refresh every 30 seconds
        setInterval(() => {{
            console.log('🔄 Auto-refreshing sensor map...');
            refreshMap();
        }}, 30000);
    </script>
</body>
</html>
            """
            
            return html_content
            
        except Exception as e:
            logger.error(f"❌ Generate map HTML error: {str(e)}")
            return f"<html><body><h1>Error generating sensor map: {str(e)}</h1></body></html>"
    
    async def generate_and_save_map(self, output_file: str = "sensor_map.html"):
        """Generate and save sensor map HTML"""
        try:
            # Get sensor data
            sensors = await self.api.get_all_sensors()
            health_data = await self.api.get_sensor_health()
            
            # Generate HTML
            html_content = self.generate_map_html(sensors, health_data)
            
            # Save to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ Sensor map saved to {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"❌ Generate and save map error: {str(e)}")
            return None

# Main execution
async def main():
    """Main sensor map component execution"""
    logger.info("🌊 Starting JalRakshā AI Sensor Map Component...")
    
    visualizer = SensorMapVisualizer()
    output_file = await visualizer.generate_and_save_map()
    
    if output_file:
        print(f"✅ Sensor map generated successfully: {output_file}")
        print(f"🌐 Open in browser: http://localhost:8080/{output_file}")
    else:
        print("❌ Failed to generate sensor map")

if __name__ == "__main__":
    asyncio.run(main())

