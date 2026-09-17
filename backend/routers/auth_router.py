"""
Smart NER Logistics Control Platform
Authentication Router: Sign In, Sign Up, Session Verification & Credentials Vault API
"""

import secrets
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, status, Header
from pydantic import BaseModel, Field

from backend.services.user_service import user_service

router = APIRouter(prefix="/api/auth", tags=["Authentication & User Management"])

class SignUpRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=120)
    password: str = Field(..., min_length=6, max_length=100)
    role: Optional[str] = "planner"
    phone: Optional[str] = None
    organization: Optional[str] = None

class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=1)

class UserProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    username: str
    phone: str
    role: str
    role_display: str
    organization: str
    created_at: str
    last_login: Optional[str] = None

class AuthResponse(BaseModel):
    token: str
    user: UserProfileResponse
    message: str

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(req: SignUpRequest):
    """
    Registers a new user, hashes/encrypts password with salted PBKDF2, and saves to users.json.
    """
    try:
        user = user_service.register_user(
            name=req.name,
            email=req.email,
            password=req.password,
            role=req.role or "planner",
            phone=req.phone,
            organization=req.organization
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

    token = f"tok_{secrets.token_hex(24)}"
    return AuthResponse(
        token=token,
        user=UserProfileResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            username=user["username"],
            phone=user.get("phone", "N/A"),
            role=user["role"],
            role_display=user.get("role_display", user["role"]),
            organization=user.get("organization", "N/A"),
            created_at=user["created_at"],
            last_login=user.get("last_login")
        ),
        message="Account registered successfully. Encrypted credentials saved."
    )

@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest):
    """
    Authenticates user using email/username and raw password against salted encrypted hash.
    """
    user = user_service.authenticate_user(req.email, req.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email/username or password. Please verify credentials."
        )

    token = f"tok_{secrets.token_hex(24)}"
    return AuthResponse(
        token=token,
        user=UserProfileResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            username=user["username"],
            phone=user.get("phone", "N/A"),
            role=user["role"],
            role_display=user.get("role_display", user["role"]),
            organization=user.get("organization", "N/A"),
            created_at=user["created_at"],
            last_login=user.get("last_login")
        ),
        message=f"Welcome back, {user['name']}!"
    )

@router.get("/me")
def get_current_user(user_id: Optional[str] = None):
    """
    Returns user profile for the given user_id.
    """
    if not user_id:
        # Return first user or default planner if no ID
        credentials = user_service.get_all_credentials()
        if credentials:
            u = credentials[0]
            return {
                "id": u["id"],
                "name": u["name"],
                "email": u["email"],
                "role": u["role"],
                "role_display": u["role_display"],
                "organization": u["organization"]
            }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active user found.")

    user = user_service.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "role_display": user.get("role_display", user["role"]),
        "organization": user.get("organization", "N/A")
    }

@router.get("/credentials", response_model=List[Dict[str, Any]])
def get_all_credentials():
    """
    Returns all registered credentials with salted encrypted password hashes.
    Fulfills: 'i need all the credentials entered by the user but password must be remained encrypted'
    """
    return user_service.get_all_credentials()

@router.post("/reset-demo")
def reset_demo_users():
    """
    Resets the default demo user accounts in users.json.
    """
    user_service._seed_default_users()
    user_service._save_to_disk()
    return {"message": "Demo user credentials reset successfully."}
