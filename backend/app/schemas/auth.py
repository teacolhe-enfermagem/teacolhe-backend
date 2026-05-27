from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        if len(value) < 8:
            raise ValueError(
                "A senha deve conter no mínimo 8 caracteres."
            )

        return value


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):

        if len(value.strip()) < 3:
            raise ValueError(
                "O nome deve conter pelo menos 3 caracteres."
            )

        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        if len(value) < 8:
            raise ValueError(
                "A senha deve conter no mínimo 8 caracteres."
            )

        return value

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, value: str, info):

        password = info.data.get("password")

        if value != password:
            raise ValueError("As senhas não coincidem.")

        return value


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RegisterResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None