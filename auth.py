from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
import pymongo
import datetime

app = FastAPI()

# Database connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["codebar"]
users_collection = db["users"]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "1c0d3b4r"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30        

class User(BaseModel):
     username: str
     password: str
     role: str

class LoginData(BaseModel):
    username: str
    password: str

# Create User endpoint
@app.post("/register/")
async def register(user: User):
     hashed_password = pwd_context.hash(user.password)
     user_password = hashed_password
     users_collection.insert_one(user.dict())
     return {"message": "User created"}

# Login and get JWT

