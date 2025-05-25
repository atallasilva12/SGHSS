# SGHSS - Sistema de Gestão Hospitalar e de Serviços de Saúde (Back-end)

Este projeto implementa a API REST de um sistema hospitalar usando **FastAPI** e **PostgreSQL**.

## ✅ Funcionalidades

- Cadastro e autenticação de usuários (JWT)
- Registro de pacientes
- Agendamento de consultas
- Visualização do histórico clínico

## 🚀 Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/atallasilva12/SGHSS.git
cd SGHSS
````

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie o arquivo `.env` com os dados do PostgreSQL:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sghss
DB_USER=postgres
DB_PASSWORD=********
```

### 5. Criar as tabelas

```bash
python init_db.py
```

### 6. Rodar o servidor

```bash
uvicorn app.main:app --reload
```

Acesse:
📘 Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
📕 Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Testes

Os testes podem ser feitos usando **Postman** ou a interface Swagger.

---

## 📂 Organização

* `app/` → Código principal da API
* `routes/` → Endpoints
* `models/` → ORM com SQLAlchemy
* `services/` → Lógica de negócio
* `utils/` → Conexão com banco, inicialização
* `tests/` → Testes automatizados

---
