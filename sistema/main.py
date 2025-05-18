from db import executar_ddl


def exibir_menu():
    print("\n=== Sistema Hortifruti Colaborativo ===")
    print("1. Exibir Produtor")
    print("2. Exibir Fazendas")
    print("3. Exibir Fazendas x Produtores")
    print("4. Excluir produtor")
    print("5. Exibir Culturas")
    print("6. Exibir Plantacoes")
    print("7. Exibir Tipo Sensor")
    print("8. Exibir Sensor")
    print("9. Exibir Tipo Produto")
    print("10. Exibir Aplicacao Produto")
    print("11. Inserir Leitura Sensor")
    print("12. Editar Leitura Sensor")
    print("13. Exibir Leitura Sensor")
    print("14. Excluir Leitura Sensor")
    print("15. Sair")


def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
        elif opcao == "2":
        elif opcao == "3":
        elif opcao == "4":
        elif opcao == "5":
        elif opcao == "6":
        elif opcao == "7":
        elif opcao == "8":
        elif opcao == "9":
        elif opcao == "10":
        elif opcao == "11":
        elif opcao == "12":
        elif opcao == "13":
        elif opcao == "14":
        elif opcao == "15":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        executar_ddl()
        main()
    except Exception as e:
        print(f"\n Ocorreu um erro inesperado: {e}")