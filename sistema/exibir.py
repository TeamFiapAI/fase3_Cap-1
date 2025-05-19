from db import buscar_todos

def exibir_registros(registros, nome_tabela, nomes_colunas):
    if not registros:
        print(f"\nNenhum registro encontrado em {nome_tabela}.")
        return

    print(f"\n=== Lista de {nome_tabela} ===")
    for idx, registro in enumerate(registros, start=1):
        output = f"{idx}. "
        for i, valor in enumerate(registro):
            output += f"{nomes_colunas[i]}: {valor}"
            if i < len(registro) - 1:
                output += ", "
        print(output)
    return registros

def exibir_produtores():
    colunas = "id_produtor, nome, email, telefone"
    nomes_colunas = ["ID", "Nome", "Email", "Telefone"]
    produtores = buscar_todos("Produtor", colunas, "nome")
    exibir_registros(produtores, "Produtores", nomes_colunas)

def exibir_fazendas():
    colunas = "id_fazenda, nome, localizacao, tamanho_ha"
    nomes_colunas = ["ID", "Nome", "Localização", "Tamanho (ha)"]
    fazendas = buscar_todos("Fazenda", colunas, "nome")
    exibir_registros(fazendas, "Fazendas", nomes_colunas)

def exibir_fazendas_produtores():
    sql = """
    SELECT pf.id_produtor, p.nome AS nome_produtor, pf.id_fazenda, f.nome AS nome_fazenda, pf.data_inicio, pf.data_fim
    FROM ProdutorFazenda pf
    JOIN Produtor p ON pf.id_produtor = p.id_produtor
    JOIN Fazenda f ON pf.id_fazenda = f.id_fazenda
    ORDER BY p.nome, f.nome
    """
    registros = buscar_todos(sql_query=sql)
    if not registros:
        print("\nNenhuma relação entre Produtor e Fazenda encontrada.")
        return
    print("\n=== Relação Produtor x Fazenda ===")
    for idx, (id_produtor, nome_produtor, id_fazenda, nome_fazenda, data_inicio, data_fim) in enumerate(registros, start=1):
        print(f"{idx}. Produtor (ID: {id_produtor}): {nome_produtor}, Fazenda (ID: {id_fazenda}): {nome_fazenda}, Início: {data_inicio}, Fim: {data_fim}")

def exibir_tipo_sensor():
    colunas = "id_tipo_sensor, nome_tipo, unidade_medida"
    nomes_colunas = ["ID", "Nome Tipo", "Unidade Medida"]
    tipos_sensor = buscar_todos("TipoSensor", colunas, "nome_tipo")
    exibir_registros(tipos_sensor, "Tipos de Sensor", nomes_colunas)

def exibir_sensor():
    sql = """
    SELECT s.id_sensor, ts.nome_tipo AS tipo_sensor, p.id_plantacao AS id_plantacao, s.modelo
    FROM Sensor s
    JOIN TipoSensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
    JOIN Plantacao p ON s.id_plantacao = p.id_plantacao
    ORDER BY s.id_sensor
    """
    registros = buscar_todos(sql_query=sql)
    if not registros:
        print("\nNenhum sensor cadastrado.")
        return
    print("\n=== Lista de Sensores ===")
    for idx, (id_sensor, tipo_sensor, id_plantacao, modelo) in enumerate(registros, start=1):
        print(f"{idx}. ID: {id_sensor}, Tipo: {tipo_sensor}, Plantacao ID: {id_plantacao}, Modelo: {modelo}")

def exibir_plantacao():
    sql = """
    SELECT pl.id_plantacao, f.nome AS nome_fazenda, c.nome_cultura, pl.data_inicio, pl.data_fim
    FROM Plantacao pl
    JOIN Fazenda f ON pl.id_fazenda = f.id_fazenda
    JOIN Cultura c ON pl.id_cultura = c.id_cultura
    ORDER BY pl.id_plantacao
    """
    registros = buscar_todos(sql_query=sql)
    if not registros:
        print("\nNenhuma plantação cadastrada.")
        return
    print("\n=== Lista de Plantações ===")
    for idx, (id_plantacao, nome_fazenda, nome_cultura, data_inicio, data_fim) in enumerate(registros, start=1):
        print(f"{idx}. ID: {id_plantacao}, Fazenda: {nome_fazenda}, Cultura: {nome_cultura}, Início: {data_inicio}, Fim: {data_fim}")

def exibir_culturas():
    colunas = "id_cultura, nome_cultura, descricao"
    nomes_colunas = ["ID", "Nome", "Descrição"]
    culturas = buscar_todos("Cultura", colunas, "nome_cultura")
    exibir_registros(culturas, "Culturas", nomes_colunas)

def exibir_tipo_produto():
    colunas = "id_tipo_produto, nome_produto, descricao"
    nomes_colunas = ["ID", "Nome", "Descrição"]
    tipos_produto = buscar_todos("TipoProduto", colunas, "nome_produto")
    exibir_registros(tipos_produto, "Tipos de Produto", nomes_colunas)

def exibir_aplicacao_produto():
    sql = """
    SELECT ap.id_aplicacao, p.id_plantacao AS id_plantacao, tp.nome_produto AS tipo_produto, ap.data_hora, ap.quantidade, ap.unidade
    FROM AplicacaoProduto ap
    JOIN Plantacao p ON ap.id_plantacao = p.id_plantacao
    JOIN TipoProduto tp ON ap.id_tipo_produto = tp.id_tipo_produto
    ORDER BY ap.id_aplicacao
    """
    registros = buscar_todos(sql_query=sql)
    if not registros:
        print("\nNenhuma aplicação de produto registrada.")
        return
    print("\n=== Lista de Aplicações de Produto ===")
    for idx, (id_aplicacao, id_plantacao, tipo_produto, data_hora, quantidade, unidade) in enumerate(registros, start=1):
        print(f"{idx}. ID: {id_aplicacao}, Plantacao ID: {id_plantacao}, Produto: {tipo_produto}, Data/Hora: {data_hora}, Quantidade: {quantidade}, Unidade: {unidade}")

def exibir_leitura_sensor():
    sql = """
    SELECT ls.id_leitura, s.id_sensor AS id_sensor, ts.nome_tipo AS tipo_sensor, ls.data_hora, ls.valor_lido
    FROM LeituraSensor ls
    JOIN Sensor s ON ls.id_sensor = s.id_sensor
    JOIN TipoSensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
    ORDER BY ls.data_hora DESC
    """
    registros = buscar_todos(sql_query=sql)
    if not registros:
        print("\nNenhuma leitura de sensor registrada.")
        return
    print("\n=== Lista de Leituras de Sensor ===")
    for idx, (id_leitura, id_sensor, tipo_sensor, data_hora, valor_lido) in enumerate(registros, start=1):
        print(f"{idx}. ID Leitura: {id_leitura}, Sensor ID: {id_sensor} ({tipo_sensor}), Data/Hora: {data_hora}, Valor: {valor_lido}")