from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_mins)



# a function to generate the access token for the user
def create_access_token(data: dict):
    # the payload generated from data dict (data has the user id)
    to_encode = data.copy()

    # sets the expiration time (30 mins from the current time)
    # datetime.utcnow()  -->  returns the current date and time
    # timedelta(minutes)  --> returns the time of 30 minutes
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # adding exiration time to the payload dict
    to_encode.update({"exp" : expire})

    # generating the token 
    # payload --> to_encode 
    # signature --> to_encode + algorithm + SECRET_KEY 
    # header --> algorithm 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # return the encoded token
    return encoded_jwt


    

# a function to verify the token sent by the user is valid and hasn't expired
def verify_access_token(token:str,credentials_exception):

    try:
        # decode the
        #  payload from the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM,])

        # extract the user id from the payload
        id = payload.get("user_id")

        # if the id doesn't exist throw an exception
        if not id:
            raise credentials_exception

        # validate the token data if id exists
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    # returns the token_data
    return token_data



# a function that can be passed as a dependency that (i) gets the token,
# (ii) verifies if he has the valid access_token,
# (iii) then fetches the user from the db and add to the path operations 
# that require users to be logged in to access the data from the fastapi
def get_current_user(token : str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    # define the credentials_exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials",
        headers={"WWW-Authenticate" : "Bearer"})

    # verify the access_token 
    verified_token = verify_access_token(token, credentials_exception)

    # fetch the user from db (users)
    user = db.query(models.User).filter(models.User.id == verified_token.id).first()

    return user