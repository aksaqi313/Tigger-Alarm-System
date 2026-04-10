#!/usr/bin/env python3
"""
Water Level Alarm System - Setup Verification Script

Run this script to verify your Python environment is set up correctly:
    python verify_setup.py
"""

import sys
import subprocess
import os

print("=" * 60)
print("Water Level Alarm System - Setup Verification")
print("=" * 60)
print()

# Track results
results = []

# Check 1: Python Version
print("[1/6] Checking Python version...")
py_version = sys.version_info
print(f"      Python {py_version.major}.{py_version.minor}.{py_version.micro}")
if py_version >= (3, 7):
    print("      ✓ Python 3.7+ required")
    results.append(True)
else:
    print("      ✗ Python 3.7+ required! Please upgrade.")
    results.append(False)

print()

# Check 2: Flask Installation
print("[2/6] Checking Flask installation...")
try:
    import flask
    print(f"      Installed: Flask {flask.__version__}")
    print("      ✓ Flask is installed")
    results.append(True)
except ImportError:
    print("      ✗ Flask not found!")
    print("      Install with: pip install -r requirements.txt")
    results.append(False)

print()

# Check 3: Werkzeug Installation
print("[3/6] Checking Werkzeug installation...")
try:
    import werkzeug
    print(f"      Installed: Werkzeug {werkzeug.__version__}")
    print("      ✓ Werkzeug is installed")
    results.append(True)
except ImportError:
    print("      ✗ Werkzeug not found!")
    print("      Install with: pip install -r requirements.txt")
    results.append(False)

print()

# Check 4: Project Files
print("[4/6] Checking project files...")
required_files = [
    'app.py',
    'requirements.txt',
    'static/index.html',
]
all_files_exist = True
for file in required_files:
    exists = os.path.isfile(file)
    status = "✓" if exists else "✗"
    print(f"      {status} {file}")
    if not exists:
        all_files_exist = False
results.append(all_files_exist)

print()

# Check 5: Documentation Files
print("[5/6] Checking documentation...")
doc_files = [
    'QUICKSTART.md',
    'PYTHON_README.md',
    'SUMMARY.md',
    'INDEX.md',
]
all_docs_exist = True
for file in doc_files:
    exists = os.path.isfile(file)
    status = "✓" if exists else "✗"
    print(f"      {status} {file}")
    if not exists:
        all_docs_exist = False
results.append(all_docs_exist)

print()

# Check 6: Port 5000 Available (if Flask is available)
print("[6/6] Checking if port 5000 is available...")
try:
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 5000))
    sock.close()
    
    if result != 0:
        print("      ✓ Port 5000 is available")
        results.append(True)
    else:
        print("      ✗ Port 5000 is already in use!")
        print("      Hint: Stop the application using port 5000 first")
        results.append(False)
except Exception as e:
    print(f"      ? Could not check port: {e}")
    results.append(True)  # Don't fail on this

print()
print("=" * 60)

# Summary
passed = sum(results)
total = len(results)

if all(results):
    print(f"✓ All checks passed! ({passed}/{total})")
    print()
    print("You're ready to go!")
    print()
    print("To start the application, run:")
    print("  python app.py")
    print()
    print("Or use the batch file:")
    print("  run.bat")
    print()
    print("Then open http://localhost:5000 in your browser")
    sys.exit(0)
else:
    print(f"✗ Some checks failed ({passed}/{total})")
    print()
    print("Please fix the issues above and try again.")
    print()
    print("Common fixes:")
    print("  1. Install Python 3.7+: https://www.python.org/")
    print("  2. Install dependencies: pip install -r requirements.txt")
    print("  3. Close any other Flask application on port 5000")
    print()
    print("For help, see QUICKSTART.md or PYTHON_README.md")
    sys.exit(1)
