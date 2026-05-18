from typing import List

from fastapi import APIRouter, Depends, Request

from app.dependencies.auth import get_current_user
from app.schemas.chat import (
    ChatListItemResponse,
    ChatResponse,
    CreateChatRequest,
    SendMessageRequest,
    SendMessageResponse,
)
from app.services.chat_service import chat_service

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse, status_code=201)
async def create_chat(
    data: CreateChatRequest,
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    user_id = int(current_user["sub"])
    ip_address = request.client.host if request.client else None
    return await chat_service.create_chat(dto=data, user_id=user_id, ip_address=ip_address)


@router.get("/", response_model=List[ChatListItemResponse])
async def list_chats(
    current_user: dict = Depends(get_current_user),
):
    user_id = int(current_user["sub"])
    return await chat_service.list_chats(user_id=user_id)


@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: int,
    current_user: dict = Depends(get_current_user),
):
    user_id = int(current_user["sub"])
    return await chat_service.get_chat(chat_id=chat_id, user_id=user_id)


@router.post("/{chat_id}/messages", response_model=SendMessageResponse, status_code=201)
async def send_message(
    chat_id: int,
    data: SendMessageRequest,
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    user_id = int(current_user["sub"])
    ip_address = request.client.host if request.client else None
    return await chat_service.send_message(
        chat_id=chat_id,
        message=data.message,
        user_id=user_id,
        ip_address=ip_address,
    )
