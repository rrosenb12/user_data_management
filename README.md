# User Data Management Microservice

A FastAPI-based microservice for managing program-specific user data. This README documents the communication contract (endpoints, request/response formats), example calls, a simple UML sequence diagram, and how to run the provided test program that demonstrates the service behavior.

## Getting Started

### Prerequisites
- Python 3.7 or higher
- The microservice must be running on your local machine or network
- Python library: `requests` (install with `pip install requests`)

### Starting the Service
The service runs on **port 8002** by default. Start it using:
```bash
uvicorn main:app --host 0.0.0.0 --port 8002
```

Or using the provided run script:
```bash
python run.py
```

### Connecting to the Service
All requests are made to `http://localhost:8002` (or the appropriate host/port where the service is running).

The service uses RESTful HTTP methods:
- **POST** for creating new user profiles
- **GET** for retrieving user information
- **PATCH** for updating existing user profiles
- **DELETE** for removing user profiles

All POST and PATCH requests must include `Content-Type: application/json` header and send data as JSON in the request body.

## Communication Contract (Stable)

All endpoints return JSON and use standard HTTP status codes. The contract below must remain stable for teammates to interact with this microservice.

- Base path: `/api/users`

Endpoints:

- POST `/api/users`
  - Purpose: Create a new user profile.
  - Request JSON fields:
    - `firstName` (string, required, non-empty)
    - `lastName` (string, required, non-empty)
    - `bio` (string, optional)
    - `dateOfBirth` (YYYY-MM-DD, optional)
    - `location` (string, optional)
    - `email` (string, optional)
    - `phone` (string, optional)
  - Response: 201 Created with the created user object, including numeric `id`.
  - Errors: 422 for validation failures.

- GET `/api/users`
  - Purpose: Return a JSON array of all user profiles.
  - Response: 200 OK with list (may be empty).

- GET `/api/users/{user_id}`
  - Purpose: Return a single user profile by `id`.
  - Response: 200 with user object, or 404 if not found.

- GET `/api/users/by-email/{email}`
  - Purpose: Lookup a user by email (case-insensitive).
  - Response: 200 with user object, or 404 if not found.

- GET `/api/users/by-phone/{phone}`
  - Purpose: Lookup a user by phone; service normalizes to digits only before comparison.
  - Response: 200 with user object, or 404 if not found.



## How to programmatically REQUEST data (detailed guide)

### 1. Creating a New User Profile (`POST /api/users`)

**Purpose**: Create a new user profile with personal information.

**Connection Details**:
- URL: `http://localhost:8002/api/users`
- Method: POST
- Content-Type: application/json

**Required Parameters**:
- `firstName` (string): User's first name (cannot be empty)
- `lastName` (string): User's last name (cannot be empty)

**Optional Parameters**:
- `bio` (string): User biography or description
- `dateOfBirth` (string): Birth date in YYYY-MM-DD format (e.g., "1990-01-15")
- `location` (string): User's location or address
- `email` (string): User's email address
- `phone` (string): User's phone number (any format accepted)

**Response**: Returns the created user object with a unique numeric `id` field (status code 201).

**Validation Notes**:
- First and last names are required and cannot be empty strings
- Invalid field types or missing required fields return 422 Unprocessable Entity

**Example Request**:

```python
import requests

BASE = "http://localhost:8002"
payload = {
  "firstName": "Charlie",
  "lastName": "Example",
  "email": "charlie@example.com",
  "phone": "555-000-1111"
}
resp = requests.post(f"{BASE}/api/users", json=payload, timeout=5)
print(resp.status_code)
print(resp.json())
# On success (201): the created user object with an `id` field is returned
```

### 2. Getting All Users (`GET /api/users`)

**Purpose**: Retrieve a list of all user profiles in the system.

**Connection Details**:
- URL: `http://localhost:8002/api/users`
- Method: GET
- Content-Type: Not required for GET requests

**Required Parameters**: None

**Optional Parameters**: None

**Response**: Returns a JSON array of all user objects (may be empty array if no users exist).

**Example Request**:

```python
import requests

BASE = "http://localhost:8002"
resp = requests.get(f"{BASE}/api/users", timeout=5)
print(resp.status_code)
users = resp.json()
print(f"Found {len(users)} users")
for user in users:
    print(f"- {user['firstName']} {user['lastName']} (ID: {user['id']})")
```

### 3. Getting User by ID (`GET /api/users/{user_id}`)

**Purpose**: Retrieve a specific user profile using their unique ID.

**Connection Details**:
- URL: `http://localhost:8002/api/users/{user_id}` (replace `{user_id}` with the numeric ID)
- Method: GET
- Content-Type: Not required for GET requests

**Required Parameters**:
- `user_id` (path parameter): The numeric ID of the user (included in the URL)

