from backtesting import Backtest, Strategy
import pandas as pd
import numpy as np
import yfinance as yf

class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        # SMA usando pandas rolling, compatible con Backtesting.py
        self.sma1 = self.I(lambda x: pd.Series(x).rolling(self.n1).mean(), self.data.Close)
        self.sma2 = self.I(lambda x: pd.Series(x).rolling(self.n2).mean(), self.data.Close)

    def next(self):
        if self.sma1[-2] < self.sma2[-2] and self.sma1[-1] > self.sma2[-1]:
            self.buy()
        elif self.sma1[-2] > self.sma2[-2] and self.sma1[-1] < self.sma2[-1]:
            self.sell()

# Descargar datos reales con yfinance
ticker = 'AAPL'  # puedes cambiarlo por otro activo
data = yf.download(ticker, start="2020-01-01", end=None)

# Asegurarse que tenga las columnas correctas
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

# Ejecutar backtest
bt = Backtest(data, SmaCross, cash=10000, commission=.002)
stats = bt.run()
bt.plot()
print(stats)


