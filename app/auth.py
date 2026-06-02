from jose import jwt 
from datetime import datetime, timedelta, timezone
from app.settings import settings

ALGORITHM = "HS256"

def create_access_token(data:dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    

    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return token
