# User Data Management Microservice

A FastAPI-based microservice for managing user data.

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

Alternatively, you can use:
```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Create User Profile

**POST** `/api/users`

Create a new user profile. All fields are required.

**Request Body:**
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "bio": "Software engineer passionate about building scalable applications.",
  "dateOfBirth": "1990-01-15",
  "location": "New York, NY"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "firstName": "John",
  "lastName": "Doe",
  "bio": "Software engineer passionate about building scalable applications.",
  "dateOfBirth": "1990-01-15",
  "location": "New York, NY"
}
```

**Validation Rules:**
- `firstName`: Required, cannot be empty
- `lastName`: Required, cannot be empty
- `bio`: Optional
- `dateOfBirth`: Optional, must be a valid date in YYYY-MM-DD format
- `location`: Optional

**Error Responses:**
- `422 Unprocessable Entity`: Validation errors with detailed messages
- `500 Internal Server Error`: Server errors

## Example Usage

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Alice",
    "lastName": "Johnson",
    "bio": "Product manager with 5 years of experience in tech startups.",
    "dateOfBirth": "1985-06-20",
    "location": "San Francisco, CA"
  }'
```

### Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/api/users",
    json={
        "firstName": "Alice",
        "lastName": "Johnson",
        "bio": "Product manager with 5 years of experience in tech startups.",
        "dateOfBirth": "1985-06-20",
        "location": "San Francisco, CA"
    }
)
print(response.json())
```

### Update User Profile

**POST** `/api/users/{user_id}`

Update user profile. User ID is not modifiable. On update profile must still contain a first and last name. Submit empty string to delete a profile field. 

**Request Body:**
```json
{
  "firstName": "John",
  "lastName": "Donne",
  "bio": "Sonnet writer.",
  "dateOfBirth": "1572-01-22",
  "location": "London, England"
}
```

**Response (200 OK):**
```json
{
  "message": "Updated user <user_id> profile successfully",
  "profile" : {
    "id": 1,
    "firstName": "John",
    "lastName": "Donne",
    "bio": "Sonnet writer.",
    "dateOfBirth": "1572-01-22",
    "location": "London, England"
  }
}
```

**Validation Rules:**
- `firstName`: Optional, if submitted cannot be empty
- `lastName`: Optional, if submitted cannot be empty
- `bio`: Optional
- `dateOfBirth`: Optional, must be a valid date in YYYY-MM-DD format
- `location`: Optional
- `email`: Optional
- `phone`: Optional

**Error Responses:**
- `404 Not Found`: No user profile associated with provided ID.
- `422 Unprocessable Entity`: Updated data does not meet validation rules (First and Last name cannot be blank).

## Example Usage

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "lastName": "Donne",
    "bio": "Sonnet writer.",
    "dateOfBirth": "1572-01-22",
    "location": "London, England"
  }'
```

### Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/api/users/1",
    json={
        "lastName": "Donne",
        "bio": "Sonnet writer.",
        "dateOfBirth": "1572-01-22",
        "location": "San Francisco, CA"
    }
)
print(response.json())
```

### Delete User Profile

**DELETE** `/api/users/{user_id}`

Delete user profile associated with user_id. This is not reversible!!


**Response (200 OK):**
```json
{
  "message": "Deleted user {user_id} profile successfully"
}
```

**Error Responses:**
- `404 Not Found`: No user associated with user_id


## Example Usage

### Using cURL

```bash
curl -X DELETE "http://localhost:8000/api/users/{user_id}" 

### Using Python requests

```python
import requests

response = requests.delete(
    "http://localhost:8000/api/users/{user_id}"
)
print(response.json())
```

## Data Storage

User data is stored in `users.json` file in the project root. The file is automatically created and updated when users are created.
