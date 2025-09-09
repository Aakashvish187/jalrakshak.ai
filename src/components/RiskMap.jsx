import React, { useState, useEffect, useCallback } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// Custom marker icons
const createCustomIcon = (riskLevel) => {
  const colors = {
    safe: '#22c55e',
    warning: '#f59e0b', 
    critical: '#ef4444'
  };
  
  const icons = {
    safe: '🟢',
    warning: '🟠',
    critical: '🔴'
  };
  
  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div class="marker-content ${riskLevel}" style="
        background: ${colors[riskLevel]};
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        border: 2px solid white;
        animation: pulse-${riskLevel} 2s infinite;
      ">
        ${icons[riskLevel]}
      </div>
    `,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
    popupAnchor: [0, -15]
  });
};

// Map component
const RiskMap = () => {
  const [citiesData, setCitiesData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCity, setSelectedCity] = useState(null);

  // Fetch cities data from API
  const fetchCitiesData = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/disaster/cities');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setCitiesData(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching cities data:', err);
      setError('Failed to load city data. Please check if the backend is running.');
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial data fetch
  useEffect(() => {
    fetchCitiesData();
  }, [fetchCitiesData]);

  // Auto-refresh every 60 seconds
  useEffect(() => {
    const interval = setInterval(fetchCitiesData, 60000);
    return () => clearInterval(interval);
  }, [fetchCitiesData]);

  // City popup component
  const CityPopup = ({ city }) => (
    <div className="bg-slate-900 text-white p-4 rounded-lg max-w-sm">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-cyan-400">{city.city}</h3>
        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
          city.risk === 'critical' ? 'bg-red-500 text-white' :
          city.risk === 'warning' ? 'bg-yellow-500 text-white' :
          'bg-green-500 text-white'
        }`}>
          {city.risk.toUpperCase()}
        </span>
      </div>
      
      <div className="mb-3">
        <p className="text-sm text-slate-300 mb-1">
          <strong>Current Status:</strong> {city.current_status}
        </p>
        <p className="text-sm text-slate-300">
          <strong>AI Confidence:</strong> {city.confidence}%
        </p>
      </div>

      <div className="mb-3">
        <h4 className="text-sm font-semibold text-cyan-400 mb-2">IoT Data:</h4>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="bg-slate-800 p-2 rounded">
            <div className="text-slate-400">Water Level</div>
            <div className="text-white font-semibold">{city.iot_data.water_level}</div>
          </div>
          <div className="bg-slate-800 p-2 rounded">
            <div className="text-slate-400">Rainfall</div>
            <div className="text-white font-semibold">{city.iot_data.rainfall}</div>
          </div>
          <div className="bg-slate-800 p-2 rounded">
            <div className="text-slate-400">River Flow</div>
            <div className="text-white font-semibold">{city.iot_data.river_flow}</div>
          </div>
          <div className="bg-slate-800 p-2 rounded">
            <div className="text-slate-400">Drainage</div>
            <div className="text-white font-semibold">{city.iot_data.drainage_capacity}</div>
          </div>
        </div>
      </div>

      <div className="mb-3">
        <h4 className="text-sm font-semibold text-cyan-400 mb-2">Past Tragedies:</h4>
        <div className="space-y-1">
          {city.past_events.slice(0, 3).map((event, index) => (
            <div key={index} className="text-xs text-slate-300 bg-slate-800 p-2 rounded">
              <span className="text-yellow-400">{event.year}:</span> {event.event}
            </div>
          ))}
        </div>
      </div>

      <button
        onClick={() => setSelectedCity(city)}
        className="w-full bg-cyan-500 hover:bg-cyan-600 text-white py-2 px-4 rounded-lg text-sm font-semibold transition-colors"
      >
        View Full Details
      </button>
    </div>
  );

  // City details modal
  const CityDetailsModal = ({ city, onClose }) => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-900 text-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-cyan-400">{city.city}</h2>
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-white text-2xl"
            >
              ×
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold mb-3 text-cyan-400">Current Status</h3>
              <div className="bg-slate-800 p-4 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-300">Risk Level:</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    city.risk === 'critical' ? 'bg-red-500 text-white' :
                    city.risk === 'warning' ? 'bg-yellow-500 text-white' :
                    'bg-green-500 text-white'
                  }`}>
                    {city.risk.toUpperCase()}
                  </span>
                </div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-300">Status:</span>
                  <span className="text-white">{city.current_status}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-300">AI Confidence:</span>
                  <span className="text-white font-semibold">{city.confidence}%</span>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-3 text-cyan-400">IoT Sensor Data</h3>
              <div className="bg-slate-800 p-4 rounded-lg space-y-3">
                <div className="flex justify-between">
                  <span className="text-slate-300">Water Level:</span>
                  <span className="text-white font-semibold">{city.iot_data.water_level}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-300">Rainfall:</span>
                  <span className="text-white font-semibold">{city.iot_data.rainfall}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-300">River Flow:</span>
                  <span className="text-white font-semibold">{city.iot_data.river_flow}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-300">Drainage Capacity:</span>
                  <span className="text-white font-semibold">{city.iot_data.drainage_capacity}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-3 text-cyan-400">Historical Tragedies</h3>
            <div className="bg-slate-800 p-4 rounded-lg space-y-3">
              {city.past_events.map((event, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <span className="text-yellow-400 font-semibold min-w-[50px]">{event.year}</span>
                  <span className="text-slate-300">{event.event}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="h-96 bg-slate-800 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-400 mx-auto mb-4"></div>
          <p className="text-slate-300">Loading AI Risk Map...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-96 bg-slate-800 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-400 text-4xl mb-4">⚠️</div>
          <p className="text-red-400 mb-2">Failed to load map data</p>
          <p className="text-slate-400 text-sm">{error}</p>
          <button
            onClick={fetchCitiesData}
            className="mt-4 bg-cyan-500 hover:bg-cyan-600 text-white px-4 py-2 rounded-lg text-sm"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="relative h-96 bg-slate-800 rounded-lg overflow-hidden">
        <MapContainer
          center={[20.5937, 78.9629]} // Center of India
          zoom={6}
          className="w-full h-full"
          zoomControl={true}
        >
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            attribution='© JalRakshā AI Flood Monitoring System'
            subdomains="abcd"
          />
          
          {citiesData.map((city) => (
            <Marker
              key={city.city}
              position={[city.lat, city.lng]}
              icon={createCustomIcon(city.risk)}
            >
              <Popup>
                <CityPopup city={city} />
              </Popup>
            </Marker>
          ))}
        </MapContainer>

        {/* Legend */}
        <div className="absolute top-4 right-4 bg-slate-900/90 backdrop-blur-sm p-4 rounded-lg border border-slate-700/50">
          <h4 className="text-sm font-semibold text-cyan-400 mb-2">Risk Levels</h4>
          <div className="space-y-2 text-xs">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="text-slate-300">Safe</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <span className="text-slate-300">Warning</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
              <span className="text-slate-300">Critical</span>
            </div>
          </div>
        </div>

        {/* Auto-refresh indicator */}
        <div className="absolute bottom-4 left-4 bg-slate-900/90 backdrop-blur-sm px-3 py-2 rounded-lg border border-slate-700/50">
          <div className="flex items-center space-x-2 text-xs text-slate-300">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span>Auto-refresh: 60s</span>
          </div>
        </div>
      </div>

      {/* City Details Modal */}
      {selectedCity && (
        <CityDetailsModal
          city={selectedCity}
          onClose={() => setSelectedCity(null)}
        />
      )}

      {/* Custom CSS for animations */}
      <style jsx>{`
        @keyframes pulse-safe {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }
        @keyframes pulse-warning {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }
        @keyframes pulse-critical {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </>
  );
};

export default RiskMap;
