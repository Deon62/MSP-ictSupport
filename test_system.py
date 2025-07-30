#!/usr/bin/env python3
"""
Comprehensive test script for ICT Support System
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def test_basic_endpoints():
    """Test basic endpoints without authentication"""
    print("=== Testing Basic Endpoints ===\n")
    
    # Test health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Health check working")
        else:
            print(f"✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Health check error: {e}")
    
    # Test buildings endpoint
    print("\n2. Testing buildings endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/buildings")
        if response.status_code == 200:
            data = response.json()
            buildings = data.get('buildings', [])
            print(f"✓ Found {len(buildings)} buildings")
            for building in buildings:
                print(f"  - {building.get('name', 'Unknown')}")
        else:
            print(f"✗ Buildings endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Buildings error: {e}")
    
    # Test departments endpoint
    print("\n3. Testing departments endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/departments")
        if response.status_code == 200:
            data = response.json()
            departments = data.get('departments', [])
            print(f"✓ Found {len(departments)} departments")
            for dept in departments:
                print(f"  - {dept.get('name', 'Unknown')}")
        else:
            print(f"✗ Departments endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Departments error: {e}")

def test_admin_login():
    """Test admin login functionality"""
    print("\n=== Testing Admin Login ===\n")
    
    # Test login
    print("1. Testing admin login...")
    try:
        login_data = {
            "username": "ict_support",
            "password": "Ict@support"
        }
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            user = data.get('user', {})
            must_change = data.get('must_change_password', False)
            
            print("✓ Login successful")
            print(f"  - User: {user.get('username', 'Unknown')}")
            print(f"  - Role: {user.get('role', 'Unknown')}")
            print(f"  - Must change password: {must_change}")
            
            return token
        else:
            print(f"✗ Login failed: {response.status_code}")
            print(f"  - Response: {response.json()}")
            return None
    except Exception as e:
        print(f"✗ Login error: {e}")
        return None

def test_admin_endpoints(token):
    """Test admin endpoints with authentication"""
    if not token:
        print("✗ No token available for admin tests")
        return
    
    print("\n=== Testing Admin Endpoints ===\n")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test getting tickets
    print("1. Testing tickets endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/admin/tickets", headers=headers)
        if response.status_code == 200:
            data = response.json()
            tickets = data.get('tickets', [])
            print(f"✓ Found {len(tickets)} tickets")
        else:
            print(f"✗ Tickets endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Tickets error: {e}")
    
    # Test getting departments
    print("\n2. Testing admin departments endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/admin/departments", headers=headers)
        if response.status_code == 200:
            data = response.json()
            departments = data.get('departments', [])
            print(f"✓ Found {len(departments)} departments")
        else:
            print(f"✗ Admin departments failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Admin departments error: {e}")
    
    # Test getting buildings
    print("\n3. Testing admin buildings endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/admin/buildings", headers=headers)
        if response.status_code == 200:
            data = response.json()
            buildings = data.get('buildings', [])
            print(f"✓ Found {len(buildings)} buildings")
        else:
            print(f"✗ Admin buildings failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Admin buildings error: {e}")

def test_ai_health():
    """Test AI health check"""
    print("\n=== Testing AI Health ===\n")
    
    try:
        response = requests.get(f"{BASE_URL}/health/ai")
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', 'unknown')
            error = data.get('error')
            
            if status == 'ok':
                print("✓ AI service is healthy")
            else:
                print(f"✗ AI service has issues: {error}")
        else:
            print(f"✗ AI health check failed: {response.status_code}")
    except Exception as e:
        print(f"✗ AI health error: {e}")

def test_frontend_pages():
    """Test frontend pages"""
    print("\n=== Testing Frontend Pages ===\n")
    
    # Test main page
    print("1. Testing main page...")
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✓ Main page loads successfully")
        else:
            print(f"✗ Main page failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Main page error: {e}")
    
    # Test admin page
    print("\n2. Testing admin page...")
    try:
        response = requests.get("http://localhost:5000/admin")
        if response.status_code == 200:
            print("✓ Admin page loads successfully")
        else:
            print(f"✗ Admin page failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Admin page error: {e}")

def main():
    """Run all tests"""
    print("🧪 ICT Support System - Comprehensive Test Suite\n")
    print("Make sure the server is running on http://localhost:5000")
    print("=" * 50)
    
    # Test basic endpoints
    test_basic_endpoints()
    
    # Test admin login
    token = test_admin_login()
    
    # Test admin endpoints
    if token:
        test_admin_endpoints(token)
    
    # Test AI health
    test_ai_health()
    
    # Test frontend pages
    test_frontend_pages()
    
    print("\n" + "=" * 50)
    print("✅ Test suite completed!")
    print("\nNext steps:")
    print("1. Open http://localhost:5000/ for main app")
    print("2. Open http://localhost:5000/admin for admin interface")
    print("3. Login with: ict_support / Ict@support")

if __name__ == "__main__":
    main() 