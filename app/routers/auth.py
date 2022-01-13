from fastapi import Depends, APIRouter, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2


router = APIRouter(tags=['Authentication'])



@router.post("/login", response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    # OAuth2PasswordRequestForm has 2 fields :
    #           1. username (email in this case)
    #           2. password (password in this case)
    # the user inputs are received in the form of OAuth2PasswordRequestForm

    # find the user with the given username
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # if user credentials doesn't exist for the given user id
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail =f"Invalid Credentials")

    # else validate the password

    # if the passwords dont match, throw an exception
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    # else create a token
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
    
    # return the token
    return {"access_token":access_token, "token_type" : "bearer"}

    