import os
import pickle
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any

# Scikit-learn imports
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error, 
    mean_squared_error, 
    r2_score
)

class PortfolioPredictor:
    def __init__(self, portfolio_data: pd.DataFrame, weights: np.array = None):
        """
        Initialize the PortfolioPredictor.
        
        Args:
            portfolio_data (pd.DataFrame): DataFrame of portfolio returns
            weights (np.array, optional): Portfolio weights
        """
        self.data = portfolio_data
        self.weights = weights
        self.model = None
        self.models_dir = "models"
        os.makedirs(self.models_dir, exist_ok=True)

    def prepare_data(self, window_size: int = 30) -> Tuple[np.array, np.array]:
        """
        Prepare data for time series prediction.
        
        Args:
            window_size (int): Number of previous days to use for prediction
        
        Returns:
            Tuple of X and y arrays for model training
        """
        if self.weights is not None:
            portfolio_returns = (self.data.pct_change() * self.weights).sum(axis=1)
        else:
            portfolio_returns = self.data.sum(axis=1)
        
        X, y = [], []
        for i in range(window_size, len(portfolio_returns)):
            X.append(portfolio_returns.iloc[i - window_size:i].values)
            y.append(portfolio_returns.iloc[i])
        
        return np.array(X), np.array(y)

    def train_or_load_model(self, train_new_model: bool = True, model_id: int = None) -> Dict[str, Any]:
        """
        Train a new model or load an existing model.
        
        Args:
            train_new_model (bool): If True, train and save a new model
            model_id (int, optional): ID of the model to load if train_new_model is False
        
        Returns:
            Dict containing model confidence metrics
        """
        if train_new_model:
            # Train a new model
            print("Training a new model...")
            X, y = self.prepare_data()
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            self.model = HistGradientBoostingRegressor(
                max_iter=100, 
                max_depth=15, 
                random_state=42
            )
            self.model.fit(X_train, y_train)
            
            # Save the model with a sequential number
            model_id = len(os.listdir(self.models_dir)) + 1
            model_path = os.path.join(self.models_dir, f"model_{model_id}.pkl")
            with open(model_path, "wb") as f:
                pickle.dump(self.model, f)
            print(f"Model saved in {model_path}")
            
            # Calculate model confidence
            confidence_metrics = self.calculate_model_confidence(self.model, X_test, y_test)
            return confidence_metrics
        
        else:
            # Load an existing model
            if model_id is None:
                raise ValueError("Must provide a model_id to load an existing model.")
            
            model_path = os.path.join(self.models_dir, f"model_{model_id}.pkl")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model {model_id} does not exist in {self.models_dir}.")
            
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            print(f"Model {model_id} loaded from {model_path}.")
            
            return {}

    def calculate_model_confidence(self, model, X_test, y_test) -> Dict[str, Any]:
        """
        Calculate comprehensive model confidence metrics.
        
        Args:
            model: Trained machine learning model
            X_test: Test features
            y_test: True values
        
        Returns:
            Dict with confidence metrics and composite confidence score
        """
        # Predictions
        y_pred = model.predict(X_test)
        
        # Confidence metrics
        confidence_metrics = {
            # Coefficient of determination (R-squared)
            'r_squared': r2_score(y_test, y_pred),
            
            # Mean Absolute Error (MAE)
            'mae': mean_absolute_error(y_test, y_pred),
            
            # Mean Squared Error (MSE)
            'mse': mean_squared_error(y_test, y_pred),
            
            # Root Mean Squared Error (RMSE)
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            
            # Mean Absolute Percentage Error (MAPE)
            'mape': np.mean(np.abs((y_test - y_pred) / y_test)) * 100,
            
            # Correlation between predictions and actual values
            'prediction_correlation': np.corrcoef(y_test, y_pred)[0, 1]
        }
        
        # Compute a composite confidence score
        confidence_score = (
            confidence_metrics['r_squared'] * 0.4 +  # Primary weight to R-squared
            (1 - confidence_metrics['rmse']) * 0.3 +  # Inverse of RMSE
            (1 - confidence_metrics['mape']/100) * 0.2 +  # Inverse of MAPE
            (confidence_metrics['prediction_correlation'] + 1) / 2 * 0.1  # Normalized correlation
        )
        
        # Normalize confidence score between 0 and 1
        confidence_score = max(0, min(1, confidence_score))
        
        # Print metrics for transparency
        print("\nModel Confidence Metrics:")
        for key, value in confidence_metrics.items():
            print(f"{key}: {value:.4f}")
        print(f"Composite Confidence Score: {confidence_score:.4f}")
        
        return {
            'confidence_metrics': confidence_metrics,
            'confidence_score': confidence_score
        }

    def predict_returns(self, investment: float, years: int) -> pd.DataFrame:
        """
        Predict future portfolio returns.
        
        Args:
            investment (float): Initial investment amount
            years (int): Investment horizon
        
        Returns:
            DataFrame with predicted returns and portfolio values
        """
        if self.model is None:
            raise ValueError("Must train or load a model before predicting.")
        
        days = years * 252
        last_window = self.prepare_data()[0][-1]
        predictions = []
        current_window = last_window
        
        for _ in range(days):
            pred = self.model.predict(current_window.reshape(1, -1))[0]
            predictions.append(pred)
            current_window = np.roll(current_window, -1)
            current_window[-1] = pred
        
        cumulative_returns = (1 + np.array(predictions)).cumprod()
        projected_value = investment * cumulative_returns
        
        return pd.DataFrame({
            'Day': range(1, days + 1),
            'Predicted_Return': predictions,
            'Cumulative_Return': cumulative_returns,
            'Portfolio_Value': projected_value
        })
