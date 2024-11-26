from data_loader import DataLoader
from portfolio_analysis import PortfolioAnalyzer
from ml_predictor import PortfolioPredictor
from portfolio_analysis import CompoundPortfolioAnalyzer


def main():
    # Definir los portafolios como en tu código original
    portfolios = {
        "Bonos": ["^IRX", "^FVX", "^TNX", "^TYX"],
        "ETFs": ["SPY", "QQQ", "VTI", "IVV", "XLV"],
        "Acciones": ["MSFT", "GOOGL", "O", "PG", "ISRG", "MDT", "JPM"],
        "Futuros": ["GC=F", "CL=F", "SI=F", "NQ=F", "ES=F"],
        "Criptomonedas": ["BTC-USD", "ETH-USD", "BNB-USD", "TRX-USD", "DOGE-USD"]
    }
    
    # Inicializar el cargador de datos
    loader = DataLoader()
    portfolio_data = loader.process_portfolios(portfolios)
    
    # Analizar cada portafolio
    portfolio_results = {}
    for name, data in portfolio_data.items():
        analyzer = PortfolioAnalyzer(data)
        returns, volatility = analyzer.calculate_metrics()
        optimal_weights = analyzer.optimize_weights()
        
        portfolio_results[name] = {
            'returns': returns,
            'volatility': volatility,
            'optimal_weights': optimal_weights
        }
    
       

    # Crear y analizar el portafolio compuesto
    compound_analyzer = CompoundPortfolioAnalyzer(portfolio_data)
    compound_metrics = compound_analyzer.get_compound_metrics()
    
    # Predictor para el portafolio compuesto
    compound_predictor = PortfolioPredictor(compound_analyzer.compound_returns)
    compound_predictor.train_model()
    
    # Predicciones para el portafolio compuesto
    investment = 100000  # $100,000 inicial
    compound_pred_3y = compound_predictor.predict_returns(investment, 3)
    compound_pred_5y = compound_predictor.predict_returns(investment, 5)
    compound_pred_10y = compound_predictor.predict_returns(investment, 10)
    
    return portfolio_results, compound_metrics, {
        '3y': compound_pred_3y,
        '5y': compound_pred_5y,
        '10y': compound_pred_10y
    }

if __name__ == "__main__":
    main()