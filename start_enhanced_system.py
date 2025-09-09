"""
🌊 JalRakshā AI - Enhanced System Startup Script
Orchestrates all enhanced IoT and AI components
"""

import asyncio
import subprocess
import time
import logging
import requests
import json
from datetime import datetime
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedSystemManager:
    """Enhanced System Manager for JalRakshā AI"""
    
    def __init__(self):
        self.services = {
            "fastapi": {
                "command": ["python", "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
                "url": "http://localhost:8000/health",
                "port": 8000,
                "name": "FastAPI Backend"
            },
            "telegram_bot": {
                "command": ["python", "telegram_bot_with_api.py"],
                "url": "http://localhost:5000/health",
                "port": 5000,
                "name": "Telegram Bot API"
            },
            "iot_simulator": {
                "command": ["python", "enhanced_iot_simulator_v2.py"],
                "url": None,
                "port": None,
                "name": "Enhanced IoT Simulator"
            },
            "iot_protocol_handler": {
                "command": ["python", "iot_protocol_handler.py"],
                "url": None,
                "port": None,
                "name": "IoT Protocol Handler"
            },
            "website_server": {
                "command": ["python", "-m", "http.server", "8080"],
                "url": "http://localhost:8080",
                "port": 8080,
                "name": "Website Server"
            }
        }
        
        self.processes = {}
        self.startup_delay = 3  # seconds between service starts
    
    def check_service_health(self, service_name: str) -> bool:
        """Check if a service is healthy"""
        try:
            service = self.services[service_name]
            if service["url"]:
                response = requests.get(service["url"], timeout=5)
                return response.status_code == 200
            else:
                # For services without health endpoints, check if process is running
                return service_name in self.processes and self.processes[service_name].poll() is None
        except:
            return False
    
    def start_service(self, service_name: str) -> bool:
        """Start a single service"""
        try:
            service = self.services[service_name]
            logger.info(f"🚀 Starting {service['name']}...")
            
            # Start process
            process = subprocess.Popen(
                service["command"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes[service_name] = process
            
            # Wait for service to be ready
            if service["url"]:
                max_attempts = 30
                for attempt in range(max_attempts):
                    time.sleep(1)
                    if self.check_service_health(service_name):
                        logger.info(f"✅ {service['name']} started successfully")
                        return True
                    logger.info(f"⏳ Waiting for {service['name']} to be ready... ({attempt + 1}/{max_attempts})")
                
                logger.error(f"❌ {service['name']} failed to start within timeout")
                return False
            else:
                # For services without health endpoints, just wait a bit
                time.sleep(2)
                if process.poll() is None:
                    logger.info(f"✅ {service['name']} started successfully")
                    return True
                else:
                    logger.error(f"❌ {service['name']} failed to start")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Error starting {service_name}: {str(e)}")
            return False
    
    def stop_service(self, service_name: str):
        """Stop a single service"""
        try:
            if service_name in self.processes:
                process = self.processes[service_name]
                if process.poll() is None:  # Process is still running
                    logger.info(f"🛑 Stopping {self.services[service_name]['name']}...")
                    process.terminate()
                    process.wait(timeout=10)
                    logger.info(f"✅ {self.services[service_name]['name']} stopped")
                del self.processes[service_name]
        except Exception as e:
            logger.error(f"❌ Error stopping {service_name}: {str(e)}")
    
    def start_all_services(self) -> bool:
        """Start all services in order"""
        try:
            logger.info("🌊 Starting JalRakshā AI Enhanced System...")
            
            # Start services in dependency order
            startup_order = [
                "fastapi",           # Backend API first
                "telegram_bot",      # Telegram bot
                "iot_protocol_handler",  # IoT protocol handler
                "iot_simulator",     # IoT simulator
                "website_server"     # Website server last
            ]
            
            for service_name in startup_order:
                if not self.start_service(service_name):
                    logger.error(f"❌ Failed to start {service_name}, stopping all services")
                    self.stop_all_services()
                    return False
                
                # Wait between service starts
                time.sleep(self.startup_delay)
            
            logger.info("🎉 All services started successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error starting services: {str(e)}")
            return False
    
    def stop_all_services(self):
        """Stop all running services"""
        logger.info("🛑 Stopping all services...")
        
        # Stop services in reverse order
        for service_name in reversed(list(self.processes.keys())):
            self.stop_service(service_name)
        
        logger.info("✅ All services stopped")
    
    def check_all_services(self) -> Dict[str, bool]:
        """Check health of all services"""
        health_status = {}
        for service_name in self.services:
            health_status[service_name] = self.check_service_health(service_name)
        return health_status
    
    def print_system_status(self):
        """Print current system status"""
        logger.info("📊 JalRakshā AI Enhanced System Status:")
        logger.info("=" * 50)
        
        health_status = self.check_all_services()
        
        for service_name, is_healthy in health_status.items():
            service = self.services[service_name]
            status_icon = "✅" if is_healthy else "❌"
            logger.info(f"{status_icon} {service['name']}: {'Running' if is_healthy else 'Stopped'}")
        
        logger.info("=" * 50)
    
    def register_sample_sensors(self):
        """Register sample IoT sensors with the system"""
        try:
            logger.info("📡 Registering sample IoT sensors...")
            
            sample_sensors = [
                {
                    "node_id": "WL001",
                    "name": "Ganga River Gauge - Patna",
                    "lat": 25.5941,
                    "lng": 85.1376,
                    "sensor_type": "water_level",
                    "protocol": "mqtt"
                },
                {
                    "node_id": "RF001",
                    "name": "Mumbai Rainfall Station",
                    "lat": 19.0760,
                    "lng": 72.8777,
                    "sensor_type": "rainfall",
                    "protocol": "mqtt"
                },
                {
                    "node_id": "WL002",
                    "name": "Yamuna River Gauge - Delhi",
                    "lat": 28.7041,
                    "lng": 77.1025,
                    "sensor_type": "water_level",
                    "protocol": "lorawan"
                },
                {
                    "node_id": "DC001",
                    "name": "Delhi Drainage Monitor",
                    "lat": 28.6139,
                    "lng": 77.2090,
                    "sensor_type": "drainage",
                    "protocol": "mqtt"
                }
            ]
            
            for sensor in sample_sensors:
                try:
                    response = requests.post(
                        "http://localhost:8000/api/v1/iot/register-sensor",
                        params=sensor,
                        timeout=5
                    )
                    if response.status_code == 200:
                        logger.info(f"✅ Registered sensor {sensor['node_id']}")
                    else:
                        logger.warning(f"⚠️ Failed to register sensor {sensor['node_id']}")
                except Exception as e:
                    logger.warning(f"⚠️ Error registering sensor {sensor['node_id']}: {str(e)}")
            
            logger.info("📡 Sample sensor registration completed")
            
        except Exception as e:
            logger.error(f"❌ Error registering sample sensors: {str(e)}")
    
    def generate_sensor_map(self):
        """Generate the sensor map visualization"""
        try:
            logger.info("🗺️ Generating sensor map visualization...")
            
            # Import and run sensor map component
            import sensor_map_component
            asyncio.run(sensor_map_component.main())
            
            logger.info("✅ Sensor map generated successfully")
            
        except Exception as e:
            logger.error(f"❌ Error generating sensor map: {str(e)}")
    
    def run_system_monitor(self):
        """Run continuous system monitoring"""
        try:
            logger.info("🔍 Starting system monitoring...")
            
            while True:
                time.sleep(30)  # Check every 30 seconds
                
                health_status = self.check_all_services()
                unhealthy_services = [name for name, healthy in health_status.items() if not healthy]
                
                if unhealthy_services:
                    logger.warning(f"⚠️ Unhealthy services detected: {unhealthy_services}")
                    # Could implement auto-restart logic here
                
        except KeyboardInterrupt:
            logger.info("🛑 System monitoring stopped")
        except Exception as e:
            logger.error(f"❌ System monitoring error: {str(e)}")

def main():
    """Main execution function"""
    try:
        manager = EnhancedSystemManager()
        
        # Start all services
        if not manager.start_all_services():
            logger.error("❌ Failed to start all services")
            return False
        
        # Wait a bit for services to stabilize
        time.sleep(5)
        
        # Print system status
        manager.print_system_status()
        
        # Register sample sensors
        manager.register_sample_sensors()
        
        # Generate sensor map
        manager.generate_sensor_map()
        
        # Print access information
        logger.info("🌐 System Access Information:")
        logger.info("=" * 50)
        logger.info("🌊 Main Dashboard: http://localhost:8080/index.html")
        logger.info("🗺️ Sensor Map: http://localhost:8080/sensor_map.html")
        logger.info("📡 API Documentation: http://localhost:8000/docs")
        logger.info("🤖 Telegram Bot: @jalraksha_ai_bot")
        logger.info("📊 IoT Sensors API: http://localhost:8000/api/v1/iot/sensors")
        logger.info("🏥 Sensor Health: http://localhost:8000/api/v1/iot/sensor-health")
        logger.info("=" * 50)
        
        # Start system monitoring
        try:
            manager.run_system_monitor()
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down system...")
            manager.stop_all_services()
            logger.info("✅ System shutdown complete")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ System startup error: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

