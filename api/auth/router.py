"""
Auth routes: register with password, login, verify magic link, logout, me.
"""
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from pydantic import BaseModel

from api.auth.service import AuthService
from api.auth.dependencies import get_auth_service, get_current_user
from api.auth.email import send_magic_link_email
from core.models import User
from api.limiter import limiter

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


# ── Schemas ──────────────────────────────────────────────

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class EmailRequest(BaseModel):
    email: str


class AuthResponse(BaseModel):
    message: str
    purpose: str | None = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str | None
    name: str | None
    email_verified: bool
    credits: int

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ── Routes ───────────────────────────────────────────────

@router.post("/signup", response_model=TokenResponse)
@limiter.limit("5/minute")
async def signup(
    request: Request,
    body: SignupRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    """Register a new user with username, email, and password."""
    if body.password != body.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    try:
        user = await service.register_with_password(
            username=body.username,
            email=body.email,
            password=body.password,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    access_token = service.create_access_token(user)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=86400,
        samesite="lax",
        secure=False,
    )

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login(
    request: Request,
    body: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    """Login with email and password."""
    user = await service.login_with_password(body.email, body.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = service.create_access_token(user)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=86400,
        samesite="lax",
        secure=False,
    )

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


# ── Magic Link (kept for backwards compat) ───────────────

@router.post("/register", response_model=AuthResponse)
async def register_or_login_magic(
    body: EmailRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Send a magic link email (legacy flow)."""
    token, purpose = await service.create_magic_link(body.email)
    magic_url = service.get_magic_link_url(token)
    send_magic_link_email(body.email, magic_url, purpose)

    return AuthResponse(
        message=f"Magic link sent to {body.email}. Check your inbox!",
        purpose=purpose,
    )


@router.get("/verify")
async def verify_magic_link(
    token: str,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    """Verify magic link token and return JWT."""
    user = await service.verify_magic_link(token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired magic link")

    access_token = service.create_access_token(user)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=86400,
        samesite="lax",
        secure=False,
    )

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    """Get current authenticated user profile."""
    return UserResponse.model_validate(user)


@router.post("/logout")
async def logout(response: Response):
    """Clear session cookie."""
    response.delete_cookie("access_token")
    return {"message": "Logged out"}
