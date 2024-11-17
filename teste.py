import yfinance as yf

stock = yf.Ticker("MGLU3.SA")
historical_data = stock.history(period="5d")  # Busca os últimos 5 dias de dados
print(historical_data)


# Pega o nome da empresa e o preço atual
stock_info = stock.info
print("Nome da empresa:", stock_info.get("longName"))
print("Preço atual:", stock_info.get("regularMarketPrice"))
