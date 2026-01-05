# 📦 Integração de Fornecedores — PostgreSQL, Access e SINTEGRA

Este projeto é um **sistema em Python** responsável por:

* 🔄 Sincronizar fornecedores entre **PostgreSQL** e **Microsoft Access**
* 🌐 Realizar **raspagem de dados no SINTEGRA (SEFAZ-CE)**
* 🏷️ Atualizar informações como **CNAE** e **Simples Nacional**
* 🖥️ Disponibilizar um **menu interativo via terminal**

---

## 🚀 Funcionalidades

### 🔹 1. Atualização de Banco de Dados

* Busca fornecedores no banco **PostgreSQL**
* Insere ou atualiza os dados no banco **Microsoft Access**
* Evita duplicidade por `id`

### 🔹 2. Consulta Web (SINTEGRA)

* Consulta automática pelo **CNPJ**
* Coleta:

  * CNAE
  * Situação no Simples Nacional
* Atualiza os dados diretamente no Access

### 🔹 3. Modos de Consulta

* Todos os fornecedores
* Apenas **não encontrados**
* Apenas **novos fornecedores (sem CNAE)**

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **PostgreSQL** (`psycopg2`)
* **Microsoft Access** (`pyodbc`)
* **BeautifulSoup4**
* **Requests**
* **python-dotenv**
* **Tkinter** (alertas de erro)

---

## 📁 Estrutura do Projeto

```text
📦 projeto
 ┣ 📄 main.py
 ┣ 📄 database.accdb
 ┣ 📄 .env
 ┣ 📄 README.md
 ┗ 📄 .gitignore
```

---

## 🔐 Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto:

```env
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=seu_host
POSTGRES_PORT=5432
POSTGRES_DB=seu_banco
```

> ⚠️ **Nunca versionar o `.env`**
> Adicione ao `.gitignore`

---

## 📦 Instalação

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2️⃣ Crie um ambiente virtual (opcional)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install psycopg2 pyodbc requests beautifulsoup4 python-dotenv
```

---

## ▶️ Como Executar

```bash
python main.py
```

Você verá um menu interativo no terminal:

```text
1. Atualizar banco de dados
2. Buscar dados na web (Todos os fornecedores)
3. Buscar dados na web (Apenas não encontrados)
4. Buscar dados na web (Apenas novos fornecedores)
5. Sair
```

---

## ⚠️ Observações Importantes

* Requer **driver do Microsoft Access** instalado no Windows
* A raspagem depende da **disponibilidade do site do SINTEGRA**
* Uso recomendado em redes confiáveis (consulta pública)

---

## 📌 Melhorias Futuras

* [ ] Logs estruturados
* [ ] Paralelismo nas consultas web
* [ ] Cache de resultados
* [ ] Migração total para PostgreSQL
* [ ] Interface gráfica (GUI ou Web)

---

## 👨‍💻 Autor

**Ernando Freitas**
💼 Desenvolvedor | Dados | Automação
📍 Brasil

