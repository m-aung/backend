from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from connection import get_db
from database.schemas import CreateUser, User
from auth.utils import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.sql import text 
from database.utils import format_date_and_serialize

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def sign_up(user: CreateUser, db: Session = Depends(get_db)):
    """ Sign up a new user """
    # Check if user already exists
    existing_user = db.execute(
        text("SELECT * FROM users WHERE email = :email"),
        {"email": user.email}
    ).fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user.password_hash = hash_password(user.password_hash)
    query = text("""
        INSERT INTO users (first_name, last_name, email, phone, role, password_hash)
        VALUES (:first_name, :last_name, :email, :phone, :role, :password_hash)
        RETURNING id, first_name, last_name, email, phone, role, created_at
    """) 
    result = db.execute(query, user.model_dump())
    new_user = result.fetchone()
    if new_user is None:
        raise HTTPException(status_code=500, detail="Failed to create user")
    return format_date_and_serialize(new_user,["id", "first_name", "last_name", "email", "phone", "role", "created_at"])

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """ Log in a user and return a token """
    user = db.execute("SELECT * FROM users WHERE email = :email", {"email": form_data.username}).fetchone()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    """ Get the current user from the token """
    # Logic to decode the token and retrieve user information
    pass

# Include the router in the main application
def include_auth_routes(app):
    app.include_router(router, prefix="/auth", tags=["auth"])