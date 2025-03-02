-- Tabela de logs de importação
CREATE TABLE IF NOT EXISTS import_log (
    id SERIAL ,
    chunk_id INT NOT NULL,
    table_name VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para os arquivos .CNAECSV
CREATE TABLE IF NOT EXISTS cnae (
    codigo VARCHAR(15) ,
    descricao VARCHAR(255)
);

-- Tabela para os arquivos .MOTICSV
CREATE TABLE IF NOT EXISTS motivo (
    codigo VARCHAR(15),
    descricao VARCHAR(255)
);

-- Tabela para os arquivos .MUNICCSV
CREATE TABLE IF NOT EXISTS municipio (
    codigo VARCHAR(15) ,
    descricao VARCHAR(255)
);

-- Tabela para os arquivos .NATJUCSV
CREATE TABLE IF NOT EXISTS natureza (
    codigo VARCHAR(15) ,
    descricao VARCHAR(255)
);

-- Tabela para os arquivos .QUALSCSV
CREATE TABLE IF NOT EXISTS qualificacao (
    codigo VARCHAR(15) ,
    descricao VARCHAR(255)
);

-- Tabela para os arquivos .PAISCSV
CREATE TABLE IF NOT EXISTS pais (
    codigo VARCHAR(15) ,
    descricao VARCHAR(255)
);

-- Tabela para os arquivos .ESTABELE
CREATE TABLE IF NOT EXISTS estabelecimentos (
    cnpj_basico VARCHAR(8),
    cnpj_ordem VARCHAR(4),
    cnpj_dv VARCHAR(2),
    matriz_filial INT,
    nome_fantasia VARCHAR(255),
    situacao_cadastral INT,
    data_inicio_atividade DATE,
    cnae_fiscal_principal VARCHAR(15),
    cnae_fiscal_secundaria VARCHAR(15),
    tipo_logradouro VARCHAR(255),
    logradouro VARCHAR(255),
    numero VARCHAR(255),
    complemento VARCHAR(255),
    bairro VARCHAR(255),
    cep VARCHAR(8),
    uf VARCHAR(2),
    codigo_municipio VARCHAR(15),
    ddd_telefone_1 VARCHAR(2),
    telefone_1 VARCHAR(255),
    ddd_telefone_2 VARCHAR(2),
    telefone_2 VARCHAR(255),
    ddd_fax VARCHAR(2),
    fax VARCHAR(255),
    email VARCHAR(255),
    situacao_especial VARCHAR(255)
);

-- Tabela para os arquivos .EMPRECSV
CREATE TABLE IF NOT EXISTS empresas (
    cnpj_basico INT,
    nome_emprsarial VARCHAR(255),
    natureza_juridica VARCHAR(15),
    qual_responsavel TEXT,
    capital_social TEXT,
    porte TEXT,
    ente_federativo VARCHAR(255)
);

-- Tabela para os arquivos .SOCIOCSV
CREATE TABLE IF NOT EXISTS socios (
    cnpj_basico INT,
    tipo_socio INTEGER,
    nome_socio TEXT,
    cpf_socio TEXT,
    qualificacao_socio VARCHAR(15),
    data_entrada_sociedade INTEGER,
    pais VARCHAR(15),
    representante_legal TEXT,
    nome_representante TEXT,
    faixa_etaria TEXT
);

-- Tabela para os arquivos .SIMPLES.CSV.D50208
CREATE TABLE IF NOT EXISTS simples (
    cnpj_basico INT,
    opcao_pelo_simples VARCHAR(1),
    data_opcao_simples DATE,
    data_exclusao_simples DATE,
    opcao_mei VARCHAR(1),
    data_opcao_mei DATE,
    data_exclusao_mei DATE
);