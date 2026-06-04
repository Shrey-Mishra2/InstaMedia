from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db, UserModel
from app.settings import settings 
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256"

security = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data:dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    

    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return token


def get_current_user(
    token: Annotated[str, Depends(security)],
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = (
        db.query(UserModel)
        .filter(UserModel.username == username)
        .first()
    )

    if user is None:
        raise credentials_exception

    return user