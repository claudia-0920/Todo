from datetime import datetime
from sqlalchemy import Integer, ForeignKey, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Todo(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey("user.id"),nullable=False)
    title: Mapped[str] = mapped_column(String(100),nullable=False,comment="代办标题")
    description: Mapped[str|None] = mapped_column(String(500),comment="详细描述")
    completed: Mapped[bool] = mapped_column(Boolean,default=False,comment="是否完成")
    created_at: Mapped[datetime] = mapped_column(DateTime,server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),onupdate=func.now())