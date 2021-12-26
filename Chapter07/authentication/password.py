import secrets
from passlib.context import CryptContext

# Hashing passwords
# Let's implement some important utility functions for hashing passwords. 
# Fortunately, libraries exist that provide the most secure and efficient algorithms for this task. 
# Here, we'll use passlib. 
# You can install it with its optional bcrypt dependency, which is one of the safest hash functions at the time of writing:
# $ pip install passlib[bcrypt]
# Now, we'll just instantiate the passlib classes and wrap some of their functions to make our lives easier:

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_token() -> str:
    return secrets.token_urlsafe(32)


# CryptContext is a very useful class since it allows us to work with different hash algorithms. 
# If, one day, a better algorithm than bcrypt emerges, we can just add it to our allowed schemes. 
# New passwords will be hashed using the new algorithm, but existing passwords will still be recognized (and optionally upgraded to the new algorithm).