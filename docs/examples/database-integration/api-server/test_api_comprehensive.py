#!/usr/bin/env python3
"""
Comprehensive API server functionality test.
Tests API endpoints and basic functionality.
"""

import json
import subprocess
import sys
import time
from urllib.error import HTTPError
from urllib.request import urlopen


def start_server():
    """Start the Django server."""
    process = subprocess.Popen(
        ["uv", "run", "python", "manage.py", "runserver", "127.0.0.1:8004"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    time.sleep(3)  # Wait for server to start
    return process


def stop_server(process):
    """Stop the Django server."""
    process.terminate()
    process.wait()


def test_api_root():
    """Test API root endpoint."""
    print("Testing API root endpoint...")
    try:
        response = urlopen("http://127.0.0.1:8004/")
        data = json.loads(response.read().decode())

        if "api_name" in data and data["api_name"] == "PyBiorythm REST API Server":
            print("✅ API root endpoint working correctly")
            return True
        else:
            print(f"❌ Unexpected data in API root: {data}")
            return False
    except Exception as e:
        print(f"❌ Error testing API root: {e}")
        return False


def test_api_info():
    """Test API info endpoint."""
    print("Testing API info endpoint...")
    try:
        response = urlopen("http://127.0.0.1:8004/api/")
        data = json.loads(response.read().decode())

        if "api_name" in data:
            print("✅ API info endpoint working correctly")
            return True
        else:
            print(f"❌ Unexpected data in API info: {data}")
            return False
    except Exception as e:
        print(f"❌ Error testing API info: {e}")
        return False


def test_protected_endpoints():
    """Test that protected endpoints require authentication."""
    print("Testing protected endpoint authentication...")

    endpoints = ["http://127.0.0.1:8004/api/people/", "http://127.0.0.1:8004/api/statistics/"]

    for url in endpoints:
        try:
            urlopen(url)
            print(f"❌ Endpoint {url} should require authentication but didn't")
            return False
        except HTTPError as e:
            if e.code == 401:  # Unauthorized
                print(f"✅ Endpoint {url} correctly requires authentication")
            else:
                print(f"❌ Endpoint {url} returned unexpected status: {e.code}")
                return False
        except Exception as e:
            print(f"❌ Error testing endpoint {url}: {e}")
            return False

    return True


def main():
    """Run comprehensive API tests."""
    print("🧪 Running Comprehensive API Server Tests\n")

    # Start server
    print("Starting Django server...")
    server_process = start_server()

    try:
        tests = [test_api_root, test_api_info, test_protected_endpoints]

        passed = 0
        total = len(tests)

        for test in tests:
            if test():
                passed += 1
            print()

        print(f"📊 Test Results: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All comprehensive tests passed!")
            success = True
        else:
            print("❌ Some tests failed")
            success = False

    finally:
        # Always stop server
        print("Stopping Django server...")
        stop_server(server_process)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
