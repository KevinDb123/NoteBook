# A project for Online-Notebook
- A practice for Python Programme.
- Using Flask,MySQL,and html
- by KevinDb123
- NoteBook!
- completed:login,register,repwd(update password),deleteUser,UserLists

/online_notebook

│

|── exts.py                # db

├── app.py                 # 主入口文件

├── config.py              # 配置文件

├── models.py              # 数据库模型文件

├── routes

│   ├── __init__.py        # 将路由文件作为模块导入

│   ├── users.py            # 登录、注册、注销、删除用户

│   ├── administrator.py # 用户管理路由（查看用户）

│   ├── notebook.py        # 笔记本相关功能路由

├── templates              # HTML 模板文件夹

│   ├── homepage.html

│   ├── homepage-login.html

│   ├── login.html

│   ├── register.html

│   ├── reset_password.html

│   ├── deleteUser.html

│   ├── UserLists.html

│   └── notebook.html

└── __init__.py            # 包初始化文件
