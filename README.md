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
uvicorn main:app --reload
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

## Data Storage

User data is stored in `users.json` file in the project root. The file is automatically created and updated when users are created.
