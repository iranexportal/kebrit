#!/usr/bin/env python
"""
Test script for Exam App API endpoints
Usage: python test_exam_app.py
"""
import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_BASE = f"{BASE_URL}/api"

# Test data
TEST_DATA = {
    "evaluation": {
        "type": True,
        "accept_score": 70,
        "number_of_question": 10,
        "is_active": True,
        "can_back": True,
        "duration": 3600
    },
    "question": {
        "description": "What is 2 + 2?",
        "type": True,
        "c1": "3",
        "c2": "4",
        "c3": "5",
        "c4": "6",
        "correct": 2,
        "weight": 1.0,
        "can_shuffle": False
    },
    "quiz": {
        "start_at": datetime.now().isoformat(),
        "end_at": (datetime.now() + timedelta(hours=1)).isoformat(),
        "score": None,
        "is_accept": None,
        "state": "in_progress"
    },
    "quiz_response": {
        "answer": 2,
        "score": 1.0,
        "done": "completed"
    },
    "quiz_response_evaluation": {
        "score": 1.0
    }
}

# Store created IDs
created_ids = {
    "evaluation_id": None,
    "question_id": None,
    "quiz_id": None,
    "quiz_response_id": None,
    "quiz_response_evaluation_id": None
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
    print("\nNote: mission_id and user_id should exist in the database.")


def get_auth_token():
    """Get authentication token"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY2ODQxMzMwLCJpYXQiOjE3NjY4Mzc3MzAsImp0aSI6ImZhMGQ3YTU1MTQ5ZjRmZTRhYjg5ZWZjOWVkNzYxMjYxIiwidXNlcl9pZCI6IjEifQ.u3q38X0Zo__seb2rdSHVHtqRjxBvhBVtyUPc40SecCU"


def test_evaluations(headers):
    """Test Evaluation endpoints"""
    print_section("TESTING EVALUATIONS API")
    
    endpoint = f"{API_BASE}/evaluations/"
    
    # CREATE
    print("\n1. CREATE Evaluation (POST)")
    response = requests.post(endpoint, json=TEST_DATA["evaluation"], headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["evaluation_id"] = data.get("id")
        TEST_DATA["question"]["evaluation"] = created_ids["evaluation_id"]
        TEST_DATA["quiz"]["evaluation"] = created_ids["evaluation_id"]
        print(f"   Created Evaluation ID: {created_ids['evaluation_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST Evaluations (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total Evaluations: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def test_questions(headers):
    """Test Question endpoints"""
    print_section("TESTING QUESTIONS API")
    
    if not created_ids["evaluation_id"]:
        print("\n⚠️  Skipping: Evaluation not created")
        return
    
    endpoint = f"{API_BASE}/questions/"
    
    # CREATE
    print("\n1. CREATE Question (POST)")
    response = requests.post(endpoint, json=TEST_DATA["question"], headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["question_id"] = data.get("id")
        TEST_DATA["quiz_response"]["question"] = created_ids["question_id"]
        print(f"   Created Question ID: {created_ids['question_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST Questions (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total Questions: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def test_quizzes(headers):
    """Test Quiz endpoints"""
    print_section("TESTING QUIZZES API")
    
    if not created_ids["evaluation_id"]:
        print("\n⚠️  Skipping: Evaluation not created")
        return
    
    endpoint = f"{API_BASE}/quizzes/"
    
    # CREATE
    print("\n1. CREATE Quiz (POST)")
    response = requests.post(endpoint, json=TEST_DATA["quiz"], headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["quiz_id"] = data.get("id")
        TEST_DATA["quiz_response"]["quiz"] = created_ids["quiz_id"]
        print(f"   Created Quiz ID: {created_ids['quiz_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST Quizzes (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total Quizzes: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def test_quiz_responses(headers):
    """Test QuizResponse endpoints"""
    print_section("TESTING QUIZ RESPONSES API")
    
    if not created_ids["quiz_id"] or not created_ids["question_id"]:
        print("\n⚠️  Skipping: Quiz or Question not created")
        return
    
    endpoint = f"{API_BASE}/quiz-responses/"
    
    # CREATE
    print("\n1. CREATE QuizResponse (POST)")
    response = requests.post(endpoint, json=TEST_DATA["quiz_response"], headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["quiz_response_id"] = data.get("id")
        TEST_DATA["quiz_response_evaluation"]["quiz_response"] = created_ids["quiz_response_id"]
        print(f"   Created QuizResponse ID: {created_ids['quiz_response_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST QuizResponses (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total QuizResponses: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def test_quiz_response_evaluations(headers):
    """Test QuizResponseEvaluation endpoints"""
    print_section("TESTING QUIZ RESPONSE EVALUATIONS API")
    
    if not created_ids["quiz_response_id"]:
        print("\n⚠️  Skipping: QuizResponse not created")
        return
    
    endpoint = f"{API_BASE}/quiz-response-evaluations/"
    
    # CREATE
    print("\n1. CREATE QuizResponseEvaluation (POST)")
    response = requests.post(endpoint, json=TEST_DATA["quiz_response_evaluation"], headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        created_ids["quiz_response_evaluation_id"] = data.get("id")
        print(f"   Created QuizResponseEvaluation ID: {created_ids['quiz_response_evaluation_id']}")
        print(f"   Response: {json.dumps(data, indent=4, default=str)}")
    else:
        print(f"   Error: {response.text}")
    
    # LIST
    print("\n2. LIST QuizResponseEvaluations (GET)")
    response = requests.get(endpoint, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total QuizResponseEvaluations: {data.get('count', len(data.get('results', [])))}")
    else:
        print(f"   Error: {response.text}")


def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("  EXAM APP API TEST SUITE")
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
        test_evaluations(headers)
        test_questions(headers)
        test_quizzes(headers)
        test_quiz_responses(headers)
        test_quiz_response_evaluations(headers)
        
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

