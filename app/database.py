from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database URL - using SQLite for simplicity
DATABASE_URL = "sqlite:///./reddit_lead_finder.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    company = Column(String)
    beta_code = Column(String, nullable=False)
    results_used = Column(Integer, default=0)  # Track total results used by user
    posts_analyzed = Column(Integer, default=0)  # Track total posts analyzed by user
    total_tokens_used = Column(Integer, default=0)  # Track total OpenAI tokens used
    total_cost = Column(Float, default=0.0)  # Track total cost incurred
    last_search_time = Column(Float, default=0.0)  # Track last search time for rate limiting
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BetaCode(Base):
    __tablename__ = "beta_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    is_used = Column(Boolean, default=False)
    used_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by_admin_id = Column(Integer, ForeignKey("admin_users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    used_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", backref="beta_code_usage")
    created_by_admin = relationship("AdminUser", backref="created_beta_codes")

class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SearchMetrics(Base):
    __tablename__ = "search_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for anonymous users
    user_session_id = Column(String, nullable=True)  # For anonymous users
    problem_description = Column(Text, nullable=False)
    business_type = Column(String, nullable=True)
    result_count_requested = Column(Integer, nullable=False)
    result_count_returned = Column(Integer, nullable=False)
    posts_scraped = Column(Integer, nullable=False)
    posts_analyzed = Column(Integer, nullable=False)
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    model_used = Column(String, nullable=True)
    search_duration_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="search_metrics")

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Migration function to add missing columns
def migrate_database():
    """Add missing columns to existing tables if they don't exist"""
    from sqlalchemy import inspect, text
    
    db = SessionLocal()
    try:
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('users')]
        
        # Check and add last_search_time column if missing
        if 'last_search_time' not in columns:
            print("🔄 MIGRATION: Adding missing column 'last_search_time' to users table...")
            db.execute(text("ALTER TABLE users ADD COLUMN last_search_time REAL DEFAULT 0.0"))
            db.commit()
            print("✅ MIGRATION: Successfully added 'last_search_time' column")
        else:
            print("✅ MIGRATION: Column 'last_search_time' already exists")
            
    except Exception as e:
        print(f"⚠️ MIGRATION WARNING: {e}")
        db.rollback()
    finally:
        db.close()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database with admin user
def init_database():
    create_tables()
    migrate_database()  # Run migrations after creating tables
    
    from sqlalchemy.orm import Session
    from app.core.auth import get_password_hash
    
    db = SessionLocal()
    try:
        # Check if admin user already exists
        admin_user = db.query(AdminUser).filter(AdminUser.email == "szzein2005@gmail.com").first()
        if not admin_user:
            # Create admin user with consistent password hashing
            admin_user = AdminUser(
                email="szzein2005@gmail.com",
                password_hash=get_password_hash("Plokplok1"),
                name="Admin User",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Admin user created successfully")
        else:
            # Reset admin password to ensure it uses correct hashing method
            print("✅ Admin user already exists - resetting password hash for consistency")
            admin_user.password_hash = get_password_hash("Plokplok1")
            admin_user.is_active = True
            db.commit()
            print("✅ Admin password hash updated successfully")
            
        # Start with 0 beta codes - admin will generate them as needed
        existing_codes = db.query(BetaCode).count()
        print(f"✅ {existing_codes} beta codes currently exist")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

