from datetime import datetime
from app import login, db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __sal = "Esto es la sal del cetys"
    id = db.Column(db.Integer, primary_key=True)
    """index te ayuda a encontrar tus datos,
        Unique es para que no se repite"""
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author',lazy='dynamic')

    def set_password(self, password_text):
        self.password_hash = generate_password_hash(password_text + self.__sal)

    def check_password(self, password_text):
        return check_password_hash(self.password_hash, password_text+ self.__sal)

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    """El timestamp se indexará, lo cual es útil si desea recuperar publicaciones en orden cronológico. También he agregado un valor predeterminado
    argumento, y pasó la función datetime.utcnow."""
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post {self.body}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
