from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix = "/users",
    tags= ['Users']
)


# ------------ PATH ROUTES FOR USERS -----------------------------


# registration of a user (POST REQUEST --> send data to server)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password -> retrived from user.password
    user.password = utils.hash(user.password)

    # storing the details of new user in new_user
    new_user = models.User(**user.dict())

    # add the new user to database: db - relation: users
    db.add(new_user)
    
    # commit the changes to db
    db.commit()
    
    # refresh the db and store the newly added users in new_user
    db.refresh(new_user)
    
    return new_user


# show a specific user (GET REQUEST --> retrieve data from server)
@router.get("/{id}", response_model=schemas.User)    
def get_user(id: int, db: Session = Depends(get_db)):    

    # find the user with specific id    
    user = db.query(models.User).filter(models.User.id == id).first()

    # if the user doesn't exist throw an exception
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f"The user with id: {id} was not found")
        
    # else return the details of the user    
    return user
