import requests
import json

# Base URL for the user data management microservice
BASE_URL = "http://localhost:8000"

# Test configuration: edit these values to run the tests with different data
CONFIG = {
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "phone": "5551234567",
    "bio": "Test user for API testing",
    "location": "Test City, TC",
    "dateOfBirth": "1990-01-01",
    "alt_firstName": "anotheruser",
    "alt_lastName": "otherlastname",
    "alt_email": "another@example.com"
}


def test_list_users():
    """Test listing all users."""
    print("1. Testing list all users...")
    response = requests.get(f"{BASE_URL}/api/users")
    print(f"Request: GET {BASE_URL}/api/users")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response Body: {len(data)} users found")
        print("✓ List users successful\n")
        return data
    else:
        print(f"Response Body: {response.json()}")
        print("✗ List users failed\n")
        return []


def test_create_user_minimal(firstName, lastName):
    """Test user creation with minimal required fields."""
    print("2. Testing user creation (minimal)...")
    payload = {
        "firstName": firstName,
        "lastName": lastName
    }
    response = requests.post(f"{BASE_URL}/api/users", json=payload)
    print(
        f"Request: POST {BASE_URL}/api/users with payload {json.dumps(payload)}")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"Response Body: {data}")
        user_id = data.get("id")
        print("✓ User created successfully\n")
        return user_id
    else:
        print(f"Response Body: {response.json()}")
        print("✗ User creation failed\n")
        return None


def test_create_user_full(firstName, lastName, email, phone, bio, location, dateOfBirth):
    """Test user creation with all fields."""
    print("3. Testing user creation (full)...")
    payload = {
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "phone": phone,
        "bio": bio,
        "location": location,
        "dateOfBirth": dateOfBirth
    }
    response = requests.post(f"{BASE_URL}/api/users", json=payload)
    print(
        f"Request: POST {BASE_URL}/api/users with payload {json.dumps(payload)}")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"Response Body: {data}")
        user_id = data.get("id")
        print("✓ User created successfully\n")
        return user_id
    else:
        print(f"Response Body: {response.json()}")
        print("✗ User creation failed\n")
        return None


def test_get_user_by_id(user_id):
    """Test getting user by ID."""
    print("4. Testing get user by ID...")
    response = requests.get(f"{BASE_URL}/api/users/{user_id}")
    print(f"Request: GET {BASE_URL}/api/users/{user_id}")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response Body: {data}")
        print("✓ User retrieved successfully\n")
        return data
    else:
        print(f"Response Body: {response.json()}")
        print("✗ User retrieval failed\n")
        return None


def test_get_user_by_id_not_found():
    """Test getting user by non-existent ID."""
    print("5. Testing get user by non-existent ID...")
    response = requests.get(f"{BASE_URL}/api/users/99999")
    print(f"Request: GET {BASE_URL}/api/users/99999")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 404:
        print(f"Response Body: {response.json()}")
        print("✓ Correctly handled non-existent user\n")
    else:
        print(f"Response Body: {response.json()}")
        print("✗ Failed to handle non-existent user\n")


def test_get_user_by_email(email):
    """Test getting user by email."""
    print("6. Testing get user by email...")
    response = requests.get(f"{BASE_URL}/api/users/by-email/{email}")
    print(f"Request: GET {BASE_URL}/api/users/by-email/{email}")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response Body: {data}")
        print("✓ User retrieved successfully\n")
        return data
    else:
        print(f"Response Body: {response.json()}")
        print("✗ User retrieval failed\n")
        return None


def test_get_user_by_email_not_found():
    """Test getting user by non-existent email."""
    print("7. Testing get user by non-existent email...")
    response = requests.get(
        f"{BASE_URL}/api/users/by-email/nonexistent@example.com")
    print(
        f"Request: GET {BASE_URL}/api/users/by-email/nonexistent@example.com")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 404:
        print(f"Response Body: {response.json()}")
        print("✓ Correctly handled non-existent email\n")
    else:
        print(f"Response Body: {response.json()}")
        print("✗ Failed to handle non-existent email\n")


