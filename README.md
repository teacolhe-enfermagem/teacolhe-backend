# TEAcolhe Agent - Backend API

Este é o serviço de backend do projeto **TEAcolhe**, um agente de Inteligência Artificial desenvolvido para auxiliar no atendimento de enfermagem.

O sistema utiliza uma arquitetura **RAG (Retrieval-Augmented Generation)** com modelos Llama via Groq e armazenamento vetorial FAISS.

## 🚀 Como Rodar o Projeto

### 1. Pré-requisitos

Certifique-se de ter instalado em sua máquina:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Uma chave de API da **Groq** (obtida em [console.groq.com](https://console.groq.com/))

### 2. Configuração do Ambiente

Crie um arquivo `.env` na raiz do diretório `/agent` (ou onde seu `DockerFile` reside) e adicione suas credenciais:

```env
GROQ_API_KEY=sua_chave_aqui
```

### 3. Acessar arquivos usados como dataset.

- [Acessar pelo drive](https://drive.google.com/drive/folders/1-K3W47mu_WRCx63xddHUGzT2rrfpUJ7C?usp=sharing)

### 4. Execução com Docker

Para subir o ambiente completo, utilize o Docker Compose. O comando abaixo irá construir a imagem e iniciar os containers:

```
docker compose up --build
```

- O backend estará disponível em: http://localhost:8001
- O agent estará disponível em: http://localhost:8002

### 🛠️ Comandos Úteis

**Parar os containers:**

```
docker compose down
```

**Ver logs em tempo real:**

```
docker compose logs -f teacolhe-agent
```
