from app.provider.groq.groq_agent import GroqRAGProvider 

class Model:
    def __init__(self, model_name: str = "llama3-8b-8192", temperature: float = 0.2):
        print(f"Iniciando a classe Model com {model_name} e temperatura {temperature}")
        
        self.groq_agent = GroqRAGProvider(
            model_name=model_name, 
            temperature=temperature
        )

    def ask(self, mensagem: str):
        try:
            return self.groq_agent.ask(mensagem)
        except Exception as e:
            return {
                "response": f"Error querying RAG: {e}",
                "metrics": {
                    "documents_found": 0,
                    "sources_used": []
                }
            }