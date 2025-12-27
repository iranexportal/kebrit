#!/usr/bin/env python
"""
Test script for Media App API endpoints
Usage: python test_media_app.py
"""
import requests
import json
from datetime import datetime
import uuid

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_BASE = f"{BASE_URL}/api"

# Test data
TEST_DATA = {
    "file": {
        "file_name": f"test_file_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf",
        "file_type": "application/pdf",
        "file_size": 1024000,
        "path": "/uploads/test/test_file.pdf",
        "bucket": "test-bucket",
        "url": "https://example.com/files/test_file.pdf",
        "is_public": False
    },
    "tag": {
        "title": f"Test Tag {datetime.now().strftime('%Y%m%d%H%M%S')}"
    },
    "file_tag": {
        "file": None,  # Will be set after creating file
        "tag": None    # Will be set after creating tag
    }
}

# Store created IDs
created_ids = {
    "file_id": None,
    "tag_id": None,
    "file_tag_id": None
}


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_test_data():
    """Display test data"""
    print_section("TEST DATA")
    print(json.dumps(TEST_DATA, indent=2, default=str))
    print("\nNote: user_id and company_id are optional.")


def get_auth_token():
    """Get authentication token"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY2ODQxMzMwLCJpYXQiOjE3NjY4Mzc3MzAsImp0aSI6ImZhMGQ3YTU1MTQ5ZjRmZTRhYjg5ZWZjOWVkNzYxMjYxIiwidXNlcl9pZCI6IjEifQ.u3q38X0Zo__seb2rdSHVHtqRjxBvhBVtyUPc40SecCU"


def test_files(headers):
    """Test File endpoints"""
    print_section("TESTING FILES API")
    
    endpoint = f"{API_BASE}/files/"
    
    # CREATE
    print("\n1. CREATE File (POST)")
    file_data = TEST_DATA["file"].copy()
    file_data["uuid"] = str(uuid.uuid4())
    response = requests.post(endpoint, json=file_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["file_id"] = data.get("id")
        TEST_DATA["file_tag"]["file"] = created_ids["file_id"]
        print(f"   Created File ID: {created_ids['file_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST Files (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total Files: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")
    
    # RETRIEVE
    if created_ids["file_id"]:
        print(f"\n3. RETRIEVE File (GET /{created_ids['file_id']}/)")
        response = requests.get(f"{endpoint}{created_ids['file_id']}/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {json.dumps(response.json(), indent=4, default=str)}")
        else:
            print(f"   Error: {response.text}")


def test_tags(headers):
    """Test Tag endpoints"""
    print_section("TESTING TAGS API")
    
    endpoint = f"{API_BASE}/tags/"
    
    # CREATE
    print("\n1. CREATE Tag (POST)")
    response = requests.post(endpoint, json=TEST_DATA["tag"], headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["tag_id"] = data.get("id")
        TEST_DATA["file_tag"]["tag"] = created_ids["tag_id"]
        print(f"   Created Tag ID: {created_ids['tag_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST Tags (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total Tags: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def test_file_tags(headers):
    """Test FileTag endpoints"""
    print_section("TESTING FILE TAGS API")
    
    if not created_ids["file_id"] or not created_ids["tag_id"]:
        print("\n⚠️  Skipping: File or Tag not created")
        return
    
    endpoint = f"{API_BASE}/file-tags/"
    
    # CREATE
    print("\n1. CREATE FileTag (POST)")
    response = requests.post(endpoint, json=TEST_DATA["file_tag"], headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["file_tag_id"] = data.get("id")
        print(f"   Created FileTag ID: {created_ids['file_tag_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST FileTags (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total FileTags: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("  MEDIA APP API TEST SUITE")
    print("=" * 60)
    
    print_test_data()
    
    token = get_auth_token()
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    else:
        print("\n⚠️  Warning: No authentication token. Some endpoints may fail.")
    
    headers["Content-Type"] = "application/json"
    
    try:
        test_files(headers)
        test_tags(headers)
        test_file_tags(headers)
        
        print_section("TEST SUMMARY")
        print(f"Created Resources:")
        for key, value in created_ids.items():
            if value:
                print(f"  - {key}: {value}")
        
        print("\n✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server.")
        print(f"   Make sure the Django server is running on {BASE_URL}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

