from app.database.connection import database
from app.schemas.auth import RegisterRequest


class AuthRepository:

    @staticmethod
    async def get_account(email: str):
        query = """
            SELECT *
            FROM users
            WHERE email = :email
        """

        return await database.fetch_one(
            query=query,
            values={"email": email}
        )

    @staticmethod
    async def create_account_user(dto: RegisterRequest):
        query = """
            INSERT INTO users (
                name,
                email,
                password
            )
            VALUES (
                :name,
                :email,
                :password
            )
            RETURNING id, name, email
        """

        return await database.fetch_one(
            query=query,
            values={
                "name": dto.name,
                "email": dto.email,
                "password": dto.password
            }
        )