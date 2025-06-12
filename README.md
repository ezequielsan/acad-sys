# Sistema Acadêmico - FastAPI

## Descrição
API REST para gerenciamento de um sistema acadêmico, desenvolvida em Python com FastAPI, SQLAlchemy ORM e MySQL. O projeto implementa funcionalidades completas para entidades acadêmicas, além de recursos avançados de consulta, paginação, filtros, logging e migração de banco de dados.

## Funcionalidades

### CRUD Completo
- **Professor, Departamento, Estudante, Curso, Matrícula**
- Criação, leitura, atualização e deleção de registros
- **Autor:** Ezequiel Santos

### Contagem de Registros
- Endpoints `/count` para todas as entidades
- **Autor:** Ezequiel Santos

### Paginação
- Endpoints `/paged` para todas as entidades
- **Autor:** Ezequiel Santos

### Filtros e Buscas Avançadas
- Filtros por atributos (nome, email, curso, etc.)
- Busca textual parcial (`/search`)
- Filtros por ano/data
- Listagens por relacionamento (ex: professores de um departamento)
- Consultas complexas envolvendo múltiplas entidades (ex: cursos com departamento, matrículas com estudante e curso)
- **Autor:** Ezequiel Santos

### Agregações e Ordenações
- Contagem por relacionamento (ex: número de professores por departamento)
- Ordenação por campos customizáveis
- **Autor:** Ezequiel Santos

### Criação em Lote
- Endpoints `/batch` para criar múltiplos registros de uma vez para todas as entidades
- **Autor:** Ezequiel Santos

### Schemas Pydantic e Validação
- Schemas para documentação automática e validação de dados
- **Autor:** Ezequiel Santos

### Estrutura Modular
- Separação em models, repositórios, services, schemas e rotas
- **Autor:** Ezequiel Santos

### Tratamento de Exceções HTTP
- Mensagens detalhadas para erros de negócio e validação
- **Autor:** Ezequiel Santos

### Sistema de Logging
- Registro de todas as operações relevantes da API (criação, atualização, deleção, consultas, falhas, etc.)
- Logs em arquivo e console
- **Autor:** Michael

### Migração de Banco de Dados com Alembic
- Sistema de migração Alembic configurado
- Migração inicial para criação do esquema
- Migração adicional para adicionar campo `syllabus_url` em `courses`
- **Autor:** Michael

### Configuração do Banco de Dados
- Configuração do SQLAlchemy para MySQL
- Uso de variáveis de ambiente e boas práticas de segurança
- **Autor:** Michael

## Como Executar

1. **Clone o repositório**
2. **Crie e ative um ambiente virtual**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # Windows
   # ou
   source venv/bin/activate  # Linux/Mac
   ```
3. **Instale as dependências**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure o banco de dados**
   - Edite o arquivo `alembic.ini` com a URL do seu banco MySQL
5. **Rode as migrações**
   ```sh
   alembic upgrade head
   ```
6. **Inicie a aplicação**
   ```sh
   uvicorn app.main:app --reload
   ```
7. **Acesse a documentação interativa**
   - http://localhost:8000/docs

## Autores
- **Ezequiel Santos**: Todas as funcionalidades exceto as abaixo
- **Michael**: Sistema de logs, migração com Alembic, configuração do banco de dados
