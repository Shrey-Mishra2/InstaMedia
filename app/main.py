from fastapi import FastAPI, Depends, HTTPException
from app.database import Base, engine, get_db,UserModel
from sqlalchemy.orm import Session
from app.model import UserSchema
from passlib.context import CryptContext

Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

app = FastAPI()

@app.post('/Register')
def user_register(body:UserSchema, db:Session=Depends(get_db)):
    is_user = db.query(UserModel).filter(UserModel.username== body.username).first()
    if is_user:
        raise HTTPException(400, detail="username already exist...")
    is_user = db.query(UserModel).filter(UserModel.email== body.email).first()
    if is_user:
        raise HTTPException(400, detail="email already exist...")
    
    hash_password =get_password_hash(body.password)

    new_user = UserModel(
        name = body.name,
        username = body.username,
        email = body.email,
        hash_password = hash_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
 

    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}
