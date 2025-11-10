from backtesting import Backtest, Strategy
import pandas as pd
import numpy as np

class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        # Indicadores SMA usando pandas rolling
        self.sma1 = self.I(lambda x: pd.Series(x).rolling(self.n1).mean(), self.data.Close)
        self.sma2 = self.I(lambda x: pd.Series(x).rolling(self.n2).mean(), self.data.Close)

    def next(self):
        if self.sma1[-2] < self.sma2[-2] and self.sma1[-1] > self.sma2[-1]:
            self.buy()
        elif self.sma1[-2] > self.sma2[-2] and self.sma1[-1] < self.sma2[-1]:
            self.sell()

# Datos simulados
dates = pd.date_range(start="2025-01-01", periods=100)
close = 100 + np.cumsum(np.random.randn(100))
data = pd.DataFrame({
    'Open': close + np.random.randn(100),
    'High': close + np.random.rand(100)*2,
    'Low': close - np.random.rand(100)*2,
    'Close': close,
    'Volume': np.random.randint(100, 1000, size=100)
}, index=dates)

# Ejecutar backtest
bt = Backtest(data, SmaCross, cash=10000, commission=.002)
stats = bt.run()
bt.plot()
print(stats)

