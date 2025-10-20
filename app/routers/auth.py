from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import os

from app.database import get_db, User, AdminUser, BetaCode
from app.models.auth import UserLoginRequest, AuthResponse, UserResponse, UserSignupRequest
from app.core.auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash

router = APIRouter()

@router.post("/login", response_model=AuthResponse)
async def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return access token"""
    
    print(f"🔍 LOGIN DEBUG: Attempting login for email: {request.email}")
    
    # Find user
    user = db.query(User).filter(User.email == request.email).first()
    print(f"🔍 LOGIN DEBUG: User found: {user is not None}")
    if user:
        print(f"🔍 LOGIN DEBUG: User email: {user.email}, active: {user.is_active}")
    
    if not user or not verify_password(request.password, user.password_hash):
        print(f"🔍 LOGIN DEBUG: Authentication failed - user exists: {user is not None}")
        if user:
            print(f"🔍 LOGIN DEBUG: Password verification failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    print(f"🔍 LOGIN DEBUG: Creating response for user: {user.email}")
    
    response = {
        "access_token": access_token,
        "user": UserResponse.model_validate(user).model_dump()
    }
    
    print(f"🔍 LOGIN DEBUG: Response created successfully, returning to client")
    return response

@router.post("/admin/login", response_model=AuthResponse)
async def admin_login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """Authenticate admin user and return access token"""
    
    print(f"🔍 ADMIN LOGIN DEBUG: Attempting admin login for email: {request.email}")
    
    # Find admin user
    admin_user = db.query(AdminUser).filter(AdminUser.email == request.email).first()
    print(f"🔍 ADMIN LOGIN DEBUG: Admin user found: {admin_user is not None}")
    
    if not admin_user or not verify_password(request.password, admin_user.password_hash):
        print(f"🔍 ADMIN LOGIN DEBUG: Admin authentication failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not admin_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin account is deactivated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with admin flag
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin_user.email, "admin": True}, expires_delta=access_token_expires
    )
    
    print(f"🔍 ADMIN LOGIN DEBUG: Creating admin response for: {admin_user.email}")
    
    # Create user response from admin user
    user_response = {
        "id": admin_user.id,
        "email": admin_user.email,
        "name": admin_user.name,
        "company": "Admin",
        "beta_code": "",
        "is_active": admin_user.is_active,
        "created_at": admin_user.created_at
    }
    
    response = {
        "access_token": access_token,
        "user": user_response
    }
    
    print(f"🔍 ADMIN LOGIN DEBUG: Admin response created successfully")
    return response

@router.post("/signup", response_model=AuthResponse)
async def signup(request: UserSignupRequest, db: Session = Depends(get_db)):
    """Create new user account with beta code validation"""
    
    print(f"🔍 SIGNUP DEBUG: Attempting signup for email: {request.email}")
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate beta code
    beta_code = db.query(BetaCode).filter(BetaCode.code == request.beta_code).first()
    if not beta_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid beta code"
        )
    
    if beta_code.is_used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Beta code already used"
        )
    
    # Create new user
    hashed_password = get_password_hash(request.password)
    new_user = User(
        email=request.email,
        password_hash=hashed_password,
        name=request.name,
        company=request.company,
        is_active=True,
        is_admin=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Mark beta code as used
    beta_code.is_used = True
    beta_code.used_by_user_id = str(new_user.id)
    db.commit()
    
    print(f"🔍 SIGNUP DEBUG: User created successfully: {new_user.email}")
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )
    
    response = {
        "access_token": access_token,
        "user": UserResponse.model_validate(new_user).model_dump()
    }
    
    print(f"🔍 SIGNUP DEBUG: Signup response created successfully")
    return response

@router.post("/init-admin")
async def init_admin(db: Session = Depends(get_db)):
    """Initialize admin user in database (one-time setup)"""
    
    print(f"🔧 INIT ADMIN: Attempting to initialize admin user")
    
    # Check if admin user already exists
    existing_admin = db.query(AdminUser).filter(AdminUser.email == "szzein2005@gmail.com").first()
    if existing_admin:
        return {"message": "Admin user already exists", "status": "success"}
    
    try:
        # Create admin user
        hashed_password = get_password_hash("Plokplok1")
        admin_user = AdminUser(
            email="szzein2005@gmail.com",
            password_hash=hashed_password,
            name="Salah Zein",
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"✅ Admin user created successfully: {admin_user.email}")
        
        # Create initial beta codes
        beta_codes = ["ADMIN2024", "HOPE2024", "BETA2024"]
        for code in beta_codes:
            # Check if beta code already exists
            existing_code = db.query(BetaCode).filter(BetaCode.code == code).first()
            if not existing_code:
                beta_code = BetaCode(
                    code=code,
                    is_used=False,
                    created_by_admin_id=admin_user.id
                )
                db.add(beta_code)
                print(f"✅ Beta code created: {code}")
        
        db.commit()
        
        return {
            "message": "Admin user and beta codes created successfully",
            "status": "success",
            "admin_email": "szzein2005@gmail.com",
            "beta_codes": beta_codes
        }
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return {"message": f"Error creating admin user: {str(e)}", "status": "error"}

@router.get("/test-db")
async def test_database(db: Session = Depends(get_db)):
    """Test database connection and show info"""
    try:
        # Get database URL info first
        database_url = os.getenv("DATABASE_URL", "Not set")
        
        # Test basic connection
        from sqlalchemy import text
        result = db.execute(text("SELECT 1 as test")).fetchone()
        
        # Check if tables exist
        admin_count = db.query(AdminUser).count()
        user_count = db.query(User).count()
        beta_count = db.query(BetaCode).count()
        
        return {
            "database_connection": "success",
            "database_url": database_url[:30] + "..." if len(database_url) > 30 else database_url,
            "admin_users": admin_count,
            "regular_users": user_count,
            "beta_codes": beta_count,
            "test_query": result[0] if result else None,
            "database_type": "PostgreSQL" if database_url.startswith("postgresql://") else "SQLite"
        }
    except Exception as e:
        return {
            "database_connection": "failed",
            "error": str(e),
            "database_url": os.getenv("DATABASE_URL", "Not set"),
            "database_type": "Unknown"
        }