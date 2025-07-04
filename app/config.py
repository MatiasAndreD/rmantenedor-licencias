import os


class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "devkey")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
    FORCED_USER = None
    ADMIN_USERS = os.getenv("ADMIN_USERS", "").split(',') if os.getenv("ADMIN_USERS") else []


class DevelopmentConfig(Config):
    DEBUG = True
    FORCED_USER = os.getenv("FORCED_USER")


class ProductionConfig(Config):
    DEBUG = False
