from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    name:str
    username : str
    email : EmailStr
    password: str = Field(max_length=72)
    
class LoginSchema(BaseModel):
    username : str
    password : str