import bcrypt
import jwt
import datetime
import os

class Security:
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def check_password(password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    @staticmethod
    def generate_jwt(user_id):
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        }
        return jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def decode_jwt(token):
        try:
            return jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None
