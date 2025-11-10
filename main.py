from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import date
from typing import Optional
import json
import os

app = FastAPI(docs=None, redoc=None)

DATA_FILE = "users.json"


class UserProfile(BaseModel):
    firstName: str
    lastName: str
    bio: Optional[str] = None
    dateOfBirth: Optional[date] = None
    location: Optional[str] = None


def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data if isinstance(data, list) else []


def save_users(users):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def get_next_id(users):
    if not users:
        return 1
    existing_ids = [user.get('id', 0) for user in users if isinstance(user.get('id'), int)]
    return max(existing_ids, default=0) + 1


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
async def create_user_profile(profile: UserProfile):
    if not profile.firstName.strip() or not profile.lastName.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="firstName and lastName are required and cannot be empty"
        )
    
    users = load_users()
    new_user = {
        "id": get_next_id(users),
        "firstName": profile.firstName.strip(),
        "lastName": profile.lastName.strip()
    }
    
    if profile.bio:
        new_user["bio"] = profile.bio.strip()
    if profile.dateOfBirth:
        new_user["dateOfBirth"] = profile.dateOfBirth.isoformat()
    if profile.location:
        new_user["location"] = profile.location.strip()
    
    users.append(new_user)
    save_users(users)
    return new_user
