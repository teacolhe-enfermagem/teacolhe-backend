<img
  src="./docs/banner.jpeg"
/>

Este é o serviço de backend do projeto **TEAcolhe**, um agente de Inteligência Artificial desenvolvido para auxiliar no atendimento de enfermagem.

O sistema utiliza uma arquitetura **RAG (Retrieval-Augmented Generation)** com modelos Llama via Groq e armazenamento vetorial FAISS.

## 🚀 Como Rodar o Projeto

### 1. Pré-requisitos

Certifique-se de ter instalado em sua máquina:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Uma chave de API da **Groq** (obtida em [console.groq.com](https://console.groq.com/))

### 2. Configuração do Ambiente

**1. Configuração do Agente**

Crie um arquivo `.env` na raiz do diretório `/agent` (ou onde seu `DockerFile` reside) e adicione suas credenciais:

```env
GROQ_API_KEY=sua_chave_aqui

# Essa KEY deve ser a mesma definida no backend, serve apenas para validar a requisição.
INTERNAL_API_KEY=teacolhe_internal_key_2026
```

**2. Configuração do Backend**
Crie um arquivo `.env` na raiz do diretório `/backend`. Adicione a URL do banco e as chaves de segurança para criptografia dos tokens de sessão:

```env
# Importante: Como o banco roda via Docker, o host deve ser 'postgres' (nome do container), e não 'localhost'

DATABASE_URL="postgresql://postgres:postgres@postgres:5432/teacolhe"

SECRET_KEY="sua_chave_secreta_super_segura_aqui"

REFRESH_SECRET_KEY="sua_outra_chave_secreta_para_refresh"

# Essa KEY deve ser a mesma definida no agent, serve apenas para validar a requisição.
INTERNAL_API_KEY=teacolhe_internal_key_2026
```

### 3. Acessar arquivos usados como dataset.

- [Acessar pelo drive](https://drive.google.com/drive/folders/1-K3W47mu_WRCx63xddHUGzT2rrfpUJ7C?usp=sharing)

Esses arquivos devem ser colocados em: `agent/app/datasets`. É necessário para iniciar o agente.

### 4. Execução com Docker

Para subir o ambiente completo, utilize o Docker Compose. O comando abaixo irá construir a imagem e iniciar os containers:

```
docker compose up --build
```

##### Os serviços estarão disponíveis nos seguintes endereços:

- Backend API: http://localhost:8001

- Agent API: http://localhost:8002

- PostgreSQL: postgresql://postgres:postgres@postgres:5432/teacolhe

### 🛠️ Comandos Úteis

**Parar os containers:**

```
docker compose down
```

**Ver logs em tempo real:**

```
docker compose logs -f teacolhe-agent
```
