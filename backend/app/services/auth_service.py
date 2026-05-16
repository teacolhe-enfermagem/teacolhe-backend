from os import getenv
from datetime import datetime, timedelta
from dotenv import load_dotenv

import bcrypt

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.schemas.auth import RegisterRequest, LoginRequest
from app.repositories.auth_repository import AuthRepository


load_dotenv()


SECRET_KEY = getenv("SECRET_KEY", "secret")
REFRESH_SECRET_KEY = getenv("REFRESH_SECRET_KEY", "refresh_secret")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class AuthService:

    def _verify_password(
        self,
        plain_password: str,
        hashed_password: str
    ) -> bool:

        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )

    def _hash_password(
        self,
        password: str
    ) -> str:

        encoded = password.encode("utf-8")

        if len(encoded) > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve ter no máximo 72 bytes"
            )

        return bcrypt.hashpw(encoded, bcrypt.gensalt()).decode("utf-8")

    def _create_access_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None
    ) -> str:

        to_encode = data.copy()

        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=15)
        )

        to_encode.update({
            "exp": expire
        })

        return jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    def _create_refresh_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None
    ) -> str:

        to_encode = data.copy()

        expire = datetime.utcnow() + (
            expires_delta or timedelta(days=7)
        )

        to_encode.update({
            "exp": expire
        })

        return jwt.encode(
            to_encode,
            REFRESH_SECRET_KEY,
            algorithm=ALGORITHM
        )

    def _decode_token(
        self,
        token: str,
        secret_key: str
    ) -> dict:

        try:
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=[ALGORITHM]
            )

            return payload

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

    async def authenticate_user(
        self,
        dto: LoginRequest
    ):

        account = await AuthRepository.get_account(
            dto.email
        )

        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas"
            )

        valid_password = self._verify_password(
            dto.password,
            account["password"]
        )

        if not valid_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas"
            )

        access_token = self._create_access_token(
            data={
                "sub": str(account["id"]),
                "email": account["email"]
            },
            expires_delta=timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

        refresh_token = self._create_refresh_token(
            data={
                "sub": str(account["id"]),
                "email": account["email"]
            },
            expires_delta=timedelta(
                days=REFRESH_TOKEN_EXPIRE_DAYS
            )
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def refresh_access_token(
        self,
        refresh_token: str
    ):

        payload = self._decode_token(
            refresh_token,
            REFRESH_SECRET_KEY
        )

        user_id = payload.get("sub")
        user_email = payload.get("email")

        if not user_id or not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        account = await AuthRepository.get_account(
            user_email
        )

        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado"
            )

        access_token = self._create_access_token(
            data={
                "sub": str(account["id"]),
                "email": account["email"]
            },
            expires_delta=timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

        new_refresh_token = self._create_refresh_token(
            data={
                "sub": str(account["id"]),
                "email": account["email"]
            },
            expires_delta=timedelta(
                days=REFRESH_TOKEN_EXPIRE_DAYS
            )
        )

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    async def create_account(
        self,
        dto: RegisterRequest
    ):

        account = await AuthRepository.get_account(
            dto.email
        )

        if account:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Usuário já existe"
            )

        hashed_password = self._hash_password(
            dto.password
        )

        dto.password = hashed_password

        user = await AuthRepository.create_account_user(dto)

        access_token = self._create_access_token(
            data={
                "sub": str(user["id"]),
                "email": user["email"]
            },
            expires_delta=timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

        refresh_token = self._create_refresh_token(
            data={
                "sub": str(user["id"]),
                "email": user["email"]
            },
            expires_delta=timedelta(
                days=REFRESH_TOKEN_EXPIRE_DAYS
            )
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }


auth_service = AuthService()