from inserir import insert_db
from datetime import datetime
from api.api import obter_temperatura

ID_SENSOR_UMIDADE = 1
ID_SENSOR_PH = 2
ID_SENSOR_FOSFORO = 3
ID_SENSOR_POTASSIO = 4
ID_SENSOR_TEMPERATURA = 5
ID_SENSOR_BOMBA = 6

def insere_via_simulador(usar_api=False):
    print("\n=== Inserir via simulador ===")
    print("Copie a linha gerada do simulador")
    print("Formato esperado: id_esp32;fosforo;potassio;pH;umidade;temperatura;irrigacao")
    print("Exemplo: 100100C40A24;f;f;4.79;34.50;19.30;t")
    linha_simulador = input("COLE AQUI: ")
    split_linha(linha_simulador, usar_api)

def insere_via_texto():
    nome_arquivo = "./files/registrosESP32.txt"
    try:
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    split_linha(linha)
        print(f"\nProcessamento do arquivo '{nome_arquivo}' concluído.")
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")

def decidir_irrigacao_api(irrigacao):
    temperatura = obter_temperatura("ORLÂNDIA", -20.7204, -47.8876)
    print(f"Temperatura obtida da API: {temperatura} °C")
    if temperatura is not None:
        if temperatura < 20:
            return 'f'
        else:
            return 't'
    else:
        print("Erro ao obter temperatura da API.")
        return irrigacao


def split_linha(linha, usar_api):
    try:
        partes = linha.split(';')
        if len(partes) in [7, 8]:
            id_esp32 = partes[0]
            fosforo = partes[1]
            potassio = partes[2]
            ph_str = partes[3]
            umidade_str = partes[4]
            temperatura = partes[5]
            irrigacao = partes[6]

            #EXTRA - Consumir API
            if usar_api:
                print(f"Irrigação atual: {irrigacao}")
                irrigacao = decidir_irrigacao_api(irrigacao)
                print(f"Irrigação Final: {irrigacao}")
            
            if fosforo == 't':
                fosforo = 1
            else:
                fosforo = 0

            if potassio == 't':
                potassio = 1
            else:
                potassio = 0

            if irrigacao == 't':
                irrigacao = 1
            else:
                irrigacao = 0

            try:
                umidade = float(umidade_str)
                ph = float(ph_str)

                if len(partes) == 8:
                    try:
                        data_hora_atual = datetime.strptime(partes[7], '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        print("Formato da data inválido. Usando data e hora atuais do servidor.")
                        data_hora_atual = datetime.now()
                else:
                    data_hora_atual = datetime.now()

                data_hora_str = data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')

                print(f"\nDados recuperados:")
                print(f"Umidade: {umidade}")
                print(f"pH: {ph}")
                print(f"Data e Hora: {data_hora_str}")
                print(f"Fósforo: {fosforo}")
                print(f"Potássio: {potassio}")
                print(f"Temperatura: {temperatura}")
                print(f"Irrigação: {irrigacao}")

                insert_db(ID_SENSOR_UMIDADE, data_hora_str, umidade)
                insert_db(ID_SENSOR_PH, data_hora_str, ph)
                insert_db(ID_SENSOR_FOSFORO, data_hora_str, fosforo)
                insert_db(ID_SENSOR_POTASSIO, data_hora_str, potassio)
                insert_db(ID_SENSOR_TEMPERATURA, data_hora_str, temperatura)
                insert_db(ID_SENSOR_BOMBA, data_hora_str, irrigacao)

            except ValueError:
                print("Erro: pH e umidade devem ser valores numéricos.")
        else:
            print("Erro: Formato da linha inválido. Esperados 7 ou 8 campos separados por ';'.")
    except Exception as e:
        print(f"Ocorreu um erro ao processar a linha: {e}")
