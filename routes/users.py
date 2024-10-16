from exts import db
from models import User,Notes
from flask import Blueprint, Flask, render_template, request, redirect, url_for, g, session, jsonify

users_bp=Blueprint('users',__name__,template_folder='../templates')
@users_bp.route("/login", methods=['GET'])
def login():
    if not g.isLogin:
        return render_template("login.html")
    return "<script>alert('您已经登录过了！')</script>"


@users_bp.route("/login", methods=['POST'])
def login_check():
    users = User.query.all()
    for user in users:
        if user.username == request.form['username']:
            if user.password == request.form['password']:
                if user.administrator==True:
                    session['isAdministrator'] = True
                session['isLogin'] = True
                session['login_user'] = user.username
                return jsonify({"message":"登录成功！", "redirect_url": url_for('notebook.upload_note')}), 200
            else:
                return jsonify({"message":"密码错误！"}),401
    return jsonify({"message":"未查询到该用户！"}),404


@users_bp.route("/register", methods=['GET'])
def register():
    return render_template("register.html")


@users_bp.route("/register", methods=['POST'])
def register_check():
    username = request.form.get('username')
    password = request.form.get('password')
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message":"该用户已被注册！"}),409

    new_user = User(username=username, password=password,administrator=False,note_numbers=0)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"注册成功！"}),200


@users_bp.route("/logout", methods=['GET'])
def logout():
    session['isLogin'] = False
    session['isAdministrator']=False
    session['login_user'] = None
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
                return jsonify({"message":"修改密码成功！"}),200
            else:
                return jsonify({"message":"新密码不能与原密码相同"}),400
        else:
            return jsonify({"message":"密码错误！"}),401
    return jsonify({"message":"未查询到该用户"}),404

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
                notes=Notes.query.filter_by(author_id=user1.id).all()
                for note in notes:
                    db.session.delete(note)
                db.session.delete(user1)
                db.session.commit()
                session['isLogin'] = False
                session['isAdministrator'] = False
                session['login_user'] = None
                return jsonify({"message":"已成功注销！"}),200
            else:
                return jsonify({"message":"密码错误！"}),401
        else:
            return jsonify({"message":"密码错误！"}),401
    else:
        return jsonify({"message":"未查询到该用户！"}),404