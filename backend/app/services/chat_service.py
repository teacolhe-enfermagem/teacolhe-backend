import httpx

from fastapi import HTTPException, status

from app.schemas.chat import CreateChatRequest
from app.repositories.chat_repository import ChatRepository

AGENT_URL = "http://localhost:8002/chat/"


class ChatService:

    async def _call_agent(self, message: str, nivel: str) -> str:
        """
        Envia mensagem e nível TEA ao microservice do agente (http://localhost:8002).
        Retorna o texto da resposta gerada pela IA.
        """
        payload = {
            "message": (
                f"[Nível de suporte TEA: {nivel}]\n{message}"
            )
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(AGENT_URL, json=payload)
                response.raise_for_status()
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="O microservice do agente não respondeu a tempo."
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Erro no microservice do agente: {e.response.status_code}"
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Não foi possível conectar ao microservice do agente."
            )

        data = response.json()
        return data["response"]

    async def create_chat(self, dto: CreateChatRequest, user_id: int) -> dict:

        chat = await ChatRepository.create_chat(
            user_id=user_id,
            autism_level=dto.nivel_chat,
        )

        user_message = await ChatRepository.create_message(
            chat_id=chat["id"],
            sender="user",
            content=dto.mensagem_inicial,
        )

        bot_text = await self._call_agent(
            message=dto.mensagem_inicial,
            nivel=dto.nivel_chat,
        )

        bot_message = await ChatRepository.create_message(
            chat_id=chat["id"],
            sender="ai",
            content=bot_text,
        )

        messages = [
            {
                "id": user_message["id"],
                "chat_id": user_message["chat_id"],
                "sender": user_message["sender"],
                "content": user_message["content"],
                "created_at": user_message["created_at"],
            },
            {
                "id": bot_message["id"],
                "chat_id": bot_message["chat_id"],
                "sender": bot_message["sender"],
                "content": bot_message["content"],
                "created_at": bot_message["created_at"],
            },
        ]

        return {
            "id": chat["id"],
            "user_id": chat["user_id"],
            "autism_level": chat["autism_level"],
            "status": chat["status"],
            "created_at": chat["created_at"],
            "messages": messages,
        }


chat_service = ChatService()
