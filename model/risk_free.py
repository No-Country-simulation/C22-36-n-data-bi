import yfinance as yf

def get_average_risk_free_rate(start_date="2017-11-09", end_date="2024-10-31"):
    data = yf.download("^TNX", start=start_date, end=end_date)
    average_rate = data['Close'].mean() / 100
    return average_rate