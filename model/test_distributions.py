# test_portfolio.py
import pandas as pd
import numpy as np
from data_loader import DataLoader
from portfolio_analysis import PortfolioAnalyzer
from ml_predictor import PortfolioPredictor
import matplotlib.pyplot as plt

def mostrar_resultados_portafolio(nombre, resultados):
    """Función helper para mostrar resultados de manera formateada"""
    print(f"\n=== Resultados para {nombre} ===")
    print("\nRetornos anualizados por activo:")
    print(resultados['returns'].round(4) * 100, "%")
    
    print("\nVolatilidad anualizada por activo:")
    print(resultados['volatility'].round(4) * 100, "%")
    
    print("\nPesos óptimos:")
    for asset, weight in zip(resultados['returns'].index, 
                           resultados['optimal_weights']['weights']):
        print(f"{asset}: {weight:.4%}")
    
    print(f"\nRatio Sharpe del portafolio: {resultados['optimal_weights']['sharpe_ratio']:.4f}")

def mostrar_grafico_portafolio(analyzer, optimal_weights, nombre):
    """
    Función para mostrar el gráfico de distribución del portafolio.
    """
    print(f"\nGenerando gráfico para el portafolio {nombre}...")
    analyzer.distribution_graphics(
        weights=optimal_weights['weights'],
        title=f"Distribución del Portafolio {nombre}"
    )

def ejecutar_analisis():
    # 1. Definir los portafolios
    portfolios = {
        "Bonos": ["^IRX", "^FVX", "^TNX", "^TYX"],
        "ETFs": ["SPY", "QQQ", "VTI", "IVV", "XLV"],
        "Acciones": ["MSFT", "GOOGL", "O", "PG", "ISRG", "MDT", "JPM"],
        "Futuros": ["GC=F", "CL=F", "SI=F", "NQ=F", "ES=F"],
        "Criptomonedas": ["BTC-USD", "ETH-USD", "BNB-USD", "TRX-USD", "DOGE-USD"]
    }

    # 2. Cargar datos
    print("Cargando datos...")
    loader = DataLoader(start_date="2020-01-01")  # Últimos 4 años de datos
    portfolio_data = loader.process_portfolios(portfolios)

    # 3. Analizar cada portafolio
    portfolio_results = {}
    for name, data in portfolio_data.items():
        if not data.empty:
            print(f"\nAnalizando portafolio {name}...")
            analyzer = PortfolioAnalyzer(data)
            returns, volatility = analyzer.calculate_metrics()
            optimal_weights = analyzer.optimize_weights()
            
            portfolio_results[name] = {
                'returns': returns,
                'volatility': volatility,
                'optimal_weights': optimal_weights
            }
            
            # Mostrar resultados en consola
            mostrar_resultados_portafolio(name, portfolio_results[name])
            
            # Mostrar gráfico de distribución
            mostrar_grafico_portafolio(analyzer, optimal_weights, name)

# Ejecutar el análisis
if __name__ == "__main__":
    ejecutar_analisis()
