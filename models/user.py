from datetime import datetime
from sqlalchemy import func, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class User(Base):
    __tablename__ = 'user'
    id : Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    username : Mapped[str] = mapped_column(String(50),unique=True,nullable=False)
    password : Mapped[str] = mapped_column(String(255),nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime,server_default=func.now())

class UserToken(Base):
    __tablename__ = 'user_token'
    id : Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    user_id : Mapped[int] = mapped_column(Integer,ForeignKey('user.id'),nullable=False)
    token : Mapped[str] = mapped_column(String(255),unique=True,nullable=False)
    expires_at : Mapped[datetime] = mapped_column(DateTime,nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime,server_default=func.now())

    