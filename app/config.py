"""
    Configuration settings for the application.
    This module uses Pydantic to manage application settings and environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Settings configuration class for application environment variables.
    Attributes:
        DATABASE_HOST (str): The hostname or IP address of the database server.
        DATABASE_USER (str): The username used to connect to the database.
        DATABASE_PASSWORD (str): The password used to authenticate with the database.
        DATABASE_NAME (str): The name of the database to connect to.
        JWT_SECRET_KEY (str): Secret key used for encoding and decoding JWT tokens.
        JWT_ALGORITHM (str): Algorithm used for JWT token encoding (default: "HS256").
        JWT_ACCESS_TOKEN_EXPIRE_MINUTES (int): Expiration time
        for JWT access tokens in minutes (default: 30).
        model_config: Configuration for loading environment variables
        from a .env file and ignoring extra fields.
    """

    DATABASE_HOST: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
