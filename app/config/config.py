from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///acronyms.db"
    
    
    
settings = Settings()