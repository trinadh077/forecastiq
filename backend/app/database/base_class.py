from typing import Any
from sqlalchemy.orm import DeclarativeBase, declared_attr

class Base(DeclarativeBase):
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        # Convert CamelCase class name to snake_case table name
        name = cls.__name__
        return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip("_") + "s"
