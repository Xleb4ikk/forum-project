import os
os.environ['DB_NAME'] = 'forumdb'

from app import create_app
from app.models.db_models import db, Forum, Topic, User, Post, Comment

app = create_app()

with app.app_context():
    print("Проверка содержимого базы данных...")
    
    # Проверка форумов
    forums = Forum.query.all()
    print(f"Найдено {len(forums)} форумов:")
    for forum in forums:
        print(f" - {forum.название}: {forum.описание}")
    
    # Проверка тем
    topics = Topic.query.all()
    print(f"\nНайдено {len(topics)} тем:")
    for topic in topics[:5]:  # Показать только первые 5
        print(f" - {topic.название} (ID форума: {topic.ID_форума})")
    if len(topics) > 5:
        print(f"   ... и еще {len(topics) - 5} тем")
    
    # Проверка пользователей
    users = User.query.all()
    print(f"\nНайдено {len(users)} пользователей:")
    for user in users[:5]:  # Показать только первые 5
        print(f" - {user.имя_пользователя} ({user.электронная_почта})")
    if len(users) > 5:
        print(f"   ... и еще {len(users) - 5} пользователей")
    
    # Проверка постов
    posts = Post.query.all()
    print(f"\nНайдено {len(posts)} постов:")
    for post in posts[:3]:  # Показать только первые 3
        print(f" - ID: {post.ID_поста}, Тема: {post.ID_темы}, Пользователь: {post.ID_пользователя}")
        print(f"   Содержимое: {post.содержимое[:50]}...")
    if len(posts) > 3:
        print(f"   ... и еще {len(posts) - 3} постов")
    
    # Проверка комментариев
    comments = Comment.query.all()
    print(f"\nНайдено {len(comments)} комментариев:")
    for comment in comments[:3]:  # Показать только первые 3
        print(f" - ID: {comment.ID_комментария}, Пост: {comment.ID_поста}, Пользователь: {comment.ID_пользователя}")
        print(f"   Содержимое: {comment.содержимое[:50]}...")
    if len(comments) > 3:
        print(f"   ... и еще {len(comments) - 3} комментариев") 