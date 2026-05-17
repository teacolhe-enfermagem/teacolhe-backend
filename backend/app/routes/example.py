from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.services.user_log_service import user_log_service

router = APIRouter(prefix="/api/example")

@router.get("/")
async def get_perfil(current_user: dict = Depends(get_current_user)):
    await user_log_service.log(
        user_id=int(current_user["sub"]),
        action="user.profile_access",
        metadata={"email": current_user["email"]}
    )
    return {"mensagem": "Você está logado!", "usuario": current_user["email"]}