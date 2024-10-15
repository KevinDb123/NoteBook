from flask import Blueprint, render_template, request, redirect, url_for,g
from models import User
from exts import db

admin_bp = Blueprint('admin', __name__,template_folder='../templates')
@admin_bp.route("/UserLists",methods=['GET'])
def UserLists():
    if not g.isAdministrator:
        return '<script>alert("只有管理员才能查看")</script>'
    users=User.query.all()
    user_lists=[user.to_dict() for user in users]
    return render_template("UserLists.html",users=user_lists)