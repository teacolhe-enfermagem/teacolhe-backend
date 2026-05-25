from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies.auth import get_current_user
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth import UserResponse

router = APIRouter(prefix="/api/user")

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    user = await AuthRepository.get_user_by_id(int(current_user["sub"]))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    return UserResponse(**dict(user._mapping))
