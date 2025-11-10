# -*- coding: utf-8 -*-
from binance.client import Client

# Tus claves reales aquí
API_KEY ="4KfnZwvUo1TF8dD1CkCDĐrLLjQpLL0bPqSUxHuy7473VOpMKKHQj FHwKUI2r9CsD"
API_SECRET = "mq5GAov6wov8Dzm05YofWzdxZt4b5jprg74lpF87bgRZyMoEGULbfvXBWcZgSyyl"
client = Client(API_KEY, API_SECRET, testnet=True)  # testnet=True para usar Binance Testnet

try:
    info = client.get_account()
    print("Conexión exitosa. Información de cuenta:")
    print(info)
except Exception as e:
    print("Error al conectar con Binance:")
    print(e)

