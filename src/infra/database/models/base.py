import re
from sqlalchemy.orm import DeclarativeBase, declared_attr  


class Base(DeclarativeBase):  
    @declared_attr  
    def __tablename__(cls) -> str:  
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
    