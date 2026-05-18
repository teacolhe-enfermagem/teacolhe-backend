from os import getenv
from dotenv import load_dotenv

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

load_dotenv()

INTERNAL_API_KEY = getenv("INTERNAL_API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

router = APIRouter(prefix="/chat", tags=["chat"])

chat_service = ChatService()


async def verify_internal_api_key(api_key: str = Depends(api_key_header)):
    if not INTERNAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Chave interna não configurada no servidor."
        )
    if api_key != INTERNAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chave de API inválida."
        )
    return api_key


@router.post("/", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    api_key: str = Depends(verify_internal_api_key),
):
    response = await chat_service.send_message(data.message)

    return ChatResponse(
        response=response["response"],
        metrics=response["metrics"]
    )