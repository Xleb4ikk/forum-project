from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user
from flask import redirect, url_for, flash, abort, request
from werkzeug.security import generate_password_hash

from app.models.db_models import db, User, Profile, Category, Forum, Topic, Post, Rating, Comment
from app.models.admin_models import Admin as AdminModel

# Создаем экземпляр административной панели с уникальным путем
admin = Admin(name='Форум: Административная панель', template_mode='bootstrap3', url='/admin_panel', base_template='admin/my_master.html')

# Настройка LoginManager
login_manager = LoginManager()
login_manager.login_view = 'admin_routes.login'

@login_manager.user_loader
def load_user(user_id):
    return AdminModel.query.get(int(user_id))

# Базовый класс для административных представлений с проверкой доступа
class SecureModelView(ModelView):
    def is_accessible(self):
        # Для отладки - временно разрешаем доступ всем
        return True
        # Раскомментировать когда всё заработает:
        # return current_user.is_authenticated and current_user.is_active
    
    def inaccessible_callback(self, name, **kwargs):
        flash('Пожалуйста, войдите в систему для доступа к этой странице.', 'warning')
        return redirect(url_for('admin_routes.login', next=request.url))

# Специализированные представления для различных моделей
class UserModelView(SecureModelView):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = ['ID_пользователя', 'имя_пользователя', 'электронная_почта']
    column_searchable_list = ['имя_пользователя', 'электронная_почта']
    column_filters = ['имя_пользователя']
    
class ProfileModelView(SecureModelView):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = ['ID_профиля', 'ID_пользователя', 'статус', 'дата_регистрации']
    column_filters = ['статус']
    column_searchable_list = ['статус']
    
class ForumModelView(SecureModelView):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = ['ID_форума', 'название', 'описание']
    column_searchable_list = ['название']
    
class CategoryModelView(SecureModelView):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = ['ID_категории', 'название', 'описание']
    column_searchable_list = ['название']
    
class TopicModelView(SecureModelView):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = ['ID_темы', 'ID_форума', 'название', 'дата_создания']
    column_searchable_list = ['название']
    column_filters = ['ID_форума']
    
class PostModelView(SecureModelView):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = ['ID_поста', 'ID_темы', 'ID_пользователя', 'содержимое', 'дата_публикации']
    column_searchable_list = ['содержимое']
    column_filters = ['ID_темы', 'ID_пользователя']
    
class CommentModelView(SecureModelView):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = ['ID_комментария', 'ID_поста', 'ID_пользователя', 'содержимое', 'дата_отправки']
    column_searchable_list = ['содержимое']
    column_filters = ['ID_поста', 'ID_пользователя']
    
class RatingModelView(SecureModelView):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = ['ID_рейтинга', 'ID_поста', 'оценка', 'комментарий']
    column_filters = ['ID_поста', 'оценка']
    
class AdminModelView(SecureModelView):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = ['id', 'username', 'email', 'is_active', 'is_superadmin']
    column_searchable_list = ['username', 'email']
    column_filters = ['is_active', 'is_superadmin']
    form_columns = ['username', 'email', 'password_hash', 'is_active', 'is_superadmin']
    
    def on_model_change(self, form, model, is_created):
        # Хэшируем пароль при создании нового администратора
        if is_created and form.password_hash.data:
            model.password_hash = generate_password_hash(form.password_hash.data)

# Функция для регистрации административных представлений
def init_admin(app):
    admin.init_app(app)
    login_manager.init_app(app)
    
    # Создаем шаблонный каталог для админки, если его нет
    import os
    admin_templates = os.path.join(app.root_path, 'templates', 'admin')
    if not os.path.exists(admin_templates):
        os.makedirs(admin_templates)
    
    # Регистрация административных представлений
    admin.add_view(UserModelView(User, db.session, name='Пользователи', endpoint='user'))
    admin.add_view(ProfileModelView(Profile, db.session, name='Профили', endpoint='profile'))
    admin.add_view(ForumModelView(Forum, db.session, name='Форумы', endpoint='forum'))
    admin.add_view(CategoryModelView(Category, db.session, name='Категории', endpoint='category'))
    admin.add_view(TopicModelView(Topic, db.session, name='Темы', endpoint='topic'))
    admin.add_view(PostModelView(Post, db.session, name='Посты', endpoint='post'))
    admin.add_view(CommentModelView(Comment, db.session, name='Комментарии', endpoint='comment'))
    admin.add_view(RatingModelView(Rating, db.session, name='Оценки', endpoint='rating'))
    admin.add_view(AdminModelView(AdminModel, db.session, name='Администраторы', endpoint='admin_users')) 