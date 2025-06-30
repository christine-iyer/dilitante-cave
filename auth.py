from fastapi import FastAPI, HTTPException, DepOAuth2PasswordBearer
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")    

# Create User endpoint
@app.post("/register/")
async def register(user: User):
    hashed_password = pwd_context.hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password  # Replace plain-text password with hashed password
    users_collection.insert_one(user_data)
    return {"message": "User created"}

# Login and get JWT
@app.post("/login/")
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
        {"sub": user["username"], "exp": datetime.datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {"access_token": access_token, "token_type": "bearer"}

