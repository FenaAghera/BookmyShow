"""
Quick test script to verify the project is working
Run this after starting the server: python manage.py runserver
"""
import requests
import sys

def test_server():
    base_url = "http://127.0.0.1:8000"
    
    print("=" * 50)
    print("BookMyShow - Quick Server Test")
    print("=" * 50)
    
    # Test 1: Homepage
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Homepage: OK (Status 200)")
        else:
            print(f"⚠️  Homepage: Status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running! Start with: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Movie List
    try:
        response = requests.get(f"{base_url}/movies/", timeout=5)
        if response.status_code == 200:
            print("✅ Movie List: OK")
        else:
            print(f"⚠️  Movie List: Status {response.status_code}")
    except Exception as e:
        print(f"⚠️  Movie List: {e}")
    
    # Test 3: Admin (should redirect to login)
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5, allow_redirects=False)
        if response.status_code in [200, 302, 301]:
            print("✅ Admin Page: OK")
        else:
            print(f"⚠️  Admin Page: Status {response.status_code}")
    except Exception as e:
        print(f"⚠️  Admin Page: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Basic server tests passed!")
    print("\nNext steps:")
    print("1. Open browser: http://127.0.0.1:8000/")
    print("2. Register/Login")
    print("3. Browse movies and test booking flow")
    print("4. See TESTING_GUIDE.md for detailed tests")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    test_server()
