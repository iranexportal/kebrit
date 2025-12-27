#!/usr/bin/env python
"""
Test script for Users App API endpoints
Usage: python test_users_app.py
"""
import requests
import json
from datetime import datetime, timedelta
import uuid

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_BASE = f"{BASE_URL}/api"

# Test data
TEST_DATA = {
    "company": {
        "name": f"Test Company {datetime.now().strftime('%Y%m%d%H%M%S')}"
    },
    "user": {
        "uuid": str(uuid.uuid4()),
        "mobile": "09123456789",
        "name": "Test User",
        "password": "testpassword123"
    },
    "role": {
        "title": "Test Role"
    },
    "session": {
        "expier_at": (datetime.now() + timedelta(days=1)).isoformat()
    },
    "token": {}
}

# Store created IDs for cleanup
created_ids = {
    "company_id": None,
    "user_id": None,
    "role_id": None,
    "session_uuid": None,
    "token_uuid": None,
    "user_role_id": None
}


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_test_data():
    """Display test data that will be used"""
    print_section("TEST DATA")
    print(json.dumps(TEST_DATA, indent=2, default=str))
    print("\nNote: Some fields like company_id and user_id will be set after creation")


def get_auth_token():
    """
    Get authentication token.
    Note: This requires a valid user in the database.
    For testing, you may need to create a user first or use an existing one.
    """
    # Try to get token (you may need to adjust this based on your auth setup)
    # For now, return None - tests will run but may fail on authenticated endpoints
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY2ODQxMzMwLCJpYXQiOjE3NjY4Mzc3MzAsImp0aSI6ImZhMGQ3YTU1MTQ5ZjRmZTRhYjg5ZWZjOWVkNzYxMjYxIiwidXNlcl9pZCI6IjEifQ.u3q38X0Zo__seb2rdSHVHtqRjxBvhBVtyUPc40SecCU"


def test_companies(headers):
    """Test Company endpoints"""
    print_section("TESTING COMPANIES API")
    
    endpoint = f"{API_BASE}/companies/"
    
    # CREATE
    print("\n1. CREATE Company (POST)")
    response = requests.post(endpoint, json=TEST_DATA["company"], headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["company_id"] = data.get("id")
        TEST_DATA["user"]["company"] = created_ids["company_id"]
        TEST_DATA["role"]["company"] = created_ids["company_id"]
        print(f"   Created Company ID: {created_ids['company_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST Companies (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total Companies: {data.get('count', len(data.get('results', [])))}")
        if data.get('results'):
            print(f"   First Company: {json.dumps(data['results'][0], indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # RETRIEVE
    if created_ids["company_id"]:
        print(f"\n3. RETRIEVE Company (GET /{created_ids['company_id']}/)")
        response = requests.get(f"{endpoint}{created_ids['company_id']}/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {json.dumps(response.json(), indent=4, default=str)}")
        else:
            print(f"   Error: {response.text}")
        
        # UPDATE
        print(f"\n4. UPDATE Company (PUT /{created_ids['company_id']}/)")
        update_data = {"name": f"Updated {TEST_DATA['company']['name']}"}
        response = requests.put(f"{endpoint}{created_ids['company_id']}/", json=update_data, headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Updated: {json.dumps(response.json(), indent=4, default=str)}")
        else:
            print(f"   Error: {response.text}")


def test_users(headers):
    """Test User endpoints"""
    print_section("TESTING USERS API")
    
    endpoint = f"{API_BASE}/users/"
    
    # CREATE
    print("\n1. CREATE User (POST)")
    response = requests.post(endpoint, json=TEST_DATA["user"], headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["user_id"] = data.get("id")
        TEST_DATA["session"]["user"] = created_ids["user_id"]
        TEST_DATA["token"]["user"] = created_ids["user_id"]
        print(f"   Created User ID: {created_ids['user_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST Users (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total Users: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")
    
    # RETRIEVE
    if created_ids["user_id"]:
        print(f"\n3. RETRIEVE User (GET /{created_ids['user_id']}/)")
        response = requests.get(f"{endpoint}{created_ids['user_id']}/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {json.dumps(response.json(), indent=4, default=str)}")
        else:
            print(f"   Error: {response.text}")


def test_roles(headers):
    """Test Role endpoints"""
    print_section("TESTING ROLES API")
    
    endpoint = f"{API_BASE}/roles/"
    
    # CREATE
    print("\n1. CREATE Role (POST)")
    response = requests.post(endpoint, json=TEST_DATA["role"], headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["role_id"] = data.get("id")
        print(f"   Created Role ID: {created_ids['role_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST Roles (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total Roles: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def test_user_roles(headers):
    """Test UserRole endpoints"""
    print_section("TESTING USER ROLES API")
    
    if not created_ids["user_id"] or not created_ids["role_id"]:
        print("\n⚠️  Skipping: User or Role not created")
        return
    
    endpoint = f"{API_BASE}/user-roles/"
    
    # CREATE
    print("\n1. CREATE UserRole (POST)")
    user_role_data = {
        "user": created_ids["user_id"],
        "role": created_ids["role_id"]
    }
    response = requests.post(endpoint, json=user_role_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["user_role_id"] = data.get("id")
        print(f"   Created UserRole ID: {created_ids['user_role_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST UserRoles (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total UserRoles: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def test_sessions(headers):
    """Test Session endpoints"""
    print_section("TESTING SESSIONS API")
    
    if not created_ids["user_id"]:
        print("\n⚠️  Skipping: User not created")
        return
    
    endpoint = f"{API_BASE}/sessions/"
    
    # CREATE
    print("\n1. CREATE Session (POST)")
    session_data = TEST_DATA["session"].copy()
    session_data["uuid"] = str(uuid.uuid4())
    response = requests.post(endpoint, json=session_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["session_uuid"] = data.get("uuid")
        print(f"   Created Session UUID: {created_ids['session_uuid']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST Sessions (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total Sessions: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def test_tokens(headers):
    """Test Token endpoints"""
    print_section("TESTING TOKENS API")
    
    if not created_ids["user_id"]:
        print("\n⚠️  Skipping: User not created")
        return
    
    endpoint = f"{API_BASE}/tokens/"
    
    # CREATE
    print("\n1. CREATE Token (POST)")
    token_data = {"uuid": str(uuid.uuid4())}
    token_data.update(TEST_DATA["token"])
    response = requests.post(endpoint, json=token_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["token_uuid"] = data.get("uuid")
        print(f"   Created Token UUID: {created_ids['token_uuid']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST Tokens (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total Tokens: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("  USERS APP API TEST SUITE")
    print("=" * 60)
    
    # Display test data
    print_test_data()
    
    # Get auth token (if needed)
    token = get_auth_token()
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    else:
        print("\n⚠️  Warning: No authentication token. Some endpoints may fail.")
        print("   Make sure the server is running and you have valid credentials.")
    
    headers["Content-Type"] = "application/json"
    
    # Run tests
    try:
        test_companies(headers)
        test_users(headers)
        test_roles(headers)
        test_user_roles(headers)
        test_sessions(headers)
        test_tokens(headers)
        
        print_section("TEST SUMMARY")
        print(f"Created Resources:")
        for key, value in created_ids.items():
            if value:
                print(f"  - {key}: {value}")
        
        print("\n✅ All tests completed!")
        print("\nNote: Created test data remains in the database.")
        print("      You may want to clean it up manually if needed.")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server.")
        print(f"   Make sure the Django server is running on {BASE_URL}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

