import oracledb
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.json")
CAMINHO_SCRIPT = os.path.join(BASE_DIR, "scripts", "script.sql")
CAMINHO_SCRIPT_INSERT = os.path.join(BASE_DIR, "scripts", "insert.sql")

# Carrega a configuração
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

ORACLE_USER = config["ORACLE_USER"]
ORACLE_PASSWORD = config["ORACLE_PASSWORD"]
ORACLE_DSN = config["ORACLE_DSN"]

def conectar():
    return oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)

def executar_ddl():
    print("\n=== Verificando base de dados ===")

    if not os.path.exists(CAMINHO_SCRIPT):
        print(f"Script de criação de tabelas não encontrado em '{CAMINHO_SCRIPT}'.")
        return

    with open(CAMINHO_SCRIPT, "r", encoding="utf-8") as f:
        ddl = f.read()

    comandos = [cmd.strip() for cmd in ddl.split(";") if cmd.strip()]

    with conectar() as conn:
        with conn.cursor() as cursor:
            for comando in comandos:
                try:
                    cursor.execute(comando)
                except oracledb.DatabaseError as e:
                    msg = str(e)
                    if "ORA-00955" in msg:
                        print("Objeto já existe. Ignorando criação.")
                        continue
                    elif "ORA-02275" in msg:
                        print("FK já existente. Ignorando.")
                        continue
                    else:
                        print(f"\nErro ao executar comando:\n{comando}\n→ {msg}")
                        raise
        conn.commit()
        print("Script DDL executado (ou comandos ignorados onde já existiam).")

def executar_insert():
    print("\n=== Verificando necessidade de inserir dados ===")

    if not os.path.exists(CAMINHO_SCRIPT_INSERT):
        print(f"Script de inserção de dados não encontrado em '{CAMINHO_SCRIPT_INSERT}'.")
        return

    with open(CAMINHO_SCRIPT_INSERT, "r", encoding="utf-8") as f:
        inserts = f.read()

    comandos_insert = [cmd.strip() for cmd in inserts.split(";") if cmd.strip()]

    with conectar() as conn:
        with conn.cursor() as cursor:
            for comando in comandos_insert:
                try:
                    cursor.execute(comando)
                    print(f"Comando INSERT executado com sucesso:\n{comando}")
                except oracledb.DatabaseError as e:
                    msg = str(e)
                    print(f"\nErro ao executar comando INSERT:\n{comando}\n→ {msg}")
                    # Decidi não interromper a execução em caso de erro no INSERT,
                    # para tentar executar os próximos comandos.
                    # Se for crucial que todos os inserts funcionem, remova o 'continue'
                    # e deixe o 'raise' para interromper.
                    continue
            conn.commit()
            print("Script de inserção de dados executado.")