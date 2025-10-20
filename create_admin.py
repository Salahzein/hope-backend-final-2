#!/usr/bin/env python3
"""
Script to create admin user in Railway database
"""
import requests
import json

RAILWAY_BACKEND_URL = "https://hope-backend-final-2-production.up.railway.app"

# Admin credentials
ADMIN_EMAIL = "szzein2005@gmail.com"
ADMIN_PASSWORD = "Plokplok1"
ADMIN_NAME = "Salah Zein"

# First, try to generate beta codes (this will fail without admin, but we need a beta code)
def create_admin_user():
    print("🚀 Creating admin user...")
    
    # Step 1: Try to create admin via signup with a dummy beta code
    # We'll use a simple beta code that we'll create manually
    BETA_CODE = "ADMIN2024"
    
    signup_url = f"{RAILWAY_BACKEND_URL}/api/auth/signup"
    signup_payload = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD,
        "name": ADMIN_NAME,
        "beta_code": BETA_CODE,
        "company": "Admin"
    }
    
    try:
        print(f"📝 Attempting to create admin user: {ADMIN_EMAIL}")
        response = requests.post(signup_url, json=signup_payload)
        
        if response.status_code == 200:
            print("✅ Admin user created successfully!")
            data = response.json()
            print(f"Access Token: {data.get('access_token')}")
            return True
        else:
            print(f"❌ Signup failed: {response.status_code}")
            print(f"Response: {response.json()}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False

def test_admin_login():
    print("\n🔐 Testing admin login...")
    
    login_url = f"{RAILWAY_BACKEND_URL}/api/auth/admin/login"
    login_payload = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    
    try:
        response = requests.post(login_url, json=login_payload)
        
        if response.status_code == 200:
            print("✅ Admin login successful!")
            data = response.json()
            print(f"Access Token: {data.get('access_token')}")
            return data.get('access_token')
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            print(f"Response: {response.json()}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None

if __name__ == "__main__":
    print("🎯 ADMIN USER SETUP SCRIPT")
    print("=" * 50)
    
    # Try to create admin user
    if create_admin_user():
        print("\n✅ Admin user created successfully!")
        
        # Test login
        token = test_admin_login()
        if token:
            print("\n🎉 ADMIN SETUP COMPLETE!")
            print("=" * 50)
            print(f"📧 Email: {ADMIN_EMAIL}")
            print(f"🔑 Password: {ADMIN_PASSWORD}")
            print("=" * 50)
        else:
            print("\n⚠️ Admin user created but login failed")
    else:
        print("\n❌ Failed to create admin user")
        print("💡 You may need to manually create the admin user in the database")

