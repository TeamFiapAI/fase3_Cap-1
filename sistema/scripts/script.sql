-- Tabela: Produtor
CREATE TABLE Produtor (
    id_produtor NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(100),
    email VARCHAR2(100),
    telefone VARCHAR2(20)
);

-- Tabela: Fazenda
CREATE TABLE Fazenda (
    id_fazenda NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(100),
    localizacao VARCHAR2(100),
    tamanho_ha NUMBER(10,2)
);

-- Tabela Associativa: ProdutorFazenda
CREATE TABLE ProdutorFazenda (
    id_produtor NUMBER,
    id_fazenda NUMBER,
    data_inicio DATE,
    data_fim DATE,
    PRIMARY KEY (id_produtor, id_fazenda),
    FOREIGN KEY (id_produtor) REFERENCES Produtor(id_produtor),
    FOREIGN KEY (id_fazenda) REFERENCES Fazenda(id_fazenda)
);

-- Tabela: Cultura
CREATE TABLE Cultura (
    id_cultura NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
    nome_cultura VARCHAR2(100),
    descricao CLOB
);

-- Tabela: Plantacao
CREATE TABLE Plantacao (
    id_plantacao NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
    id_fazenda NUMBER,
    id_cultura NUMBER,
    data_inicio DATE,
    data_fim DATE,
    FOREIGN KEY (id_fazenda) REFERENCES Fazenda(id_fazenda),
    FOREIGN KEY (id_cultura) REFERENCES Cultura(id_cultura)
);

-- Tabela: TipoSensor
CREATE TABLE TipoSensor (
    id_tipo_sensor NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
    nome_tipo VARCHAR2(50),
    unidade_medida VARCHAR2(20)
);

-- Tabela: Sensor
CREATE TABLE Sensor (
    id_sensor NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
    id_tipo_sensor NUMBER,
    id_plantacao NUMBER,
    modelo VARCHAR2(50),
    FOREIGN KEY (id_tipo_sensor) REFERENCES TipoSensor(id_tipo_sensor),
    FOREIGN KEY (id_plantacao) REFERENCES Plantacao(id_plantacao)
);

-- Tabela: LeituraSensor
CREATE TABLE LeituraSensor (
    id_leitura NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_sensor  NUMBER NOT NULL,
    data_hora  TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    valor_lido NUMBER(10,2) NOT NULL,
    CONSTRAINT fk_leitura_sensor FOREIGN KEY (id_sensor)
        REFERENCES Sensor(id_sensor)
);

-- Tabela: TipoProduto
CREATE TABLE TipoProduto (
    id_tipo_produto NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
    nome_produto VARCHAR2(100),
    descricao VARCHAR2(200)
);

-- Tabela: AplicacaoProduto
CREATE TABLE AplicacaoProduto (
    id_aplicacao NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
    id_plantacao NUMBER,
    id_tipo_produto NUMBER,
    data_hora TIMESTAMP,
    quantidade NUMBER(10,2),
    unidade VARCHAR2(20),
    FOREIGN KEY (id_plantacao) REFERENCES Plantacao(id_plantacao),
    FOREIGN KEY (id_tipo_produto) REFERENCES TipoProduto(id_tipo_produto)
);