**Optional Parameters**: None

**Response**: Returns the user object (status 200) or 404 if the user doesn't exist.

**Example Request**:

```python
import requests

BASE = "http://localhost:8002"
user_id = 1
resp = requests.get(f"{BASE}/api/users/{user_id}", timeout=5)
print(resp.status_code)
print(resp.json())
# 200 -> user object, 404 -> {'detail': 'User not found'}
```

### 4. Getting User by Email (`GET /api/users/by-email/{email}`)

**Purpose**: Look up a user profile using their email address (case-insensitive).

**Connection Details**:
- URL: `http://localhost:8002/api/users/by-email/{email}` (replace `{email}` with the email)
- Method: GET
- Content-Type: Not required for GET requests

**Required Parameters**:
- `email` (path parameter): The email address to search for (included in the URL)

**Optional Parameters**: None

**Important Notes**:
- Email matching is case-insensitive ("charlie@example.com" matches "Charlie@Example.com")
- URL-encode the email if it contains special characters

**Example Request** (case-insensitive):

```python
import requests

BASE = "http://localhost:8002"
email = "Charlie@Example.com"
resp = requests.get(f"{BASE}/api/users/by-email/{email}", timeout=5)
print(resp.status_code)
print(resp.json())
```

### 5. Getting User by Phone (`GET /api/users/by-phone/{phone}`)

**Purpose**: Look up a user profile using their phone number.

**Connection Details**:
- URL: `http://localhost:8002/api/users/by-phone/{phone}` (replace `{phone}` with the phone number)
- Method: GET
- Content-Type: Not required for GET requests

**Required Parameters**:
- `phone` (path parameter): The phone number to search for (included in the URL)

**Optional Parameters**: None

**Important Notes**:
- The service normalizes phone numbers to digits only before comparison
- "(555)000-1111", "555-000-1111", and "5550001111" all match the same user
- Any non-digit characters are automatically stripped

**Example Request** (numeric normalization):

```python
import requests

BASE = "http://localhost:8002"
phone = "(555)000-1111"
resp = requests.get(f"{BASE}/api/users/by-phone/{phone}", timeout=5)
print(resp.status_code)
print(resp.json())
```

### 6. Updating a User Profile (`PATCH /api/users/{user_id}`)

**Purpose**: Update one or more fields of an existing user profile.

**Connection Details**:
- URL: `http://localhost:8002/api/users/{user_id}` (replace `{user_id}` with the numeric ID)
- Method: PATCH
- Content-Type: application/json

**Required Parameters**:
- `user_id` (path parameter): The numeric ID of the user to update (included in the URL)
- At least one field to update in the request body

**Optional Parameters** (all updatable fields):
- `firstName` (string)
- `lastName` (string)
- `bio` (string)
- `dateOfBirth` (string, YYYY-MM-DD format)
- `location` (string)
- `email` (string)
- `phone` (string)

**Important Notes**:
- Only include fields you want to update (partial updates supported)
- Fields not included in the request remain unchanged
- Returns 404 if the user_id doesn't exist

**Example Request** (PATCH) example:

```python
import requests

BASE = "http://localhost:8002"
user_id = 1
payload = {"lastName": "Updated"}
resp = requests.patch(f"{BASE}/api/users/{user_id}", json=payload, timeout=5)
print(resp.status_code)
print(resp.json())
```

### 7. Deleting a User (`DELETE /api/users/{user_id}`)

**Purpose**: Permanently remove a user profile from the system.

**Connection Details**:
- URL: `http://localhost:8002/api/users/{user_id}` (replace `{user_id}` with the numeric ID)
- Method: DELETE
- Content-Type: Not required for DELETE requests

**Required Parameters**:
- `user_id` (path parameter): The numeric ID of the user to delete (included in the URL)

**Optional Parameters**: None

**Important Notes**:
- This operation is permanent and cannot be undone
- Returns 404 if the user_id doesn't exist
- Returns 200 with a confirmation message on successful deletion

**Example Request**:

```python
import requests

BASE = "http://localhost:8002"
user_id = 1
resp = requests.delete(f"{BASE}/api/users/{user_id}", timeout=5)
print(resp.status_code)
print(resp.json())
```

## How to programmatically RECEIVE and parse data

When calling the service from Python, always check the response status code before using `resp.json()`.

```python
resp = requests.post(f"http://localhost:8002/api/users", json=payload, timeout=5)
if resp.status_code in (200, 201):
  data = resp.json()
  # handle success
else:
  try:
    error = resp.json().get("detail")
  except Exception:
    error = resp.text
  print("Error:", resp.status_code, error)
```

## UML Diagram
<img width="1580" height="3660" alt="Sequence diagram" src="https://github.com/user-attachments/assets/bc829195-318a-48ce-89a7-ae09b401a718" />

