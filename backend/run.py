#!/usr/bin/env python3
"""
Startup script for ICT Support System Backend
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if Gemini API key is set
if not os.getenv('GEMINI_API_KEY'):
    print("⚠️  Warning: GEMINI_API_KEY not found in environment variables.")
    print("   The AI assistant will not work without a valid API key.")
    print("   Please add your Gemini API key to the .env file.")
    print()

# Check if required packages are installed
try:
    import flask
    import google.generativeai
    print("✅ All required packages are installed.")
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

# Start the application
if __name__ == "__main__":
    print("🚀 Starting ICT Support System Backend...")
    print("📍 Server will be available at: http://localhost:5000")
    print("🔗 API endpoints will be at: http://localhost:5000/api")
    print()
    
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000) 