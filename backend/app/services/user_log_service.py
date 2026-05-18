from app.repositories.user_log_repository import UserLogRepository


class UserLogService:

    async def log(self, user_id: int, action: str, metadata: dict = None):
        await UserLogRepository.create(user_id, action, metadata)


user_log_service = UserLogService()
