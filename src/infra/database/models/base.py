import re
from sqlalchemy import UUID, Column
from sqlalchemy.orm import DeclarativeBase, declared_attr  


class Base(DeclarativeBase):  
    id = Column(UUID, primary_key=True)

    @declared_attr  
    def __tablename__(cls) -> str:  
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
    