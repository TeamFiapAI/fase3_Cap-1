import cx_Oracle
from db import conectar

def excluir_leitura_sensor():
    print("\n=== Excluir Leitura de Sensor ===")
    try:
        id_leitura = input("ID da Leitura a Excluir: ")

        sql = "DELETE FROM LeituraSensor WHERE id_leitura = :1"
        conn = None
        try:
            conn = conectar()
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_leitura,))
                if cursor.rowcount > 0:
                    conn.commit()
                    print(f"Leitura de sensor com ID {id_leitura} excluída com sucesso.")
                else:
                    print(f"Nenhuma leitura de sensor encontrada com o ID {id_leitura}.")
        except cx_Oracle.Error as e:
            error, = e.args
            print(f"Erro ao excluir leitura de sensor: {error.message}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()
    except Exception as e:
        print(f"Erro ao processar entrada: {e}")