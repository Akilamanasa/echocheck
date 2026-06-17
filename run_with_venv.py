#!/usr/bin/env python3
"""
Wrapper script that uses venv Python to run the application
This ensures the correct Python interpreter with all dependencies is used
"""
import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).parent
venv_python = project_root / 'venv' / 'bin' / 'python3'

if not venv_python.exists():
    print("❌ Virtual environment not found!")
    print("   Please run: python3 -m venv venv")
    print("   Then: pip install -r requirements.txt")
    sys.exit(1)

# Use venv Python to run the actual script
script_path = project_root / 'run.py'
subprocess.run([str(venv_python), str(script_path)] + sys.argv[1:])

