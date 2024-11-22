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

def ejecutar_analisis():
    # 1. Definir los portafolios
    portfolios = {
        "Bonos": ["^IRX", "^FVX", "^TNX", "^TYX"],
        "Acciones": ["SPY", "QQQ", "VTI", "IVV", "XLV"],
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
            
            mostrar_resultados_portafolio(name, portfolio_results[name])

    # 4. Realizar predicciones para un portafolio específico
    print("\n=== Predicciones para el portafolio de Acciones ===")
    
    # Usar el portafolio de Acciones para las predicciones
    if 'Acciones' in portfolio_data:
        etf_data = portfolio_data['Acciones']
        etf_weights = portfolio_results['Acciones']['optimal_weights']['weights']
        
        predictor = PortfolioPredictor(etf_data, etf_weights)
        predictor.train_model()
        
        # Hacer predicciones para diferentes horizontes temporales
        investment = 100000  # $100,000 inicial
        
        for years in [3, 5, 10]:
            predictions = predictor.predict_returns(investment, years)
            final_value = predictions['Portfolio_Value'].iloc[-1]
            total_return = (final_value - investment) / investment * 100
            
            print(f"\nPredicción a {years} años:")
            print(f"Inversión inicial: ${investment:,.2f}")
            print(f"Valor final estimado: ${final_value:,.2f}")
            print(f"Retorno total estimado: {total_return:.2f}%")
            
            # Graficar la evolución del portafolio
            plt.figure(figsize=(10, 6))
            plt.plot(predictions['Day'], predictions['Portfolio_Value'])
            plt.title(f'Proyección del Valor del Portafolio a {years} años')
            plt.xlabel('Días')
            plt.ylabel('Valor del Portafolio ($)')
            plt.grid(True)
            plt.show()

if __name__ == "__main__":
    ejecutar_analisis()