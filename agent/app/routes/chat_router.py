from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])

chat_service = ChatService()

@router.post("/", response_model= ChatResponse)
async def chat(data: ChatRequest):
    response = await chat_service.send_message(data.message)

    return ChatResponse(
        response=response["response"],
        metrics=response["metrics"]
    )