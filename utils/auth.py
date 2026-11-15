from fastapi import Depends,Header,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.user import get_user_by_token
from database import get_db

# token处理
async def get_current_user(
        authorization: str = Header(...,alias="Authorization"),
        db: AsyncSession = Depends(get_db)):
    token = authorization.replace("Bearer ","")
    user = await get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=401,detail="未登录或登录过期")
    return user
