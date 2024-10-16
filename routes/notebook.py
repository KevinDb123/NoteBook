from flask import Blueprint, render_template, request, redirect, url_for,g,abort,jsonify
from models import User,Notes
import markdown2
from datetime import datetime
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from exts import db
notebook_bp = Blueprint('notebook', __name__,template_folder='../templates')
notes={}
def highlight_code_block(code, language):
    try:
        lexer = get_lexer_by_name(language)
    except:
        lexer = get_lexer_by_name("text")
    formatter = HtmlFormatter()
    return highlight(code, lexer, formatter)

def render_markdown(content):
    html_content = markdown2.markdown(content, extras=["fenced-code-blocks", "code-friendly"])
    def replace_code_blocks(match):
        code_block = match.group(1)
        code_lines = code_block.split('\n', 1)
        if len(code_lines) == 2:
            language, code = code_lines[0], code_lines[1]
        else:
            language, code = "", code_lines[0]
        return highlight_code_block(code, language)
    import re
    pattern = r'<pre><code class="language-(\w+)">(.*?)</code></pre>'
    highlighted_content = re.sub(pattern, lambda match: replace_code_blocks(match), html_content, flags=re.DOTALL)

    return highlighted_content

@notebook_bp.route("/homepage", methods=['GET'])
def homepage():
    if g.isLogin:
        if g.isAdministrator:
            return render_template("homepage-admin.html", user=g.login_user)
        return render_template("homepage-login.html", user=g.login_user)
    return render_template("homepage.html")

@notebook_bp.route("/upload_note", methods=['GET'])
def upload_note():
    if g.isLogin:
        user1=User.query.filter_by(username=g.login_user).first()
        if user1:
            return render_template("upload_note.html",username=user1.username,num=user1.note_numbers+1)
    return redirect(url_for('users.login'))

@notebook_bp.route("/upload_note", methods=['POST'])
def upload_note_post():
    if g.isLogin:
        title = request.form.get("note_title")
        content = request.form.get("note_content")
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content_html = render_markdown(content)
        user1=User.query.filter_by(username=g.login_user).first()
        author_id=user1.id
        new_note = Notes(
            author_id=author_id,
            title=title,
            content=content,
            update_time=update_time
        )
        db.session.add(new_note)
        db.session.commit()
        user1.note_numbers=user1.note_numbers+1
        db.session.commit()
        return redirect(url_for('notebook.upload_note'))


@notebook_bp.route("/view_note/<int:note_id>")
def view_note(note_id):
    if g.isLogin:
        note1 = Notes.query.filter_by(note_id=note_id).first()
        if note1:
            note_dict = note1.to_dict()
            user1=User.query.filter_by(id=note1.author_id).first()
            note_dict['content']=render_markdown(note_dict['content'])
            note_dict['username']=user1.username
            return render_template("viewnote.html", note=note_dict)
        else:
            abort(404)
    else:
        abort(403)

# 查看所有笔记
@notebook_bp.route("/allNotes/<username>")
def allNotes(username):
    user2=User.query.filter_by(username=username).first()
    if user2:
        if g.isLogin:
            user1=User.query.filter_by(username=g.login_user).first()
            if username==g.login_user or user1.administrator:
                user1 = User.query.filter_by(username=username).first()
                if user1:
                    user1_id = user1.id
                    notes1 = Notes.query.filter_by(author_id=user1_id).all()
                    notes_info = [note.to_dict() for note in notes1]
                    return render_template("allNotes.html", notes=notes_info,username=username)
        return "<script>alert('您没有权限访问该用户的所有笔记！')</script>"
    return "<script>alert('未找到该用户！')</script>"

@notebook_bp.route("/deleteNote/<int:note_id>",methods=['POST'])
def deleteNote(note_id):
    note1=Notes.query.filter_by(note_id=note_id).first()
    if note1:
        user1=User.query.filter_by(id=note1.author_id).first()
        if user1:
            user1.note_numbers=user1.note_numbers-1
        db.session.delete(note1)
        db.session.commit()
        return jsonify({"message":"删除成功！"}),200