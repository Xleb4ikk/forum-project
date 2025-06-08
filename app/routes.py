from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import DatabaseManager
from app.analytics import AnalyticsManager
from app.models.db_models import db, User

# Create a blueprint
main_bp = Blueprint('main', __name__)

# Set a default user for demo purposes
DEFAULT_USER_ID = 1

@main_bp.route('/')
def index():
    """Home page showing forums"""
    forums = DatabaseManager.get_forums()
    return render_template('index.html', forums=forums)

@main_bp.route('/forum/<int:forum_id>')
def forum(forum_id):
    """Show topics in a forum"""
    forum = DatabaseManager.get_forum(forum_id)
    topics = DatabaseManager.get_topics(forum_id)
    return render_template('forum.html', forum=forum, topics=topics)

@main_bp.route('/topic/<int:topic_id>')
def topic(topic_id):
    """Show posts in a topic"""
    topic = DatabaseManager.get_topic(topic_id)
    posts = DatabaseManager.get_posts(topic_id)
    return render_template('topic.html', topic=topic, posts=posts)

@main_bp.route('/post/<int:post_id>')
def post(post_id):
    """Show a post and its comments"""
    post_data, comments = DatabaseManager.get_post_with_comments(post_id)
    return render_template('post.html', post=post_data, comments=comments)

@main_bp.route('/create_post/<int:topic_id>', methods=['GET', 'POST'])
def create_post(topic_id):
    """Create a new post in a topic"""
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            DatabaseManager.create_post(topic_id, DEFAULT_USER_ID, content)
            return redirect(url_for('main.topic', topic_id=topic_id))
    
    topic = DatabaseManager.get_topic(topic_id)
    return render_template('create_post.html', topic=topic)

@main_bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    """Edit an existing post"""
    post_data, _ = DatabaseManager.get_post(post_id)
    
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            DatabaseManager.update_post(post_id, content)
            return redirect(url_for('main.post', post_id=post_id))
    
    return render_template('edit_post.html', post=post_data)

@main_bp.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    """Delete a post"""
    post_data = DatabaseManager.get_post(post_id)
    topic_id = post_data[0].ID_темы
    DatabaseManager.delete_post(post_id)
    return redirect(url_for('main.topic', topic_id=topic_id))

@main_bp.route('/create_comment/<int:post_id>', methods=['POST'])
def create_comment(post_id):
    """Create a new comment on a post"""
    content = request.form.get('content')
    if content:
        DatabaseManager.create_comment(post_id, DEFAULT_USER_ID, content)
    return redirect(url_for('main.post', post_id=post_id))

@main_bp.route('/rate_post/<int:post_id>', methods=['POST'])
def rate_post(post_id):
    """Rate a post"""
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    if rating:
        DatabaseManager.rate_post(post_id, int(rating), comment)
    return redirect(url_for('main.post', post_id=post_id))

# Базовые аналитические маршруты
@main_bp.route('/analytics/top_posts')
def top_posts():
    """Show top rated posts"""
    limit = request.args.get('limit', 10, type=int)
    min_rating = request.args.get('min_rating', 0, type=float)
    posts = AnalyticsManager.get_top_rated_posts(limit, min_rating)
    return render_template('analytics/top_posts.html', posts=posts, limit=limit, min_rating=min_rating)

@main_bp.route('/analytics/user_activity')
def user_activity():
    """Show user activity"""
    limit = request.args.get('limit', 10, type=int)
    days = request.args.get('days', None, type=int)
    users = AnalyticsManager.get_user_activity(limit, days)
    return render_template('analytics/user_activity.html', users=users, limit=limit, days=days)

# Расширенные аналитические маршруты
@main_bp.route('/analytics/topic_statistics')
def topic_statistics():
    """Show topic statistics"""
    limit = request.args.get('limit', 10, type=int)
    topics = AnalyticsManager.get_topic_statistics(limit)
    return render_template('analytics/topic_statistics.html', topics=topics, limit=limit)

@main_bp.route('/analytics/time_activity')
def time_activity():
    """Show activity by time"""
    days = request.args.get('days', 30, type=int)
    interval = request.args.get('interval', 'day')
    activity = AnalyticsManager.get_activity_by_time(days, interval)
    return render_template('analytics/time_activity.html', activity=activity, days=days, interval=interval)

@main_bp.route('/analytics/category_statistics')
def category_statistics():
    """Show category statistics"""
    categories = AnalyticsManager.get_category_statistics()
    return render_template('analytics/category_statistics.html', categories=categories) 