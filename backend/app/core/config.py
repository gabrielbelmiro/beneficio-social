from pydantic_settings import BaseSettings
import keyring


class Settings(BaseSettings):
    APP_NAME: str = "Beneficio Social"
    APP_ENV: str = "dev"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "beneficio_social"
    DB_USER: str = "beneficio_app"

    DB_PASSWORD_SERVICE: str = "beneficio_social_db_password"
    JWT_SECRET_SERVICE: str = "beneficio_social_jwt_secret"

    DB_PASSWORD: str | None = None
    JWT_SECRET: str | None = None

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = "../.env"
        extra = "ignore"
        env_file_encoding = "utf-8"

    @property
    def db_password(self) -> str:
        if self.DB_PASSWORD:
            return self.DB_PASSWORD

        password = keyring.get_password(
            self.DB_PASSWORD_SERVICE,
            self.DB_USER
        )

        if not password:
            raise RuntimeError(
                "Senha do banco de dados não encontrada. "
                f"Service: {self.DB_PASSWORD_SERVICE} | User: {self.DB_USER}"
            )

        return password

    @property
    def jwt_secret(self) -> str:
        if self.JWT_SECRET:
            return self.JWT_SECRET

        secret = keyring.get_password(
            self.JWT_SECRET_SERVICE,
            "jwt"
        )

        if not secret:
            raise RuntimeError(
                "JWT secret não encontrado. "
                f"Service: {self.JWT_SECRET_SERVICE}"
            )

        return secret

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.db_password}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()