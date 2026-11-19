
# Todo 待办事项管理系统

## 一、项目简介

基于 FastAPI 开发的多用户待办事项管理后端系统，实现用户认证、待办事项管理及用户数据隔离等功能。

## 二、技术栈

- Python
- FastAPI
- SQLAlchemy（异步 ORM）
- MySQL
- Ubuntu Linux
- Nginx
- Git

## 三、主要功能

### 用户管理
- 用户注册与登录
- UUID Token 身份认证
- 用户信息查询
- 修改密码，清除该用户已有 Token

### 待办事项管理
- 创建待办事项
- 查询待办事项列表及详情
- 修改待办事项
- 删除待办事项
- 分页查询与完成状态筛选
- 用户数据隔离

### 通用功能
- 统一响应格式
- 全局异常处理


## 四、项目结构

```text
Todo/
├── main.py              # FastAPI 应用入口
├── config.py            # 配置管理
├── database.py          # 数据库连接及会话管理
├── requirements.txt     # 项目依赖
├── models/              # SQLAlchemy 数据模型
│   ├── user.py
│   └── todo.py
├── schemas/             # Pydantic 数据校验模型
│   ├── user.py
│   ├── todo.py
│   └── common.py
├── routers/             # API 路由
│   ├── user.py
│   └── todo.py
├── crud/                # 数据库 CRUD 操作
│   ├── user.py
│   └── todo.py
├── utils/               # 工具模块
│   ├── security.py
│   └── auth.py
└── exceptions.py        # 全局异常处理
```


## 五、环境配置与运行

### 1. 克隆项目

```bash
git clone https://github.com/claudia-0920/Todo.git
cd Todo
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
```

激活虚拟环境：

Windows：
```bash
.venv\Scripts\activate
```

Linux：
```bash
source .venv/bin/activate
```

### 3. 安装项目依赖

```bash
pip install -r requirements.txt
```

### 4. 配置数据库

确保 MySQL 已安装并运行，创建项目数据库：

```sql
CREATE DATABASE todo_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

在项目根目录创建 `.env` 文件，配置数据库连接：

```env
DATABASE_URL=mysql+aiomysql://用户名:密码@localhost:3306/todo_app?charset=utf8mb4
```

请根据自己的 MySQL 用户名和密码修改连接信息。

### 5. 启动项目

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```


## 六、接口文档

项目启动后，可通过以下地址访问 Swagger UI 接口文档：

```text
http://127.0.0.1:8000/docs
```

通过 Swagger UI 可以查看接口信息、请求参数及响应结果，并进行接口测试。


