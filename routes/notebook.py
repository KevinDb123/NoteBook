from flask import Blueprint, render_template, request, redirect, url_for,g

notebook_bp = Blueprint('notebook', __name__,template_folder='../templates')

@notebook_bp.route("/homepage", methods=['GET'])
def homepage():
    if g.isLogin:
        return render_template("homepage-login.html", user=g.login_user)
    return render_template("homepage.html")

@notebook_bp.route("/notebook")
def notebook():
    print(g.isLogin)
    if g.isLogin:
        return render_template("notebook.html", user=g.login_user)
    return redirect(url_for('users.login'))
