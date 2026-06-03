from app.db.database import Base, engine

from app.models import *


print("Criando tabelas...")

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso.")