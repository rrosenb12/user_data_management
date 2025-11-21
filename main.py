from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import date
from typing import Optional
import json
import os

app = FastAPI(docs=None, redoc=None)

DATA_FILE = "users.json"


class UserProfile(BaseModel):
    """User profile data model for creating new user profiles.

    Attributes:
        firstName: User's first name (required).
        lastName: User's last name (required).
        bio: Optional biography or description text.
        dateOfBirth: Optional date of birth.
        location: Optional location information.
        email: Optional email address.
        phone: Optional phone number.
        user_id: Optional user-provided ID. If not provided, an ID will be
            automatically generated during profile creation using sequential
            numbering based on existing user IDs.
    """
    firstName: str
    lastName: str
    bio: Optional[str] = None
    dateOfBirth: Optional[date] = None
    location: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    user_id: Optional[str] = None


class UserProfileUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    bio: Optional[str] = None
    dateOfBirth: Optional[date] = None
    location: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


def load_users():
    if not os.path.exists(DATA_FILE):
        return []
   # Treat empty or invalid JSON as an empty list
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            contents = f.read()
            if not contents or contents.strip() == "":
                return []
            data = json.loads(contents)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        # If the file is corrupt or unreadable, return empty list so the app
        # can continue and we don't crash on first POST. Caller will overwrite
        # the file when saving users.
        return []


def save_users(users):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def get_next_id(users):
    if not users:
        return 1
    existing_ids = [user.get('id', 0)
                    for user in users if isinstance(user.get('id'), int)]
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
        "id": profile.user_id if profile.user_id else get_next_id(users),
        "firstName": profile.firstName.strip(),
        "lastName": profile.lastName.strip()
    }

    if profile.bio:
        new_user["bio"] = profile.bio.strip()
    if profile.dateOfBirth:
        new_user["dateOfBirth"] = profile.dateOfBirth.isoformat()
    if profile.location:
        new_user["location"] = profile.location.strip()
    if profile.email:
        new_user["email"] = profile.email.strip()
    if profile.phone:
        new_user["phone"] = profile.phone.strip()

    users.append(new_user)
    save_users(users)
    return new_user


@app.get("/api/users")
async def list_user_profiles():
    """Return all user profiles stored in users.json."""
    return load_users()


@app.get("/api/users/{user_id}")
async def get_user_profile(user_id: int):
    """Return a single user profile by id or 404 if not found."""
    users = load_users()
    for user in users:
        # stored users are dicts with an 'id' key
        if isinstance(user, dict) and user.get('id') == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")


@app.get("/api/users/by-email/{email}")
async def get_user_by_email(email: str):
    users = load_users()
    target = email.strip().lower()
    for user in users:
        if isinstance(user, dict) and isinstance(user.get('email'), str):
            if user.get('email').strip().lower() == target:
                return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")


@app.get("/api/users/by-phone/{phone}")
async def get_user_by_phone(phone: str):
    def normalize(p: str) -> str:
        return ''.join(ch for ch in p if ch.isdigit())

    users = load_users()
    target = normalize(phone)
    for user in users:
        if isinstance(user, dict) and isinstance(user.get('phone'), str):
            if normalize(user.get('phone')) == target:
                return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")


@app.patch("/api/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user_profile(profile: UserProfileUpdate, user_id: str | int):
    users = load_users()
    user_profile = None

    # Pull user profile by user_id
    for user in users:
        # stored users are dicts with an 'id' key
        if isinstance(user, dict) and str(user.get('id')) == str(user_id):
            user_profile = user
            break

    if not user_profile:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    # Add update info to profile dict
    if profile.firstName is not None:
        firstName = profile.firstName.strip()
        if firstName == "":
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="First name cannot be blank")
        user_profile["firstName"] = firstName
    if profile.lastName is not None:
        lastName = profile.lastName.strip()
        if lastName == "":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Last name cannot be blank",
            )
        user_profile["lastName"] = lastName
    if profile.bio is not None:
        user_profile["bio"] = profile.bio.strip()
    if profile.dateOfBirth is not None:
        user_profile["dateOfBirth"] = profile.dateOfBirth.isoformat()
    if profile.location is not None:
        user_profile["location"] = profile.location.strip()
    if profile.email is not None:
        user_profile["email"] = profile.email.strip()
    if profile.phone is not None:
        user_profile["phone"] = profile.phone.strip()

    # Delete any empty dict entries
    for key in list(user_profile.keys()):
        val = user_profile.get(key)
        if val is None or str(val).strip() == "":
            user_profile.pop(key, None)

    # Save updated profiles to file
    save_users(users)

    return {"message": f"Updated user {user_id} profile successfully",
            "profile": user_profile,
            }


@app.delete("/api/users/{user_id}")
async def delete_user_profile(user_id: str | int):
    users = load_users()
    for i, user in enumerate(users):
        if str(user["id"]) == str(user_id):
            users.pop(i)
            save_users(users)
            return {"message": f"Deleted user {user_id} profile successfully"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found",
                        )
