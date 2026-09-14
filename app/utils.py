# CryptContext: configurable password hashing/verification helper
from passlib.context import CryptContext

# pwd_context: hashes with bcrypt; deprecated="auto" flags older schemes for rehashing if any are added later
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# hash_password: returns the bcrypt hash of a plaintext password, safe to store in the database
def hash_password(password: str):
    return pwd_context.hash(password)


# verify_password: checks a plaintext password against a stored bcrypt hash, returns True/False
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


