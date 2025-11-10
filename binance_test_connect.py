import os
from binance.client import Client

# Leer las claves desde variables de entorno
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

if not api_key or not api_secret:
    raise SystemExit("No se encuentran las variables de entorno BINANCE_API_KEY / BINANCE_API_SECRET")

# Conexión al Testnet
client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binance.vision/api'

# Obtener tiempo del servidor
print("Server time:", client.get_server_time())

# Obtener un ejemplo de saldo de la cuenta
try:
    acct = client.get_account()
    print("Saldo (ejemplo, primeras 5 monedas):", acct.get("balances", [])[:5])
except Exception as e:
    print("No se pudo obtener account info:", e)

