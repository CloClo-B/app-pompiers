# api/auth_utils.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt



PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
# pour bcrypt rounds (coût) on peut configurer via CryptContext kwargs:
# e.g. CryptContext(schemes=["bcrypt"], bcrypt__rounds=12) si besoin

# secret (mettre en .env en prod)
JWT_SECRET = "CHANGE_THIS_SECRET"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24h

def hash_password(password: str) -> str:
    return PWD_CONTEXT.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return PWD_CONTEXT.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
