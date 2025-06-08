from sqlalchemy import func, desc, extract, case, and_, or_, distinct, literal_column, literal, text
from datetime import datetime, timedelta

from app.models.db_models import db, User, Post, Comment, Rating, Topic, Forum, Category, Profile

class AnalyticsManager:
    """Модуль для выполнения аналитических запросов к базе данных форума"""
    
    @staticmethod
    def get_top_rated_posts(limit=10, min_rating=0):
        """Получить посты с самыми высокими средними оценками"""
        return db.session.query(
            Post,
            User.имя_пользователя.label('author_name'),
            Topic.название.label('topic_name'),
            Forum.название.label('forum_name'),
            func.avg(Rating.оценка).label('avg_rating'),
            func.count(Rating.ID_рейтинга).label('rating_count')
        ).join(
            User, Post.ID_пользователя == User.ID_пользователя
        ).join(
            Topic, Post.ID_темы == Topic.ID_темы
        ).join(
            Forum, Topic.ID_форума == Forum.ID_форума
        ).join(
            Rating, Post.ID_поста == Rating.ID_поста
        ).group_by(
            Post.ID_поста, User.имя_пользователя, Topic.название, Forum.название
        ).having(
            func.avg(Rating.оценка) >= min_rating
        ).order_by(
            func.avg(Rating.оценка).desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_user_activity(limit=10, days=None):
        """Получить статистику активности пользователей"""
        query = db.session.query(
            User,
            func.count(Post.ID_поста).label('post_count'),
            func.count(Comment.ID_комментария).label('comment_count'),
            (func.count(Post.ID_поста) + func.count(Comment.ID_комментария)).label('total_activity')
        ).outerjoin(
            Post, User.ID_пользователя == Post.ID_пользователя
        ).outerjoin(
            Comment, User.ID_пользователя == Comment.ID_пользователя
        )
        
        # Если указано количество дней, фильтруем по датам
        if days:
            start_date = datetime.now() - timedelta(days=days)
            query = query.filter(
                or_(
                    Post.дата_публикации >= start_date,
                    Comment.дата_отправки >= start_date
                )
            )
            
        return query.group_by(
            User.ID_пользователя
        ).order_by(
            desc('total_activity')
        ).limit(limit).all()
    
    @staticmethod
    def get_topic_statistics(limit=10):
        """Получить статистику по темам форума"""
        return db.session.query(
            Topic,
            Forum.название.label('forum_name'),
            func.count(Post.ID_поста).label('post_count'),
            func.count(Comment.ID_комментария).label('comment_count'),
            func.avg(Rating.оценка).label('avg_rating'),
            func.min(Post.дата_публикации).label('first_post_date'),
            func.max(Post.дата_публикации).label('last_post_date')
        ).join(
            Forum, Topic.ID_форума == Forum.ID_форума
        ).outerjoin(
            Post, Topic.ID_темы == Post.ID_темы
        ).outerjoin(
            Comment, Post.ID_поста == Comment.ID_поста
        ).outerjoin(
            Rating, Post.ID_поста == Rating.ID_поста
        ).group_by(
            Topic.ID_темы, Forum.название
        ).order_by(
            desc('post_count')
        ).limit(limit).all()
    
    @staticmethod
    def get_activity_by_time(days=30, interval='day'):
        """Получить активность пользователей по времени"""
        start_date = datetime.now() - timedelta(days=days)
        
        # Используем более простой подход с прямыми запросами к базе данных
        if interval == 'hour':
            # Активность постов по часам
            hour_expr = extract('hour', Post.дата_публикации).cast(db.Integer).label('period')
            posts_by_hour = db.session.query(
                hour_expr,
                func.count().label('count'),
                literal('post').label('type')
            ).filter(
                Post.дата_публикации >= start_date
            ).group_by(
                hour_expr
            )
            
            # Активность комментариев по часам
            hour_comment_expr = extract('hour', Comment.дата_отправки).cast(db.Integer).label('period')
            comments_by_hour = db.session.query(
                hour_comment_expr,
                func.count().label('count'),
                literal('comment').label('type')
            ).filter(
                Comment.дата_отправки >= start_date
            ).group_by(
                hour_comment_expr
            )
            
            # Объединяем результаты
            result = posts_by_hour.union_all(comments_by_hour).order_by('period').all()
            
        elif interval == 'day':
            # Активность постов по дням
            day_expr = extract('day', Post.дата_публикации).cast(db.Integer).label('period')
            posts_by_day = db.session.query(
                day_expr,
                func.count().label('count'),
                literal('post').label('type')
            ).filter(
                Post.дата_публикации >= start_date
            ).group_by(
                day_expr
            )
            
            # Активность комментариев по дням
            day_comment_expr = extract('day', Comment.дата_отправки).cast(db.Integer).label('period')
            comments_by_day = db.session.query(
                day_comment_expr,
                func.count().label('count'),
                literal('comment').label('type')
            ).filter(
                Comment.дата_отправки >= start_date
            ).group_by(
                day_comment_expr
            )
            
            # Объединяем результаты
            result = posts_by_day.union_all(comments_by_day).order_by('period').all()
            
        elif interval == 'month':
            # Активность постов по месяцам
            month_expr = extract('month', Post.дата_публикации).cast(db.Integer).label('period')
            posts_by_month = db.session.query(
                month_expr,
                func.count().label('count'),
                literal('post').label('type')
            ).filter(
                Post.дата_публикации >= start_date
            ).group_by(
                month_expr
            )
            
            # Активность комментариев по месяцам
            month_comment_expr = extract('month', Comment.дата_отправки).cast(db.Integer).label('period')
            comments_by_month = db.session.query(
                month_comment_expr,
                func.count().label('count'),
                literal('comment').label('type')
            ).filter(
                Comment.дата_отправки >= start_date
            ).group_by(
                month_comment_expr
            )
            
            # Объединяем результаты
            result = posts_by_month.union_all(comments_by_month).order_by('period').all()
            
        else:
            raise ValueError("Интервал должен быть 'hour', 'day' или 'month'")
            
        return result
    
    @staticmethod
    def get_category_statistics():
        """Получить статистику по категориям"""
        return db.session.query(
            Category,
            func.count(distinct(Forum.ID_форума)).label('forum_count'),
            func.count(distinct(Topic.ID_темы)).label('topic_count'),
            func.count(distinct(Post.ID_поста)).label('post_count')
        ).outerjoin(
            db.session.query(Forum, Category)
            .join(
                db.Table('форум_категория'),
                Forum.ID_форума == db.Table('форум_категория').c.ID_форума
            )
            .filter(
                db.Table('форум_категория').c.ID_категории == Category.ID_категории
            ).subquery()
        ).outerjoin(
            Topic, Forum.ID_форума == Topic.ID_форума
        ).outerjoin(
            Post, Topic.ID_темы == Post.ID_темы
        ).group_by(
            Category.ID_категории
        ).order_by(
            desc('post_count')
        ).all() 