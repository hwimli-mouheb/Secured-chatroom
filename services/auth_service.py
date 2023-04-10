import json
import hashlib
import secrets
from services.user_repository import UserRepository
from config.message import Message


class AuthService:
    @staticmethod
    def hash_password(password, salt):
        return hashlib.sha256(password + salt).hexdigest()

    @staticmethod
    def handle_login(login_object):
        if not login_object:
            return None
        username = login_object['username'].encode()
        password = login_object['password'].encode()
        user_from_db = UserRepository.get_by_username(username)
        if user_from_db:
            (db_password, db_salt) = user_from_db
            hashed_password = AuthService.hash_password(password, db_salt)
            return hashed_password == db_password
        return None

    @staticmethod
    def handle_register(register_object):
        if not register_object:
            return None
        register_object['salt'] = secrets.token_bytes(16)
        hashed_password = AuthService.hash_password(
            register_object['password'].encode(), register_object['salt'])
        register_object['password'] = hashed_password
        UserRepository.insert_user(register_object)
        return True

    @staticmethod
    def connect_chat(client):
        UserRepository.connect(client['username'])

    @staticmethod
    def disconnect_chat(client):
        UserRepository.disconnect(client['username'])
