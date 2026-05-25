from app.database.connection import database
from app.schemas.auth import RegisterRequest

class AuthRepository:

    @staticmethod
    async def get_user_by_id(user_id: int):
        query = """
            SELECT id, name, email, role, created_at, updated_at
            FROM users
            WHERE id = :user_id AND is_deleted = FALSE
        """
        return await database.fetch_one(
            query=query,
            values={"user_id": user_id}
        )

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

    @staticmethod
    async def create_session(user_id: int, refresh_token_hash: str, ip_address: str = None):
        query = """
            INSERT INTO user_sessions (
                user_id,
                refresh_token,
                ip_address
            )
            VALUES (
                :user_id,
                :refresh_token,
                :ip_address
            )
            RETURNING id
        """
        return await database.execute(
            query=query,
            values={
                "user_id": user_id,
                "refresh_token": refresh_token_hash,
                "ip_address": ip_address
            }
        )

    @staticmethod
    async def get_session_by_token(refresh_token_hash: str):
        query = """
            SELECT *
            FROM user_sessions
            WHERE refresh_token = :refresh_token AND is_deleted = FALSE
        """
        return await database.fetch_one(
            query=query,
            values={"refresh_token": refresh_token_hash}
        )

    @staticmethod
    async def delete_session(session_id: int):
        query = """
            UPDATE user_sessions
            SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP
            WHERE id = :session_id
        """
        await database.execute(
            query=query,
            values={"session_id": session_id}
        )