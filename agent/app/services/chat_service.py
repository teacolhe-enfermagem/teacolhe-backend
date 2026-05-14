from app.provider.groq.llama_3_1_8b_instant.model import Model

class ChatService:
    def __init__(self):
        self.chat_groq = None

    def _get_agent(self):
        if self.chat_groq is None:
            print("Carregando o modelo pela primeira vez...")
            self.chat_groq = Model(
                model_name="llama-3.1-8b-instant",
                temperature=0.2
            )
        return self.chat_groq

    async def send_message(self, mensagem):
        agente = self._get_agent()
        
        return agente.ask(mensagem)