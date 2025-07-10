from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import List, Optional
import pymongo
import datetime

# Initialize APIRouter
router = APIRouter()

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

# Pydantic models
class PublicUser(BaseModel):
    username: str
    role: str
class User(BaseModel):
    username: str
    password: str
    role: str

class LoginData(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Endpoint to register a new user
@router.post("/register/")
async def register(user: User):
    # Check if the username already exists
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password and save the user
    hashed_password = pwd_context.hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password  # Replace plain-text password with hashed password
    users_collection.insert_one(user_data)
    return {"message": "User created"}

# Endpoint to log in and get a JWT token
@router.post("/login/")
async def login(login_data: LoginData):
    # Find the user in the database
    user = users_collection.find_one({"username": login_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Verify the password
    if not pwd_context.verify(login_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Generate a JWT token
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": user["username"], "exp": (datetime.datetime.utcnow() + access_token_expires).timestamp()},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Example protected route
@router.get("/protected/")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}. This is a protected route."}

@router.get("/users/", response_model=List[PublicUser])
async def get_all_users():
    users = users_collection.find({}, {"password": 0})  # Exclude passwords
    return list(users)

@router.put("/users/me/")
async def update_user_info(
    updated_data: UserUpdate, current_user: str = Depends(get_current_user)
):
    user = users_collection.find_one({"username": current_user})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Hash the password if it is being updated
    if updated_data.password:
        updated_data.password = pwd_context.hash(updated_data.password)

    # Update the user's information
    users_collection.update_one(
        {"username": current_user}, {"$set": updated_data.dict(exclude_unset=True)}
    )
    return {"message": "User information updated successfully"}