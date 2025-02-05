from src.infra.database.models.user import User
from src.infra.protocols import AbstractSQLRepository
from sqlalchemy import exists, select


class UserRepository(AbstractSQLRepository):

    async def is_user_exist(self, user: User) -> bool:
        stmt = select(self.model).where(
            exists().where(self.model.email == user.email))
        return (await self.session.execute(stmt)).scalar()

    async def get_user_by_email(self, user: User) -> User:
        stmt = select(self.model).where(self.model.email == user.email)
        return (await self.session.execute(stmt)).scalar_one_or_none()
