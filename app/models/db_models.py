from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# Association table for forum_category
forum_category = db.Table(
    'форум_категория',
    db.Column('ID_форума', db.Integer, db.ForeignKey('форум.ID_форума'), primary_key=True),
    db.Column('ID_категории', db.Integer, db.ForeignKey('категория.ID_категории'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'пользователь'
    
    ID_пользователя = db.Column(db.Integer, primary_key=True)
    имя_пользователя = db.Column(db.String(255), nullable=False)
    электронная_почта = db.Column(db.String(255), nullable=False, unique=True)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True)
    profile = db.relationship('Profile', backref='user', lazy=True, uselist=False)
    
    def __repr__(self):
        return f'<User {self.имя_пользователя}>'

class Profile(db.Model):
    __tablename__ = 'профиль'
    
    ID_профиля = db.Column(db.Integer, primary_key=True)
    ID_пользователя = db.Column(db.Integer, db.ForeignKey('пользователь.ID_пользователя'), nullable=False)
    статус = db.Column(db.String(255))
    дата_регистрации = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Profile {self.ID_профиля}>'

class Category(db.Model):
    __tablename__ = 'категория'
    
    ID_категории = db.Column(db.Integer, primary_key=True)
    название = db.Column(db.String(255), nullable=False)
    описание = db.Column(db.Text)
    
    # Relationships
    forums = db.relationship('Forum', secondary=forum_category, backref='categories')
    
    def __repr__(self):
        return f'<Category {self.название}>'

class Forum(db.Model):
    __tablename__ = 'форум'
    
    ID_форума = db.Column(db.Integer, primary_key=True)
    название = db.Column(db.String(255), nullable=False)
    описание = db.Column(db.Text)
    
    # Relationships
    topics = db.relationship('Topic', backref='forum', lazy=True)
    
    def __repr__(self):
        return f'<Forum {self.название}>'

class Topic(db.Model):
    __tablename__ = 'тема'
    
    ID_темы = db.Column(db.Integer, primary_key=True)
    ID_форума = db.Column(db.Integer, db.ForeignKey('форум.ID_форума'), nullable=False)
    название = db.Column(db.String(255), nullable=False)
    дата_создания = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='topic', lazy=True)
    
    def __repr__(self):
        return f'<Topic {self.название}>'

class Post(db.Model):
    __tablename__ = 'пост'
    
    ID_поста = db.Column(db.Integer, primary_key=True)
    ID_темы = db.Column(db.Integer, db.ForeignKey('тема.ID_темы'), nullable=False)
    ID_пользователя = db.Column(db.Integer, db.ForeignKey('пользователь.ID_пользователя'), nullable=False)
    содержимое = db.Column(db.Text, nullable=False)
    дата_публикации = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    ratings = db.relationship('Rating', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)
    
    def __repr__(self):
        return f'<Post {self.ID_поста}>'

class Rating(db.Model):
    __tablename__ = 'рейтинг'
    
    ID_рейтинга = db.Column(db.Integer, primary_key=True)
    ID_поста = db.Column(db.Integer, db.ForeignKey('пост.ID_поста'), nullable=False)
    оценка = db.Column(db.Integer)
    комментарий = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Rating {self.ID_рейтинга}>'

class Comment(db.Model):
    __tablename__ = 'комментарий'
    
    ID_комментария = db.Column(db.Integer, primary_key=True)
    ID_поста = db.Column(db.Integer, db.ForeignKey('пост.ID_поста'), nullable=False)
    ID_пользователя = db.Column(db.Integer, db.ForeignKey('пользователь.ID_пользователя'), nullable=False)
    содержимое = db.Column(db.Text, nullable=False)
    дата_отправки = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship for the user who wrote the comment
    author = db.relationship('User', backref='comments')
    
    def __repr__(self):
        return f'<Comment {self.ID_комментария}>' 