from flask import Flask, render_template, request, redirect, url_for,jsonify
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
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f'<User {self.username}>'
# login.html登录界面
@app.route("/login",methods=['GET'])
def login():
    return render_template("login.html")
@app.route("/login",methods=['POST'])
def login_check():
    users=User.query.all()
    for user in users:
        if user.username == request.form['username']:
            if user.password == request.form['password']:
                return redirect(url_for('notebook'))
            else:
                return redirect(url_for('login', message="密码错误!"))
    else:
        return redirect(url_for('login', message="该用户未注册!"))
# register.html 注册界面
@app.route("/register",methods=['GET'])
def register():
    return render_template("register.html")
@app.route("/register",methods=['POST'])
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
#notebook.html 主页
@app.route("/notebook")
def notebook():
    return render_template("notebook.html")
if(__name__ == "__main__"):
    with app.app_context():
        db.create_all()
    app.run(debug=True)