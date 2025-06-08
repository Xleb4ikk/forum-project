import sys
import os
from datetime import datetime, timedelta

# Принудительно используем SQLite
os.environ['USE_SQLITE'] = 'true'

# Добавляем родительскую директорию в путь
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.models.db_models import db, User, Forum, Topic, Post, Comment, Category, Rating, Profile

def add_test_data():
    """Добавление тестовых данных в базу"""
    print("Добавление тестовых данных...")
    
    # Создание пользователей
    users = []
    for i in range(1, 6):
        user = User(
            имя_пользователя=f"user{i}",
            электронная_почта=f"user{i}@example.com"
        )
        users.append(user)
        db.session.add(user)
    
    db.session.commit()
    print(f"Создано {len(users)} пользователей")
    
    # Создание профилей пользователей
    for i, user in enumerate(users):
        profile = Profile(
            ID_пользователя=user.ID_пользователя,
            статус="Активный",
            дата_регистрации=datetime.now() - timedelta(days=i*10)
        )
        db.session.add(profile)
    
    db.session.commit()
    print("Созданы профили пользователей")
    
    # Создание категорий
    categories = []
    category_names = ["Технологии", "Спорт", "Наука", "Искусство", "Путешествия"]
    for name in category_names:
        category = Category(
            название=name,
            описание=f"Обсуждение тем, связанных с {name.lower()}"
        )
        categories.append(category)
        db.session.add(category)
    
    db.session.commit()
    print(f"Создано {len(categories)} категорий")
    
    # Создание форумов
    forums = []
    forum_data = [
        {"название": "Программирование", "описание": "Обсуждение языков программирования и разработки", "категории": [0]},
        {"название": "Искусственный интеллект", "описание": "Обсуждение ИИ и машинного обучения", "категории": [0, 2]},
        {"название": "Футбол", "описание": "Обсуждение футбольных матчей и команд", "категории": [1]},
        {"название": "Физика", "описание": "Обсуждение физических теорий и открытий", "категории": [2]},
        {"название": "Живопись", "описание": "Обсуждение живописи и художников", "категории": [3]},
        {"название": "Европа", "описание": "Обсуждение путешествий по Европе", "категории": [4]}
    ]
    
    for data in forum_data:
        forum = Forum(
            название=data["название"],
            описание=data["описание"]
        )
        db.session.add(forum)
        db.session.flush()  # Чтобы получить ID форума
        
        # Связывание форума с категориями
        for cat_index in data["категории"]:
            if cat_index < len(categories):
                forum.categories.append(categories[cat_index])
        
        forums.append(forum)
    
    db.session.commit()
    print(f"Создано {len(forums)} форумов")
    
    # Создание тем
    topics = []
    for i, forum in enumerate(forums):
        for j in range(1, 4):  # 3 темы для каждого форума
            topic = Topic(
                ID_форума=forum.ID_форума,
                название=f"Тема {j} в форуме {forum.название}",
                дата_создания=datetime.now() - timedelta(days=i+j)
            )
            topics.append(topic)
            db.session.add(topic)
    
    db.session.commit()
    print(f"Создано {len(topics)} тем")
    
    # Создание постов
    posts = []
    for i, topic in enumerate(topics):
        for j in range(1, 4):  # 3 поста для каждой темы
            user_index = (i + j) % len(users)
            post = Post(
                ID_темы=topic.ID_темы,
                ID_пользователя=users[user_index].ID_пользователя,
                содержимое=f"Это содержимое поста {j} в теме '{topic.название}'. Добавлено пользователем {users[user_index].имя_пользователя}.",
                дата_публикации=datetime.now() - timedelta(days=i, hours=j)
            )
            posts.append(post)
            db.session.add(post)
    
    db.session.commit()
    print(f"Создано {len(posts)} постов")
    
    # Создание комментариев
    for i, post in enumerate(posts):
        for j in range(1, 3):  # 2 комментария для каждого поста
            user_index = (i + j + 1) % len(users)
            comment = Comment(
                ID_поста=post.ID_поста,
                ID_пользователя=users[user_index].ID_пользователя,
                содержимое=f"Это комментарий {j} к посту. Добавлен пользователем {users[user_index].имя_пользователя}.",
                дата_отправки=datetime.now() - timedelta(hours=j)
            )
            db.session.add(comment)
    
    db.session.commit()
    print("Созданы комментарии")
    
    # Создание рейтингов
    for i, post in enumerate(posts):
        for j in range(1, 4):  # 3 рейтинга для каждого поста
            rating = Rating(
                ID_поста=post.ID_поста,
                оценка=(i + j) % 5 + 1,  # Оценка от 1 до 5
                комментарий=f"Рейтинг {j} для поста {i+1}"
            )
            db.session.add(rating)
    
    db.session.commit()
    print("Созданы рейтинги")
    
    print("Тестовые данные успешно добавлены!")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        add_test_data() 