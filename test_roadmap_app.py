#!/usr/bin/env python
"""
Test script for Roadmap App API endpoints
Usage: python test_roadmap_app.py
"""
import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_BASE = f"{BASE_URL}/api"

# Test data - Note: company_id and user_id should exist in database
TEST_DATA = {
    "mission": {
        "type": "A",
        "title": f"Test Mission {datetime.now().strftime('%Y%m%d%H%M%S')}",
        "content": "This is a test mission content",
        "mo": True,
        "point": 100,
        "expier_at": (datetime.now() + timedelta(days=30)).isoformat(),
        "is_active": True,
        "at_least_point": 50
    },
    "mission_relation": {
        "parent": None,  # Will be set after creating missions
        "child": None
    },
    "mission_result": {
        "state": "completed",
        "user_grant": 100,
        "quiz_id": None,
        "ability": None
    },
    "ability": {
        "title": f"Test Ability {datetime.now().strftime('%Y%m%d%H%M%S')}"
    }
}

# Store created IDs
created_ids = {
    "mission_id": None,
    "mission_id_2": None,
    "mission_relation_id": None,
    "mission_result_id": None,
    "ability_id": None
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
    print("\nNote: company_id and user_id should exist in the database.")
    print("      You may need to create them first or use existing IDs.")


def get_auth_token():
    """Get authentication token"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY2ODQxMzMwLCJpYXQiOjE3NjY4Mzc3MzAsImp0aSI6ImZhMGQ3YTU1MTQ5ZjRmZTRhYjg5ZWZjOWVkNzYxMjYxIiwidXNlcl9pZCI6IjEifQ.u3q38X0Zo__seb2rdSHVHtqRjxBvhBVtyUPc40SecCU"


def test_missions(headers):
    """Test Mission endpoints"""
    print_section("TESTING MISSIONS API")
    
    endpoint = f"{API_BASE}/missions/"
    
    # CREATE
    print("\n1. CREATE Mission (POST)")
    response = requests.post(endpoint, json=TEST_DATA["mission"], headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["mission_id"] = data.get("id")
        print(f"   Created Mission ID: {created_ids['mission_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # Create second mission for relation
    print("\n2. CREATE Second Mission (POST)")
    mission_2 = TEST_DATA["mission"].copy()
    mission_2["title"] = f"Test Mission 2 {datetime.now().strftime('%Y%m%d%H%M%S')}"
    response = requests.post(endpoint, json=mission_2, headers=headers)
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["mission_id_2"] = data.get("id")
        print(f"   Created Mission ID: {created_ids['mission_id_2']}")
    
    # LIST
    print("\n3. LIST Missions (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total Missions: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")
    
    # RETRIEVE
    if created_ids["mission_id"]:
        print(f"\n4. RETRIEVE Mission (GET /{created_ids['mission_id']}/)")
        response = requests.get(f"{endpoint}{created_ids['mission_id']}/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {json.dumps(response.json(), indent=4, default=str)}")
        else:
            print(f"   Error: {response.text}")


def test_mission_relations(headers):
    """Test MissionRelation endpoints"""
    print_section("TESTING MISSION RELATIONS API")
    
    if not created_ids["mission_id"] or not created_ids["mission_id_2"]:
        print("\n⚠️  Skipping: Missions not created")
        return
    
    endpoint = f"{API_BASE}/mission-relations/"
    
    # CREATE
    print("\n1. CREATE MissionRelation (POST)")
    relation_data = {
        "mission": created_ids["mission_id"],
        "parent": created_ids["mission_id"],
        "child": created_ids["mission_id_2"]
    }
    response = requests.post(endpoint, json=relation_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["mission_relation_id"] = data.get("id")
        print(f"   Created MissionRelation ID: {created_ids['mission_relation_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST MissionRelations (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total MissionRelations: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def test_mission_results(headers):
    """Test MissionResult endpoints"""
    print_section("TESTING MISSION RESULTS API")
    
    if not created_ids["mission_id"]:
        print("\n⚠️  Skipping: Mission not created")
        return
    
    endpoint = f"{API_BASE}/mission-results/"
    
    # CREATE
    print("\n1. CREATE MissionResult (POST)")
    result_data = TEST_DATA["mission_result"].copy()
    result_data["mission"] = created_ids["mission_id"]
    response = requests.post(endpoint, json=result_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["mission_result_id"] = data.get("id")
        print(f"   Created MissionResult ID: {created_ids['mission_result_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST MissionResults (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total MissionResults: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def test_abilities(headers):
    """Test Ability endpoints"""
    print_section("TESTING ABILITIES API")
    
    endpoint = f"{API_BASE}/abilities/"
    
    # CREATE
    print("\n1. CREATE Ability (POST)")
    response = requests.post(endpoint, json=TEST_DATA["ability"], headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["ability_id"] = data.get("id")
        print(f"   Created Ability ID: {created_ids['ability_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST Abilities (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total Abilities: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("  ROADMAP APP API TEST SUITE")
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
        test_missions(headers)
        test_mission_relations(headers)
        test_mission_results(headers)
        test_abilities(headers)
        
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

