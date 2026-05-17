from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime

class CreateChatRequest(BaseModel):
    nivel_chat: str
    message: str

    @field_validator("nivel_chat")
    @classmethod
    def validate_nivel_chat(cls, value: str):
        niveis = {"1", "2", "3"}
        if value.strip() not in niveis:
            raise ValueError(
                "O nível do chat deve ser '1', '2' ou '3' "
                "(níveis de suporte TEA conforme DSM-5)."
            )
        return value.strip()

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str):
        if not value or not value.strip():
            raise ValueError("A mensagem inicial não pode estar vazia.")
        return value.strip()


class SendMessageRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str):
        if not value or not value.strip():
            raise ValueError("A mensagem não pode estar vazia.")
        return value.strip()


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
    updated_at: datetime
    messages: List[MessageResponse]


class ChatListItemResponse(BaseModel):
    id: int
    user_id: int
    autism_level: str
    status: str
    created_at: datetime
    updated_at: datetime


class SendMessageResponse(BaseModel):
    messages: List[MessageResponse]


class SendMessageResponse(BaseModel):
    messages: List[MessageResponse]
