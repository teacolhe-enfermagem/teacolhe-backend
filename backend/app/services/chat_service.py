import httpx
from os import getenv
from dotenv import load_dotenv

from fastapi import HTTPException, status

from app.schemas.chat import CreateChatRequest
from app.repositories.chat_repository import ChatRepository
from app.services.user_log_service import user_log_service

load_dotenv()

AGENT_URL = "http://agent:8002/chat/"
INTERNAL_API_KEY = getenv("INTERNAL_API_KEY")


class ChatService:

    @staticmethod
    def _build_message_dict(record):
        return {
            "id": record["id"],
            "chat_id": record["chat_id"],
            "sender": record["sender"],
            "content": record["content"],
            "created_at": record["created_at"],
        }

    async def _call_agent(self, message: str, nivel: str) -> str:
        payload = {
            "message": (
                f"[Nível de suporte TEA: {nivel}]\n{message}"
            )
        }

        headers = {}
        if INTERNAL_API_KEY:
            headers["X-API-Key"] = INTERNAL_API_KEY

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(AGENT_URL, json=payload, headers=headers)
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

    async def create_chat(self, dto: CreateChatRequest, user_id: int, ip_address: str = None) -> dict:
        chat = await ChatRepository.create_chat(
            user_id=user_id,
            autism_level=dto.nivel_chat,
        )

        user_message = await ChatRepository.create_message(
            chat_id=chat["id"],
            sender="user",
            content=dto.message,
        )

        bot_text = await self._call_agent(
            message=dto.message,
            nivel=dto.nivel_chat,
        )

        bot_message = await ChatRepository.create_message(
            chat_id=chat["id"],
            sender="ai",
            content=bot_text,
        )

        await user_log_service.log(
            user_id=user_id,
            action="chat.created",
            metadata={
                "chat_id": chat["id"],
                "autism_level": dto.nivel_chat,
                "ip_address": ip_address,
            }
        )

        messages = [
            self._build_message_dict(user_message),
            self._build_message_dict(bot_message),
        ]

        return {
            "id": chat["id"],
            "user_id": chat["user_id"],
            "autism_level": chat["autism_level"],
            "status": chat["status"],
            "created_at": chat["created_at"],
            "messages": messages,
        }

    async def get_chat(self, chat_id: int, user_id: int) -> dict:
        chat = await ChatRepository.get_chat_by_id(chat_id)

        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat não encontrado."
            )

        if chat["user_id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este chat."
            )

        messages = await ChatRepository.get_messages_by_chat(chat_id)

        return {
            "id": chat["id"],
            "user_id": chat["user_id"],
            "autism_level": chat["autism_level"],
            "status": chat["status"],
            "created_at": chat["created_at"],
            "updated_at": chat["updated_at"],
            "messages": [self._build_message_dict(m) for m in messages],
        }

    async def list_chats(self, user_id: int) -> list:
        chats = await ChatRepository.get_chats_by_user_id(user_id)
        return [
            {
                "id": chat["id"],
                "user_id": chat["user_id"],
                "autism_level": chat["autism_level"],
                "status": chat["status"],
                "created_at": chat["created_at"],
                "updated_at": chat["updated_at"],
            }
            for chat in chats
        ]

    async def send_message(self, chat_id: int, message: str, user_id: int, ip_address: str = None) -> dict:
        chat = await ChatRepository.get_chat_by_id(chat_id)

        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat não encontrado."
            )

        if chat["user_id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para enviar mensagens neste chat."
            )

        user_message = await ChatRepository.create_message(
            chat_id=chat_id,
            sender="user",
            content=message,
        )

        bot_text = await self._call_agent(
            message=message,
            nivel=chat["autism_level"],
        )

        bot_message = await ChatRepository.create_message(
            chat_id=chat_id,
            sender="ai",
            content=bot_text,
        )

        await user_log_service.log(
            user_id=user_id,
            action="chat.message_sent",
            metadata={
                "chat_id": chat_id,
                "message_id": user_message["id"],
                "ip_address": ip_address,
            }
        )

        return {
            "messages": [
                self._build_message_dict(user_message),
                self._build_message_dict(bot_message),
            ]
        }


chat_service = ChatService()
