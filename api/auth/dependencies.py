"""
Authentication dependencies for FastAPI routes.
Implements 'deny by default' pattern from nextjs-senior-dev skill.
"""
from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from api.auth.service import AuthService


async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)


async def get_current_user_optional(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Returns user or None — for routes that work with or without auth."""
    token = _extract_token(request)
    if not token:
        return None
    service = AuthService(db)
    payload = service.verify_access_token(token)
    if not payload:
        return None
    return await service.get_user_by_id(int(payload["sub"]))


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Returns user or raises 401 — for protected routes."""
    token = _extract_token(request)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    service = AuthService(db)
    payload = service.verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await service.get_user_by_id(int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def _extract_token(request: Request) -> str | None:
    """Extract JWT from Authorization header or cookie."""
    # Try Authorization header first
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.removeprefix("Bearer ")

    # Try cookie
    return request.cookies.get("access_token")
