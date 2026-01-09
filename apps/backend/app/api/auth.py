"""Authentication API endpoints for user signup and signin.

This module provides JWT-based authentication with Better Auth integration.
It handles user registration, login, and token generation.

Endpoints:
- POST /api/auth/signup - Register new user
- POST /api/auth/signin - Login and get JWT token

Security:
- Passwords hashed with bcrypt (work factor 12)
- JWT tokens with configurable expiration
- Email validation and uniqueness checks
- Protection against timing attacks
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import get_session
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User

# Create router
router = APIRouter(prefix="/auth", tags=["Authentication"])


# ============================================================================
# Request/Response Schemas
# ============================================================================

class SignupRequest(BaseModel):
    """User registration request."""

    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["alice@example.com"]
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="User's password (8-100 characters)",
        examples=["SecureP@ssw0rd"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "alice@example.com",
                "password": "SecureP@ssw0rd"
            }
        }


class SigninRequest(BaseModel):
    """User login request."""

    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["alice@example.com"]
    )
    password: str = Field(
        ...,
        description="User's password",
        examples=["SecureP@ssw0rd"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "alice@example.com",
                "password": "SecureP@ssw0rd"
            }
        }


class UserResponse(BaseModel):
    """User information in response."""

    id: str = Field(..., description="User ID (UUID)")
    email: str = Field(..., description="User's email address")
    created_at: datetime = Field(..., description="Account creation timestamp")
    is_active: bool = Field(..., description="Account active status")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "alice@example.com",
                "created_at": "2026-01-09T12:00:00Z",
                "is_active": True
            }
        }


class AuthResponse(BaseModel):
    """Authentication response with JWT token."""

    success: bool = Field(True, description="Operation success status")
    message: str = Field(..., description="Success message")
    data: dict = Field(..., description="Response data")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "User authenticated successfully",
                "data": {
                    "user": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "email": "alice@example.com",
                        "created_at": "2026-01-09T12:00:00Z",
                        "is_active": True
                    },
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "Bearer",
                    "expires_in": 604800
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response format."""

    success: bool = Field(False, description="Operation success status")
    error: dict = Field(..., description="Error details")

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": {
                    "code": "EMAIL_EXISTS",
                    "message": "An account with this email already exists"
                }
            }
        }


# ============================================================================
# Authentication Endpoints
# ============================================================================

@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register New User",
    description="Create a new user account with email and password",
    responses={
        201: {
            "description": "User created successfully",
            "model": AuthResponse
        },
        400: {
            "description": "Invalid request (validation error)",
            "model": ErrorResponse
        },
        409: {
            "description": "Email already exists",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)
async def signup(
    request: SignupRequest,
    session: Session = Depends(get_session)
) -> AuthResponse:
    """Register a new user account.

    This endpoint creates a new user with hashed password and returns
    a JWT token for immediate authentication.

    Steps:
    1. Validate email format and password strength
    2. Check if email already exists
    3. Hash password with bcrypt
    4. Create user in database
    5. Generate JWT token
    6. Return user info and token

    Args:
        request: Signup request with email and password
        session: Database session (injected)

    Returns:
        AuthResponse with user data and JWT token

    Raises:
        HTTPException 409: Email already exists
        HTTPException 500: Database or hashing error
    """
    try:
        # Check if user already exists
        statement = select(User).where(User.email == request.email.lower())
        existing_user = session.exec(statement).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "success": False,
                    "error": {
                        "code": "EMAIL_EXISTS",
                        "message": "An account with this email already exists"
                    }
                }
            )

        # Hash password
        password_hash = hash_password(request.password)

        # Create new user
        new_user = User(
            email=request.email.lower(),
            password_hash=password_hash,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Save to database
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # Generate JWT token
        token = create_access_token(
            data={
                "userId": str(new_user.id),
                "email": new_user.email
            }
        )

        # Build response
        user_data = UserResponse(
            id=str(new_user.id),
            email=new_user.email,
            created_at=new_user.created_at,
            is_active=new_user.is_active
        )

        return AuthResponse(
            success=True,
            message="User registered successfully",
            data={
                "user": user_data.model_dump(),
                "token": token,
                "token_type": "Bearer",
                "expires_in": settings.JWT_EXPIRE_DAYS * 24 * 60 * 60  # seconds
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log error and return generic message
        print(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": {
                    "code": "SIGNUP_FAILED",
                    "message": "Failed to create user account"
                }
            }
        )


@router.post(
    "/signin",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="Authenticate user and get JWT token",
    responses={
        200: {
            "description": "Login successful",
            "model": AuthResponse
        },
        401: {
            "description": "Invalid credentials",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)
async def signin(
    request: SigninRequest,
    session: Session = Depends(get_session)
) -> AuthResponse:
    """Authenticate user and return JWT token.

    This endpoint verifies user credentials and returns a JWT token
    for authenticated requests.

    Steps:
    1. Find user by email
    2. Verify password hash
    3. Update last_login timestamp
    4. Generate JWT token
    5. Return user info and token

    Args:
        request: Signin request with email and password
        session: Database session (injected)

    Returns:
        AuthResponse with user data and JWT token

    Raises:
        HTTPException 401: Invalid email or password
        HTTPException 500: Database error
    """
    try:
        # Find user by email
        statement = select(User).where(User.email == request.email.lower())
        user = session.exec(statement).first()

        # Verify user exists and is active
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "error": {
                        "code": "INVALID_CREDENTIALS",
                        "message": "Invalid email or password"
                    }
                }
            )

        # Verify password
        if not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "error": {
                        "code": "INVALID_CREDENTIALS",
                        "message": "Invalid email or password"
                    }
                }
            )

        # Update last_login
        user.last_login = datetime.utcnow()
        session.add(user)
        session.commit()
        session.refresh(user)

        # Generate JWT token
        token = create_access_token(
            data={
                "userId": str(user.id),
                "email": user.email
            }
        )

        # Build response
        user_data = UserResponse(
            id=str(user.id),
            email=user.email,
            created_at=user.created_at,
            is_active=user.is_active
        )

        return AuthResponse(
            success=True,
            message="User authenticated successfully",
            data={
                "user": user_data.model_dump(),
                "token": token,
                "token_type": "Bearer",
                "expires_in": settings.JWT_EXPIRE_DAYS * 24 * 60 * 60  # seconds
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log error and return generic message
        print(f"Signin error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": {
                    "code": "SIGNIN_FAILED",
                    "message": "Failed to authenticate user"
                }
            }
        )


# Export router
__all__ = ["router"]
