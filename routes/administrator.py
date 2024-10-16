from flask import Blueprint, render_template, request, redirect, url_for,g,render_template_string,jsonify
from models import User,Notes
from exts import db

admin_bp = Blueprint('admin', __name__,template_folder='../templates')
@admin_bp.route("/UserLists",methods=['GET'])
def UserLists():
    if not g.isAdministrator:
        return '<script>alert("只有管理员才能查看")</script>'
    users=User.query.all()
    user_lists=[user.to_dict() for user in users]
    return render_template("UserLists.html",users=user_lists)
#管理员给用户修改密码
@admin_bp.route("/Admin_repwd/<username>",methods=['GET'])
def Admin_repwd(username):
    return render_template("Admin_repwd.html",username=username)
@admin_bp.route("/Admin_repwd/<username>",methods=['POST'])
def Admin_rep(username):
    new_password=request.form.get("newPassword")
    user1=User.query.filter_by(username=username).first()
    if user1:
        user1.password = new_password
        db.session.commit()
    return redirect(url_for('admin.UserLists'))
# 删除用户
@admin_bp.route("/Admin_deleteUser/<username>", methods=['POST'])
def Admin_deleteUser(username):
    user1 = User.query.filter_by(username=username).first()
    if user1:
        if user1.administrator:
            return jsonify({"message": "管理员的账号不可被注销！"}), 405
        else:
            Notes.query.filter_by(author_id=user1.id).delete()
            db.session.delete(user1)
            db.session.commit()
            return jsonify({"message": "用户已成功注销！"}), 200
    else:
        return jsonify({"message": "用户不存在！"}), 404