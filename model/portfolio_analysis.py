import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Dict, Tuple
from risk_free import get_average_risk_free_rate
import matplotlib.pyplot as plt


class PortfolioAnalyzer:
    def __init__(self, data: pd.DataFrame, risk_free_rate: float = None):
        self.data = data
        self.returns = data.pct_change().dropna()
        # Si no se proporciona risk_free_rate, se calcula desde risk_free.py
        self.risk_free_rate = risk_free_rate if risk_free_rate is not None else get_average_risk_free_rate()

    def calculate_metrics(self) -> Tuple[pd.Series, pd.Series]:
        """Calcula retorno y volatilidad por activo."""
        annual_returns = self.returns.mean() * 252
        annual_volatility = self.returns.std() * np.sqrt(252)
        return annual_returns, annual_volatility
    
    def optimize_weights(self, max_weight: float = 0.6, min_weight: float = 0.05) -> Dict:
        """Optimiza los pesos del portafolio usando Sharpe Ratio con restricción de peso máximo."""
        n_assets = len(self.data.columns)
        
        def neg_sharpe_ratio(weights):
            port_return = np.sum(self.returns.mean() * weights) * 252
            port_vol = np.sqrt(np.dot(weights.T, np.dot(self.returns.cov() * 252, weights)))
            sharpe = (port_return - self.risk_free_rate) / port_vol
            return -sharpe
        
        # Restricciones: suma de pesos = 1 y ningún peso mayor a max_weight
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # suma = 1
        ]
        bounds = tuple((min_weight, max_weight) for _ in range(n_assets))  # 0 ≤ peso ≤ 0.6
        
        result = minimize(neg_sharpe_ratio, 
                        n_assets * [1./n_assets,],
                        method='SLSQP',
                        bounds=bounds,
                        constraints=constraints)
        
        return {
            'weights': result.x,
            'sharpe_ratio': -result.fun,
            'success': result.success
        }

    def portfolio_performance(self, weights: np.array) -> Dict:
        """Calcula el rendimiento y riesgo del portafolio."""
        portfolio_return = np.sum(self.returns.mean() * weights) * 252
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(self.returns.cov() * 252, weights)))
        
        return {
            'return': portfolio_return,
            'volatility': portfolio_vol,
            'sharpe_ratio': (portfolio_return - self.risk_free_rate) / portfolio_vol
        }

    def distribution_graphics(self, weights: np.array, title: str = "Portfolio Distribution", 
                              others: float = 0.05, cmap: str = "tab20", height: int = 6, 
                              width: int = 10, nrow: int = 25, ax=None):
        """
        Grafica la distribución de pesos del portafolio en un gráfico de torta.
        
        Args:
            weights (np.array): Pesos optimizados del portafolio.
            title (str): Título del gráfico.
            others (float): Límite para agregar categorías pequeñas en "Otros".
            cmap (str): Paleta de colores.
            height (int): Altura del gráfico.
            width (int): Ancho del gráfico.
            nrow (int): Número de colores en el cmap.
            ax (matplotlib.axes.Axes): Objeto Axes para el gráfico.
        """
        # Validar entrada
        if not isinstance(weights, np.ndarray):
            raise ValueError("Los pesos deben ser un arreglo numpy (np.array).")
        
        asset_names = self.data.columns
        weights = pd.Series(weights, index=asset_names).sort_values(ascending=False)
        
        # Combinar categorías pequeñas en "Otros"
        if others > 0:
            small_weights = weights[weights < others].sum()
            weights = weights[weights >= others]
            if small_weights > 0:
                weights["Otros"] = small_weights
        
        # Crear el gráfico
        if ax is None:
            fig, ax = plt.subplots(figsize=(width, height))
        cmap = plt.get_cmap(cmap, nrow)
        
        wedges, texts, autotexts = ax.pie(
            weights,
            labels=weights.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=[plt.cm.tab20(i % 20) for i in range(len(weights))],
            pctdistance=0.85
        )
        
        # Estilo
        plt.setp(autotexts, size=8, weight="bold")
        ax.set_title(title, fontsize=14)
        ax.axis("equal")  # Asegurar que el gráfico sea circular
        
        plt.show()














class CompoundPortfolioAnalyzer:
    def __init__(self, portfolio_data: Dict[str, pd.DataFrame], portfolio_weights: Dict[str, float] = None, risk_free_rate: float = None):
        """
        Inicializa el analizador de portafolio compuesto.
        
        Args:
            portfolio_data: Diccionario con los datos de cada portafolio
            portfolio_weights: Pesos de cada portafolio en el portafolio total
        """
        self.portfolio_data = portfolio_data
        self.risk_free_rate = risk_free_rate if risk_free_rate is not None else get_average_risk_free_rate()
        self.portfolio_weights = portfolio_weights or {name: 0.2 for name in portfolio_data.keys()}
        self.create_compound_returns()
        
    def create_compound_returns(self):
        """Crea los retornos del portafolio compuesto."""
        # Calcular retornos para cada portafolio individual
        portfolio_returns = {}
        for name, data in self.portfolio_data.items():
            portfolio_returns[name] = data.pct_change().dropna()
            
        # Crear un DataFrame con todos los retornos
        all_returns = pd.DataFrame()
        for name, returns in portfolio_returns.items():
            # Multiplicar los retornos por el peso del portafolio
            weighted_returns = returns.mul(self.portfolio_weights[name])
            if all_returns.empty:
                all_returns = weighted_returns
            else:
                # Alinear las fechas antes de sumar
                all_returns = all_returns.add(weighted_returns, fill_value=0)
                
        self.compound_returns = all_returns

    def get_compound_metrics(self) -> Dict:
        """Calcula métricas para el portafolio compuesto."""
        annual_return = self.compound_returns.mean() * 252
        annual_vol = self.compound_returns.std() * np.sqrt(252)
        return {
            'return': annual_return,
            'volatility': annual_vol,
            'sharpe_ratio': (annual_return - self.risk_free_rate) / annual_vol
        }
