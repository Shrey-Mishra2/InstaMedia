from fastapi import FastAPI, Depends, HTTPException
from app.database import Base, engine, get_db,UserModel
from app.auth import create_access_token, get_current_user
from sqlalchemy.orm import Session
from app.model import UserSchema, LoginSchema
from passlib.context import CryptContext

Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

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


@app.post('/login')
def user_login(body:LoginSchema, db:Session=Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username== body.username).first()
    if not user:
        raise HTTPException(401, detail="Invalid Username or password...")
    
    if not verify_password(body.password, user.hash_password):
        raise HTTPException(401, detail="Invalid Username or password...")
    
    access_token = create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/me")
def get_me(current_user: UserModel = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }

@app.put("/update-profile")
def update_profile(
    name: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.name = name

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profile updated successfully",
        "name": current_user.name
    }