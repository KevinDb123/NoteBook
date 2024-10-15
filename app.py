from flask import Flask,g
from flask_sqlalchemy import SQLAlchemy
from config import Config
import webbrowser
from exts import db
# 导入各个蓝图
from routes.users import users_bp
from routes.administrator import admin_bp
from routes.notebook import notebook_bp

# 创建 Flask 应用实例
app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)


# 注册蓝图
app.register_blueprint(users_bp, url_prefix='/Notebook')
app.register_blueprint(admin_bp, url_prefix='/Notebook')
app.register_blueprint(notebook_bp, url_prefix='/Notebook')
@app.before_request
def before_request():
    g.isAdministrator = False
    g.isLogin = False
    g.login_user = None
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    webbrowser.open('http://127.0.0.1:5000/Notebook/homepage')
    app.run(debug=True)
