import cx_Oracle
from db import conectar

def editar_leitura_sensor():
    print("\n=== Editar Leitura de Sensor ===")
    try:
        id_leitura = input("ID da Leitura a Editar: ")
        novo_valor_lido = input("Novo Valor Lido: ")

        sql = "UPDATE LeituraSensor SET valor_lido = :1 WHERE id_leitura = :2"
        conn = None
        try:
            conn = conectar()
            with conn.cursor() as cursor:
                cursor.execute(sql, (novo_valor_lido, id_leitura))
                if cursor.rowcount > 0:
                    conn.commit()
                    print(f"Leitura de sensor com ID {id_leitura} atualizada com sucesso.")
                else:
                    print(f"Nenhuma leitura de sensor encontrada com o ID {id_leitura}.")
        except cx_Oracle.Error as e:
            error, = e.args
            print(f"Erro ao editar leitura de sensor: {error.message}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()
    except Exception as e:
        print(f"Erro ao processar entrada: {e}")