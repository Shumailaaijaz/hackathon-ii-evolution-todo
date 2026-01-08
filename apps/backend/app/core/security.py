"""Security utilities for JWT token validation.

This module provides functions for verifying JWT tokens issued by Better Auth.
All protected API endpoints use these utilities to authenticate requests.
"""

from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, status

from app.core.config import settings


def verify_jwt_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token from Better Auth.

    This function validates the token signature using BETTER_AUTH_SECRET
    and checks for expiration. It expects tokens to contain a 'userId' claim.

    Args:
        token: The JWT token string to verify

    Returns:
        The decoded token payload if valid, None if invalid

    Example:
        >>> payload = verify_jwt_token("eyJ...")
        >>> if payload:
        ...     user_id = payload.get("userId")
        ...     print(f"Authenticated user: {user_id}")
    """
    try:
        # Decode and verify token
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "require": ["userId", "exp", "iat"]
            }
        )

        # Verify userId claim exists
        if "userId" not in payload:
            return None

        return payload

    except jwt.ExpiredSignatureError:
        # Token has expired
        return None

    except jwt.InvalidTokenError:
        # Token is invalid (bad signature, malformed, etc.)
        return None

    except Exception:
        # Any other error (shouldn't happen with proper tokens)
        return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """Extract user ID from a JWT token.

    This is a convenience function that verifies the token and extracts
    the userId claim in one step.

    Args:
        token: The JWT token string

    Returns:
        The user ID if token is valid, None otherwise

    Example:
        >>> user_id = get_user_id_from_token("eyJ...")
        >>> if user_id:
        ...     # Fetch user's tasks
        ...     tasks = get_tasks_for_user(user_id)
    """
    payload = verify_jwt_token(token)
    return payload.get("userId") if payload else None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token.

    Note: This function is typically used by Better Auth for token generation.
    We include it here for testing purposes and potential future use.

    Args:
        data: Dictionary of claims to encode in the token
        expires_delta: Optional expiration time delta (defaults to JWT_EXPIRE_DAYS)

    Returns:
        Encoded JWT token string

    Example:
        >>> token = create_access_token({"userId": "user-123"})
        >>> # Token valid for 7 days (default)
    """
    to_encode = data.copy()

    # Set expiration
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.JWT_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })

    # Encode token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.BETTER_AUTH_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def validate_token_or_raise(token: str) -> dict:
    """Verify token and raise HTTPException if invalid.

    This function is used by API dependencies to ensure authentication.
    It raises a 401 Unauthorized exception with a clear message if the
    token is invalid or expired.

    Args:
        token: The JWT token string to verify

    Returns:
        The decoded token payload

    Raises:
        HTTPException: 401 if token is invalid or expired

    Example:
        >>> try:
        ...     payload = validate_token_or_raise(token)
        ...     user_id = payload["userId"]
        ... except HTTPException:
        ...     # Token is invalid, user not authenticated
        ...     pass
    """
    payload = verify_jwt_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


# Export commonly used functions
__all__ = [
    "verify_jwt_token",
    "get_user_id_from_token",
    "create_access_token",
    "validate_token_or_raise",
]
