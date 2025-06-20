import subprocess
import webbrowser
import os
import sys
from db import executar_ddl, executar_insert, dropar_tabelas
from exibir import exibir_produtores, exibir_fazendas, exibir_fazendas_produtores, exibir_tipo_sensor, exibir_sensor, exibir_plantacao, exibir_culturas, exibir_tipo_produto, exibir_aplicacao_produto, exibir_leitura_sensor
from inserir import inserir_leitura_sensor
from editar import editar_leitura_sensor
from excluir import excluir_leitura_sensor
from simulador import insere_via_simulador, insere_via_texto
from dashboard.dashoboard import gerar_graficos
from api.api import consultar_api

def exibir_menu():
    print("\n=== Sistema ESP32 - Sensores ===")
    print("0. Reiniciar o banco de dados")
    print("1. Exibir Produtor")
    print("2. Exibir Fazenda")
    print("3. Exibir Fazenda x Produtor")
    print("4. Exibir Tipo Sensor")
    print("5. Exibir Sensor")
    print("6. Exibir Plantacao")
    print("7. Exibir Culturas")
    print("8. Exibir Tipo Produto")
    print("9. Exibir Aplicacao Produto")
    print("10. Exibir Leitura Sensor")
    print("11. Inserir Leitura Sensor")
    print("12. Editar Leitura Sensor")
    print("13. Excluir Leitura Sensor")
    print("14. Insere via simulador (Copia e Cola)")
    print("15. Insere via arquivo (Conjunto de Leituras)")
    print("16. * EXTRA - Graficos")
    print("17. * EXTRA - Consumir API")
    print("171. * EXTRA - Inserir Leitura Sensor via API")
    print("18. Scikit-learn (oracle)")
    print("181 Scikit-learn (simulado CSV)")
    print("19. Sair")


def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            dropar_tabelas()
            executar_ddl()
            executar_insert()
        elif opcao == "1":
            exibir_produtores()
        elif opcao == "2":
            exibir_fazendas()
        elif opcao == "3":
            exibir_fazendas_produtores()
        elif opcao == "4":
            exibir_tipo_sensor()
        elif opcao == "5":
            exibir_sensor()
        elif opcao == "6":
            exibir_plantacao()
        elif opcao == "7":
            exibir_culturas()
        elif opcao == "8":
            exibir_tipo_produto()
        elif opcao == "9":
            exibir_aplicacao_produto()
        elif opcao == "10":
            exibir_leitura_sensor()
        elif opcao == "11":
            inserir_leitura_sensor()
        elif opcao == "12":
            editar_leitura_sensor()
        elif opcao == "13":
            excluir_leitura_sensor()
        elif opcao == "14":
            insere_via_simulador()
        elif opcao == "15":
            insere_via_texto(False)
        elif opcao == "16":
            gerar_graficos()
        elif opcao == "17":
            consultar_api()
        elif opcao == "171":
            insere_via_simulador(True)
        elif opcao == "18":

            # Abrir o navegador e Executar o Streamlit em segundo plano
            webbrowser.open("http://localhost:8501")
            subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", "app_scikit_learn.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print("✅ Streamlit iniciado. Acesse http://localhost:8501")
        elif opcao == "181":
            caminho = os.path.join("Scikit-learn_Streamlit", "app_atualizado.py")
            
            # Abrir o navegador e Executar o Streamlit em segundo plano
            webbrowser.open("http://localhost:8502")
            subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", caminho],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print("✅ Streamlit iniciado. Acesse http://localhost:8502")
        elif opcao == "19":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n Ocorreu um erro inesperado: {e}")

