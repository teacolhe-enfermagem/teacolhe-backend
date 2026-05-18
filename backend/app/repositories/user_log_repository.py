import json

from app.database.connection import database


class UserLogRepository:

    @staticmethod
    async def create(user_id: int, action: str, metadata: dict = None):
        query = """
            INSERT INTO user_logs (
                user_id,
                action,
                metadata
            )
            VALUES (
                :user_id,
                :action,
                CAST(:metadata AS jsonb)
            )
            RETURNING id
        """
        return await database.execute(
            query=query,
            values={
                "user_id": user_id,
                "action": action,
                "metadata": json.dumps(metadata) if metadata else None
            }
        )