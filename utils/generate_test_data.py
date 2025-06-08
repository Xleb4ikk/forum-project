import os
import sys
import random
from datetime import datetime, timedelta
import pymysql
from dotenv import load_dotenv

# Добавляем родительскую директорию в путь, чтобы импортировать модули из app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models.db_models import db, User, Profile, Category, Forum, Topic, Post, Comment, Rating

# Загрузка переменных окружения
load_dotenv()

# Тестовые данные
usernames = [
    'user1', 'admin123', 'moderator', 'tester', 'johndoe', 'janedoe', 
    'alex123', 'maria_s', 'peter42', 'techguy', 'coder99', 'dev_master',
    'gamer123', 'music_lover', 'bookreader', 'traveler', 'foodie', 'fitness_pro'
]

domains = ['gmail.com', 'mail.ru', 'yandex.ru', 'outlook.com', 'hotmail.com', 'example.com']

statuses = ['новичок', 'активный', 'продвинутый', 'эксперт', 'модератор']

forum_names = [
    'Технологии', 'Спорт', 'Кино и ТВ', 'Музыка', 'Книги', 'Игры',
    'Путешествия', 'Кулинария', 'Наука', 'Искусство', 'Автомобили', 'Здоровье'
]

topic_templates = [
    'Обсуждение {0}', 'Вопрос про {0}', 'Помогите с {0}', 'Лучшие {0}',
    'Новости: {0}', 'Обзор {0}', 'Как выбрать {0}', '{0}: мнения и отзывы'
]

topic_subjects = [
    'смартфоны', 'ноутбуки', 'игровые консоли', 'фильмы', 'сериалы',
    'книги', 'музыкальные альбомы', 'страны для путешествий', 'рецепты',
    'автомобили', 'спортивное снаряжение', 'научные открытия'
]

post_templates = [
    'Я считаю, что {0} - это отличный выбор для всех, кто интересуется данной темой.',
    'Недавно столкнулся с проблемой при использовании {0}. Кто-нибудь может помочь?',
    'Хочу поделиться своим опытом использования {0}. Очень доволен результатом!',
    'Не могу разобраться с {0}. Подскажите, как лучше подойти к этому вопросу?',
    'По моему мнению, {0} сильно переоценен. Есть гораздо лучшие альтернативы.',
    'Какие есть мнения насчет {0}? Стоит ли тратить время на изучение?',
    'Сравнил несколько вариантов {0} и пришел к выводу, что лучший вариант - это...',
    'Ищу рекомендации по выбору {0}. Какие критерии стоит учитывать?'
]

comment_templates = [
    'Полностью согласен с автором!',
    'Не могу согласиться, у меня совсем другой опыт...',
    'Интересная точка зрения, спасибо за информацию.',
    'А вы пробовали альтернативные варианты?',
    'Можете более подробно рассказать об этом?',
    'У меня была похожая ситуация, решил проблему так: ...',
    'Очень полезная информация, спасибо!',
    'Хотелось бы больше конкретики по вопросу.',
    'А есть какие-то источники, подтверждающие эту информацию?',
    'Интересно, какие еще есть мнения по этому поводу?'
]

def random_date(start_date, end_date):
    """Генерация случайной даты в диапазоне"""
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    return start_date + timedelta(days=random_days)

