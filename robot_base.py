import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import sys
from sklearn.linear_model import LogisticRegression

try:
    # Descargar datos
    print("Descargando datos de BTC-USD...")
    data = yf.download("BTC-USD", start="2023-01-01", end="2025-01-01")
    if data.empty:
        print("No se pudieron descargar los datos.")
        sys.exit(1)

    data.dropna(inplace=True)

    # Medias móviles
    data["MA_fast"] = data["Close"].rolling(window=20).mean()
    data["MA_slow"] = data["Close"].rolling(window=50).mean()

    # Señales correctas (sin caracteres extra)
    data["Signal"] = np.where(data["MA_fast"] > data["MA_slow"], 1, -1)
    data["Return"] = data["Close"].pct_change()
    data["Strategy"] = data["Signal"].shift(1) * data["Return"]

    # Variables predictivas
    data["MA_diff"] = data["MA_fast"] - data["MA_slow"]
    data["Return_prev"] = data["Close"].pct_change().shift(1)
    data["Volatility"] = data["Close"].rolling(window=20).std()
    data.dropna(inplace=True)

    # Variable objetivo
    data["Target"] = ((data["Signal"].shift(1) * data["Return"]) > 0).astype(int)

    # Modelo de probabilidad
    X = data[["MA_diff", "Return_prev", "Volatility"]]
    y = data["Target"]
    model = LogisticRegression()
    model.fit(X, y)

    # Probabilidad de acierto
    data["Probabilidad_acierto"] = model.predict_proba(X)[:,1]

    # Resultados
    total_return = (data["Strategy"] + 1).prod() - 1
    hit_rate = (data["Signal"].shift(1) * data["Return"] > 0).sum() / len(data)
    print(f"\nRendimiento total: {total_return*100:.2f}%")
    print(f"Tasa de aciertos: {hit_rate*100:.2f}%")
    print("\nÚltimas señales con probabilidad de acierto:")
    print(data[["Signal", "Probabilidad_acierto"]].tail())

    # Gráfico
    plt.figure(figsize=(12,6))
    plt.plot(data["Close"], label="Precio BTC")
    plt.plot(data["MA_fast"], label="Media rápida (20)")
    plt.plot(data["MA_slow"], label="Media lenta (50)")
    plt.title("Estrategia cruzamiento de medias con probabilidad de acierto")
    plt.legend()
    plt.grid(True)
    plt.show(block=True)

except Exception as e:
    print(f"Ha ocurrido un error: {e}")
    sys.exit(1)

