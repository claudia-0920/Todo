import uvicorn
from fastapi import FastAPI
from database import engine, Base
import models.user
from routers.user import router as user_router
from routers.todo import router as todo_router

app = FastAPI()

app.include_router(user_router)
app.include_router(todo_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8000,
        reload=True,)