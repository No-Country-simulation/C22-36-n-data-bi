import yfinance as yf
import pandas as pd
from typing import Dict, List

class DataLoader:
    def __init__(self, start_date: str = "2017-11-09", end_date: str = "2024-10-31"):
        self.start_date = start_date
        self.end_date = end_date
        
    def download_data(self, assets: List[str]) -> pd.DataFrame:
        """Descarga datos históricos para una lista de activos."""
        dataframes = []
        for asset in assets:
            try:
                ticker = yf.Ticker(asset)
                df = ticker.history(start=self.start_date, end=self.end_date)
                if not df.empty:
                    df = df[['Close']].rename(columns={"Close": asset})
                    dataframes.append(df)
            except Exception as e:
                print(f"Error descargando {asset}: {e}")
        
        return pd.concat(dataframes, axis=1) if dataframes else pd.DataFrame()
    
    def process_portfolios(self, portfolios: Dict[str, List[str]]) -> Dict[str, pd.DataFrame]:
        """Procesa múltiples portafolios y retorna sus dataframes."""
        return {name: self.download_data(assets) 
                for name, assets in portfolios.items()}