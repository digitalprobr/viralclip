"""
Auth service: handles registration with password, login, JWT tokens, and user management.
Password rules: min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char.
"""
import os
import re
import secrets
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, VerificationToken

SECRET_KEY = os.getenv("AUTH_SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24h
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3001")


# ── Password Rules ───────────────────────────────────────────

PASSWORD_MIN_LENGTH = 8
PASSWORD_RULES = [
    ("At least 8 characters", lambda p: len(p) >= PASSWORD_MIN_LENGTH),
    ("At least one uppercase letter (A-Z)", lambda p: bool(re.search(r'[A-Z]', p))),
    ("At least one lowercase letter (a-z)", lambda p: bool(re.search(r'[a-z]', p))),
    ("At least one digit (0-9)", lambda p: bool(re.search(r'[0-9]', p))),
    ("At least one special character (!@#$%^&*)", lambda p: bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', p))),
]


def validate_password(password: str) -> list[str]:
    """Validate password against all rules. Returns list of error messages."""
    errors = []
    for rule_msg, rule_fn in PASSWORD_RULES:
        if not rule_fn(password):
            errors.append(rule_msg)
    return errors


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ── User Management ──────────────────────────────────────

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email.lower().strip()))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.username == username.lower().strip()))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create_user(self, email: str, username: str | None = None, password: str | None = None) -> User:
        user = User(
            email=email.lower().strip(),
            username=username.lower().strip() if username else None,
            password_hash=hash_password(password) if password else None,
            email_verified=True if password else False,
            credits=50,
        )
        self.db.add(user)
        await self.db.flush()
        return user

    # ── Password Registration ────────────────────────────────

    async def register_with_password(
        self, username: str, email: str, password: str
    ) -> User:
        """
        Register a new user with username, email, and password.
        Validates password rules, checks uniqueness of email and username.
        """
        # Validate password
        errors = validate_password(password)
        if errors:
            raise ValueError(f"Password does not meet requirements: {'; '.join(errors)}")

        # Validate username
        username = username.strip()
        if len(username) < 3 or len(username) > 30:
            raise ValueError("Username must be between 3 and 30 characters")
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens")

        # Check uniqueness
        existing_email = await self.get_user_by_email(email)
        if existing_email:
            raise ValueError("An account with this email already exists")

        existing_username = await self.get_user_by_username(username)
        if existing_username:
            raise ValueError("This username is already taken")

        # Create user
        user = await self.create_user(email=email, username=username, password=password)
        return user

    # ── Password Login ───────────────────────────────────────

    async def login_with_password(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.
        Returns the user if credentials are valid, None otherwise.
        """
        user = await self.get_user_by_email(email)
        if not user or not user.password_hash:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    # ── Magic Link (kept for backwards compat) ───────────────

    async def create_magic_link(self, email: str) -> tuple[str, str]:
        email = email.lower().strip()
        user = await self.get_user_by_email(email)
        purpose = "login" if user else "register"

        token_str = VerificationToken.generate_token()
        token = VerificationToken(
            token=token_str,
            email=email,
            user_id=user.id if user else None,
            purpose=purpose,
            expires_at=VerificationToken.default_expiry(),
        )
        self.db.add(token)
        await self.db.flush()

        return token_str, purpose

    async def verify_magic_link(self, token_str: str) -> Optional[User]:
        result = await self.db.execute(
            select(VerificationToken).where(
                VerificationToken.token == token_str,
                VerificationToken.used == False,  # noqa: E712
                VerificationToken.expires_at > datetime.utcnow(),
            )
        )
        token = result.scalar_one_or_none()
        if not token:
            return None

        token.used = True

        user = await self.get_user_by_email(token.email)
        if not user:
            user = await self.create_user(token.email)

        user.email_verified = True
        await self.db.flush()
        return user

    # ── JWT ───────────────────────────────────────────────────

    def create_access_token(self, user: User) -> str:
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def verify_access_token(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.PyJWTError:
            return None

    # ── Credits ──────────────────────────────────────────────

    async def check_credits(self, user: User, cost: int = 10) -> bool:
        return user.credits >= cost

    async def deduct_credits(self, user: User, cost: int = 10) -> int:
        user.credits = max(0, user.credits - cost)
        await self.db.flush()
        return user.credits

    def get_magic_link_url(self, token: str) -> str:
        return f"{FRONTEND_URL}/auth/callback?token={token}"
