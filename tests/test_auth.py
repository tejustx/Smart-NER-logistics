"""
Smart NER Logistics Control Platform
Authentication & Password Encryption Automated Test Suite
"""

import sys
import os
import json
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.user_service import UserService, hash_password, verify_password

class TestAuthAndEncryption(unittest.TestCase):
    def setUp(self):
        self.service = UserService()

    def test_password_encryption_hashing(self):
        plain = "MountainPass@2026"
        encrypted = hash_password(plain)
        
        # Must start with pbkdf2:sha256:100000$
        self.assertTrue(encrypted.startswith("pbkdf2:sha256:100000$"), f"Unexpected hash format: {encrypted}")
        
        # Must not contain plain password
        self.assertNotIn(plain, encrypted)

        # Verification must succeed with correct password
        self.assertTrue(verify_password(plain, encrypted))

        # Verification must fail with wrong password
        self.assertFalse(verify_password("WrongPassword123", encrypted))

    def test_unique_salts_for_same_password(self):
        plain = "IdenticalPassword99"
        hash1 = hash_password(plain)
        hash2 = hash_password(plain)

        # Unique random salts ensure two identical passwords yield different hashes
        self.assertNotEqual(hash1, hash2)
        self.assertTrue(verify_password(plain, hash1))
        self.assertTrue(verify_password(plain, hash2))

    def test_user_registration_and_persistence(self):
        email = f"test_{os.urandom(4).hex()}@mountainlogistics.in"
        user = self.service.register_user(
            name="Sonam Tsering",
            email=email,
            password="StrongPassword!456",
            role="driver",
            phone="+91 94360-55443",
            organization="Tawang Hill Convoy"
        )

        self.assertIsNotNone(user["id"])
        self.assertEqual(user["email"], email)
        self.assertEqual(user["role"], "driver")
        
        # Stored password MUST be encrypted
        self.assertTrue(user["encrypted_password"].startswith("pbkdf2:sha256:100000$"))
        self.assertNotIn("StrongPassword!456", user["encrypted_password"])

        # Authenticate with valid password
        auth_user = self.service.authenticate_user(email, "StrongPassword!456")
        self.assertIsNotNone(auth_user)
        self.assertEqual(auth_user["name"], "Sonam Tsering")

        # Authenticate with invalid password
        bad_auth = self.service.authenticate_user(email, "WrongPassword")
        self.assertIsNone(bad_auth)

    def test_duplicate_email_rejection(self):
        email = f"dup_{os.urandom(4).hex()}@mountainlogistics.in"
        self.service.register_user(name="User One", email=email, password="Password123")
        with self.assertRaises(ValueError):
            self.service.register_user(name="User Two", email=email, password="Password123")

    def test_get_all_credentials_has_encrypted_passwords(self):
        credentials = self.service.get_all_credentials()
        self.assertGreater(len(credentials), 0)
        for cred in credentials:
            self.assertIn("encrypted_password", cred)
            self.assertTrue(cred["encrypted_password"].startswith("pbkdf2:sha256:100000$"))
            self.assertIn("name", cred)
            self.assertIn("email", cred)
            self.assertIn("role", cred)

if __name__ == "__main__":
    unittest.main()
