from datetime import datetime

from pydantic import BaseModel, ConfigDict

# 创建待办
class TodoCreate(BaseModel):
    title: str
    description: str | None = None

# 更新待办
class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

# 返回待办
class TodoResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime
    updated_at: datetime

    # 允许 Pydantic 从 ORM 对象的属性中读取数据。
    model_config = ConfigDict(from_attributes=True)
