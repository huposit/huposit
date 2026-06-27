from argon2 import PasswordHasher
from argon2.low_level import Type

password_hasher = PasswordHasher(type=Type.ID)


def hash_password(password: str) -> str:
    return password_hasher.hash(password)
