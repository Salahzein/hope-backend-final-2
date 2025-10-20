#!/usr/bin/env python3
"""
Manual admin setup script - creates admin user directly in database
"""
import sqlite3
import bcrypt
import os

# Database path (this will be the Railway database)
DB_PATH = "reddit_lead_finder.db"

# Admin credentials
ADMIN_EMAIL = "szzein2005@gmail.com"
ADMIN_PASSWORD = "Plokplok1"
ADMIN_NAME = "Salah Zein"

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_admin_user():
    """Create admin user in database"""
    conn = None
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("🔍 Checking database connection...")
        
        # Create tables if they don't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT,
                company TEXT,
                beta_code TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                is_admin BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS beta_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                is_used BOOLEAN DEFAULT FALSE,
                used_by_user_id TEXT,
                used_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✅ Database tables created/verified")
        
        # Check if admin user already exists
        cursor.execute("SELECT id FROM admin_users WHERE email = ?", (ADMIN_EMAIL,))
        existing_admin = cursor.fetchone()
        
        if existing_admin:
            print(f"✅ Admin user {ADMIN_EMAIL} already exists")
            return True
        
        # Create admin user
        hashed_password = hash_password(ADMIN_PASSWORD)
        cursor.execute("""
            INSERT INTO admin_users (email, password_hash, name, is_active)
            VALUES (?, ?, ?, ?)
        """, (ADMIN_EMAIL, hashed_password, ADMIN_NAME, True))
        
        admin_id = cursor.lastrowid
        print(f"✅ Admin user created with ID: {admin_id}")
        
        # Create a beta code for testing
        beta_code = "ADMIN2024"
        cursor.execute("""
            INSERT INTO beta_codes (code, is_used, used_by_user_id)
            VALUES (?, ?, ?)
        """, (beta_code, True, str(admin_id)))
        
        print(f"✅ Beta code {beta_code} created and marked as used")
        
        # Commit changes
        conn.commit()
        print("✅ Database changes committed")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🎯 MANUAL ADMIN SETUP")
    print("=" * 50)
    print(f"📧 Email: {ADMIN_EMAIL}")
    print(f"🔑 Password: {ADMIN_PASSWORD}")
    print("=" * 50)
    
    if create_admin_user():
        print("\n🎉 ADMIN SETUP COMPLETE!")
        print("=" * 50)
        print("✅ Admin user created successfully")
        print("✅ Beta code created")
        print("✅ Database updated")
        print("=" * 50)
        print("\n💡 You can now:")
        print("1. Upload the updated backend files to GitHub")
        print("2. Wait for Railway to redeploy")
        print("3. Test admin login at: https://hope-backend-final-2-production.up.railway.app/api/auth/admin/login")
    else:
        print("\n❌ ADMIN SETUP FAILED")
        print("💡 Check the error messages above")

