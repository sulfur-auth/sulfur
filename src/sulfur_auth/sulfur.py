from database import Database
import time
import uuid
import hashlib


class auth:
    def __init__(self, port: int = 1391, host: str = "0.0.0.0"):
        self.port = port
        self.host = host

        self.subscriptions: dict[str, list[callable]] = {}

        self.database = Database("sulfur-db")

        self.database.create_table("users", ["username", "passwordHash"])
        self.database.create_table("tokens", ["username", "token", "expiresAt"])

    def subscribe(self, topic: str, callback: callable):
        self.subscriptions[topic].append(callback)

    def unsubscribe(self, topic: str, callback: callable):
        self.subscriptions[topic].remove(callback)

    def publish(self, topic: str, ctx: any):
        for callback in self.subscriptions[topic]:
            callback(ctx)

    def check_if_user_exists(self, username: str):
        if self.database.select("users", {"username": username}):
            return True
        else:
            return False

    def check_if_authorized(self, token: str):
        self.prune_token(token)

        if self.database.select("tokens", {"token": token}):
            return self.database.select("tokens", {"token": token})[0]["username"]
        else:
            return False

    def gen_auth_token(self, username: str):
        if not self.check_if_user_exists(username):
            return {}

        expires_at = int(time.time()) + (60 * 60 * 12)  # 12 hours

        return {
            "username": username,
            "expiresAt": expires_at,
            "token": str(uuid.uuid4()),
        }

    def prune_token(self, token: str):
        if not self.database.select("tokens", {"token": token}):
            return False

        if (
            int(time.time())
            >= self.database.select("tokens", {"token": token})[0]["expiresAt"]
        ):
            self.database.delete("tokens", {"token": token})
            return True

        return False

    def remove_all_tokens(self, username: str):
        self.database.delete("tokens", {"username": username})

    def verify_password(self, username: str, password_hash: str):
        if not self.check_if_user_exists(username):
            return False

        if (
            self.database.select("users", {"username": username})[0]["passwordHash"]
            == password_hash
        ):
            return True
        else:
            return False

    def register(self, username: str, password_hash: str):
        if self.check_if_user_exists(username):
            self.publish("userRegister", "User already exists")
            return {}

        self.database.insert("users", [username, password_hash])
        
        self.publish("userRegister", {
            "username": username,
            "passwordHash": password_hash
        })
        return self.gen_auth_token(username)

    def auth(self, username: str, password_hash: str):
        if not self.verify_password(username, password_hash):
            self.publish("userAuth", "Invalid username or password")
            return {}

        token = self.gen_auth_token(username)

        self.database.insert("tokens", [username, token["token"], token["expiresAt"]])

        self.publish("userAuth", {
            "username": username,
            "token": token["token"],
            "expiresAt": token["expiresAt"]
        })
        return token
