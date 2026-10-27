"""
Smart NER Logistics Control Platform
User Management, Cryptographic Password Encryption & Persistent Credentials Store
"""

import os
import json
import uuid
import secrets
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any

try:
    from backend.db.database import SessionLocal
    from backend.db.models import UserModel
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")

def hash_password(password: str, salt: Optional[str] = None) -> str:
    """
    Encrypts password using salted PBKDF2-HMAC-SHA256 with 100,000 iterations.
    Format: pbkdf2:sha256:100000$<salt>$<hash>
    """
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"pbkdf2:sha256:100000${salt}${key.hex()}"

def verify_password(plain_password: str, encrypted_password: str) -> bool:
    """
    Verifies a plain password against the stored encrypted hash using constant-time comparison.
    """
    try:
        parts = encrypted_password.split("$")
        if len(parts) != 3:
            return False
        algorithm, salt, stored_hash = parts
        computed = hash_password(plain_password, salt=salt)
        return secrets.compare_digest(computed, encrypted_password)
    except Exception:
        return False

class UserService:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.users: Dict[str, Dict[str, Any]] = {}
        self._load_or_seed_users()

    def _db_load_users(self) -> Dict[str, Dict[str, Any]]:
        """Attempts to load users from the connected PostgreSQL / SQLite database."""
        if not DB_AVAILABLE:
            return {}
        try:
            db = SessionLocal()
            try:
                db_users = db.query(UserModel).all()
                if db_users:
                    result = {}
                    for u in db_users:
                        d = u.to_dict()
                        d["username"] = d["email"]
                        d["role_display"] = d.get("role", "Operator")
                        d["is_active"] = True
                        result[u.id] = d
                    return result
            finally:
                db.close()
        except Exception as e:
            print(f"[UserService] Database load bypassed or unavailable: {e}")
        return {}

    def _db_save_user(self, user_record: Dict[str, Any]):
        """Persists a new or updated user to the database."""
        if not DB_AVAILABLE:
            return
        try:
            db = SessionLocal()
            try:
                existing = db.query(UserModel).filter(UserModel.id == user_record["id"]).first()
                if not existing:
                    existing = db.query(UserModel).filter(UserModel.email == user_record["email"]).first()
                
                if existing:
                    existing.full_name = user_record["name"]
                    existing.phone = user_record.get("phone")
                    existing.role = user_record["role"]
                    existing.organization = user_record.get("organization")
                    existing.encrypted_password = user_record["encrypted_password"]
                    existing.last_login = user_record.get("last_login")
                    existing.status = user_record.get("status", "Active")
                else:
                    new_user = UserModel(
                        id=user_record["id"],
                        full_name=user_record["name"],
                        email=user_record["email"],
                        phone=user_record.get("phone"),
                        role=user_record["role"],
                        organization=user_record.get("organization"),
                        encrypted_password=user_record["encrypted_password"],
                        status=user_record.get("status", "Active"),
                        created_at=user_record.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        last_login=user_record.get("last_login")
                    )
                    db.add(new_user)
                db.commit()
            finally:
                db.close()
        except Exception as e:
         import traceback
         print("[UserService] DATABASE SAVE ERROR:")
         print(str(e))
         traceback.print_exc()

    def _db_update_login(self, user_id: str, last_login: str):
        """Updates last_login timestamp in the database."""
        if not DB_AVAILABLE:
            return
        try:
            db = SessionLocal()
            try:
                user = db.query(UserModel).filter(UserModel.id == user_id).first()
                if user:
                    user.last_login = last_login
                    db.commit()
            finally:
                db.close()
        except Exception as e:
            pass

    def _load_or_seed_users(self):
        """Loads users from database or users.json, or seeds default accounts with encrypted passwords."""
        # 1. Try loading from database first
        db_users = self._db_load_users()
        if db_users:
            self.users = db_users
            self._save_to_disk()
            return

        # 2. Fallback to local users.json if database has no records or is offline
        if os.path.exists(USERS_FILE):
            try:
                with open(USERS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.users = {u["id"]: u for u in data}
                    if self.users:
                        # Sync file cache to database if DB is available
                        for u in self.users.values():
                            self._db_save_user(u)
                        return
            except Exception as e:
                print(f"[UserService] Warning loading users.json: {e}")

        # 3. Seed realistic default role accounts with encrypted passwords
        self._seed_default_users()
        self._save_to_disk()
        for u in self.users.values():
            self._db_save_user(u)

    def _seed_default_users(self):
        self.users = {}
        defaults = [
            {
                "name": "Dr. Anamika Barman",
                "email": "planner@nerlogistics.in",
                "username": "planner@nerlogistics.in",
                "phone": "+91 94350-11223",
                "role": "planner",
                "role_display": "Logistics Planner / Dispatch Operator",
                "organization": "NER Freight Control Hub, Guwahati",
                "raw_default_password": "Planner@123"
            },
            {
                "name": "Col. Ranjit Gogoi (Retd.)",
                "email": "gov@nerlogistics.in",
                "username": "gov@nerlogistics.in",
                "phone": "+91 98640-33445",
                "role": "government",
                "role_display": "Government Regional Emergency Control-Room",
                "organization": "North Eastern Council / Disaster Relief Cell",
                "raw_default_password": "Gov@123"
            },
            {
                "name": "Tashi Norbu",
                "email": "driver@nerlogistics.in",
                "username": "driver@nerlogistics.in",
                "phone": "+91 94351-88291",
                "role": "driver",
                "role_display": "Field Fleet Mountain Driver (Grade-A)",
                "organization": "Arunachal Hill Express Convoy",
                "raw_default_password": "Driver@123"
            },
            {
                "name": "System Administrator",
                "email": "admin@nerlogistics.in",
                "username": "admin@nerlogistics.in",
                "phone": "+91 98640-99999",
                "role": "admin",
                "role_display": "Platform Super Admin",
                "organization": "Smart NER Logistics Technical Operations",
                "raw_default_password": "Admin@123"
            }
        ]

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for d in defaults:
            uid = f"usr_{uuid.uuid4().hex[:8]}"
            enc_pwd = hash_password(d["raw_default_password"])
            self.users[uid] = {
                "id": uid,
                "name": d["name"],
                "email": d["email"].lower().strip(),
                "username": d["username"].lower().strip(),
                "phone": d["phone"],
                "role": d["role"],
                "role_display": d["role_display"],
                "organization": d["organization"],
                "encrypted_password": enc_pwd,
                "created_at": now,
                "last_login": None,
                "is_active": True
            }

    def _save_to_disk(self):
        """Persists all user records with encrypted passwords to backend/data/users.json."""
        try:
            temp_file = USERS_FILE + ".tmp"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(list(self.users.values()), f, indent=2)
            os.replace(temp_file, USERS_FILE)
        except Exception as e:
            print(f"[UserService] Error saving users.json: {e}")

    def find_by_email_or_username(self, identifier: str) -> Optional[Dict[str, Any]]:
        clean = identifier.lower().strip()
        for u in self.users.values():
            if u["email"].lower() == clean or u["username"].lower() == clean:
                return u
        return None

    def find_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.users.get(user_id)

    def register_user(
        self,
        name: str,
        email: str,
        password: str,
        role: str = "planner",
        phone: Optional[str] = None,
        organization: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Registers a new user, hashes/encrypts password with salt, and persists to users.json.
        """
        clean_email = email.lower().strip()
        if not clean_email or "@" not in clean_email:
            raise ValueError("A valid email address is required.")
        if not name or len(name.strip()) < 2:
            raise ValueError("Full name must be at least 2 characters.")
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")
        if self.find_by_email_or_username(clean_email):
            raise ValueError("An account with this email address already exists.")

        role = role.lower().strip() if role else "planner"
        if role not in ["planner", "government", "driver", "admin"]:
            role = "planner"

        role_titles = {
            "planner": "Logistics Planner / Dispatch Operator",
            "government": "Government Regional Emergency Control-Room",
            "driver": "Field Fleet Mountain Driver",
            "admin": "Platform Administrator"
        }

        uid = f"usr_{uuid.uuid4().hex[:8]}"
        encrypted_pwd = hash_password(password)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        user_record = {
            "id": uid,
            "name": name.strip(),
            "email": clean_email,
            "username": clean_email,
            "phone": phone.strip() if phone else "N/A",
            "role": role,
            "role_display": role_titles.get(role, "Logistics Operator"),
            "organization": organization.strip() if organization else "NER Logistics Network",
            "encrypted_password": encrypted_pwd,
            "created_at": now,
            "last_login": now,
            "is_active": True
        }

        self.users[uid] = user_record
        self._save_to_disk()
        self._db_save_user(user_record)
        return user_record

    def authenticate_user(self, identifier: str, raw_password: str) -> Optional[Dict[str, Any]]:
        """
        Validates raw password against the encrypted hash.
        Updates last_login upon successful authentication.
        """
        user = self.find_by_email_or_username(identifier)
        if not user:
            return None
        if not verify_password(raw_password, user["encrypted_password"]):
            return None

        # Update last login timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user["last_login"] = now
        self._save_to_disk()
        self._db_update_login(user["id"], now)
        return user

    def get_all_credentials(self) -> List[Dict[str, Any]]:
        """
        Returns all registered credentials in the system with their encrypted password hashes.
        Fulfills user requirement: "i need all the credentials entered by the user but password must be remained encrypted"
        """
        # Refresh from database if connected
        if DB_AVAILABLE:
            db_users = self._db_load_users()
            if db_users:
                self.users = db_users

        records = []
        for u in self.users.values():
            records.append({
                "id": u["id"],
                "name": u["name"],
                "email": u["email"],
                "username": u["username"],
                "phone": u.get("phone", "N/A"),
                "role": u["role"],
                "role_display": u.get("role_display", u["role"]),
                "organization": u.get("organization", "N/A"),
                "encrypted_password": u["encrypted_password"],  # Preserved in salted PBKDF2 encrypted form
                "created_at": u["created_at"],
                "last_login": u.get("last_login") or "Never",
                "is_active": u.get("is_active", True)
            })
        # Sort newest first
        records.sort(key=lambda x: x["created_at"], reverse=True)
        return records

# Global singleton
user_service = UserService()
