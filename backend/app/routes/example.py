from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/example")

@router.get("/")
async def get_perfil(current_user: dict = Depends(get_current_user)):
    return {"mensagem": "Você está logado!", "usuario": current_user["email"]}