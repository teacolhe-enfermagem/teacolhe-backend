from fastapi import APIRouter, Request
from fastapi.security import OAuth2PasswordBearer
from app.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, RefreshTokenRequest, RefreshTokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth")

auth_service = AuthService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/register", response_model=RegisterResponse)
async def register(data: RegisterRequest, request: Request):
    ip_address = request.client.host if request.client else None
    return await auth_service.create_account(data, ip_address)

@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest, request: Request):
    ip_address = request.client.host if request.client else None
    tokens = await auth_service.authenticate_user(data, ip_address)
    return tokens

@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(data: RefreshTokenRequest, request: Request):
    ip_address = request.client.host if request.client else None
    tokens = await auth_service.refresh_access_token(data.refresh_token, ip_address)
    return tokens