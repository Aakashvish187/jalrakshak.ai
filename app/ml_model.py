"""
Machine Learning Model for Flood Risk Prediction

This module handles the training, saving, and loading of the ML model
used for flood risk prediction. It uses RandomForestClassifier from scikit-learn
to classify flood risk into LOW, MEDIUM, and HIGH categories.
"""

import logging
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, Any
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

# Model configuration
MODEL_PATH = Path("model.pkl")
SCALER_PATH = Path("scaler.pkl")
RISK_LEVELS = ["LOW", "MEDIUM", "HIGH"]


class FloodRiskPredictor:
    """
    Flood risk prediction model using RandomForestClassifier.
    
    This class handles model training, prediction, and persistence.
    It generates synthetic training data and trains a classifier
    to predict flood risk levels based on water level, rainfall, and river flow.
    """
    
    def __init__(self):
        """Initialize the flood risk predictor."""
        self.model = None
        self.scaler = None
        self.is_trained = False
        self.feature_names = ["water_level", "rainfall", "river_flow"]
        
    def generate_synthetic_data(self, n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate synthetic training data for flood risk prediction.
        
        Args:
            n_samples: Number of samples to generate
            
        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and labels
        """
        logger.info(f"Generating {n_samples} synthetic training samples...")
        
        np.random.seed(42)  # For reproducible results
        
        # Generate features with realistic ranges
        water_levels = np.random.uniform(0, 10, n_samples)  # 0-10 meters
        rainfall = np.random.uniform(0, 200, n_samples)     # 0-200 mm
        river_flow = np.random.uniform(0, 1000, n_samples)  # 0-1000 m³/s
        
        # Create feature matrix
        X = np.column_stack([water_levels, rainfall, river_flow])
        
        # Generate labels based on realistic flood risk criteria
        y = np.zeros(n_samples, dtype=int)
        
        for i in range(n_samples):
            wl, rf, rv = X[i]
            
            # Risk assessment logic
            risk_score = 0
            
            # Water level contribution (0-3 points)
            if wl > 7:
                risk_score += 3
            elif wl > 5:
                risk_score += 2
            elif wl > 3:
                risk_score += 1
            
            # Rainfall contribution (0-3 points)
            if rf > 150:
                risk_score += 3
            elif rf > 100:
                risk_score += 2
            elif rf > 50:
                risk_score += 1
            
            # River flow contribution (0-3 points)
            if rv > 800:
                risk_score += 3
            elif rv > 500:
                risk_score += 2
            elif rv > 200:
                risk_score += 1
            
            # Add some noise for realism
            noise = np.random.normal(0, 0.5)
            risk_score += noise
            
            # Assign risk level based on total score
            if risk_score >= 6:
                y[i] = 2  # HIGH
            elif risk_score >= 3:
                y[i] = 1  # MEDIUM
            else:
                y[i] = 0  # LOW
        
        logger.info(f"Generated data distribution: LOW={np.sum(y==0)}, MEDIUM={np.sum(y==1)}, HIGH={np.sum(y==2)}")
        return X, y
    
    def train_model(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """
        Train the RandomForest model on the provided data.
        
        Args:
            X: Feature matrix
            y: Target labels
            
        Returns:
            Dict[str, Any]: Training metrics and results
        """
        logger.info("Training RandomForest model...")
        
        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train RandomForest model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Get feature importance
        feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
        
        # Generate classification report
        class_report = classification_report(
            y_test, y_pred, 
            target_names=RISK_LEVELS, 
            output_dict=True
        )
        
        self.is_trained = True
        
        metrics = {
            "accuracy": accuracy,
            "feature_importance": feature_importance,
            "classification_report": class_report,
            "n_samples": len(X),
            "n_train": len(X_train),
            "n_test": len(X_test)
        }
        
        logger.info(f"Model training completed. Accuracy: {accuracy:.3f}")
        logger.info(f"Feature importance: {feature_importance}")
        
        return metrics
    
    def predict(self, water_level: float, rainfall: float, river_flow: float) -> Tuple[str, float]:
        """
        Predict flood risk level for given input parameters.
        
        Args:
            water_level: Water level in meters
            rainfall: Rainfall in millimeters
            river_flow: River flow in cubic meters per second
            
        Returns:
            Tuple[str, float]: Risk level and confidence score
            
        Raises:
            ValueError: If model is not trained
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model is not trained. Please train the model first.")
        
        # Prepare input data
        X = np.array([[water_level, rainfall, river_flow]])
        X_scaled = self.scaler.transform(X)
        
        # Make prediction
        prediction = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]
        confidence = np.max(probabilities)
        
        risk_level = RISK_LEVELS[prediction]
        
        logger.info(f"Prediction: {risk_level} (confidence: {confidence:.3f})")
        
        return risk_level, confidence
    
    def save_model(self, model_path: Path = MODEL_PATH, scaler_path: Path = SCALER_PATH) -> bool:
        """
        Save the trained model and scaler to disk.
        
        Args:
            model_path: Path to save the model
            scaler_path: Path to save the scaler
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            if not self.is_trained:
                logger.error("Cannot save untrained model")
                return False
            
            # Save model
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            
            # Save scaler
            with open(scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            
            logger.info(f"Model saved to {model_path}")
            logger.info(f"Scaler saved to {scaler_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
            return False
    
    def load_model(self, model_path: Path = MODEL_PATH, scaler_path: Path = SCALER_PATH) -> bool:
        """
        Load a pre-trained model and scaler from disk.
        
        Args:
            model_path: Path to the saved model
            scaler_path: Path to the saved scaler
            
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        try:
            if not model_path.exists() or not scaler_path.exists():
                logger.warning("Model files not found. Training new model...")
                return self.train_and_save()
            
            # Load model
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            # Load scaler
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            
            self.is_trained = True
            logger.info(f"Model loaded from {model_path}")
            logger.info(f"Scaler loaded from {scaler_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def train_and_save(self) -> bool:
        """
        Train a new model and save it to disk.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Generate synthetic data
            X, y = self.generate_synthetic_data()
            
            # Train model
            metrics = self.train_model(X, y)
            
            # Save model
            success = self.save_model()
            
            if success:
                logger.info("Model training and saving completed successfully")
                return True
            else:
                logger.error("Model training succeeded but saving failed")
                return False
                
        except Exception as e:
            logger.error(f"Model training and saving failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model.
        
        Returns:
            Dict[str, Any]: Model information
        """
        if not self.is_trained:
            return {"status": "not_trained"}
        
        return {
            "status": "trained",
            "model_type": "RandomForestClassifier",
            "feature_names": self.feature_names,
            "risk_levels": RISK_LEVELS,
            "n_estimators": self.model.n_estimators if self.model else None,
            "model_path": str(MODEL_PATH),
            "scaler_path": str(SCALER_PATH)
        }


# Global model instance
predictor = FloodRiskPredictor()


def initialize_model() -> bool:
    """
    Initialize the ML model by loading or training.
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("Initializing ML model...")
    
    # Try to load existing model first
    if predictor.load_model():
        logger.info("ML model loaded successfully")
        return True
    
    # If loading fails, train a new model
    logger.info("Training new ML model...")
    if predictor.train_and_save():
        logger.info("ML model trained and saved successfully")
        return True
    
    logger.error("Failed to initialize ML model")
    return False


def predict_flood_risk(water_level: float, rainfall: float, river_flow: float) -> Tuple[str, float]:
    """
    Predict flood risk using the global model instance.
    
    Args:
        water_level: Water level in meters
        rainfall: Rainfall in millimeters
        river_flow: River flow in cubic meters per second
        
    Returns:
        Tuple[str, float]: Risk level and confidence score
    """
    return predictor.predict(water_level, rainfall, river_flow)
