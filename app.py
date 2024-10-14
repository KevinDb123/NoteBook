from django.contrib.messages.context_processors import messages
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
HOSTNAME = "localhost"
PORT = '3306'
USERNAME = "root"
PASSWORD = "Tmz_20200212_zmT"
DATABASE = "online_notebook"
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
isAdministrator=False
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f'<User {self.username}>'
    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'password': self.password}
# login.html登录界面
@app.route("/Notebook/login",methods=['GET'])
def login():
    return render_template("login.html")
@app.route("/Notebook/login",methods=['POST'])
def login_check():
    users=User.query.all()
    for user in users:
        if user.username == request.form['username']:
            if user.password == request.form['password']:
                if user.username=='KevinDb123':
                    global isAdministrator
                    isAdministrator=True
                return redirect(url_for('notebook'))
            else:
                return redirect(url_for('login', message="密码错误!"))
    else:
        return redirect(url_for('login', message="该用户未注册!"))
# register.html 注册界面
@app.route("/Notebook/register",methods=['GET'])
def register():
    return render_template("register.html")
@app.route("/Notebook/register",methods=['POST'])
def register_check():
    username = request.form.get('username')
    password = request.form.get('password')
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return redirect(url_for('register', message="该用户名已被注册!"))
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('register', message="注册成功！"))
#reset_password.html 修改密码
@app.route("/Notebook/repwd",methods=['GET'])
def repwd():
    return render_template("reset_password.html")
@app.route("/Notebook/repwd",methods=['POST'])
def reset_password():
    username = request.form.get('username')
    password = request.form.get('password')
    new_password=request.form.get('new_password')
    user1 = User.query.filter_by(username=username).first()
    if user1:
        if user1.password == password:
            if new_password !=password:
                user1.password = new_password
                db.session.commit()
                return redirect(url_for('repwd',message="修改密码成功！"))
            else:
                return redirect(url_for("repwd",message="新密码不能与原密码相同"))
        else:
            return redirect(url_for("repwd",message="密码错误！"))
    return redirect(url_for("repwd",message="该用户并未注册"))
#deleteUser.html 注销用户
@app.route("/Notebook/deleteUser",methods=['GET'])
def deleteUser():
    return render_template("deleteUser.html")
@app.route("/Notebook/deleteUser",methods=['POST'])
def delete_user():
    username = request.form.get('username')
    password=request.form.get('password')
    repassword=request.form.get('repassword')
    user1=User.query.filter_by(username=username).first()
    if user1:
        if user1.password == password:
            if user1.password == repassword:
                db.session.delete(user1)
                db.session.commit()
                return redirect(url_for("deleteUser",message="已成功注销！"))
            else:
                return redirect(url_for("deleteUser",message="密码错误（密码或确认密码）！"))
        else:
            return redirect(url_for("deleteUser",message="密码错误（密码或确认密码）！"))
    else:
        return redirect(url_for("deleteUser",message="未查询到该用户"))
#管理员查看用户信息
@app.route("/Notebook/UserLists",methods=['GET'])
def UserLists():
    if not isAdministrator:
        print(isAdministrator)
        return '<script>alert("只有管理员才能查看")</script>'
    users=User.query.all()
    user_lists=[user.to_dict() for user in users]
    return render_template("UserLists.html",users=user_lists)
#notebook.html 主页
@app.route("/Notebook/notebook")
def notebook():
    return render_template("notebook.html")
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)