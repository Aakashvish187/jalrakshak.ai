import React, { useState, useEffect, useCallback, useRef } from 'react';
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

// State boundaries and zoom levels for India
const INDIA_STATES = {
  'Gujarat': { center: [23.5, 72.5], zoom: 7, cities: ['Ahmedabad', 'Baroda', 'Surat', 'Dwarka', 'Somnath', 'Rajkot', 'Bhavnagar'] },
  'Maharashtra': { center: [19.5, 75.5], zoom: 7, cities: ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad', 'Solapur', 'Kolhapur', 'Sangli'] },
  'Delhi': { center: [28.7, 77.1], zoom: 10, cities: ['Delhi'] },
  'Uttar Pradesh': { center: [26.5, 80.5], zoom: 7, cities: ['Lucknow', 'Kanpur', 'Agra', 'Varanasi', 'Allahabad', 'Meerut'] },
  'Bihar': { center: [25.5, 85.5], zoom: 7, cities: ['Patna', 'Gaya', 'Muzaffarpur', 'Bhagalpur', 'Darbhanga'] },
  'West Bengal': { center: [23.5, 87.5], zoom: 7, cities: ['Kolkata', 'Siliguri', 'Howrah', 'Durgapur', 'Asansol', 'Malda'] },
  'Tamil Nadu': { center: [11.5, 78.5], zoom: 7, cities: ['Chennai', 'Madurai', 'Coimbatore', 'Salem', 'Tiruchirappalli', 'Tirunelveli'] },
  'Telangana': { center: [17.5, 79.5], zoom: 7, cities: ['Hyderabad', 'Warangal', 'Nizamabad'] },
  'Karnataka': { center: [15.5, 76.5], zoom: 7, cities: ['Bangalore', 'Mysuru', 'Mangalore', 'Hubli', 'Belgaum', 'Gulbarga'] },
  'Kerala': { center: [10.5, 76.5], zoom: 7, cities: ['Kochi', 'Trivandrum', 'Kollam', 'Thrissur', 'Kottayam', 'Palakkad', 'Malappuram', 'Kozhikode', 'Kannur', 'Kasaragod', 'Alappuzha', 'Pathanamthitta', 'Idukki', 'Wayanad', 'Ernakulam'] },
  'Punjab': { center: [31.5, 75.5], zoom: 7, cities: ['Chandigarh', 'Ludhiana', 'Amritsar', 'Jalandhar'] },
  'Assam': { center: [26.5, 92.5], zoom: 7, cities: ['Guwahati', 'Dibrugarh', 'Silchar', 'Jorhat', 'Tezpur'] },
  'Rajasthan': { center: [26.5, 73.5], zoom: 7, cities: ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Ajmer', 'Bikaner'] },
  'Madhya Pradesh': { center: [23.5, 77.5], zoom: 7, cities: ['Bhopal', 'Indore', 'Gwalior', 'Jabalpur', 'Ujjain', 'Sagar'] },
  'Andhra Pradesh': { center: [15.5, 79.5], zoom: 7, cities: ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Nellore', 'Kurnool', 'Tirupati'] },
  'Odisha': { center: [20.5, 85.5], zoom: 7, cities: ['Bhubaneswar', 'Cuttack', 'Rourkela', 'Berhampur', 'Sambalpur', 'Puri'] },
  'Jharkhand': { center: [23.5, 85.5], zoom: 7, cities: ['Ranchi', 'Jamshedpur', 'Dhanbad', 'Bokaro', 'Deoghar', 'Hazaribagh'] },
  'Chhattisgarh': { center: [21.5, 81.5], zoom: 7, cities: ['Raipur', 'Bhilai', 'Bilaspur', 'Korba', 'Rajnandgaon', 'Durg'] },
  'Haryana': { center: [29.5, 76.5], zoom: 7, cities: ['Chandigarh', 'Gurgaon', 'Faridabad', 'Panipat', 'Ambala', 'Karnal'] },
  'Himachal Pradesh': { center: [31.5, 77.5], zoom: 7, cities: ['Shimla', 'Dharamshala', 'Solan', 'Mandi', 'Palampur', 'Kullu'] },
  'Uttarakhand': { center: [30.5, 78.5], zoom: 7, cities: ['Dehradun', 'Haridwar', 'Rishikesh', 'Nainital', 'Mussoorie', 'Almora'] },
  'Jammu and Kashmir': { center: [34.5, 76.5], zoom: 7, cities: ['Srinagar', 'Jammu', 'Leh', 'Anantnag', 'Baramulla', 'Pulwama'] },
  'Ladakh': { center: [34.5, 77.5], zoom: 7, cities: ['Leh', 'Kargil'] },
  'Goa': { center: [15.5, 74.5], zoom: 8, cities: ['Panaji', 'Margao', 'Vasco da Gama', 'Mapusa', 'Ponda'] },
  'Manipur': { center: [24.5, 93.5], zoom: 8, cities: ['Imphal', 'Thoubal', 'Bishnupur', 'Churachandpur'] },
  'Meghalaya': { center: [25.5, 91.5], zoom: 8, cities: ['Shillong', 'Tura', 'Jowai', 'Nongstoin'] },
  'Mizoram': { center: [23.5, 92.5], zoom: 8, cities: ['Aizawl', 'Lunglei', 'Saiha', 'Champhai'] },
  'Nagaland': { center: [26.5, 94.5], zoom: 8, cities: ['Kohima', 'Dimapur', 'Mokokchung', 'Tuensang'] },
  'Tripura': { center: [23.5, 91.5], zoom: 8, cities: ['Agartala', 'Dharmanagar', 'Udaipur', 'Ambassa'] },
  'Arunachal Pradesh': { center: [28.5, 94.5], zoom: 8, cities: ['Itanagar', 'Naharlagun', 'Pasighat', 'Tezpur'] },
  'Sikkim': { center: [28.5, 88.5], zoom: 8, cities: ['Gangtok', 'Namchi', 'Mangan', 'Rangpo'] }
};

// Custom marker icons with animations
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
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        border: 3px solid white;
        animation: pulse-${riskLevel} 2s infinite;
        cursor: pointer;
        transition: all 0.3s ease;
      ">
        ${icons[riskLevel]}
      </div>
    `,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16]
  });
};

// Map component
const IndiaRiskMap = () => {
  const [citiesData, setCitiesData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCity, setSelectedCity] = useState(null);
  const [currentZoom, setCurrentZoom] = useState(6);
  const [visibleCities, setVisibleCities] = useState([]);
  const mapRef = useRef(null);

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
      
      // Set initial visible cities based on zoom level
      updateVisibleCities(data, currentZoom);
    } catch (err) {
      console.error('Error fetching cities data:', err);
      setError('Failed to load city data. Please check if the backend is running.');
    } finally {
      setLoading(false);
    }
  }, [currentZoom]);

  // Update visible cities based on zoom level
  const updateVisibleCities = (data, zoom) => {
    if (zoom >= 8) {
      // Show all cities when zoomed in
      setVisibleCities(data);
    } else if (zoom >= 7) {
      // Show major cities only
      setVisibleCities(data.filter(city => 
        city.population && parseInt(city.population.replace(/[^\d]/g, '')) >= 1000000
      ));
    } else {
      // Show only major metropolitan cities
      setVisibleCities(data.filter(city => 
        city.population && parseInt(city.population.replace(/[^\d]/g, '')) >= 5000000
      ));
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchCitiesData();
  }, [fetchCitiesData]);

  // Auto-refresh every 60 seconds
  useEffect(() => {
    const interval = setInterval(fetchCitiesData, 60000);
    return () => clearInterval(interval);
  }, [fetchCitiesData]);

  // Handle map zoom changes
  const handleZoomChange = useCallback(() => {
    if (mapRef.current) {
      const zoom = mapRef.current.getZoom();
      setCurrentZoom(zoom);
      updateVisibleCities(citiesData, zoom);
    }
  }, [citiesData]);

  // City popup component
  const CityPopup = ({ city }) => (
    <div className="bg-slate-900 text-white p-4 rounded-lg max-w-sm border border-slate-700">
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
          <strong>State:</strong> {city.state}
        </p>
        <p className="text-sm text-slate-300 mb-1">
          <strong>Status:</strong> {city.current_status}
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
        <h4 className="text-sm font-semibold text-cyan-400 mb-2">Past 5 Years Tragedies:</h4>
        <div className="space-y-1 max-h-32 overflow-y-auto">
          {city.past_events.slice(0, 5).map((event, index) => (
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
      <div className="bg-slate-900 text-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-3xl font-bold text-cyan-400">{city.city}</h2>
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-white text-3xl"
            >
              ×
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h3 className="text-xl font-semibold mb-4 text-cyan-400">Current Status</h3>
              <div className="bg-slate-800 p-4 rounded-lg">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-slate-300">Risk Level:</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    city.risk === 'critical' ? 'bg-red-500 text-white' :
                    city.risk === 'warning' ? 'bg-yellow-500 text-white' :
                    'bg-green-500 text-white'
                  }`}>
                    {city.risk.toUpperCase()}
                  </span>
                </div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-slate-300">State:</span>
                  <span className="text-white">{city.state}</span>
                </div>
                <div className="flex items-center justify-between mb-3">
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
              <h3 className="text-xl font-semibold mb-4 text-cyan-400">IoT Sensor Data</h3>
              <div className="bg-slate-800 p-4 rounded-lg space-y-4">
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
            <h3 className="text-xl font-semibold mb-4 text-cyan-400">Past 5 Years Tragedies</h3>
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

  // State selector component
  const StateSelector = () => (
    <div className="absolute top-4 left-4 bg-slate-900/90 backdrop-blur-sm p-4 rounded-lg border border-slate-700/50 z-[1000]">
      <h4 className="text-sm font-semibold text-cyan-400 mb-2">Jump to State</h4>
      <select 
        onChange={(e) => {
          if (e.target.value && mapRef.current) {
            const state = INDIA_STATES[e.target.value];
            mapRef.current.setView(state.center, state.zoom);
          }
        }}
        className="bg-slate-800 text-white text-xs rounded px-2 py-1 border border-slate-600"
      >
        <option value="">Select State</option>
        {Object.keys(INDIA_STATES).map(state => (
          <option key={state} value={state}>{state}</option>
        ))}
      </select>
    </div>
  );

  if (loading) {
    return (
      <div className="h-96 bg-slate-800 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-cyan-400 mx-auto mb-4"></div>
          <p className="text-slate-300 text-lg">Loading India Risk Map...</p>
          <p className="text-slate-400 text-sm">Fetching data for 100+ cities</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-96 bg-slate-800 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-400 text-6xl mb-4">⚠️</div>
          <p className="text-red-400 mb-2 text-lg">Failed to load map data</p>
          <p className="text-slate-400 text-sm mb-4">{error}</p>
          <button
            onClick={fetchCitiesData}
            className="bg-cyan-500 hover:bg-cyan-600 text-white px-6 py-3 rounded-lg text-sm font-semibold"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="relative h-[600px] bg-slate-800 rounded-lg overflow-hidden border border-slate-700">
        <MapContainer
          center={[20.5937, 78.9629]} // Center of India
          zoom={6}
          className="w-full h-full"
          zoomControl={true}
          ref={mapRef}
          whenReady={() => {
            if (mapRef.current) {
              mapRef.current.on('zoomend', handleZoomChange);
            }
          }}
        >
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            attribution='© JalRakshā AI India Disaster Risk Map'
            subdomains="abcd"
          />
          
          {visibleCities.map((city) => (
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

        {/* State Selector */}
        <StateSelector />

        {/* Legend */}
        <div className="absolute top-4 right-4 bg-slate-900/90 backdrop-blur-sm p-4 rounded-lg border border-slate-700/50 z-[1000]">
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
        <div className="absolute bottom-4 left-4 bg-slate-900/90 backdrop-blur-sm px-3 py-2 rounded-lg border border-slate-700/50 z-[1000]">
          <div className="flex items-center space-x-2 text-xs text-slate-300">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span>Auto-refresh: 60s</span>
          </div>
        </div>

        {/* Zoom level indicator */}
        <div className="absolute bottom-4 right-4 bg-slate-900/90 backdrop-blur-sm px-3 py-2 rounded-lg border border-slate-700/50 z-[1000]">
          <div className="text-xs text-slate-300">
            Zoom: {currentZoom} | Cities: {visibleCities.length}
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
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.8; transform: scale(1.05); }
        }
        @keyframes pulse-warning {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.7; transform: scale(1.1); }
        }
        @keyframes pulse-critical {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.6; transform: scale(1.15); }
        }
        
        .marker-content:hover {
          transform: scale(1.2) !important;
          z-index: 1000;
        }
      `}</style>
    </>
  );
};

export default IndiaRiskMap;
