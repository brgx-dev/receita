-- Tabela de logs de importação
CREATE TABLE IF NOT EXISTS import_log (
    id SERIAL PRIMARY KEY,
    chunk_id INT NOT NULL,
    table_name VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
