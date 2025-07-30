#!/usr/bin/env python3
"""
Simple test script to verify backend functionality
"""

import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running.")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_buildings():
    """Test getting buildings"""
    print("\nTesting get buildings...")
    try:
        response = requests.get(f"{BASE_URL}/buildings")
        if response.status_code == 200:
            buildings = response.json().get('buildings', [])
            print(f"✅ Got {len(buildings)} buildings")
            for building in buildings:
                print(f"  - {building['name']} ({building['floors']} floors)")
        else:
            print(f"❌ Get buildings failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_departments():
    """Test getting departments"""
    print("\nTesting get departments...")
    try:
        response = requests.get(f"{BASE_URL}/departments")
        if response.status_code == 200:
            departments = response.json().get('departments', [])
            print(f"✅ Got {len(departments)} departments")
            for dept in departments:
                print(f"  - {dept['name']} ({dept['building']}, Floor {dept['floor']})")
        else:
            print(f"❌ Get departments failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_create_ticket():
    """Test creating a support ticket"""
    print("\nTesting create ticket...")
    ticket_data = {
        "building": "Teleposta Tower",
        "floor": "10",
        "department": "Finance Department",
        "issue_type": "WiFi Connectivity",
        "description": "WiFi is very slow on the 10th floor. Need assistance.",
        "contact_person": "Test User",
        "phone_number": "+254-700-123-999",
        "priority": "medium"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/tickets",
            json=ticket_data,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 201:
            result = response.json()
            print("✅ Ticket created successfully")
            print(f"Ticket ID: {result.get('ticket_id')}")
            return result.get('ticket_id')
        else:
            print(f"❌ Create ticket failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    return None

def test_get_tickets():
    """Test getting all tickets with enhanced features"""
    print("\nTesting get tickets...")
    try:
        response = requests.get(f"{BASE_URL}/tickets")
        if response.status_code == 200:
            data = response.json()
            tickets = data.get('tickets', [])
            summary = data.get('summary', {})
            print(f"✅ Got {len(tickets)} tickets")
            print(f"📊 Summary: {summary['pending']} pending, {summary['in_progress']} in progress")
            for ticket in tickets[:3]:  # Show first 3 tickets
                print(f"  - Ticket {ticket['id']}: {ticket['issue_type']} ({ticket['status']})")
                if ticket.get('notification'):
                    print(f"    📢 {ticket['notification']}")
        else:
            print(f"❌ Get tickets failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_dashboard():
    """Test dashboard endpoint"""
    print("\nTesting dashboard...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard")
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard data retrieved")
            print(f"📊 Status counts: {data.get('status_counts', {})}")
            print(f"📊 Priority counts: {data.get('priority_counts', {})}")
            print(f"📊 Building counts: {data.get('building_counts', {})}")
        else:
            print(f"❌ Dashboard failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_ticket_assignment():
    """Test ticket assignment"""
    print("\nTesting ticket assignment...")
    try:
        # First create a ticket
        ticket_data = {
            "building": "Teleposta Tower",
            "floor": "20",
            "department": "Legal Department",
            "issue_type": "Computer Hardware",
            "description": "Computer not starting up properly",
            "contact_person": "Test User 2",
            "phone_number": "+254-700-123-888",
            "priority": "high"
        }
        
        create_response = requests.post(f"{BASE_URL}/tickets", json=ticket_data)
        if create_response.status_code == 201:
            ticket_id = create_response.json().get('ticket_id')
            
            # Now assign the ticket
            assign_data = {"assigned_to": "ICT Staff Member"}
            assign_response = requests.put(f"{BASE_URL}/tickets/{ticket_id}/assign", json=assign_data)
            
            if assign_response.status_code == 200:
                result = assign_response.json()
                print("✅ Ticket assigned successfully")
                print(f"   Assigned to: {result.get('assigned_to')}")
                print(f"   Notification: {result.get('notification')}")
            else:
                print(f"❌ Ticket assignment failed: {assign_response.status_code}")
        else:
            print(f"❌ Ticket creation failed: {create_response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_ai_chat():
    """Test AI chat functionality"""
    print("\nTesting AI chat...")
    chat_data = {
        "message": "How do I connect to the WiFi?"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/ai/chat",
            json=chat_data,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ AI chat working")
            print(f"AI Response: {result.get('response', '')[:100]}...")
        else:
            print(f"❌ AI chat failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting ICT Support System Backend Tests")
    print("=" * 50)
    
    # Test basic functionality
    test_health_check()
    test_get_buildings()
    test_get_departments()
    test_get_tickets()
    
    # Test enhanced features
    test_dashboard()
    test_ticket_assignment()
    
    # Test ticket creation
    ticket_id = test_create_ticket()
    
    # Test AI functionality
    test_ai_chat()
    
    print("\n" + "=" * 50)
    print("🏁 Backend tests completed!")
    print("\nTo run the backend server:")
    print("1. cd backend")
    print("2. python app.py")
    print("3. Server will start on http://localhost:5000")

if __name__ == "__main__":
    main() 