#!/usr/bin/env python3
"""
Basic API server functionality test.
Tests that the API server can start and basic endpoints work.
"""

import json
import subprocess
import sys
import time
from urllib.request import urlopen
from urllib.error import URLError

def test_django_check():
    """Test that Django system check passes."""
    print("Testing Django system check...")
    result = subprocess.run(
        ["uv", "run", "python", "manage.py", "check"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Django system check passed")
        return True
    else:
        print(f"❌ Django system check failed: {result.stderr}")
        return False

def test_migrations():
    """Test that migrations can be applied."""
    print("Testing database migrations...")
    result = subprocess.run(
        ["uv", "run", "python", "manage.py", "migrate", "--check"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Database migrations are up to date")
        return True
    else:
        print(f"❌ Database migrations failed: {result.stderr}")
        return False

def test_server_start():
    """Test that the server can start."""
    print("Testing server startup...")
    
    # Start server in background
    process = subprocess.Popen(
        ["uv", "run", "python", "manage.py", "runserver", "127.0.0.1:8003"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test root API endpoint
        response = urlopen("http://127.0.0.1:8003/")
        data = json.loads(response.read().decode())
        
        if "api_name" in data:
            print("✅ Server started and root API endpoint accessible")
            success = True
        else:
            print("❌ API endpoint returned unexpected data")
            success = False
            
    except URLError as e:
        print(f"❌ Could not connect to server: {e}")
        success = False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        success = False
    finally:
        # Stop server
        process.terminate()
        process.wait()
    
    return success

def main():
    """Run all tests."""
    print("🧪 Running API Server Basic Tests\n")
    
    tests = [
        test_django_check,
        test_migrations, 
        test_server_start
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()