import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from db import buscar_todos

def scikit_learn():
    st.set_page_config(page_title="📊 Análise com Scikit-learn", layout="wide")
    st.title("📊 Submenu: Análise de Sensores com Scikit-Learn e Oracle")

    # SQL da análise
    query = """
        SELECT
            Leitura.data_hora,
            Cultura.Nome_Cultura,
            Tipo.Nome_Tipo,
            Leitura.valor_lido
        FROM 
            LeituraSensor Leitura
        LEFT JOIN Sensor Sensor ON Sensor.id_sensor = Leitura.id_sensor
        LEFT JOIN TipoSensor Tipo ON Sensor.id_tipo_sensor = Tipo.id_tipo_sensor
        LEFT JOIN Plantacao Plantacao ON Sensor.id_Plantacao = Plantacao.id_plantacao
        LEFT JOIN Cultura Cultura ON Plantacao.id_cultura = Cultura.id_cultura
    """

    # Buscar dados usando função centralizada
    registros = buscar_todos(sql_query=query)

    if not registros:
        st.error("Nenhum dado foi retornado do banco.")
        return

    # Criar DataFrame
    df = pd.DataFrame(registros, columns=["data_hora", "NOME_CULTURA", "NOME_TIPO", "valor_lido"])

    # Conversões e tratamento
    df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
    df['valor_lido'] = pd.to_numeric(df['valor_lido'].astype(str).str.replace(',', '.'), errors='coerce')

    # Filtros
    with st.sidebar:
        culturas = st.multiselect("🌾 Filtrar por Cultura", sorted(df['NOME_CULTURA'].dropna().unique()))
        sensores = st.multiselect("📟 Filtrar por Tipo de Sensor", sorted(df['NOME_TIPO'].dropna().unique()))
        datas = st.date_input("📅 Intervalo de Datas", [])

    df_filtrado = df.copy()

    if culturas:
        df_filtrado = df_filtrado[df_filtrado['NOME_CULTURA'].isin(culturas)]

    if sensores:
        df_filtrado = df_filtrado[df_filtrado['NOME_TIPO'].isin(sensores)]

    if len(datas) == 2:
        inicio, fim = pd.to_datetime(datas[0]), pd.to_datetime(datas[1])
        df_filtrado = df_filtrado[(df_filtrado['data_hora'] >= inicio) & (df_filtrado['data_hora'] <= fim)]

    st.subheader("Dados Filtrados")
    st.dataframe(df_filtrado.sort_values("data_hora", ascending=False).head(100))

    st.subheader("Gráficos por Tipo de Sensor")

    for sensor in df_filtrado['NOME_TIPO'].dropna().unique():
        dados_sensor = df_filtrado[df_filtrado['NOME_TIPO'] == sensor]
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=dados_sensor, x='data_hora', y='valor_lido', hue='NOME_CULTURA', marker='o', ax=ax)
        ax.set_title(f"Sensor: {sensor}")
        ax.set_xlabel("Data")
        ax.set_ylabel("Valor Lido")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    st.success("Fim da análise com dados do Oracle.")