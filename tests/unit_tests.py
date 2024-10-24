import requests
import unittest
import hashlib


class TestSulfur(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:1391"

    def test_index(self):
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        json = {
            "username": "testuser",
            "passwordHash": hashlib.sha256("testpassword".encode()).hexdigest()
        }
        response = requests.post(f"{self.base_url}/register", json=json)
        self.assertEqual(response.status_code, 200)
        
        json = {
            "username": "testuser",
            "passwordHash": hashlib.sha256("testpassword".encode()).hexdigest(),
        }
        response = requests.post(f"{self.base_url}/auth", json=json)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
