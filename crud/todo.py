from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.todo import Todo
from schemas.todo import TodoUpdate


async def create_todo_crud(db:AsyncSession,user_id:int,title:str,description:str):
    todo = Todo(user_id = user_id,title=title,description=description)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo

async def get_todo_list(db:AsyncSession,
                        user_id:int,
                        page:int = 1,page_size:int = 10,
                        completed: bool | None = None,
                        ):
    offset = (page-1)*page_size
    conditions = [Todo.user_id == user_id]
    if completed is not None:
        conditions.append(Todo.completed == completed)
    stmt = (select(Todo).where(*conditions).
            order_by(Todo.created_at.desc())
            .offset(offset).limit(page_size))
    todo_list = await db.execute(stmt)
    todo_list = todo_list.scalars().all()
    count_stmt = select(func.count(Todo.id)).where(*conditions)
    count = await db.execute(count_stmt)
    count_result = count.scalar_one()
    # total = count_result // page_size
    # if count_result % page_size:
    #     total += 1
    total = (count_result + page_size - 1) // page_size
    return todo_list, count_result, total


async def get_todo_by_id(db:AsyncSession,todo_id:int,user_id:int):
    stmt = select(Todo).where(Todo.id == todo_id,Todo.user_id == user_id)
    todo_one = await db.execute(stmt)
    return todo_one.scalar_one_or_none()

async def update_todo_crud(db:AsyncSession,todo_id:int,todo_data:TodoUpdate,user_id:int):
    todo = await get_todo_by_id(db,todo_id,user_id)
    if not todo:
        return None
    todo_dict = todo_data.model_dump(exclude_unset=True) # 只提取用户实际提交的字段
    todo_update = (update(Todo).
                   where(Todo.id == todo_id,Todo.user_id == user_id).
                   values(**todo_dict)) # 把字典展开成 values() 接收的关键字参数
    await db.execute(todo_update)
    await db.commit()
    await db.refresh(todo)
    return todo

async def delete_todo_crud(db:AsyncSession,todo_id:int,user_id:int):
    todo = await get_todo_by_id(db, todo_id, user_id)
    if not todo:
        return None
    await db.delete(todo)
    await db.commit()
    return True

