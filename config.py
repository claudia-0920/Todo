import os
from dotenv import load_dotenv

# 读取项目根目录下的 .env 文件
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "未设置 DATABASE_URL，请在项目根目录创建 .env 文件，"
        "并写入：DATABASE_URL=mysql+aiomysql://用户:密码@localhost:3306/todo_app?charset=utf8mb4"
    )