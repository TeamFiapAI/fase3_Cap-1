import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

class ModeloIrrigacao:
    def __init__(self, nome_csv="mock.csv", nome_modelo="modelo.pkl", nome_scaler="scaler.pkl"):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        raiz = os.path.abspath(os.path.join(self.base_dir, ".."))

        self.caminho_csv = os.path.join(raiz, "Scikit-learn_Streamlit", nome_csv)
        self.caminho_modelo = os.path.join(raiz, "Scikit-learn_Streamlit", nome_modelo)
        self.caminho_scaler = os.path.join(raiz, "Scikit-learn_Streamlit", nome_scaler)

    def treinar(self):
        if not os.path.exists(self.caminho_csv):
            raise FileNotFoundError(f"❌ Arquivo CSV não encontrado: {self.caminho_csv}")

        df = pd.read_csv(self.caminho_csv)

        features = ['temperature', 'humidity', 'rainfall']
        x = df[features]
        y = df['Irrigation'] if 'Irrigation' in df.columns else (df['humidity'] < 30).astype(int)

        scaler = StandardScaler()
        scaler.fit(x)
        x_scaled = scaler.transform(x)

        modelo = RandomForestClassifier()
        modelo.fit(x_scaled, y)

        joblib.dump(modelo, self.caminho_modelo)
        joblib.dump(scaler, self.caminho_scaler)

        print("✅ Modelo treinado e salvo com sucesso.")