def generate_test_data(app):
    """Генерация тестовых данных для базы данных"""
    with app.app_context():
        # Проверка, есть ли уже данные в базе
        if User.query.count() > 5:
            print("В базе данных уже есть записи. Генерация тестовых данных отменена.")
            return
        
        # Генерация случайных пользователей
        print("Создаем пользователей...")
        users = []
        for i in range(15):
            username = random.choice(usernames) + str(random.randint(1, 999))
            email = f"{username}@{random.choice(domains)}"
            user = User(имя_пользователя=username, электронная_почта=email)
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        
        # Генерация профилей
        print("Создаем профили пользователей...")
        for user in users:
            start_date = datetime(2020, 1, 1)
            end_date = datetime.now()
            profile = Profile(
                ID_пользователя=user.ID_пользователя,
                статус=random.choice(statuses),
                дата_регистрации=random_date(start_date, end_date)
            )
            db.session.add(profile)
        
        db.session.commit()
        
        # Генерация категорий
        print("Создаем категории...")
        categories = []
        for i, name in enumerate(forum_names[:6]):
            category = Category(
                название=f"Категория: {name}",
                описание=f"Все форумы, связанные с темой '{name}'."
            )
            db.session.add(category)
            categories.append(category)
        
        db.session.commit()
        
        # Генерация форумов
        print("Создаем форумы...")
        forums = []
        for name in forum_names:
            forum = Forum(
                название=name,
                описание=f"Форум для обсуждения всего, что связано с темой '{name}'."
            )
            # Связываем форум с категориями (от 1 до 2 случайных категорий)
            for category in random.sample(categories, random.randint(1, 2)):
                forum.categories.append(category)
            db.session.add(forum)
            forums.append(forum)
        
        db.session.commit()
        
        # Генерация тем
        print("Создаем темы...")
        topics = []
        for forum in forums:
            # Создаем от 3 до 8 тем для каждого форума
            for _ in range(random.randint(3, 8)):
                template = random.choice(topic_templates)
                subject = random.choice(topic_subjects)
                topic_name = template.format(subject)
                start_date = datetime(2022, 1, 1)
                end_date = datetime.now()
                topic = Topic(
                    ID_форума=forum.ID_форума,
                    название=topic_name,
                    дата_создания=random_date(start_date, end_date)
                )
                db.session.add(topic)
                topics.append(topic)
        
        db.session.commit()
        
        # Генерация постов
        print("Создаем посты...")
        posts = []
        for topic in topics:
            # Создаем от 2 до 10 постов для каждой темы
            for _ in range(random.randint(2, 10)):
                template = random.choice(post_templates)
                subject = topic.название.split(':')[-1].strip() if ':' in topic.название else topic.название
                content = template.format(subject)
                
                # Добавляем немного случайного контента для разнообразия
                additional_content = "\n\n" + random.choice([
                    "Буду рад услышать ваши мнения и комментарии!",
                    "Что вы думаете по этому поводу?",
                    "Поделитесь своим опытом, если сталкивались с подобным.",
                    "Интересно, есть ли здесь эксперты по этой теме?",
                    "Надеюсь на конструктивное обсуждение."
                ])
                
                content += additional_content
                
                # Дата публикации после даты создания темы, но не позже сегодня
                post_date = random_date(topic.дата_создания, datetime.now())
                
                post = Post(
                    ID_темы=topic.ID_темы,
                    ID_пользователя=random.choice(users).ID_пользователя,
                    содержимое=content,
                    дата_публикации=post_date
                )
                db.session.add(post)
                posts.append(post)
        
        db.session.commit()
        
        # Генерация комментариев
        print("Создаем комментарии...")
        for post in posts:
            # Создаем от 0 до 5 комментариев для каждого поста
            for _ in range(random.randint(0, 5)):
                comment_text = random.choice(comment_templates)
                # Дата комментария после даты публикации поста
                comment_date = random_date(post.дата_публикации, datetime.now())
                
                comment = Comment(
                    ID_поста=post.ID_поста,
                    ID_пользователя=random.choice(users).ID_пользователя,
                    содержимое=comment_text,
                    дата_отправки=comment_date
                )
                db.session.add(comment)
        
        db.session.commit()
        
        # Генерация оценок
        print("Создаем оценки...")
        for post in posts:
            # Для каждого поста 0-8 пользователей оставляют оценки
            rating_users = random.sample(users, random.randint(0, min(8, len(users))))
            for user in rating_users:
                # Оценка от 1 до 5
                rating_value = random.randint(1, 5)
                rating_comment = None
                # Примерно в 30% случаев добавляем комментарий к оценке
                if random.random() < 0.3:
                    rating_comments = [
                        "Очень полезный пост!",
                        "Интересная информация, спасибо.",
                        "Неплохо, но можно было подробнее.",
                        "Не совсем согласен с автором.",
                        "Отличный материал, очень помог!"
                    ]
                    rating_comment = random.choice(rating_comments)
                
                rating = Rating(
                    ID_поста=post.ID_поста,
                    оценка=rating_value,
                    комментарий=rating_comment
                )
                db.session.add(rating)
        
        db.session.commit()
        
        print("Генерация тестовых данных завершена успешно!")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    generate_test_data(app) 