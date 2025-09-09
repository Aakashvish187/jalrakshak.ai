# 🌊 JalRakshā AI - Enhanced System Guide

## 🚀 Advanced IoT + AI Features

### ✅ **Completed Enhancements**

#### 1. **IoT Sensor Network (Simulation + Real Devices)**
- ✅ **LoRaWAN/MQTT Protocol Support**: Real IoT sensor integration
- ✅ **Live Sensor Map**: Interactive map showing all IoT nodes
- ✅ **Sensor Health Monitoring**: Online/offline status tracking
- ✅ **Multi-Protocol Support**: MQTT, LoRaWAN, HTTP protocols

#### 2. **AI-Powered Prediction Engine**
- ✅ **Multi-Class Outputs**: Safe/Moderate/Critical risk levels
- ✅ **Explainable AI**: Shows why risk is high (e.g., rainfall > 100mm)
- ✅ **OpenWeather Integration**: 5-day rainfall forecast
- ✅ **Historical Learning**: Updates model with real-time data

---

## 🛠️ **System Architecture**

### **Enhanced Components**

1. **IoT Protocol Handler** (`iot_protocol_handler.py`)
   - LoRaWAN gateway integration
   - MQTT broker communication
   - HTTP sensor data collection
   - Real-time sensor health monitoring

2. **Enhanced AI Engine** (`enhanced_ai_engine.py`)
   - Multi-class risk prediction (Safe/Moderate/Critical)
   - Explainable AI with reasoning
   - OpenWeather API integration
   - Historical learning system

3. **Sensor Map Component** (`sensor_map_component.py`)
   - Live IoT sensor visualization
   - Real-time health status display
   - Interactive sensor details
   - Network statistics dashboard

4. **Enhanced IoT Simulator V2** (`enhanced_iot_simulator_v2.py`)
   - Multi-protocol simulation (MQTT, LoRaWAN, HTTP)
   - Realistic sensor data generation
   - Health status simulation
   - Comprehensive sensor network

5. **Enhanced FastAPI Backend** (`app/routers/iot_enhanced.py`)
   - IoT sensor management API
   - Real-time data collection
   - Health monitoring endpoints
   - Protocol support information

