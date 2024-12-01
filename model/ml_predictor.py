from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from typing import Dict, Tuple

class PortfolioPredictor:
    def __init__(self, portfolio_data: pd.DataFrame, weights: np.array):
        self.data = portfolio_data
        self.weights = weights
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        
    def prepare_data(self, window_size: int = 30) -> Tuple[np.array, np.array]:
        """Preparación los datos para el modelo de ML."""
        if self.weights is not None:
            # Caso de portafolio específico
            portfolio_returns = (self.data.pct_change() * self.weights).sum(axis=1)
        else:
            # Caso de portafolio compuesto (datos ya ponderados)
            portfolio_returns = self.data.sum(axis=1)
            
        X, y = [], []
        for i in range(window_size, len(portfolio_returns)):
            X.append(portfolio_returns.iloc[i-window_size:i].values)
            y.append(portfolio_returns.iloc[i])
            
        return np.array(X), np.array(y)
    
    def train_model(self) -> None:
        """Entrena el modelo de predicción."""
        X, y = self.prepare_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.model.fit(X_train, y_train)
        
    def predict_returns(self, investment: float, years: int) -> pd.DataFrame:
        """Predice retornos futuros para un monto de inversión."""
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