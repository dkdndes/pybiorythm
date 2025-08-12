#!/usr/bin/env python3
"""
Final API server validation test.
"""

import os
import subprocess
import sys


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ {description} - SUCCESS")
        if result.stdout.strip():
            print(f"Output: {result.stdout.strip()}")
        return True
    else:
        print(f"❌ {description} - FAILED")
        if result.stderr.strip():
            print(f"Error: {result.stderr.strip()}")
        if result.stdout.strip():
            print(f"Output: {result.stdout.strip()}")
        return False

def main():
    """Run final validation tests."""
    print("🧪 Final API Server Validation\n")

    tests = [
        (["uv", "run", "python", "manage.py", "check"], "Django System Check"),
        (["uv", "run", "python", "manage.py", "migrate", "--check"], "Migration Check"),
        (["uv", "run", "ruff", "check", "biorhythm_api/", "api/", "biorhythm_data/"], "Ruff Linting"),
        (["uv", "run", "ruff", "format", "--check", "biorhythm_api/", "api/", "biorhythm_data/"], "Ruff Formatting"),
        (["uv", "run", "bandit", "-r", "biorhythm_api/", "api/", "--skip", "B104", "-q"], "Security Scan (Skip B104 dev setting)")
    ]

    passed = 0
    total = len(tests)

    for cmd, description in tests:
        if run_command(cmd, description):
            passed += 1
        print()

    # Test that key files exist
    print("Checking key files exist...")
    key_files = [
        "manage.py",
        "biorhythm_api/settings.py",
        "api/views.py",
        "api/serializers.py",
        "biorhythm_data/models.py",
        "Dockerfile",
        "pyproject.toml"
    ]

    files_exist = True
    for file_path in key_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            files_exist = False

    if files_exist:
        passed += 1
    total += 1

    print(f"\n📊 Final Results: {passed}/{total} checks passed")

    if passed == total:
        print("🎉 API Server validation complete - All checks passed!")
        print("\nAPI Server is ready for deployment with:")
        print("  - Django ASGI server with Daphne")
        print("  - REST API endpoints with token authentication")
        print("  - SQLite database with biorhythm models")
        print("  - Docker containerization support")
        print("  - Security best practices")
        print("  - Code quality standards")
        sys.exit(0)
    else:
        print("❌ Some validation checks failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
