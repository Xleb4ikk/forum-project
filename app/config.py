import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # Database configuration
    # Use environment variables for database connection
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    
    # Здесь жёстко задаём имя базы данных, игнорируя переменные окружения
    DB_NAME = 'forumdb'
    
    # MySQL connection string
    MYSQL_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    # SQLite connection string (fallback)
    SQLITE_URI = 'sqlite:///forum.db'
    
    # Use SQLite for development if set in environment or if SQLALCHEMY_DATABASE_URI is explicitly set
    USE_SQLITE = os.environ.get('USE_SQLITE', 'false').lower() == 'true'
    
    # Set the database URI
    SQLALCHEMY_DATABASE_URI = SQLITE_URI if USE_SQLITE else MYSQL_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_for_forum_app') 