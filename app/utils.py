from passlib.context import CryptContext

# telling the passlib, the default hashing algorithm (bcrypt in this case) 
# being used on passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

# a function to perform the hashing
def hash(password:str):
    return pwd_context.hash(password)

# a function to verify the password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

    