from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/register")
def user_register():
    return render_template("register.html")
login_data={
    "张三":"123456"
}
@app.route("/login",methods=["post"])
def login():
    name=request.form.get("username")
    pwd=request.form.get("password")
    if name in login_data.keys():
        if pwd==login_data[name]:
            return "登录成功"
        else:
            return '密码错误 <a href="/">返回登录</a>'
    else:
        return '用户不存在 <a href="/">返回登录</a>'
@app.route("/register",methods=["post"])
def register():
    name=request.form.get("username")
    pwd=request.form.get("password")
    if name in login_data.keys():
        return '用户已经存在 <a href="/">返回登录</a>'
    else:
        login_data[name]=pwd
        return redirect(url_for("index"))
if __name__ == "__main__":
    app.run(debug=True)