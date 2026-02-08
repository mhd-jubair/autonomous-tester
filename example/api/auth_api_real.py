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

    if USERS_DB[request.email] != request.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    role = "admin" if "admin" in request.email else "user"
    return {
        "message": "Login successful",
        "role": role
    }

@app.get("/health")
def health():
    return {"status": "ok"}
