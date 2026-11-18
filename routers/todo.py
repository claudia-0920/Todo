from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from crud.todo import (create_todo_crud,
                       get_todo_list, get_todo_by_id, update_todo_crud, delete_todo_crud)
from database import get_db
from models.user import User
from schemas.common import CommonResponse
from schemas.todo import TodoResponse, TodoUpdate, TodoCreate
from utils.auth import get_current_user

router = APIRouter(prefix='/api/todo')

@router.post('/create_todo')
async def create_todo(todo_info:TodoCreate,
                        db: AsyncSession = Depends(get_db),
                        user: User = Depends(get_current_user),
):
    data = await create_todo_crud(db,user.id,todo_info.title,todo_info.description)
    return CommonResponse(
        code=200,
        msg="success",
        data=TodoResponse.model_validate(data))


@router.get('/get_todos')
async def get_todos(
                    page:int=Query(default=1,ge=1),
                    page_size:int=Query(default=10,ge=1,le=100),
                    completed:bool| None = None,
                    db: AsyncSession = Depends(get_db),
                    user: User = Depends(get_current_user)):
    todo_list, count, total = await get_todo_list(db,user.id,page,page_size,completed)
    items = [TodoResponse.model_validate(item) for item in todo_list]
    return CommonResponse(
        code=200,
        msg="success",
        data={
            "items":items,
            "count":count,
            "total":total})

@router.get('/get_details')
async def get_todo_details(todo_id:int,
                       db: AsyncSession = Depends(get_db),
                       user: User = Depends(get_current_user)):
    data = await get_todo_by_id(db,todo_id,user.id)
    if data is None:
        raise HTTPException(status_code=404,detail="无此todo")
    return CommonResponse(
            code=200,
            msg="success",
            data=TodoResponse.model_validate(data))

@router.put('/update_todo')
async def update_todo(todo_id:int,
                      todo_data:TodoUpdate,
                      db: AsyncSession = Depends(get_db),
                      user: User = Depends(get_current_user)):
    data = await update_todo_crud(db,todo_id,todo_data,user.id)
    if data is None:
        raise HTTPException(status_code=404,detail="无此todo")
    return CommonResponse(
        code=200,
        msg="success",
        data=TodoResponse.model_validate(data))

@router.delete('/delete_todo')
async def delete_todo(todo_id:int,
                      db: AsyncSession = Depends(get_db),
                      user: User = Depends(get_current_user)):
    data = await delete_todo_crud(db,todo_id,user.id)
    if data is None:
        raise HTTPException(status_code=404, detail="无此todo")
    return CommonResponse(
        code=200,
        msg="删除成功",
        )

