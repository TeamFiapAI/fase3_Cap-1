
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Configuração da página
st.set_page_config(page_title="🌾 Sistema Inteligente de Irrigação", layout="wide")

# Carregar dados do CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_CSV = os.path.join(BASE_DIR, "mock.csv")

df = pd.read_csv(CAMINHO_CSV)


# Treinar modelo de exemplo (Random Forest)
features = ['temperature', 'humidity', 'rainfall', 'N', 'P', 'K']
x = df[features]
y = df['Irrigation'] if 'Irrigation' in df.columns else (df['humidity'] < 30).astype(int)  # Supondo que não tenha target, cria um

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

modelo = RandomForestClassifier()
modelo.fit(x_scaled, y)

# Salvar modelo e scaler (se quiser usar depois)
joblib.dump(modelo, "modelo_irrigacao.pkl")
joblib.dump(scaler, "scaler_irrigacao.pkl")

st.title("🌱 Sistema Inteligente de Irrigação")

# Criar abas
aba = st.tabs(["🔍 Previsão", "📊 Gráficos", "💡 Insights"])

with aba[0]:
    st.header("🔍 Previsão de Irrigação")
    modo_entrada = st.radio("Modo de entrada:", ["Automático (Simulado)", "Manual"])

    if modo_entrada == "Automático (Simulado)":
        temperature = random.uniform(20, 40)
        humidity = random.uniform(10, 60)
        rainfall = random.uniform(0, 50)
        N = random.randint(0, 150)
        P = random.choice([0, 1])
        K = random.choice([0, 1])
    else:
        temperature = st.number_input("Temperatura (°C)", -10.0, 60.0, 30.0)
        humidity = st.number_input("Umidade (%)", 0.0, 100.0, 35.0)
        rainfall = st.number_input("Chuva (mm)", 0.0, 500.0, 10.0)
        N = st.number_input("Nitrogênio (N)", 0, 200, 70)
        P = st.selectbox("Fósforo (P)", [0, 1], format_func=lambda x: "Presente" if x else "Ausente")
        K = st.selectbox("Potássio (K)", [0, 1], format_func=lambda x: "Presente" if x else "Ausente")

    if st.button("🔎 Verificar Necessidade de Irrigação"):
        entrada = pd.DataFrame([[temperature, humidity, rainfall, N, P, K]], columns=features)
        entrada_scaled = scaler.transform(entrada)
        resultado = modelo.predict(entrada_scaled)

        if resultado[0] == 1:
            st.error("⚠️ Necessário irrigar agora.")
        else:
            st.success("✅ Irrigação não necessária no momento.")

        st.write("**Dados utilizados:**")
        st.write(entrada)

with aba[1]:
    st.header("📊 Análise Gráfica da Umidade e Nutrientes")

    # Gráfico de variação da umidade
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x=df.index, y='humidity', ax=ax)
    ax.set_title("Variação da Umidade do Solo")
    ax.set_xlabel("Índice da Amostra")
    ax.set_ylabel("Umidade (%)")
    st.pyplot(fig)

    # Gráficos de nutrientes
    fig, axs = plt.subplots(1, 3, figsize=(15, 4))
    sns.histplot(df['N'], ax=axs[0], kde=True, color='green')
    axs[0].set_title("Distribuição de Nitrogênio (N)")

    sns.countplot(x='P', hue='P', data=df, ax=axs[1], palette='muted', legend=False)
    axs[1].set_title("Fósforo (P) - Presença")

    sns.countplot(x='K', hue='K', data=df, ax=axs[2], palette='pastel', legend=False)
    axs[2].set_title("Potássio (K) - Presença")

    st.pyplot(fig)

with aba[2]:
    st.header("💡 Insights do Modelo de Machine Learning")
    importances = modelo.feature_importances_
    feature_imp = pd.DataFrame({'Feature': features, 'Importância': importances})
    feature_imp = feature_imp.sort_values(by="Importância", ascending=False)

    st.subheader("Importância das Variáveis na Decisão de Irrigação:")
    st.bar_chart(feature_imp.set_index('Feature'))

    st.markdown("### Principais Insights:")
    for idx, row in feature_imp.iterrows():
        if row['Importância'] > 0.2:
            st.markdown(f"- 🚩 **{row['Feature']}** tem grande influência na decisão de irrigação.")
        else:
            st.markdown(f"- ✅ **{row['Feature']}** tem influência menor.")

    st.info("⚙️ Modelo usado: Random Forest Classifier treinado com os dados agrícolas.")
