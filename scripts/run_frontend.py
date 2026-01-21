#!/usr/bin/env python3

import subprocess
import sys
import os

def main():
    print("Starting Chronicle AI Streamlit Frontend...")
    print("Open http://localhost:8501 in your browser")
    print("Make sure the FastAPI backend is running on http://localhost:8000")

    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "frontend/app.py",
        "--server.port", "8501",
        "--server.address", "localhost"
    ])

if __name__ == "__main__":
    main()