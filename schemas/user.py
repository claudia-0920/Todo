from pydantic import BaseModel, ConfigDict
class UserRequest(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)
    # from_attributes=True：允许从 SQLAlchemy 的 User 对象直接转成这个 Schema

class UserResponse(BaseModel):
    token: str
    user_info: UserInfo

class UpdatePassword(BaseModel):
    old_password: str
    new_password: str

