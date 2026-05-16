import re

from pydantic import BaseModel, EmailStr, field_validator

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
            r"(?=.*[@$!%*?&._-])[A-Za-z\d@$!%*?&._-]{8,}$"
        )

        if not re.match(pattern, value):
            raise ValueError(
                "A senha deve conter no mínimo 8 caracteres, "
                "uma letra maiúscula, uma minúscula, um número "
                "e um caractere especial."
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

        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
            r"(?=.*[@$!%*?&._-])[A-Za-z\d@$!%*?&._-]{8,}$"
        )

        if not re.match(pattern, value):
            raise ValueError(
                "A senha deve conter no mínimo 8 caracteres, "
                "uma letra maiúscula, uma minúscula, um número "
                "e um caractere especial."
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