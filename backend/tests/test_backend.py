import requests
import sys

BASE_URL = "http://127.0.0.1:5000/api"

def run_tests():
    print("Running Backend Tests...")
    
    # Needs the server to be running.
    # We will try to register a new user or login if exists.
    email = "test@example.com"
    password = "password123"
    
    # 1. Register
    print("1. Testing Registration...")
    res = requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Test User",
        "email": email,
        "password": password
    })
    
    if res.status_code == 201:
        print("   -> Registration successful")
    elif res.status_code == 400 and "User already exists" in res.text:
        print("   -> User already exists (OK)")
    else:
        print(f"   -> Failed: {res.status_code} {res.text}")
        return

    # 2. Login
    print("2. Testing Login...")
    res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    if res.status_code != 200:
        print(f"   -> Login Failed: {res.status_code} {res.text}")
        return
    
    data = res.json()
    token = data['access_token']
    print("   -> Login successful, token received")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create Task
    print("3. Testing Create Task...")
    res = requests.post(f"{BASE_URL}/tasks", json={"title": "Test Task"}, headers=headers)
    if res.status_code == 201:
        task = res.json()
        task_id = task['id']
        print(f"   -> Task created, ID: {task_id}")
    else:
        print(f"   -> Create Task Failed: {res.status_code} {res.text}")
        return
        
    # 4. List Tasks
    print("4. Testing List Tasks...")
    res = requests.get(f"{BASE_URL}/tasks", headers=headers)
    if res.status_code == 200:
        tasks = res.json()
        print(f"   -> Fetched {len(tasks)} tasks")
    else:
        print(f"   -> List Tasks Failed: {res.status_code} {res.text}")
        
    # 5. Delete Task
    print(f"5. Testing Delete Task {task_id}...")
    res = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
    if res.status_code == 200:
        print("   -> Task deleted")
    else:
        print(f"   -> Delete Task Failed: {res.status_code} {res.text}")
        
    print("\nAll Tests Completed.")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"Test Execution Failed: {e}")
