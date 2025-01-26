from abc import ABC, abstractmethod
from typing import Any, BinaryIO, Generic, TypeVar, Protocol

from sqlalchemy import UUID

T = TypeVar("T")


class AbstractSQLRepository(Generic[T], Protocol):
    
    async def get_all(self) -> list[T]:
        ...
    
    async def get(self, id: UUID) -> T | None:
        ...
    
    async def create(self, item: T) -> None:
        ...
        
    async def update(self, changes: dict[str, Any], id: UUID) -> None:
        ...
        
    async def delete(self, id: UUID) -> None:
        ...
        
        
class ImageStorage(ABC):

    @abstractmethod
    async def exists(self, image_id: str) -> bool:
        ...

    @abstractmethod
    async def upload(self, filename: str, file: BinaryIO, size: int | None = None) -> str:
        ...

    @abstractmethod
    async def download(self, image_id: str) -> bytes:
        ...