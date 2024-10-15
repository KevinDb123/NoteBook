from exts import db
#用户的基本信息：id，用户名，密码
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f'<User {self.username}>'
    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'password': self.password}