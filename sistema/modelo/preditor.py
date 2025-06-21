import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_MODELO = os.path.join(BASE_DIR, "modelo.pkl")
CAMINHO_SCALER = os.path.join(BASE_DIR, "scaler.pkl")

modelo = joblib.load(CAMINHO_MODELO)
scaler = joblib.load(CAMINHO_SCALER)

FEATURES = ["temperature", "humidity", "rainfall"]

def prever_irrigacao(dados: dict) -> int:
    FEATURES = ["temperature", "humidity", "rainfall"]

    df = pd.DataFrame([[
        dados["temperature"],
        dados["humidity"],
        dados.get("rainfall", 0.0)
    ]], columns=FEATURES)

    scaled = scaler.transform(df)
    resultado = modelo.predict(scaled)
    return int(resultado[0])

