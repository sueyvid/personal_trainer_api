# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Agrupa todas as configurações da aplicação.
    """
    # ✅ Adiciona a variável da main na sua estrutura Pydantic
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    SECRET_KEY: str = "sua_chave_secreta_super_segura_e_longa"
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

# Cria a instância única que será usada em toda a aplicação
settings = Settings()