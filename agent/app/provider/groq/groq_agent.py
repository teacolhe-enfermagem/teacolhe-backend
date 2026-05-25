import os
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.csv_loader import CSVLoader 
from langchain_community.document_loaders import PyPDFLoader 
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

load_dotenv()

class GroqRAGProvider:
    def __init__(self, model_name: str, temperature: float):
        logging.info("Inicializando GroqRAGProvider...")
        
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            logging.error("A chave GROQ_API_KEY não foi encontrada nas variáveis de ambiente.")
            raise ValueError("A chave GROQ_API_KEY não foi encontrada nas variáveis de ambiente.")

        logging.info(f"Carregando modelo LLM do Groq: {model_name}")
        self.llm = ChatGroq(
            temperature=temperature,
            model_name=model_name,
            api_key=self.groq_api_key
        )

        logging.info("Carregando modelo de Embeddings (HuggingFace)...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        csv_loader = DirectoryLoader(
            path="./app/datasets/",
            glob="**/*.csv",
            loader_cls=CSVLoader,
            loader_kwargs={
                "encoding": "utf-8",
                "csv_args": {
                    "delimiter": ",", 
                }
            }
        )

        pdf_loader = DirectoryLoader(
            path="./app/datasets/",
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )

        logging.info("Carregando documentos da pasta...")
        
        documents = []
        
        try:
            logging.info("Lendo arquivos CSV...")
            documents.extend(csv_loader.load_and_split())
            
            logging.info("Lendo arquivos PDF...")
            documents.extend(pdf_loader.load_and_split())
            
            if documents:
                logging.info(f"Gerando embeddings para {len(documents)} chunks combinados (FAISS)...")
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
                logging.info("GroqRAGProvider inicializado com sucesso com PDFs e CSVs!")
            else:
                self.vector_store = None
                logging.warning("Nenhum documento válido encontrado na pasta.")
                
        except Exception as e:
            logging.error(f"Erro ao carregar documentos: {e}")
            self.vector_store = None

    def create_chunks(self, text: str, chunk_size=1000, chunk_overlap=100):
        logging.info(f"Iniciando a leitura do documento. Tamanho total: {len(text)} caracteres.")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        
        logging.info("Realizando o split (chunking) do texto...")
        chunks = text_splitter.split_documents([Document(page_content=text)])
        logging.info(f"Texto dividido em {len(chunks)} chunks.")
        return chunks

    def process_and_store(self, chunks):
        if not chunks:
            logging.warning("A lista de chunks está vazia. Processo abortado.")
            raise ValueError("A lista de chunks está vazia.")
            
        logging.info(f"Gerando embeddings para {len(chunks)} chunks e populando o FAISS...")
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        logging.info("Vector store (FAISS) criado com sucesso!")

    def _setup_chain(self):
        if self.vector_store is None:
            logging.error("Tentativa de criar chain sem inicializar o Vector Store.")
            raise RuntimeError("O Vector Store não foi inicializado. Verifique se os arquivos foram carregados corretamente.")

        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        system_prompt = """
        
Você é o Agente Virtual do "TEAcolhe Enfermagem" (Cuidado que entende), um assistente especializado e de resposta rápida projetado para apoiar profissionais de enfermagem (auxiliares, técnicos e enfermeiros) no atendimento a pacientes com Transtorno do Espectro Autista (TEA) no ambiente hospitalar.

SEU OBJETIVO:
Fornecer suporte imediato à tomada de decisão, orientações práticas e protocolos de manejo comportamental baseados no nível de suporte do paciente (DSM-5), visando um atendimento humanizado, seguro e livre de erros.

DIRETRIZES DE COMUNICAÇÃO (CRÍTICO):
1. SEJA DIRETO AO PONTO: Profissionais de saúde têm pouco tempo. Responda de forma concisa, objetiva e estruturada.
2. USE FORMATAÇÃO CLARA: Utilize bullet points, textos curtos e checklists. Evite parágrafos longos ou introduções desnecessárias.
3. TOM PROFISSIONAL E EMPÁTICO: A linguagem deve ser técnica (padrão COFEN/Ministério da Saúde), porém acolhedora e focada na humanização do paciente.
4. MODO EMERGÊNCIA: Se o usuário relatar uma "crise" ou "agitação severa", pule qualquer contexto e forneça imediatamente os passos de contenção sensorial e segurança.

BASE DE CONHECIMENTO TÉCNICO (NÍVEIS DE TEA - DSM-5):
Sempre adapte suas respostas com base no nível de suporte informado pelo profissional:

- NÍVEL 1 (Necessita de apoio):
  * Foco: Interação social e comunicação.
  * Ações: Orientações de comunicação clara, antecipação de procedimentos para evitar quebra de rotina, manejo de rigidez comportamental leve.

- NÍVEL 2 (Necessita de apoio substancial):
  * Foco: Comunicação alternativa e estruturação.
  * Ações: Uso de frases curtas, apoio visual, protocolos detalhados de adaptação ao ambiente hospitalar, redução de gatilhos sensoriais.

- NÍVEL 3 (Necessita de apoio muito substancial):
  * Foco: Segurança, suporte intensivo e crise.
  * Ações: Minimização extrema de estímulos (luz, som, toque), leitura de comunicação não-verbal, proteção contra autoagressão, envolvimento fundamental do acompanhante/cuidador.

PRINCÍPIOS DO ATENDIMENTO:
Suas orientações devem refletir as diretrizes da Organização Mundial da Saúde (OMS), Política Nacional de Humanização (PNH), Conselho Federal de Enfermagem (COFEN) e Lei Berenice Piana.

COMO RESPONDER A SOLICITAÇÕES:
- Exemplo de Procedimento: Forneça um checklist prático de 3 a 5 passos focados na redução do estresse e adaptação.
- Exemplo de Checklist Nível 3: Forneça os itens críticos de segurança e mapeamento sensorial do ambiente.
- Pergunta Genérica: Resuma a resposta em uma frase e pergunte qual o nível de suporte do paciente para direcionar o atendimento.

MENSAGEM DE ENCERRAMENTO PADRÃO (Apenas quando a interação for finalizada):
"O TEAcolhe Enfermagem transforma conhecimento em cuidado. O que mais você precisa agora?"

DOCUMENTOS DE CONTEXTO PARA BASEAR SUA RESPOSTA:
{context}"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        return rag_chain

    def ask(self, query: str):
        chain = self._setup_chain()
        
        logging.info(f"Processando pergunta: '{query}'")
        response = chain.invoke({"input": query})
        logging.info("Resposta gerada com sucesso!")
        
        answer = response["answer"]
        source_documents = response.get("context", [])
        
        fontes = []
        for doc in source_documents:
            origem = doc.metadata.get("source", "Fonte desconhecida")
            pagina = doc.metadata.get("page", "")
            ref = f"{origem} (Pág: {pagina})" if pagina else origem
            fontes.append(ref)
            
        return {
            "response": answer,
            "metrics": {
                "documents_found": len(source_documents),
                "sources_used": list(set(fontes))
            }
        }