def test_get_user_by_phone(phone):
    """Test getting user by phone."""
    print("8. Testing get user by phone...")
    response = requests.get(f"{BASE_URL}/api/users/by-phone/{phone}")
    print(f"Request: GET {BASE_URL}/api/users/by-phone/{phone}")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response Body: {data}")
        print("✓ User retrieved successfully\n")
        return data
    else:
        print(f"Response Body: {response.json()}")
        print("✗ User retrieval failed\n")
        return None


def test_update_user(user_id, updates):
    """Test updating user profile."""
    print("9. Testing update user profile...")
    response = requests.patch(f"{BASE_URL}/api/users/{user_id}", json=updates)
    print(
        f"Request: PATCH {BASE_URL}/api/users/{user_id} with payload {json.dumps(updates)}")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response Body: {data}")
        print("✓ User updated successfully\n")
        return data
    else:
        print(f"Response Body: {response.json()}")
        print("✗ User update failed\n")
        return None


def test_update_user_not_found():
    """Test updating non-existent user."""
    print("10. Testing update non-existent user...")
    payload = {"bio": "test update"}
    response = requests.patch(f"{BASE_URL}/api/users/99999", json=payload)
    print(
        f"Request: PATCH {BASE_URL}/api/users/99999 with payload {json.dumps(payload)}")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 404:
        print(f"Response Body: {response.json()}")
        print("✓ Correctly handled non-existent user\n")
    else:
        print(f"Response Body: {response.json()}")
        print("✗ Failed to handle non-existent user\n")


def test_delete_user(user_id):
    """Test deleting user profile."""
    print("11. Testing delete user...")
    response = requests.delete(f"{BASE_URL}/api/users/{user_id}")
    print(f"Request: DELETE {BASE_URL}/api/users/{user_id}")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response Body: {data}")
        print("✓ User deleted successfully\n")
        return True
    else:
        print(f"Response Body: {response.json()}")
        print("✗ User deletion failed\n")
        return False


def test_delete_user_not_found():
    """Test deleting non-existent user."""
    print("12. Testing delete non-existent user...")
    response = requests.delete(f"{BASE_URL}/api/users/99999")
    print(f"Request: DELETE {BASE_URL}/api/users/99999")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 404:
        print(f"Response Body: {response.json()}")
        print("✓ Correctly handled non-existent user\n")
    else:
        print(f"Response Body: {response.json()}")
        print("✗ Failed to handle non-existent user\n")


# Main execution: Call tests in sequence
if __name__ == "__main__":
    print("Starting User Data Management API tests...\n")
    try:
        # Load test configuration
        firstName = CONFIG["firstName"]
        lastName = CONFIG["lastName"]
        email = CONFIG["email"]
        phone = CONFIG["phone"]
        bio = CONFIG["bio"]
        location = CONFIG["location"]
        dateOfBirth = CONFIG["dateOfBirth"]
        alt_firstName = CONFIG["alt_firstName"]
        alt_lastName = CONFIG["alt_lastName"]
        alt_email = CONFIG["alt_email"]

        # Run tests in sequence
        test_list_users()

        # Create test users
        user_id1 = test_create_user_minimal(firstName, lastName)
        user_id2 = test_create_user_full(
            alt_firstName, alt_lastName, alt_email, phone, bio, location, dateOfBirth)

        # Test retrieval by different methods
        if user_id1:
            test_get_user_by_id(user_id1)
            test_get_user_by_id_not_found()

        if user_id2 and email:
            test_get_user_by_email(alt_email)
            test_get_user_by_email_not_found()

        if user_id2 and phone:
            test_get_user_by_phone(phone)

        # Test updates
        if user_id1:
            updates = {"bio": "Updated bio", "location": "Updated location"}
            test_update_user(user_id1, updates)
            test_update_user_not_found()

        # Test deletions
        if user_id1:
            test_delete_user(user_id1)
        if user_id2:
            test_delete_user(user_id2)
        test_delete_user_not_found()

        print("All tests completed.")
    except Exception as e:
        print(f"Test failed with error: {e}")
