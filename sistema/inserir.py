import cx_Oracle
from db import conectar

def inserir_leitura_sensor():
    print("\n=== Inserir Leitura de Sensor ===")

    id_sensor = input("ID do Sensor: ")
    data_hora_str = input("Data e Hora (YYYY-MM-DD HH24:MI:SS): ")
    valor_lido = input("Valor Lido: ")
    insert_db(id_sensor, data_hora_str, valor_lido)

def insert_db(id_sensor, data_hora_str, valor_lido):
    try:
        sql = "INSERT INTO LeituraSensor (id_sensor, data_hora, valor_lido) VALUES (:1, TO_TIMESTAMP(:2, 'YYYY-MM-DD HH24:MI:SS'), :3)"
        conn = None
        try:
            conn = conectar()
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_sensor, data_hora_str, valor_lido))
                conn.commit()
                print("Leitura de sensor inserida com sucesso.")
        except cx_Oracle.Error as e:
            error, = e.args
            print(f"Erro ao inserir leitura de sensor: {error.message}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()
    except Exception as e:
        print(f"Erro ao processar entrada: {e}")