---

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
pip install -r enhanced_requirements.txt
```

### **2. Start Enhanced System**
```bash
python start_enhanced_system.py
```

### **3. Access Services**
- **Main Dashboard**: http://localhost:8080/index.html
- **Sensor Map**: http://localhost:8080/sensor_map.html
- **API Docs**: http://localhost:8000/docs
- **IoT Sensors**: http://localhost:8000/api/v1/iot/sensors
- **Sensor Health**: http://localhost:8000/api/v1/iot/sensor-health

---

## 📡 **IoT Protocol Support**

### **MQTT Protocol**
- **Port**: 1883 (standard), 8883 (secure)
- **Features**: Lightweight, Publish/Subscribe, QoS Support
- **Use Case**: Real-time sensor data transmission

### **LoRaWAN Protocol**
- **Frequency**: 868 MHz (India)
- **Features**: Low Power, Long Range, Secure
- **Spreading Factors**: 7, 8, 9, 10, 11, 12
- **Use Case**: Remote sensor monitoring

### **HTTP Protocol**
- **Port**: 80 (standard), 443 (secure)
- **Features**: RESTful, Simple, Widely Supported
- **Use Case**: Direct sensor data collection

---

## 🤖 **AI Features**

### **Multi-Class Risk Prediction**
- **Safe**: Low risk, normal monitoring
- **Moderate**: Elevated risk, increased monitoring
- **Critical**: High risk, immediate action required

### **Explainable AI**
- **Risk Reasoning**: Shows why risk is high
- **Factor Analysis**: Identifies contributing factors
- **Recommendations**: Provides actionable insights

### **Weather Integration**
- **5-Day Forecast**: Rainfall predictions
- **Real-time Data**: Current weather conditions
- **Risk Assessment**: Weather-based risk evaluation

---

## 🗺️ **Sensor Map Features**

### **Live Visualization**
- **Real-time Updates**: Auto-refresh every 30 seconds
- **Health Status**: Color-coded sensor status
- **Interactive Popups**: Detailed sensor information
- **Network Statistics**: Overall health metrics

### **Sensor Types**
- **💧 Water Level**: River gauges and reservoirs
- **🌧️ Rainfall**: Weather stations
- **🌊 River Flow**: Flow rate monitors
- **🏗️ Drainage**: Capacity sensors

---

## 📊 **API Endpoints**

### **IoT Sensor Management**
- `GET /api/v1/iot/sensors` - Get all sensors
- `GET /api/v1/iot/sensor-health` - Network health summary
- `GET /api/v1/iot/sensors/{node_id}` - Sensor details
- `POST /api/v1/iot/register-sensor` - Register new sensor
- `POST /api/v1/iot/sensor-data` - Receive sensor data
- `POST /api/v1/iot/sensor-health` - Update health status

### **Protocol Information**
- `GET /api/v1/iot/protocols` - Supported protocols
- `GET /api/v1/iot/sensor-types` - Sensor types

---

## 🔧 **Configuration**

### **OpenWeather API**
```python
# Set your API key in enhanced_ai_engine.py
api_key = "your_openweather_api_key"
```

### **MQTT Broker**
```python
# Configure in iot_protocol_handler.py
broker_host = "localhost"
broker_port = 1883
```

### **LoRaWAN Gateway**
```python
# Configure gateway URL
gateway_url = "http://localhost:8080/api/lorawan"
```

---

## 📈 **Monitoring & Health**

### **Sensor Health Metrics**
- **Health Score**: 0-100% sensor reliability
- **Battery Level**: Power status
- **Signal Strength**: Communication quality
- **Error Count**: Failure tracking
- **Uptime**: Operational duration

### **Network Statistics**
- **Online Sensors**: Active sensors count
- **Offline Sensors**: Inactive sensors count
- **Error Sensors**: Failed sensors count
- **Average Health**: Overall network health

---

## 🎯 **Hackathon Advantages**

### **Technical Excellence**
- **Multi-Protocol IoT**: Industry-standard protocols
- **Explainable AI**: Transparent decision-making
- **Real-time Monitoring**: Live data visualization
- **Scalable Architecture**: Handles 100+ sensors

### **Innovation Features**
- **Historical Learning**: Self-improving AI
- **Weather Integration**: External data sources
- **Health Monitoring**: Predictive maintenance
- **Interactive Maps**: User-friendly interface

### **Production Ready**
- **Error Handling**: Robust error management
- **Logging**: Comprehensive logging system
- **Documentation**: Complete API documentation
- **Testing**: Automated health checks

---

## 🚨 **Emergency Features**

### **Real-time Alerts**
- **Critical Risk**: Immediate notifications
- **Sensor Failures**: Equipment monitoring
- **Network Issues**: Connectivity problems
- **Weather Warnings**: External threats

### **Response Actions**
- **Evacuation Orders**: Automated alerts
- **Resource Deployment**: Emergency teams
- **Communication**: Multi-channel alerts
- **Documentation**: Incident tracking

---

## 🔮 **Future Enhancements**

### **Planned Features**
- **Machine Learning**: Advanced prediction models
- **Edge Computing**: Local data processing
- **Blockchain**: Secure data integrity
- **Mobile App**: Native mobile application

### **Integration Opportunities**
- **Government APIs**: Official data sources
- **Satellite Data**: Remote sensing
- **Social Media**: Crowdsourced information
- **IoT Platforms**: Cloud integration

---

## 📞 **Support & Documentation**

### **Resources**
- **API Documentation**: http://localhost:8000/docs
- **System Logs**: Check console output
- **Health Checks**: Monitor service status
- **Error Reports**: Review log files

### **Troubleshooting**
- **Service Issues**: Check process status
- **API Errors**: Review endpoint responses
- **Sensor Problems**: Check health status
- **Performance**: Monitor resource usage

---

## 🏆 **Hackathon Success Factors**

### **Technical Innovation**
- ✅ Multi-protocol IoT integration
- ✅ Explainable AI with reasoning
- ✅ Real-time sensor monitoring
- ✅ Historical learning system

### **User Experience**
- ✅ Interactive sensor map
- ✅ Real-time data visualization
- ✅ Comprehensive health monitoring
- ✅ Intuitive dashboard interface

### **Scalability**
- ✅ 100+ sensor support
- ✅ Multi-city coverage
- ✅ Protocol flexibility
- ✅ Cloud-ready architecture

### **Production Readiness**
- ✅ Error handling
- ✅ Logging system
- ✅ Health monitoring
- ✅ Documentation

---

**🌊 JalRakshā AI - Protecting India with Advanced IoT + AI Technology! 🚀**

