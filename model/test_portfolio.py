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

def guardar_resultados_csv(portfolio_results, filename="portfolio_results.csv"):
    """
    Función para guardar los resultados del análisis de portafolio en un archivo CSV.
    """
    data_for_csv = []
    for name, results in portfolio_results.items():
        for asset in results['returns'].index:
            data_for_csv.append({
                'Portafolio': name,
                'Activo': asset,
                'Retorno Anualizado (%)': results['returns'][asset] * 100,
                'Volatilidad Anualizada (%)': results['volatility'][asset] * 100
            })
    
    df = pd.DataFrame(data_for_csv)
    df.to_csv(filename, index=False)
    print(f"\nResultados guardados en {filename}")

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
    loader = DataLoader(start_date="2017-11-09")  # Últimos 4 años de datos
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

    # 4. Guardar resultados en un archivo CSV
    guardar_resultados_csv(portfolio_results)
            
    # 4. Realizar predicciones para todos los portafolios
    # Porcentajes de inversión para cada portafolio
    portfolio_shares = {
        'Bonos': 0.40,          # 50% para Bonos
        'ETFs': 0.40,           # 50% para ETFs
        'Acciones': 0.20,        # 0% para Acciones
        'Futuros': 0.0,         # 0% para Futuros
        'Criptomonedas': 0.0    # 0% para Criptomonedas
    }

    investment_total = 100000  # Capital total inicial

    # Validar que los porcentajes asignados sumen al 100%
    active_portfolios = {k: v for k, v in portfolio_shares.items() if v > 0}
    total_share = sum(active_portfolios.values())
    if not 0.99 <= total_share <= 1.01:
        raise ValueError("Los porcentajes asignados deben sumar 100%.")

    print("\n=== Predicciones para portafolios seleccionados ===")
    portfolios = active_portfolios.keys()

    # Diccionario para almacenar resultados y datos de gráficas
    predictions_by_year = {3: [], 5: [], 10: []}

    for portfolio_name in portfolios:
        if portfolio_name in portfolio_data:
            print(f"\n=== Predicciones para el portafolio de {portfolio_name} ===")
            
            portfolio_data_current = portfolio_data[portfolio_name]
            portfolio_weights = portfolio_results[portfolio_name]['optimal_weights']['weights']
            
            predictor = PortfolioPredictor(portfolio_data_current, portfolio_weights)
            predictor.train_model()
            
            # Determinar inversión inicial para este portafolio
            investment = investment_total * active_portfolios[portfolio_name]
            
            for years in [3, 5, 10]:
                predictions = predictor.predict_returns(investment, years)
                final_value = predictions['Portfolio_Value'].iloc[-1]
                total_return = (final_value - investment) / investment * 100
                
                print(f"\nPredicción a {years} años para {portfolio_name}:")
                print(f"Inversión inicial: ${investment:,.2f}")
                print(f"Valor final estimado: ${final_value:,.2f}")
                print(f"Retorno total estimado: {total_return:.2f}%")
                
                # Guardar datos para graficar
                predictions['Portfolio'] = portfolio_name  # Identificar el portafolio en el dataframe
                predictions_by_year[years].append(predictions)

    # Generar gráficos combinados para cada horizonte temporal
    for years, predictions_list in predictions_by_year.items():
        plt.figure(figsize=(12, 8))
        for predictions in predictions_list:
            portfolio_name = predictions['Portfolio'].iloc[0]
            plt.plot(predictions['Day'], predictions['Portfolio_Value'], label=portfolio_name)
        plt.title(f'Proyección del Valor de los Portafolios a {years} años')
        plt.xlabel('Días')
        plt.ylabel('Valor del Portafolio ($)')
        plt.legend()
        plt.grid(True)
        plt.show()

    # Opcional: Resumen del retorno ponderado por horizonte
    print("\n=== Resumen del Retorno Ponderado ===")
    for years in [3, 5, 10]:
        total_weighted_return = sum(
            ((pred['Portfolio_Value'].iloc[-1] - investment_total * active_portfolios[pred['Portfolio'].iloc[0]]) /
            (investment_total * active_portfolios[pred['Portfolio'].iloc[0]]) * 100) * 
            active_portfolios[pred['Portfolio'].iloc[0]]
            for pred in predictions_by_year[years]
        )
        print(f"Retorno ponderado total estimado a {years} años: {total_weighted_return:.2f}%")




if __name__ == "__main__":
    ejecutar_analisis()