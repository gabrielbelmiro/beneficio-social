from pydantic_settings import BaseSettings
import keyring


class Settings(BaseSettings):
    APP_NAME: str = "Beneficio Social"
    APP_ENV: str = "dev"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "beneficio_social"
    DB_USER: str = "beneficio_app"

    # Fallback para CI/CD
    DB_PASSWORD: str | None = None
    JWT_SECRET: str | None = None

    # Windows Credential Manager
    DB_PASSWORD_SERVICE: str = "beneficio_social_db_password"
    JWT_SECRET_SERVICE: str = "beneficio_social_jwt_secret"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def db_password(self) -> str:
        """
        Prioridade:
        1. Variável de ambiente (GitHub Actions / Docker)
        2. Windows Credential Manager (Desenvolvimento local)
        """

        if self.DB_PASSWORD:
            return self.DB_PASSWORD

        try:
            password = keyring.get_password(
                self.DB_PASSWORD_SERVICE,
                self.DB_USER
            )

            if password:
                return password

        except Exception:
            pass

        raise RuntimeError(
            "Senha do banco não encontrada. "
            "Configure DB_PASSWORD ou Windows Credential Manager."
        )

    @property
    def jwt_secret(self) -> str:
        """
        Prioridade:
        1. Variável de ambiente
        2. Windows Credential Manager
        """

        if self.JWT_SECRET:
            return self.JWT_SECRET

        try:
            secret = keyring.get_password(
                self.JWT_SECRET_SERVICE,
                "jwt"
            )

            if secret:
                return secret

        except Exception:
            pass

        raise RuntimeError(
            "JWT Secret não encontrado. "
            "Configure JWT_SECRET ou Windows Credential Manager."
        )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.db_password}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()