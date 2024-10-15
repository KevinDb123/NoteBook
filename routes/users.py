from exts import db
from models import User
from flask import Blueprint,Flask, render_template, request, redirect, url_for,g

users_bp=Blueprint('users',__name__,template_folder='../templates')
@users_bp.route("/login", methods=['GET'])
def login():
    return render_template("login.html")


@users_bp.route("/login", methods=['POST'])
def login_check():
    users = User.query.all()
    for user in users:
        if user.username == request.form['username']:
            if user.password == request.form['password']:
                if user.username == 'KevinDb123':
                    g.isAdministrator = True
                g.isLogin = True
                g.login_user = user.username
                return redirect(url_for('notebook.notebook'))
            else:
                return redirect(url_for('users.login', message="密码错误!"))
    return redirect(url_for('users.login', message="该用户未注册!"))


@users_bp.route("/register", methods=['GET'])
def register():
    return render_template("register.html")


@users_bp.route("/register", methods=['POST'])
def register_check():
    username = request.form.get('username')
    password = request.form.get('password')
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return redirect(url_for('users.register', message="该用户名已被注册!"))

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('users.register', message="注册成功！"))


@users_bp.route("/logout", methods=['GET'])
def logout():
    g.isLogin = False
    g.isAdministrator = False
    g.login_user = 0
    return redirect(url_for('notebook.homepage'))

@users_bp.route("/repwd",methods=['GET'])
def repwd():
    return render_template("reset_password.html")
@users_bp.route("/repwd",methods=['POST'])
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
                return redirect(url_for('users.repwd',message="修改密码成功！"))
            else:
                return redirect(url_for("users.repwd",message="新密码不能与原密码相同"))
        else:
            return redirect(url_for("users.repwd",message="密码错误！"))
    return redirect(url_for("users.repwd",message="该用户并未注册"))

#deleteUser.html 注销用户
@users_bp.route("/deleteUser",methods=['GET'])
def deleteUser():
    return render_template("deleteUser.html")
@users_bp.route("/deleteUser",methods=['POST'])
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
                g.isLogin = False
                return redirect(url_for("users.deleteUser",message="已成功注销！"))
            else:
                return redirect(url_for("users.deleteUser",message="密码错误（密码或确认密码）！"))
        else:
            return redirect(url_for("users.deleteUser",message="密码错误（密码或确认密码）！"))
    else:
        return redirect(url_for("users.deleteUser",message="未查询到该用户"))