from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db, UserModel
from app.settings import settings 
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256"

security = HTTPBearer()

def create_access_token(data:dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    

    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return token



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(UserModel).filter(UserModel.username == username).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user