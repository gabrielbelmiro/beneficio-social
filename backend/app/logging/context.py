from contextvars import ContextVar
from uuid import uuid4


execution_id_ctx: ContextVar[str] = ContextVar(
    "execution_id",
    default=""
)

user_email_ctx: ContextVar[str] = ContextVar(
    "user_email",
    default="anonymous"
)


def generate_execution_id() -> str:
    return f"EXEC-{uuid4()}"


def set_execution_context(
    execution_id: str | None = None,
    user_email: str | None = None
) -> str:
    current_execution_id = execution_id or generate_execution_id()

    execution_id_ctx.set(current_execution_id)

    if user_email:
        user_email_ctx.set(user_email)

    return current_execution_id


def get_execution_id() -> str:
    return execution_id_ctx.get()


def get_user_email() -> str:
    return user_email_ctx.get()