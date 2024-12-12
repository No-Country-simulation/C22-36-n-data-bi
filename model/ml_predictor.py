import os
import pickle
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from typing import Tuple

class PortfolioPredictor:
    def __init__(self, portfolio_data: pd.DataFrame, weights: np.array):
        self.data = portfolio_data
        self.weights = weights
        self.model = None  # Se inicializa sin modelo
        self.models_dir = "models"
        os.makedirs(self.models_dir, exist_ok=True)  # Crear la carpeta si no existe

    def prepare_data(self, window_size: int = 30) -> Tuple[np.array, np.array]:
        """Prepara los datos para el modelo."""
        if self.weights is not None:
            portfolio_returns = (self.data.pct_change() * self.weights).sum(axis=1)
        else:
            portfolio_returns = self.data.sum(axis=1)

        X, y = [], []
        for i in range(window_size, len(portfolio_returns)):
            X.append(portfolio_returns.iloc[i - window_size:i].values)
            y.append(portfolio_returns.iloc[i])

        return np.array(X), np.array(y)

    def train_or_load_model(self, train_new_model: bool = True, model_id: int = None) -> None:
        """
        Entrena un nuevo modelo o carga un modelo existente.

        Args:
            train_new_model (bool): Si True, entrena y guarda un nuevo modelo.
                                    Si False, carga un modelo existente basado en model_id.
            model_id (int): ID del modelo a cargar si train_new_model es False.
        """
        if train_new_model:
            # Entrenar un nuevo modelo
            print("Entrenando un nuevo modelo...")
            X, y = self.prepare_data()
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model = HistGradientBoostingRegressor(max_iter=100, max_depth=15, random_state=42)
            self.model.fit(X_train, y_train)
            
            # Guardar el modelo con un número secuencial
            model_id = len(os.listdir(self.models_dir)) + 1
            model_path = os.path.join(self.models_dir, f"model_{model_id}.pkl")
            with open(model_path, "wb") as f:
                pickle.dump(self.model, f)
            print(f"Modelo guardado en {model_path}")
        else:
            # Cargar un modelo existente
            if model_id is None:
                raise ValueError("Debe proporcionar un model_id para cargar un modelo existente.")
            model_path = os.path.join(self.models_dir, f"model_{model_id}.pkl")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"El modelo {model_id} no existe en la carpeta {self.models_dir}.")
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            print(f"Modelo {model_id} cargado desde {model_path}.")

    def predict_returns(self, investment: float, years: int) -> pd.DataFrame:
        """Predice retornos futuros para un monto de inversión."""
        if self.model is None:
            raise ValueError("Debe entrenar o cargar un modelo antes de predecir.")
        
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
