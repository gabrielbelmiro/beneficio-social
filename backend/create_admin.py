from app.db.database import SessionLocal
from app.models.user import User
from app.security.password import hash_password


ADMIN_NAME = "Administrador"
ADMIN_EMAIL = "admin@beneficiosocial.local"
ADMIN_PASSWORD = "Admin@123"


db = SessionLocal()

try:
    existing_user = db.query(User).filter(User.email == ADMIN_EMAIL).first()

    if existing_user:
        print("Usuário admin já existe.")
    else:
        admin = User(
            name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            password_hash=hash_password(ADMIN_PASSWORD),
            role="admin"
        )

        db.add(admin)
        db.commit()

        print("Usuário admin criado com sucesso.")
        print(f"Email: {ADMIN_EMAIL}")
        print(f"Senha: {ADMIN_PASSWORD}")

finally:
    db.close()