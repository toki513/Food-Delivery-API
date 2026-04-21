from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    APP_NAME:str="Food Delivery App"
    DEBUG:bool=True
    API_V1_STR: str="/api/v1"
        
    DATABASE_URL:str
    
    SECRET_KEY:str
    ALGORITHM:str= "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 30
    REFRESH_TOKEN_EXPIRE_DAYS:int = 7
        
        
    REDIS_URL:str="redis://localhost:6379"
    
    UPLOAD_DIR:str="uploads"
    
    
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
settings=Settings()