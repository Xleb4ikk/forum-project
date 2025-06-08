from flask import Flask
from app import create_app
from app.models.db_models import db
import sqlalchemy as sa

app = create_app()

with app.app_context():
    # Check if admin table exists
    inspector = sa.inspect(db.engine)
    tables = inspector.get_table_names()
    print("Available tables:", tables)
    
    # Check if 'админы' exists in tables
    if 'админы' in tables:
        print("Admin table exists")
        # Count admin users
        from app.models.admin_models import Admin
        admin_count = Admin.query.count()
        print(f"Number of admin users: {admin_count}")
        # List admin users
        admins = Admin.query.all()
        for admin in admins:
            print(f"Admin: {admin.username}, Email: {admin.email}, Active: {admin.is_active}")
    else:
        print("Admin table does not exist") 