from sqlmodel import SQLModel, Field
from typing import Optional, ClassVar

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(index=True, unique=True, max_length=255)
    hashed_password: str = Field(max_length=255)

    __table_args__: ClassVar[dict] = {"sqlite_autoincrement": True}