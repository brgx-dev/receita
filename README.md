# 🚀 CSV to PostgreSQL Chunk Uploader

Este projeto automatiza a importação massiva de arquivos CSV para um banco de dados PostgreSQL de forma otimizada e resiliente. Ele divide os arquivos em **chunks** para evitar sobrecarga de memória e permite a retomada da importação caso ocorra uma falha.

## 📌 Recursos Principais
- **Processamento em chunks**: Evita sobrecarga de memória ao importar arquivos grandes.
- **Persistência de progresso**: Utiliza um log no banco de dados para registrar os chunks já importados e evitar reprocessamento.
- **Mapeamento automático**: Identifica a tabela correspondente para cada arquivo CSV.
- **Resistência a falhas**: Se um chunk falhar, a importação continua do último ponto bem-sucedido.
- **Criação automática de tabelas**: Se a tabela correspondente ainda não existir, ela será criada dinamicamente.

## 🛠 Configuração
### 1️⃣ **Requisitos**
- Python 3.8+
- PostgreSQL
- Bibliotecas Python: `psycopg2`, `pandas`

Instale as dependências com:
```bash
pip install -r requirements.txt
```

### 2️⃣ **Configuração do Banco de Dados**
Edite o arquivo `config.py` e insira as credenciais do seu banco PostgreSQL:
```python
DB_CONFIG = {
    "dbname": "seu_banco",
    "user": "seu_usuario",
    "password": "sua_senha",
    "host": "localhost",
    "port": "5432"
}
```

### 3️⃣ **Estrutura do Projeto**
```
📂 csv_files/          # Diretório onde devem estar os arquivos CSV
📂 scripts/
   ├── main.py        # Script principal de importação
   ├── db_utils.py    # Funções auxiliares para banco de dados
   ├── config.py      # Configurações gerais
📄 README.md          # Documentação do projeto
```

## ▶️ Como Usar
1. Coloque seus arquivos CSV dentro da pasta `csv_files`.
2. Execute o script de importação:
```bash
python main.py
```
3. Acompanhe os logs para verificar o progresso.

## 🔄 Estrutura de Reprocessamento
O sistema mantém um histórico da importação na tabela `import_log`, garantindo que **nenhum chunk seja reprocessado**.

Se for necessário reiniciar do zero, basta limpar os registros:
```sql
DELETE FROM import_log;
```

## 📌 Contribuições
Sinta-se à vontade para melhorar este projeto! Envie pull requests e sugestões.

---
Desenvolvido com 💻 e ☕ por [Seu Nome]

