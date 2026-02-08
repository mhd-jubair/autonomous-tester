"""Example of a simple authentication API using FastAPI."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple Auth API")

USERS_DB = {
    "user@test.com": "password123",
    "admin@test.com": "admin123"
}

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    if request.email not in USERS_DB:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "message": "Login successful",
        "role": "user"
    }

@app.get("/health")
def health():
    return {"status": "ok"}
