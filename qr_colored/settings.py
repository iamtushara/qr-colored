"""Settings Management for the Application"""

# pylint: disable=too-few-public-methods

from typing import Optional
from pydantic import BaseSettings


DEFAULT_CONFIG_PATH = 'settings.env'


class AppSettings(BaseSettings):
    """App Settings"""

    settings_1: str = ''
    settings_2: str = ''
    settings_3: str = ''

    class Config:
        """meta-settings"""
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'APP_'


class RESTSettings(BaseSettings):
    """settings for serving rest api"""

    host: str = '127.0.0.1'
    port: int = 8080
    server_reload: bool = False

    class Config:
        """meta-settings"""
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'REST_'


class LoggingSettings(BaseSettings):
    """settings for logging"""

    level: str = 'DEBUG'
    filename: str = 'qr-colored.log'

    class Config:
        """meta-settings"""
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'LOG_'


class Settings(BaseSettings):
    """Base Application Settings"""

    app: AppSettings
    rest: RESTSettings
    log: LoggingSettings


def load_settings(env_path: Optional[str] = None) -> Settings:
    """Load settings from .env at specified file path"""

    env_path = env_path or DEFAULT_CONFIG_PATH
    app_settings = Settings(
        app=AppSettings(_env_file=env_path),  # pyright: ignore
        rest=RESTSettings(_env_file=env_path),  # pyright: ignore
        log=LoggingSettings(_env_file=env_path),  # pyright: ignore
    )
    return app_settings


def write_settings(env_path: Optional[str] = None) -> str:
    """creates a blank configuration file"""

    env_path = env_path or DEFAULT_CONFIG_PATH
    empty_settings = load_settings().dict()
    with open(env_path, mode='w', encoding='utf-8') as config_file:
        config_file.writelines("# Application Settings Management\n")
        for category in empty_settings:
            config_file.writelines('\n')
            config_file.writelines(f"# {category.title()} Settings\n")
            for sname, svalue in empty_settings[category].items():
                config_file.writelines(
                    f"{category.upper()}_{sname.upper()}={svalue}\n")
    return env_path
