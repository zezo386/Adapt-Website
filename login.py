from fastapi import FastAPI,Query,HTTPException, Depends, Header
from typing import Optional
import jwt.exceptions
from pydantic import BaseModel
import sqlite3
import json
from datetime import datetime, timedelta
import secrets
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import jwt

JWT_SECRET_KEY="8f7d9a8f7e9d8f7a9s8df7a9s8df7a9s8df7a9s8df7a9s8df7a9s8df7a9s8df7a9s8d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

def verify_api_key(api_key):
    
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    
    # First, check and reset daily counters if needed
    cursor.execute('''
        SELECT id, name 
        FROM api_keys 
        WHERE key = ? AND is_active = 1
    ''', (api_key,))
    
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid or inactive API key")
    
    key_id, key_name = row
    
    conn.commit()
    conn.close()
    
    return True , key_id, key_name

def create_token(username):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
        row = cursor.fetchone()
        
        data = {
            "sub":username,
            "user_id":row[0],
            "role":"user",
            "iat": datetime.utcnow(),            
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
        }

        token = jwt.encode(data,JWT_SECRET_KEY,algorithm=ALGORITHM)

        return token
    except Exception as e:
        raise HTTPException(501,e)
    finally:
        conn.close()

def decode_token(token):
    try:
        return jwt.decode(token,JWT_SECRET_KEY,algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401,"token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401,"invalid token")


class add_user(BaseModel):
    username: str
    password: str
    email: str
    api_key: str

@app.get("/login/")
def user(username: str, password: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        if user[1] == username:
            if user[2] == password:
                return {
                    "logged in":True,
                    "user_id":user[0],
                    "token":create_token(username),
                    }
            else:
                return {"logged in":False,
                        "message":"Wrong password"
                        }
    return {"logged in":False,
            "message":"username not found"
            }

@app.post("/register/")
def register(user: add_user):
    
    is_valid, key_id, key_name = verify_api_key(user.api_key)

    if not is_valid:
        raise HTTPException(status_code=401,detail="unauthorized")
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?",(user.username,))
        if cursor.fetchone():
            return {
                "authorized":False,
                "message":"username already taken"
            }
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",(user.username,user.password,user.email))
        conn.commit()
        return {
            "authorized":True,
            "message":"Signed up succesfully",
            "added by":key_name
        }
    except Exception as e:
        conn.rollback()
        print(str(e))
        raise HTTPException(status_code=500,detail=f"Database error: {str(e)}")
    finally:
        conn.close()