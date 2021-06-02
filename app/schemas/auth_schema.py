from fastapi.security import OAuth2PasswordBearer


auth_schema = OAuth2PasswordBearer(tokenUrl="auth/activate")
