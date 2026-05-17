from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime


# ──────────────────────────────────────────────
#  Request DTOs
# ──────────────────────────────────────────────

class CreateChatRequest(BaseModel):
    nivel_chat: str
    mensagem_inicial: str

    @field_validator("nivel_chat")
    @classmethod
    def validate_nivel_chat(cls, value: str):
        niveis_validos = {"1", "2", "3"}
        if value.strip() not in niveis_validos:
            raise ValueError(
                "O nível do chat deve ser '1', '2' ou '3' "
                "(níveis de suporte TEA conforme DSM-5)."
            )
        return value.strip()

    @field_validator("mensagem_inicial")
    @classmethod
    def validate_mensagem_inicial(cls, value: str):
        if not value or not value.strip():
            raise ValueError("A mensagem inicial não pode estar vazia.")
        return value.strip()


# ──────────────────────────────────────────────
#  Response DTOs
# ──────────────────────────────────────────────

class MessageResponse(BaseModel):
    id: int
    chat_id: int
    sender: str
    content: str
    created_at: datetime


class ChatResponse(BaseModel):
    id: int
    user_id: int
    autism_level: str
    status: str
    created_at: datetime
    messages: List[MessageResponse]
