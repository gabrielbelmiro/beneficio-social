import keyring
import secrets

DB_SERVICE = "beneficio_social_db_password"
DB_USER = "beneficio_app"
DB_PASSWORD = "beneficio_app_dev_password"

JWT_SERVICE = "beneficio_social_jwt_secret"
JWT_USER = "jwt"
JWT_SECRET = secrets.token_urlsafe(64) 

keyring.set_password(DB_SERVICE, DB_USER, DB_PASSWORD)
keyring.set_password(JWT_SERVICE, JWT_USER, JWT_SECRET)
print(f"Credenciais configuradas com sucesso no Windows Credential Manager.")
print(f"DB Service: {DB_SERVICE} | User: {DB_USER} | Password: {DB_PASSWORD}")
print(f"JWT Service: {JWT_SERVICE}")
