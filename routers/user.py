from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import get_user_by_username, create_user, create_token, authenticate_user
from database import get_db
from models.user import User
from schemas.user import UserRequest, UserResponse, UserInfo
from utils.auth import get_current_user

router = APIRouter(prefix="/api/user",tags=["user"])

# 用户注册
@router.post("/register")
async def register(
        user_data: UserRequest,
        db: AsyncSession = Depends(get_db)):
    if await get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400,detail="用户名已存在")
    user = await create_user(db, user_data.username, user_data.password)
    token = await create_token(db,user.id)
    return{
        "code": 200,
        "msg": "注册成功",
        "data": UserResponse(
            token=token,
            user_info=UserInfo.model_validate(user)
        )
    }

# 用户登录
@router.post("/login")
async def login(
        user_data: UserRequest,
        db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    token = await create_token(db, user.id)
    return {
        "code": 200,
        "msg": "登录成功",
        "data": UserResponse(
            token=token,
            user_info=UserInfo.model_validate(user)
        )
    }

# 获取用户信息
@router.get("/info")
async def info(current_user:User = Depends(get_current_user)):
    return {
        "code": 200,
        "msg": "success",
        "data": UserInfo.model_validate(current_user)
    }

