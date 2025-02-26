CREATE TABLE CNAE (
    code VARCHAR(10),        -- Code for the category
    description VARCHAR(255) -- Description of the category
);

CREATE TABLE QUALS (
    code VARCHAR(2) PRIMARY KEY,
    description VARCHAR(255)
);

CREATE TABLE PAIS (
    code VARCHAR(3) PRIMARY KEY,
    description VARCHAR(255)
);

CREATE TABLE NATJU (
    code VARCHAR(4) PRIMARY KEY,
    description VARCHAR(255)
);

CREATE TABLE MUNIC (
    code VARCHAR(4) PRIMARY KEY,
    description VARCHAR(255)
);

CREATE TABLE MOTI (
    code VARCHAR(2),         -- Code for the reason
    description VARCHAR(255) -- Description of the reason
);

CREATE TABLE empresas (
    id INT PRIMARY KEY,
    nome VARCHAR(255),
    code1 INT,
    code2 INT,
    valor NUMERIC(15,2),
    code3 INT,
    empty VARCHAR(255) NULL
);
CREATE TABLE simples (
    cnpj_basico VARCHAR(8),
    opcao_pelo_simples VARCHAR(1),
    data_opcao_simples DATE,
    data_exclusao_simples DATE,
    opcao_mei VARCHAR(1),
    data_opcao_mei DATE,
    data_exclusao_mei DATE
);
CREATE TABLE socios (
    CNPJ TEXT,
    Tipo_Socio INTEGER,
    Nome_Socio TEXT,
    Identificacao_Socio TEXT,
    Qualificacao_Socio INTEGER,
    Data_Entrada_Sociedade INTEGER,
    Pais TEXT,
    Representante_Legal TEXT,
    Nome_Representante TEXT,
    Faixa_Etaria TEXT,
    Cpf_Representante TEXT
);
CREATE TABLE estabele (
    cnpj_basico VARCHAR(8),
    cnpj_ordem VARCHAR(4),
    cnpj_dv VARCHAR(2),
    identificador_matriz_filial INT,
    nome_fantasia VARCHAR(255),
    codigo_situacao_cadastral INT,
    data_inicio_atividade DATE,
    cnae_fiscal_principal VARCHAR(2),
    cnae_fiscal_secundaria TEXT,
    tipo_logradouro VARCHAR(255),
    logradouro VARCHAR(255),
    numero VARCHAR(255),
    complemento VARCHAR(255),
    bairro VARCHAR(255),
    cep VARCHAR(8),
    uf VARCHAR(2),
    codigo_municipio INT,
    ddd_telefone_1 VARCHAR(2),
    telefone_1 VARCHAR(255),
    ddd_telefone_2 VARCHAR(2),
    telefone_2 VARCHAR(255),
    ddd_fax VARCHAR(2),
    fax VARCHAR(255),
    email VARCHAR(255),
    situacao_especial VARCHAR(255)
);
