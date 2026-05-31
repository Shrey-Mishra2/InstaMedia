from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session, sessionmaker
from app.settings import settings

engine = create_engine(url= settings.DB_URL)

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users_info"

    id = Column(Integer, primary_key= True)
    name = Column(String, nullable= False)
    username = Column(String, nullable= False)
    email = Column(String,  nullable= False)
    hash_password = Column(String,  nullable= False)

localsession = sessionmaker(bind=engine)

def get_db():
    Session = localsession()
    try:
        yield Session
    finally:
        Session.close()
        
