#!/usr/bin/env python3
"""
Script to create admin user in PostgreSQL database
"""
import os
import sys
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import Base, AdminUser, BetaCode

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
    """Create admin user in PostgreSQL database"""
    
    print("🔧 Creating admin user in PostgreSQL database...")
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not found")
        return False
    
    if not database_url.startswith("postgresql://"):
        print("❌ DATABASE_URL is not a PostgreSQL connection string")
        return False
    
    try:
        # Create database engine
        engine = create_engine(database_url)
        
        # Create all tables
        print("🔧 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        try:
            # Check if admin user already exists
            existing_admin = session.query(AdminUser).filter(AdminUser.email == ADMIN_EMAIL).first()
            
            if existing_admin:
                print(f"✅ Admin user {ADMIN_EMAIL} already exists")
                return True
            
            # Create admin user
            hashed_password = hash_password(ADMIN_PASSWORD)
            admin_user = AdminUser(
                email=ADMIN_EMAIL,
                password_hash=hashed_password,
                name=ADMIN_NAME,
                is_active=True
            )
            
            session.add(admin_user)
            session.commit()
            
            print(f"✅ Admin user created successfully: {ADMIN_EMAIL}")
            
            # Create initial beta codes
            beta_codes = ["ADMIN2024", "HOPE2024", "BETA2024"]
            for code in beta_codes:
                # Check if beta code already exists
                existing_code = session.query(BetaCode).filter(BetaCode.code == code).first()
                if not existing_code:
                    beta_code = BetaCode(
                        code=code,
                        is_used=False,
                        created_by_admin_id=admin_user.id
                    )
                    session.add(beta_code)
                    print(f"✅ Beta code created: {code}")
            
            session.commit()
            
            return True
            
        except SQLAlchemyError as e:
            print(f"❌ Database error: {e}")
            session.rollback()
            return False
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_admin_creation():
    """Test that admin user was created successfully"""
    
    print("\n🔐 Testing admin user creation...")
    
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found")
        return False
    
    try:
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        # Check if admin user exists
        admin_user = session.query(AdminUser).filter(AdminUser.email == ADMIN_EMAIL).first()
        
        if admin_user:
            print(f"✅ Admin user found: {admin_user.email}")
            print(f"✅ Admin user active: {admin_user.is_active}")
            return True
        else:
            print("❌ Admin user not found")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False
    finally:
        session.close()

if __name__ == "__main__":
    print("🎯 POSTGRESQL ADMIN CREATION SCRIPT")
    print("=" * 50)
    print(f"📧 Email: {ADMIN_EMAIL}")
    print(f"🔑 Password: {ADMIN_PASSWORD}")
    print("=" * 50)
    
    # Check if DATABASE_URL is set
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        print(f"✅ DATABASE_URL found: {database_url[:20]}...")
    else:
        print("❌ DATABASE_URL not found in environment variables")
        exit(1)
    
    # Create admin user
    if create_admin_user():
        print("\n✅ Admin user created successfully!")
        
        # Test creation
        if test_admin_creation():
            print("\n🎉 ADMIN SETUP COMPLETE!")
            print("=" * 50)
            print("✅ PostgreSQL database configured")
            print("✅ Admin user created")
            print("✅ Beta codes created")
            print("=" * 50)
            print("\n💡 You can now:")
            print("1. Login with admin credentials")
            print("2. Generate beta codes for users")
            print("3. Beta users will have permanent accounts")
        else:
            print("\n⚠️ Admin user created but verification failed")
    else:
        print("\n❌ Failed to create admin user")
        print("💡 Check DATABASE_URL and database connection")
