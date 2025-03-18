from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from connection import engine, shutdown_db_conn
from sqlalchemy import text
from auth.routes import router as auth_router
from database.schemas import User, CreateUser, UpdateUser
from database.utils import format_date_and_serialize

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Do setup here at start of lifespan
    yield
    # Clean up at end of lifespan
    shutdown_db_conn()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173", # for react app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

all_columns = ["id", "first_name", "last_name", "email", "phone", "role","password_hash","created_at"]

@app.get("/users", response_model=List[User])
def get_users():
   """ Get all users """
   with engine.connect() as connection:
       result = connection.execute(text("SELECT * FROM users"))
       users = result.fetchall()

       formatted_users = []
       for user in users:
           print(f"user = {user}")
           formatted_users.append(format_date_and_serialize(user,all_columns))
       return formatted_users

@app.get("/users/id={user_id}", response_model=User)
def get_user_by_id(user_id: int):
    """ Get a single user by id"""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM users WHERE id = :user_id"), {"user_id": user_id})
        user = result.fetchone()
        if user:
            return format_date_and_serialize(user,all_columns)
        else:
            return HTTPException(status_code=404, detail="User not found")

@app.get("/users/email={email}", response_model=User)
def get_user_by_email(email: str):
    """ Get a single user by id"""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM users WHERE email = :email"), {"email": email})
        user = result.fetchone()
        if user:
            print(f"{user}")
            return format_date_and_serialize(user,all_columns)
        else:
            return HTTPException(status_code=404, detail="User not found")
        
@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser):
    """ Create a new user """
    with engine.begin() as connection:
        query = text("""
                     INSERT INTO users (first_name, last_name, email, phone, role, password_hash)
                     VALUES (:first_name, :last_name, :email, :phone, :role, :password_hash)
                     RETURNING id, first_name, last_name, email, phone, role, created_at
        """)
        result = connection.execute(query, user.model_dump())
        new_user = result.fetchone()
        if new_user is None:
            raise HTTPException(status_code=500, detail="Failed to create user")
        return format_date_and_serialize(new_user,["id", "first_name", "last_name", "email", "phone", "role", "created_at"])
    
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UpdateUser):
    """ Update an existing user """
    with engine.begin() as connection:
        query = text("""
                     UPDATE users
                     SET first_name = :first_name,
                         last_name = :last_name,
                         email = :email,
                         phone = :phone,
                         role = :role
                     WHERE id = :user_id
                     RETURNING id, first_name, last_name, email, phone, role, created_at
        """)
        result = connection.execute(query, {**user.model_dump(), "user_id": user_id})
        updated_user = result.fetchone()
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return format_date_and_serialize(updated_user,["id", "first_name", "last_name", "email", "phone", "role", "created_at"])

@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int):
    """ Delete a user by id"""
    with engine.begin() as connection:
        query = text("DELETE FROM users WHERE id = :user_id")
        result = connection.execute(query, {"user_id": user_id})
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}

# apply routers
app.include_router(auth_router)

# use uvicorn run as web server for FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




