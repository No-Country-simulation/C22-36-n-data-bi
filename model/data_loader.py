import os
import yfinance as yf
import pandas as pd
from typing import Dict, List

class DataLoader:
    def __init__(self, start_date: str = "2017-11-09", end_date: str = "2024-10-31", data_dir: str = "data"):
        self.start_date = start_date
        self.end_date = end_date
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)  # Crear la carpeta 'data' si no existe
        print(f"Directorio de datos: {self.data_dir}")

    def _get_file_path(self, asset: str) -> str:
        """Devuelve la ruta del archivo para un activo dado."""
        file_path = os.path.join(self.data_dir, f"{asset}.csv")
        print(f"Ruta del archivo para {asset}: {file_path}")
        return file_path
    
    def _is_data_available(self, asset: str) -> bool:
        """Verifica si los datos para un activo ya están descargados."""
        file_path = self._get_file_path(asset)
        data_available = os.path.isfile(file_path)
        print(f"¿Datos disponibles para {asset}? {'Sí' if data_available else 'No'}")
        return data_available

    def _load_existing_data(self, asset: str) -> pd.DataFrame:
        """Carga los datos existentes desde un archivo CSV."""
        file_path = self._get_file_path(asset)
        print(f"Cargando datos existentes de {file_path}")
        return pd.read_csv(file_path, index_col=0, parse_dates=True)

    def download_data(self, assets: List[str], force_download: bool = False) -> pd.DataFrame:
        """Descarga datos históricos para una lista de activos o carga los existentes."""
        print(f"Descargando datos para los activos: {assets}")
        dataframes = []
        for asset in assets:
            try:
                if not force_download and self._is_data_available(asset):
                    # Cargar datos existentes si no se requiere una nueva descarga
                    print(f"Cargando datos existentes para {asset}")
                    df = self._load_existing_data(asset)
                else:
                    # Descargar los datos y guardarlos en un archivo CSV
                    print(f"Descargando datos para {asset} desde Yahoo Finance")
                    ticker = yf.Ticker(asset)
                    df = ticker.history(start=self.start_date, end=self.end_date)
                    if not df.empty:
                        df = df[['Close']].rename(columns={"Close": asset})
                        df.to_csv(self._get_file_path(asset))
                        print(f"Datos descargados y guardados para {asset}")
                    else:
                        print(f"No se encontraron datos para {asset}")
                dataframes.append(df)
            except Exception as e:
                print(f"Error procesando {asset}: {e}")
        
        result = pd.concat(dataframes, axis=1) if dataframes else pd.DataFrame()
        print(f"Datos combinados: {result.shape[0]} filas, {result.shape[1]} columnas")
        return result
    
    def process_portfolios(self, portfolios: Dict[str, List[str]], force_download: bool = False) -> Dict[str, pd.DataFrame]:
        """Procesa múltiples portafolios y retorna sus dataframes."""
        print(f"Procesando {len(portfolios)} portafolios")
        portfolio_data = {
            name: self.download_data(assets, force_download=force_download)
            for name, assets in portfolios.items()
        }
        print(f"Portafolios procesados: {', '.join(portfolio_data.keys())}")
        return portfolio_data
