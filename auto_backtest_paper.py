from backtesting import Backtest, Strategy
import pandas as pd
import yfinance as yf

class SmaCross(Strategy):
    # Parámetros de la estrategia
    n1 = 10
    n2 = 20

    def init(self):
        # SMA usando pandas rolling
        self.sma1 = self.I(lambda x: pd.Series(x).rolling(self.n1).mean(), self.data.Close)
        self.sma2 = self.I(lambda x: pd.Series(x).rolling(self.n2).mean(), self.data.Close)

    def next(self):
        # Señales de compra/venta
        if self.sma1[-2] < self.sma2[-2] and self.sma1[-1] > self.sma2[-1]:
            self.buy()
        elif self.sma1[-2] > self.sma2[-2] and self.sma1[-1] < self.sma2[-1]:
            self.sell()

def run_backtest(ticker='AAPL', start='2020-01-01'):
    print(f"Descargando datos de {ticker}...")
    data = yf.download(ticker, start=start)
    
    # Evitar MultiIndex y columnas extra
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    data.index = pd.to_datetime(data.index)
    
    print("Ejecutando backtest...")
    bt = Backtest(data, SmaCross, cash=10000, commission=.002)
    stats = bt.run()
    bt.plot()
    print(stats)

if __name__ == "__main__":
    # Cambia el ticker aquí si quieres otro activo
    run_backtest(ticker='AAPL', start='2020-01-01')

