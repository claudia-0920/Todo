import uuid
from datetime import datetime, timedelta
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User, UserToken
from utils.security import get_hash_password, verify_password

# 用户名查用户信息
async def get_user_by_username(db:AsyncSession,username:str):
    stmt = select(User).where(User.username==username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# 用户注册
async def create_user(db:AsyncSession,username:str,password:str):
    hashed_pwd = get_hash_password(password)
    user = User(username=username,password=hashed_pwd)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# 用户登录
async def authenticate_user(db:AsyncSession,username:str,password:str):
    user = await get_user_by_username(db,username)
    if not user:
        return None
    if not verify_password(password,user.password):
        return None
    return user

# 生成登录 token 并写入数据库，返回 token 字符串
async def create_token(db:AsyncSession,user_id:int):
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    usertoken = UserToken(token=token,user_id=user_id,expires_at=expires_at)
    db.add(usertoken)
    await db.commit()
    await db.refresh(usertoken)
    return token

# 用token查用户信息
async def get_user_by_token(db:AsyncSession,token:str):
    stmt = select(UserToken).where(UserToken.token==token)
    result = await db.execute(stmt)
    db_token = result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.now():
        return None
    stmt_user = select(User).where(User.id== db_token.user_id)
    result_user = await db.execute(stmt_user)
    return result_user.scalar_one_or_none()

# 修改密码
async def update_pwd_crud(db:AsyncSession,user_id:int,old_password:str,new_password:str):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one()
    # if not user:
    #     return None
    match = verify_password(old_password,user.password)
    if not match:
        return None
    new_pwd = get_hash_password(new_password)
    result = update(User).where(User.id == user_id).values(password=new_pwd)
    await db.execute(result)
    stmt = delete(UserToken).where(UserToken.user_id == user_id)
    await db.execute(stmt)
    await db.commit()
    await db.refresh(user)
    return True
    


