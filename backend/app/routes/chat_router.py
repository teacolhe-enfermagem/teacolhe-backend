from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.schemas.chat import CreateChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse, status_code=201)
async def create_chat(
    data: CreateChatRequest,
    current_user: dict = Depends(get_current_user),
):

    user_id = int(current_user["sub"])
    return await chat_service.create_chat(dto=data, user_id=user_id)
