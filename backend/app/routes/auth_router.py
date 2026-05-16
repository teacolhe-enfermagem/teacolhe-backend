from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, RefreshTokenRequest, RefreshTokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth")

auth_service = AuthService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/register", response_model=RegisterResponse)
async def register( data: RegisterRequest):
    return await auth_service.create_account(data)

@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest):
    tokens = await auth_service.authenticate_user(data)
    return tokens

@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(data: RefreshTokenRequest):
    tokens = await auth_service.refresh_access_token(data.refresh_token)
    return tokens
