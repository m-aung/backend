import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

class User(BaseModel):
    firstName: str
    lastName: str

class Users(BaseModel):
    users: List[User]

app = FastAPI()

origins = [
    "http://localhost:3000", # for react app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

in_memory_db = {
    "users":[]
}

@app.get("/")
def read_root():
    return {"message": "connected!"}

@app.get("/users", response_model=Users)
def read_users():
    return Users(users=in_memory_db["users"])

@app.post("/users", response_model=User)
def create_user(user: User):
    in_memory_db["users"].append(user)
    return user

# use uvicorn run as web server for FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




