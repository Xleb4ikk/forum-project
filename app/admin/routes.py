from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from app.models.admin_models import Admin
from app.models.db_models import db

admin_bp = Blueprint('admin_routes', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Если пользователь уже авторизован, перенаправляем его на главную страницу админки
    if current_user.is_authenticated:
        return redirect(url_for('admin_routes.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        admin = Admin.query.filter_by(username=username).first()
        
        # Проверка наличия пользователя и правильности пароля
        if admin and admin.check_password(password):
            login_user(admin, remember=remember)
            next_page = request.args.get('next')
            flash(f'Добро пожаловать, {admin.username}!', 'success')
            return redirect(next_page or url_for('admin_routes.index'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'info')
    return redirect(url_for('admin_routes.login'))

@admin_bp.route('/')
@login_required
def index():
    # Редирект на встроенную главную страницу Flask-Admin с корректным URL
    return redirect('/admin_panel')

# Инициализация первого администратора
def init_first_admin():
    if Admin.query.count() == 0:
        admin = Admin(username='admin', email='admin@example.com', is_superadmin=True, is_active=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Создан первый администратор: admin / admin123") 