import matplotlib.pyplot as plt
import pandas as pd
from db import conectar
import os

def gerar_graficos():
    conn = conectar()
    cursor = conn.cursor()

    query = """
    SELECT id_sensor, data_hora, valor_lido
    FROM LeituraSensor
    WHERE EXTRACT(YEAR FROM data_hora) = 2025
    """
    cursor.execute(query)
    colunas = [desc[0].lower() for desc in cursor.description]
    dados = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(dados, columns=colunas)
    df["data_hora"] = pd.to_datetime(df["data_hora"])
    df["mes"] = df["data_hora"].dt.month

    # Define caminho de saída
    pasta_saida = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "files"))
    os.makedirs(pasta_saida, exist_ok=True)

    # === 1. Bomba de Irrigação ===
    df_bomba = df[df["id_sensor"] == 6]
    bomba_por_mes = df_bomba.groupby("mes").size()
    media_uso = bomba_por_mes.mean()

    plt.figure(figsize=(10, 5))
    bomba_por_mes.plot(kind="line", marker="o", color="blue", label="Acionamentos")
    plt.axhline(media_uso, color="red", linestyle="--", label=f"Média ({media_uso:.0f})")
    plt.title("Uso da Bomba de Irrigação por Mês")
    plt.xlabel("Mês")
    plt.ylabel("Quantidade de Acionamentos")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_saida, "grafico_bomba_trend.png"))
    plt.close()

    # === 2. Temperatura Média ===
    df_temp = df[df["id_sensor"] == 5]
    temp_por_mes = df_temp.groupby("mes")["valor_lido"].mean()

    plt.figure(figsize=(10, 5))
    temp_por_mes.plot(kind="line", marker="o", color="orange", label="Temperatura Média")
    plt.axhspan(20, 28, color="green", alpha=0.2, label="Faixa Ideal (20–28°C)")
    plt.title("Temperatura Média Mensal vs Faixa Ideal")
    plt.xlabel("Mês")
    plt.ylabel("Temperatura (°C)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_saida, "grafico_temperatura_ideal.png"))
    plt.close()

    # === 3. Potássio Detectado ===
    df_k = df[(df["id_sensor"] == 4) & (df["valor_lido"] == 1)]
    potassio_detectado = df_k.groupby("mes").size()

    plt.figure(figsize=(10, 5))
    potassio_detectado.plot(kind="bar", color="purple")
    plt.title("Quantidade de Detecções de Potássio por Mês")
    plt.xlabel("Mês")
    plt.ylabel("Quantidade de Leituras com Potássio")
    plt.tight_layout()
    plt.grid(axis="y")
    plt.savefig(os.path.join(pasta_saida, "grafico_potassio_detectado.png"))
    plt.close()

    # === 4. Faixa de pH do Solo ===
    df_ph = df[df["id_sensor"] == 2]
    ph_min = df_ph.groupby("mes")["valor_lido"].min()
    ph_max = df_ph.groupby("mes")["valor_lido"].max()

    plt.figure(figsize=(10, 5))
    plt.plot(ph_min.index, ph_min.values, marker="v", label="pH Mínimo", color="brown")
    plt.plot(ph_max.index, ph_max.values, marker="^", label="pH Máximo", color="blue")
    plt.axhspan(6.0, 7.0, color="green", alpha=0.2, label="Faixa Ideal (6.0–7.0)")
    plt.title("Faixa de pH do Solo por Mês")
    plt.xlabel("Mês")
    plt.ylabel("pH")
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.savefig(os.path.join(pasta_saida, "grafico_ph_zona.png"))
    plt.close()

    print(f"Gráficos gerados e salvos em: {pasta_saida}")
