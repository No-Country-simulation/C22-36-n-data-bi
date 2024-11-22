# test.py
import pandas as pd
import numpy as np
from data_loader import DataLoader
from portfolio_analysis import PortfolioAnalyzer, CompoundPortfolioAnalyzer
from ml_predictor import PortfolioPredictor

def test_data_loading():
    """Prueba la carga de datos"""
    print("\n=== Prueba de Carga de Datos ===")
    
    portfolios = {
        "Bonos": ["^IRX", "^FVX", "^TNX", "^TYX"],
        "ETFs": ["SPY", "QQQ", "VTI", "IVV", "XLV"],
        "Acciones": ["MSFT", "GOOGL", "O", "PG", "ISRG", "MDT", "JPM"],
        "Futuros": ["GC=F", "CL=F", "SI=F", "NQ=F", "ES=F"],
        "Criptomonedas": ["BTC-USD", "ETH-USD", "BNB-USD", "TRX-USD", "DOGE-USD"]
    }
    
    loader = DataLoader(start_date="2020-01-01", end_date="2024-01-01")
    portfolio_data = loader.process_portfolios(portfolios)
    
    for name, data in portfolio_data.items():
        print(f"\nPortafolio {name}:")
        print(f"Número de activos: {len(data.columns)}")
        print(f"Período: {data.index[0]} a {data.index[-1]}")
        print(f"Número de días: {len(data)}")
    
    return portfolio_data

def test_individual_portfolio(portfolio_data):
    """Prueba el análisis de portafolios individuales"""
    print("\n=== Prueba de Análisis Individual ===")
    
    results = {}
    for name, data in portfolio_data.items():
        print(f"\nAnálisis del portafolio: {name}")
        
        analyzer = PortfolioAnalyzer(data)
        returns, volatility = analyzer.calculate_metrics()
        optimal_weights = analyzer.optimize_weights(max_weight=0.6)
        
        print("\nRetornos anualizados por activo:")
        for asset, ret in returns.items():
            print(f"{asset}: {ret*100:.2f}%")
        
        print("\nVolatilidad anualizada por activo:")
        for asset, vol in volatility.items():
            print(f"{asset}: {vol*100:.2f}%")
        
        print("\nPesos óptimos (máx 60%):")
        for asset, weight in zip(data.columns, optimal_weights['weights']):
            print(f"{asset}: {weight*100:.2f}%")
        
        performance = analyzer.portfolio_performance(optimal_weights['weights'])
        print(f"\nRendimiento del portafolio optimizado:")
        print(f"Retorno anualizado: {float(performance['return'])*100:.2f}%")
        print(f"Volatilidad anualizada: {float(performance['volatility'])*100:.2f}%")
        print(f"Ratio Sharpe: {float(performance['sharpe_ratio']):.2f}")
        
        results[name] = {
            'data': data,
            'optimal_weights': optimal_weights['weights']
        }
    
    return results

def test_compound_portfolio(portfolio_data):
    """Prueba el portafolio compuesto"""
    print("\n=== Prueba de Portafolio Compuesto ===")
    
    # Crear portafolio compuesto con pesos iguales (20%)
    compound_analyzer = CompoundPortfolioAnalyzer(portfolio_data)
    compound_metrics = compound_analyzer.get_compound_metrics()
    
    print("\nMétricas del portafolio compuesto:")
    print(f"Retorno anualizado: {float(compound_metrics['return'].mean())*100:.2f}%")
    print(f"Volatilidad anualizada: {float(compound_metrics['volatility'].mean())*100:.2f}%")
    print(f"Ratio Sharpe: {float(compound_metrics['sharpe_ratio'].mean()):.2f}")
    
    return compound_analyzer

def test_predictions(portfolio_analyzer, compound_analyzer):
    """Prueba las predicciones"""
    print("\n=== Prueba de Predicciones ===")
    
    # Predicción para un portafolio individual (usando ETFs como ejemplo)
    etf_data = portfolio_analyzer["ETFs"]["data"]
    etf_weights = portfolio_analyzer["ETFs"]["optimal_weights"]
    
    print("\nPredicciones para portafolio ETFs:")
    predictor = PortfolioPredictor(etf_data, etf_weights)
    predictor.train_model()
    
    investment = 100000  # $100,000 inicial
    pred_3y = predictor.predict_returns(investment, 3)
    print(f"\nPredicción a 3 años:")
    print(f"Valor final esperado: ${float(pred_3y['Portfolio_Value'].iloc[-1]):,.2f}")
    print(f"Retorno total esperado: {(float(pred_3y['Portfolio_Value'].iloc[-1])/investment - 1)*100:.2f}%")
    
    # Predicción para el portafolio compuesto
    print("\nPredicciones para portafolio compuesto:")
    compound_predictor = PortfolioPredictor(compound_analyzer.compound_returns)
    compound_predictor.train_model()
    
    pred_compound = compound_predictor.predict_returns(investment, 3)
    print(f"\nPredicción a 3 años (portafolio compuesto):")
    print(f"Valor final esperado: ${float(pred_compound['Portfolio_Value'].iloc[-1]):,.2f}")
    print(f"Retorno total esperado: {(float(pred_compound['Portfolio_Value'].iloc[-1])/investment - 1)*100:.2f}%")

def main():
    """Función principal de prueba"""
    try:
        # Ejecutar todas las pruebas
        portfolio_data = test_data_loading()
        portfolio_analyzer = test_individual_portfolio(portfolio_data)
        compound_analyzer = test_compound_portfolio(portfolio_data)
        test_predictions(portfolio_analyzer, compound_analyzer)
        
        print("\n=== Todas las pruebas completadas exitosamente ===")
        
    except Exception as e:
        print(f"\nError durante las pruebas: {str(e)}")
        raise

if __name__ == "__main__":
    main()