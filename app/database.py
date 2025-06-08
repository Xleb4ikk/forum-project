from app.models.db_models import db, User, Forum, Topic, Post, Rating, Comment, Category, Profile
from sqlalchemy import func
from datetime import datetime

class DatabaseManager:
    @staticmethod
    def get_forums():
        """Get all forums with their categories"""
        return Forum.query.all()
    
    @staticmethod
    def get_forum(forum_id):
        """Get a specific forum by ID"""
        return Forum.query.get_or_404(forum_id)
    
    @staticmethod
    def get_topics(forum_id):
        """Get all topics for a specific forum"""
        return Topic.query.filter_by(ID_форума=forum_id).all()
    
    @staticmethod
    def get_topic(topic_id):
        """Get a specific topic by ID"""
        return Topic.query.get_or_404(topic_id)
    
    @staticmethod
    def get_posts(topic_id):
        """Get all posts for a specific topic with authors"""
        return db.session.query(
            Post,
            User.имя_пользователя
        ).join(
            User,
            Post.ID_пользователя == User.ID_пользователя
        ).filter(
            Post.ID_темы == topic_id
        ).all()
    
    @staticmethod
    def get_post(post_id):
        """Get a specific post by ID with author"""
        return db.session.query(
            Post,
            User.имя_пользователя
        ).join(
            User,
            Post.ID_пользователя == User.ID_пользователя
        ).filter(
            Post.ID_поста == post_id
        ).first_or_404()
    
    @staticmethod
    def get_post_with_comments(post_id):
        """Get a post with its comments and comment authors"""
        post = Post.query.get_or_404(post_id)
        comments = db.session.query(
            Comment,
            User.имя_пользователя
        ).join(
            User,
            Comment.ID_пользователя == User.ID_пользователя
        ).filter(
            Comment.ID_поста == post_id
        ).all()
        
        return post, comments
    
    @staticmethod
    def create_forum(name, description):
        """Create a new forum"""
        forum = Forum(название=name, описание=description)
        db.session.add(forum)
        db.session.commit()
        return forum
    
    @staticmethod
    def create_topic(forum_id, name):
        """Create a new topic in a forum"""
        # Ensure forum_id is not None
        if forum_id is None:
            raise ValueError("ID_форума не может быть None")
        topic = Topic(ID_форума=forum_id, название=name)
        db.session.add(topic)
        db.session.commit()
        return topic
    
    @staticmethod
    def create_post(topic_id, user_id, content):
        """Create a new post in a topic"""
        # Ensure topic_id and user_id are not None
        if topic_id is None or user_id is None:
            raise ValueError("ID_темы и ID_пользователя не могут быть None")
        post = Post(ID_темы=topic_id, ID_пользователя=user_id, содержимое=content)
        db.session.add(post)
        db.session.commit()
        return post
    
    @staticmethod
    def update_post(post_id, content):
        """Update an existing post"""
        post = Post.query.get_or_404(post_id)
        post.содержимое = content
        db.session.commit()
        return post
    
    @staticmethod
    def delete_post(post_id):
        """Delete a post"""
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
    
    @staticmethod
    def create_comment(post_id, user_id, content):
        """Create a new comment on a post"""
        # Ensure post_id and user_id are not None
        if post_id is None or user_id is None:
            raise ValueError("ID_поста и ID_пользователя не могут быть None")
        comment = Comment(ID_поста=post_id, ID_пользователя=user_id, содержимое=content)
        db.session.add(comment)
        db.session.commit()
        return comment
    
    @staticmethod
    def update_comment(comment_id, content):
        """Update an existing comment"""
        comment = Comment.query.get_or_404(comment_id)
        comment.содержимое = content
        db.session.commit()
        return comment
    
    @staticmethod
    def delete_comment(comment_id):
        """Delete a comment"""
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
    
    @staticmethod
    def rate_post(post_id, rating, comment=None):
        """Rate a post"""
        # Ensure post_id is not None
        if post_id is None:
            raise ValueError("ID_поста не может быть None")
        post_rating = Rating(ID_поста=post_id, оценка=rating, комментарий=comment)
        db.session.add(post_rating)
        db.session.commit()
        return post_rating
    
    # Analytical queries
    @staticmethod
    def get_top_rated_posts(limit=10):
        """Get top rated posts with their average rating and author names"""
        return db.session.query(
            Post,
            User.имя_пользователя.label('author_name'),
            func.avg(Rating.оценка).label('avg_rating')
        ).join(
            User,
            Post.ID_пользователя == User.ID_пользователя
        ).join(
            Rating,
            Post.ID_поста == Rating.ID_поста
        ).group_by(
            Post.ID_поста,
            User.имя_пользователя
        ).order_by(
            func.avg(Rating.оценка).desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_user_activity(limit=10):
        """Get users with their post and comment counts, ordered by activity"""
        return db.session.query(
            User,
            func.count(Post.ID_поста).label('post_count'),
            func.count(Comment.ID_комментария).label('comment_count')
        ).outerjoin(
            Post,
            User.ID_пользователя == Post.ID_пользователя
        ).outerjoin(
            Comment,
            User.ID_пользователя == Comment.ID_пользователя
        ).group_by(
            User.ID_пользователя
        ).order_by(
            (func.count(Post.ID_поста) + func.count(Comment.ID_комментария)).desc()
        ).limit(limit).all() 
        
    @staticmethod
    def create_profile(user_id, status, date=None):
        """Create a new user profile"""
        # Ensure user_id is not None
        if user_id is None:
            raise ValueError("ID_пользователя не может быть None")
        profile = Profile(ID_пользователя=user_id, статус=status, дата_регистрации=date or datetime.utcnow())
        db.session.add(profile)
        db.session.commit()
        return profile