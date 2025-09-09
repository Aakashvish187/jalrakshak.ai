"""
🌊 JalRakshā AI - Enhanced AI Prediction Engine
Multi-class risk prediction with explainable AI and historical learning
"""

import numpy as np
import pandas as pd
import joblib
import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import sqlite3
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenWeatherIntegration:
    """OpenWeather API integration for rainfall forecasting"""
    
    def __init__(self, api_key: str = "your_openweather_api_key"):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.cache_duration = 3600  # 1 hour cache
    
    async def get_rainfall_forecast(self, lat: float, lng: float, days: int = 5) -> List[Dict[str, Any]]:
        """Get 5-day rainfall forecast for a location"""
        try:
            # Use One Call API for detailed forecast
            url = f"{self.base_url}/onecall"
            params = {
                "lat": lat,
                "lon": lng,
                "exclude": "minutely,alerts",
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                forecasts = []
                
                # Current weather
                current = data.get("current", {})
                forecasts.append({
                    "date": datetime.fromtimestamp(current.get("dt", 0)).strftime("%Y-%m-%d"),
                    "rainfall_mm": current.get("rain", {}).get("1h", 0) * 24,  # Convert to daily
                    "humidity": current.get("humidity", 0),
                    "pressure": current.get("pressure", 0),
                    "wind_speed": current.get("wind_speed", 0),
                    "description": current.get("weather", [{}])[0].get("description", "")
                })
                
                # Daily forecasts
                daily_forecasts = data.get("daily", [])[:days-1]
                for day in daily_forecasts:
                    forecasts.append({
                        "date": datetime.fromtimestamp(day.get("dt", 0)).strftime("%Y-%m-%d"),
                        "rainfall_mm": day.get("rain", {}).get("1h", 0) * 24,
                        "humidity": day.get("humidity", 0),
                        "pressure": day.get("pressure", 0),
                        "wind_speed": day.get("wind_speed", 0),
                        "description": day.get("weather", [{}])[0].get("description", "")
                    })
                
                logger.info(f"✅ Rainfall forecast retrieved for {lat}, {lng}")
                return forecasts
                
            else:
                logger.error(f"❌ OpenWeather API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Rainfall forecast error: {str(e)}")
            return []
    
    async def get_current_weather(self, lat: float, lng: float) -> Dict[str, Any]:
        """Get current weather conditions"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": lat,
                "lon": lng,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "temperature": data.get("main", {}).get("temp", 0),
                    "humidity": data.get("main", {}).get("humidity", 0),
                    "pressure": data.get("main", {}).get("pressure", 0),
                    "wind_speed": data.get("wind", {}).get("speed", 0),
                    "rainfall": data.get("rain", {}).get("1h", 0),
                    "description": data.get("weather", [{}])[0].get("description", "")
                }
            else:
                logger.error(f"❌ Current weather API error: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Current weather error: {str(e)}")
            return {}

class ExplainableAI:
    """Explainable AI for risk prediction reasoning"""
    
    def __init__(self):
        self.feature_importance_threshold = 0.1
        self.risk_thresholds = {
            "water_level": {"safe": 2.0, "moderate": 5.0, "critical": 8.0},
            "rainfall": {"safe": 20.0, "moderate": 50.0, "critical": 100.0},
            "river_flow": {"safe": 0.3, "moderate": 0.7, "critical": 1.0},
            "drainage_capacity": {"safe": 0.8, "moderate": 0.5, "critical": 0.2}
        }
    
    def explain_prediction(self, features: Dict[str, float], prediction: str, 
                          confidence: float, feature_importance: Dict[str, float]) -> Dict[str, Any]:
        """Generate explanation for AI prediction"""
        try:
            explanation = {
                "prediction": prediction,
                "confidence": confidence,
                "reasoning": [],
                "risk_factors": [],
                "recommendations": []
            }
            
            # Analyze each feature
            for feature, value in features.items():
                if feature in self.risk_thresholds:
                    thresholds = self.risk_thresholds[feature]
                    importance = feature_importance.get(feature, 0)
                    
                    if importance > self.feature_importance_threshold:
                        risk_level = self._get_risk_level(value, thresholds)
                        
                        explanation["reasoning"].append({
                            "factor": feature.replace("_", " ").title(),
                            "value": value,
                            "risk_level": risk_level,
                            "importance": importance,
                            "threshold": thresholds
                        })
                        
                        if risk_level == "critical":
                            explanation["risk_factors"].append(f"{feature.replace('_', ' ').title()} is critically high ({value})")
                        elif risk_level == "moderate":
                            explanation["risk_factors"].append(f"{feature.replace('_', ' ').title()} is moderately high ({value})")
            
            # Generate recommendations
            explanation["recommendations"] = self._generate_recommendations(prediction, explanation["risk_factors"])
            
            return explanation
            
        except Exception as e:
            logger.error(f"❌ Explanation generation error: {str(e)}")
            return {"prediction": prediction, "confidence": confidence, "reasoning": [], "error": str(e)}
    
    def _get_risk_level(self, value: float, thresholds: Dict[str, float]) -> str:
        """Determine risk level based on thresholds"""
        if value >= thresholds["critical"]:
            return "critical"
        elif value >= thresholds["moderate"]:
            return "moderate"
        else:
            return "safe"
    
    def _generate_recommendations(self, prediction: str, risk_factors: List[str]) -> List[str]:
        """Generate recommendations based on prediction and risk factors"""
        recommendations = []
        
        if prediction == "critical":
            recommendations.extend([
                "🚨 IMMEDIATE EVACUATION REQUIRED",
                "📢 Issue emergency alerts to all residents",
                "🚁 Deploy rescue teams and helicopters",
                "🏥 Prepare emergency medical facilities",
                "📡 Activate emergency communication systems"
            ])
        elif prediction == "moderate":
            recommendations.extend([
                "⚠️ Monitor situation closely",
                "📢 Issue flood watch warnings",
                "🚧 Prepare evacuation routes",
                "📦 Stock emergency supplies",
                "📱 Keep communication channels open"
            ])
        else:
            recommendations.extend([
                "✅ Continue normal monitoring",
                "📊 Regular data collection",
                "🔍 Watch for weather changes",
                "📋 Maintain preparedness protocols"
            ])
        
        return recommendations

class HistoricalLearning:
    """Historical learning system for model improvement"""
    
    def __init__(self, database_path: str = "flood_monitoring.db"):
        self.database_path = database_path
        self.init_database()
    
    def init_database(self):
        """Initialize historical learning database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Historical data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historical_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT,
                    lat REAL,
                    lng REAL,
                    water_level REAL,
                    rainfall REAL,
                    river_flow REAL,
                    drainage_capacity REAL,
                    actual_flood_occurred INTEGER,
                    prediction_accuracy REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Model performance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS model_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_version TEXT,
                    accuracy REAL,
                    precision REAL,
                    recall REAL,
                    f1_score REAL,
                    training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ Historical learning database initialized")
            
        except Exception as e:
            logger.error(f"❌ Database initialization error: {str(e)}")
    
    def store_prediction_data(self, city: str, lat: float, lng: float, 
                            features: Dict[str, float], prediction: str, confidence: float):
        """Store prediction data for future learning"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO historical_data 
                (city, lat, lng, water_level, rainfall, river_flow, drainage_capacity, prediction_accuracy)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                city, lat, lng,
                features.get("water_level", 0),
                features.get("rainfall", 0),
                features.get("river_flow", 0),
                features.get("drainage_capacity", 0),
                confidence
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Store prediction data error: {str(e)}")
    
    def update_with_actual_outcome(self, city: str, timestamp: str, actual_flood_occurred: bool):
        """Update historical data with actual flood outcome"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE historical_data 
                SET actual_flood_occurred = ?
                WHERE city = ? AND timestamp = ?
            ''', (1 if actual_flood_occurred else 0, city, timestamp))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Update actual outcome error: {str(e)}")
    
    def get_training_data(self, limit: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Get historical data for model retraining"""
        try:
            conn = sqlite3.connect(self.database_path)
            
            query = '''
                SELECT water_level, rainfall, river_flow, drainage_capacity, actual_flood_occurred
                FROM historical_data 
                WHERE actual_flood_occurred IS NOT NULL
                ORDER BY timestamp DESC
                LIMIT ?
            '''
            
            df = pd.read_sql_query(query, conn, params=(limit,))
            conn.close()
            
            if len(df) > 0:
                X = df[['water_level', 'rainfall', 'river_flow', 'drainage_capacity']].values
                y = df['actual_flood_occurred'].values
                return X, y
            else:
                return np.array([]), np.array([])
                
        except Exception as e:
            logger.error(f"❌ Get training data error: {str(e)}")
            return np.array([]), np.array([])

class EnhancedAIPredictor:
    """Enhanced AI Predictor with multi-class outputs and explainable AI"""
    
    def __init__(self):
        self.model_path = "enhanced_model.pkl"
        self.scaler_path = "enhanced_scaler.pkl"
        self.model = None
        self.scaler = None
        self.explainable_ai = ExplainableAI()
        self.historical_learning = HistoricalLearning()
        self.openweather = OpenWeatherIntegration()
        self.class_names = ["safe", "moderate", "critical"]
        
    def load_model(self):
        """Load or create enhanced AI model"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                logger.info("✅ Enhanced AI model loaded successfully")
            else:
                logger.info("🔄 Creating new enhanced AI model...")
                self._create_new_model()
                
        except Exception as e:
            logger.error(f"❌ Model loading error: {str(e)}")
            self._create_new_model()
    
    def _create_new_model(self):
        """Create new enhanced AI model with multi-class outputs"""
        try:
            # Generate synthetic training data for demonstration
            np.random.seed(42)
            n_samples = 1000
            
            # Generate features
            water_level = np.random.uniform(0, 10, n_samples)
            rainfall = np.random.uniform(0, 200, n_samples)
            river_flow = np.random.uniform(0, 1, n_samples)
            drainage_capacity = np.random.uniform(0, 1, n_samples)
            
            # Generate multi-class labels based on combinations
            labels = []
            for i in range(n_samples):
                risk_score = 0
                
                # Water level risk
                if water_level[i] > 8:
                    risk_score += 3
                elif water_level[i] > 5:
                    risk_score += 2
                elif water_level[i] > 2:
                    risk_score += 1
                
                # Rainfall risk
                if rainfall[i] > 100:
                    risk_score += 3
                elif rainfall[i] > 50:
                    risk_score += 2
                elif rainfall[i] > 20:
                    risk_score += 1
                
                # River flow risk
                if river_flow[i] > 0.8:
                    risk_score += 2
                elif river_flow[i] > 0.5:
                    risk_score += 1
                
                # Drainage capacity risk
                if drainage_capacity[i] < 0.3:
                    risk_score += 2
                elif drainage_capacity[i] < 0.5:
                    risk_score += 1
                
                # Assign class based on total risk score
                if risk_score >= 6:
                    labels.append(2)  # critical
                elif risk_score >= 3:
                    labels.append(1)  # moderate
                else:
                    labels.append(0)  # safe
            
            # Prepare training data
            X = np.column_stack([water_level, rainfall, river_flow, drainage_capacity])
            y = np.array(labels)
            
            # Scale features
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight='balanced'
            )
            
            self.model.fit(X_scaled, y)
            
            # Save model
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            
            logger.info("✅ Enhanced AI model created and saved successfully")
            
        except Exception as e:
            logger.error(f"❌ Model creation error: {str(e)}")
    
    async def predict_flood_risk(self, city: str, lat: float, lng: float, 
                               features: Dict[str, float]) -> Dict[str, Any]:
        """Predict flood risk with explainable AI"""
        try:
            if self.model is None or self.scaler is None:
                self.load_model()
            
            # Prepare features
            feature_vector = np.array([
                features.get("water_level", 0),
                features.get("rainfall", 0),
                features.get("river_flow", 0),
                features.get("drainage_capacity", 0)
            ]).reshape(1, -1)
            
            # Scale features
            feature_vector_scaled = self.scaler.transform(feature_vector)
            
            # Make prediction
            prediction_proba = self.model.predict_proba(feature_vector_scaled)[0]
            prediction_class = self.model.predict(feature_vector_scaled)[0]
            
            # Get feature importance
            feature_importance = dict(zip(
                ["water_level", "rainfall", "river_flow", "drainage_capacity"],
                self.model.feature_importances_
            ))
            
            # Get prediction details
            prediction_name = self.class_names[prediction_class]
            confidence = prediction_proba[prediction_class] * 100
            
            # Generate explanation
            explanation = self.explainable_ai.explain_prediction(
                features, prediction_name, confidence, feature_importance
            )
            
            # Store prediction for learning
            self.historical_learning.store_prediction_data(
                city, lat, lng, features, prediction_name, confidence
            )
            
            # Get weather forecast
            weather_forecast = await self.openweather.get_rainfall_forecast(lat, lng, 5)
            
            result = {
                "city": city,
                "prediction": prediction_name,
                "confidence": round(confidence, 2),
                "risk_level": prediction_class,
                "explanation": explanation,
                "weather_forecast": weather_forecast,
                "feature_importance": feature_importance,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"✅ Flood risk prediction completed for {city}: {prediction_name} ({confidence:.1f}%)")
            return result
            
        except Exception as e:
            logger.error(f"❌ Flood risk prediction error: {str(e)}")
            return {
                "city": city,
                "prediction": "error",
                "confidence": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def retrain_model(self):
        """Retrain model with historical data"""
        try:
            logger.info("🔄 Starting model retraining with historical data...")
            
            X, y = self.historical_learning.get_training_data()
            
            if len(X) > 50:  # Minimum data for retraining
                # Scale features
                X_scaled = self.scaler.transform(X)
                
                # Retrain model
                self.model.fit(X_scaled, y)
                
                # Save updated model
                joblib.dump(self.model, self.model_path)
                
                logger.info(f"✅ Model retrained successfully with {len(X)} samples")
                return True
            else:
                logger.warning("⚠️ Insufficient historical data for retraining")
                return False
                
        except Exception as e:
            logger.error(f"❌ Model retraining error: {str(e)}")
            return False

# Main execution
async def main():
    """Main Enhanced AI Engine execution"""
    logger.info("🌊 Starting JalRakshā AI Enhanced Prediction Engine...")
    
    predictor = EnhancedAIPredictor()
    predictor.load_model()
    
    # Test prediction
    test_features = {
        "water_level": 6.5,
        "rainfall": 120.0,
        "river_flow": 0.8,
        "drainage_capacity": 0.3
    }
    
    result = await predictor.predict_flood_risk("Test City", 25.5941, 85.1376, test_features)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

