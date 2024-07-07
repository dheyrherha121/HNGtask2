from passlib.context import CryptContext
from .config import setting
from datetime import datetime, timedelta
from  jose import jwt 
SECRET_KEY = setting.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes
ALGORITHM = setting.algorithm
pwd_context = CryptContext(schemes=['bcrypt'], deprecated ='auto')

def  hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow()  + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
