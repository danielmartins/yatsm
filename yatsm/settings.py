from pydantic import BaseSettings, RedisDsn


class RedisDsnNoUserRequired(RedisDsn):
    user_required = False


class YatsmSettings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    redis_dsn: RedisDsnNoUserRequired = "redis://user:pass@127.0.0.1:6379/0"

    class Config:
        env_prefix = "yatsm_"


settings = YatsmSettings()
