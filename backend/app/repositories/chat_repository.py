from app.database.connection import database


class ChatRepository:

    # ──────────────────────────────────────────
    #  Chat
    # ──────────────────────────────────────────

    @staticmethod
    async def create_chat(user_id: int, autism_level: str):
        query = """
            INSERT INTO chats (
                user_id,
                autism_level,
                status
            )
            VALUES (
                :user_id,
                :autism_level,
                'active'
            )
            RETURNING id, user_id, autism_level, status, created_at
        """
        return await database.fetch_one(
            query=query,
            values={
                "user_id": user_id,
                "autism_level": autism_level,
            }
        )

    @staticmethod
    async def get_chat_by_id(chat_id: int):
        query = """
            SELECT id, user_id, autism_level, status, created_at
            FROM chats
            WHERE id = :chat_id AND is_deleted = FALSE
        """
        return await database.fetch_one(
            query=query,
            values={"chat_id": chat_id}
        )

    # ──────────────────────────────────────────
    #  Messages
    # ──────────────────────────────────────────

    @staticmethod
    async def create_message(chat_id: int, sender: str, content: str):
        """
        sender: 'user' | 'ai' | 'system'  (conforme ENUM sender_type do banco)
        """
        query = """
            INSERT INTO messages (
                chat_id,
                sender,
                content
            )
            VALUES (
                :chat_id,
                :sender,
                :content
            )
            RETURNING id, chat_id, sender, content, created_at
        """
        return await database.fetch_one(
            query=query,
            values={
                "chat_id": chat_id,
                "sender": sender,
                "content": content,
            }
        )

    @staticmethod
    async def get_messages_by_chat(chat_id: int):
        query = """
            SELECT id, chat_id, sender, content, created_at
            FROM messages
            WHERE chat_id = :chat_id AND is_deleted = FALSE
            ORDER BY created_at ASC
        """
        return await database.fetch_all(
            query=query,
            values={"chat_id": chat_id}
        )
