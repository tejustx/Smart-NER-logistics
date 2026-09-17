"""
Smart NER Logistics Control Platform
Database Engine, Session Management & Supabase Connection
"""

import os
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Load environment variables from .env file
load_dotenv()

# Read DATABASE_URL from environment
RAW_DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

# Default fallback to SQLite if no Supabase/PostgreSQL URL is specified
SQLITE_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "ner_logistics.db"
)

IS_POSTGRES = False
DATABASE_URL = ""

if RAW_DATABASE_URL:
    # Normalize postgres:// to postgresql:// for SQLAlchemy compatibility
    if RAW_DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = RAW_DATABASE_URL.replace("postgres://", "postgresql://", 1)
    else:
        DATABASE_URL = RAW_DATABASE_URL
    IS_POSTGRES = True
else:
    os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
    DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"

# Configure SQLAlchemy Engine
if IS_POSTGRES:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,    # Verifies connections before using them; prevents stale Supabase connection drops
        pool_recycle=300,      # Recycle connections every 5 minutes
        echo=False
    )
else:
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session and ensures proper closure.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_db_connection() -> dict:
    """
    Validates database connectivity and returns status metadata.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {
            "status": "connected",
            "type": "PostgreSQL (Supabase)" if IS_POSTGRES else "SQLite (Local Fallback)",
            "is_postgres": IS_POSTGRES,
            "url_masked": _mask_url(DATABASE_URL)
        }
    except Exception as e:
        return {
            "status": "error",
            "type": "PostgreSQL (Supabase)" if IS_POSTGRES else "SQLite (Local Fallback)",
            "is_postgres": IS_POSTGRES,
            "error": str(e)
        }

def _mask_url(url: str) -> str:
    if "@" in url:
        prefix, host = url.split("@", 1)
        scheme = prefix.split("://")[0]
        return f"{scheme}://****:****@{host}"
    return url
