from sympy.categories.baseclasses import Class
from exts import db
#用户的基本信息：id，用户名，密码
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    note_numbers=db.Column(db.Integer, nullable=False,default=0)
    administrator = db.Column(db.Boolean, nullable=False, default=False)
    def __repr__(self):
        return f'<User {self.username}>'
    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'password': self.password}

class Notes(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return f'<Note {self.note_id}>'
    def to_dict(self):
        return {'note_id': self.note_id, 'author_id': self.author_id, 'title': self.title,'content': self.content,'update_time': self.update_time}