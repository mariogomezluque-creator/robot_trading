from binance.client import Client

API_KEY = "EYFvSAVrhOx3En7RuJBq9Hdx1qmfPBfR3sVCGHF7JVKjBobXxrdkDQ6TmVcKNqDm"
API_SECRET = "mPq7BhB53vLzPsJtmBTRrirLUtKcYYfhwaucv2EHkwSCbFskURMi83rQBrTqTnim"

client = Client(API_KEY, API_SECRET, testnet=True)

try:
    server_time = client.get_server_time()
    print("Server time:", server_time)
    info = client.get_account()
    print("✅ Conexión exitosa. Información de la cuenta:")
    print(info)
except Exception as e:
    print("❌ No se pudo obtener account info:", e)

