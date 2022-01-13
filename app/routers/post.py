from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.sql import func
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

# ------------ PATH ROUTES FOR POSTS -----------------------------


# show all posts (GET REQUEST --> retrieve data from server)
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user : schemas.User = 
Depends(oauth2.get_current_user), limit : int = 10, search : Optional[str] = "",
skip : int = 0):
    
    # _databaseName_query(_tableName_) -> performs select * from _tableName_
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts




# create a post (POST REQUEST --> send data to server)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : schemas.User = 
Depends(oauth2.get_current_user)):
    
    print(current_user.id)

    # storing the new entry in new_post
    # **post.dict() will unpack all the key-value pairs --> useful when there
    # are lot of fields; manually typing those field names is avoided
    new_post = models.Post(owner_id = current_user.id,**post.dict())

    # add the new entry to database db
    db.add(new_post)
    
    # commit the changes to db
    db.commit()
    
    # refresh the db and store the newly added entries in new_post
    db.refresh(new_post)
    
    return new_post



# show a specific post (GET REQUEST --> retrieve data from server)
@router.get("/{id}", response_model=schemas.PostOut)    
def get_post(id: int, db: Session = Depends(get_db), current_user : schemas.User = 
Depends(oauth2.get_current_user)):
    
    # find the post with specific id
    # filter() -> searches the required id through all the ids in Post model
    #             used instead of where id == post.id
    # first() -> when an entry with the required id is found, it is returned
    #             rather than searching through all the entries even when 
    #             the id is found already
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    # if the post doesn't exists throw an exception
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")
        
    return post



# delete a specific post (DELETE REQUEST --> removes all current representations of the target resource)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user : schemas.User = 
Depends(oauth2.get_current_user)):
    
    # find the post with specific id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    # if the post with the specific id doesn't exists throw an exception
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail=f"post with id : {id} does not exist")
    
    # if the post doesn't belong to the current user
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Sorry! You're not authuorized to perform the requested action!")
    
    # else delete the entry with that required id
    post_query.delete(synchronize_session=False)
    
    # commit the changes to the db
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT )



# update a specific post (PUT REQUEST --> replaces all the current representations with the updated data)
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
current_user : schemas.User = 
Depends(oauth2.get_current_user)):
    
    # find the post with specific id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    Post = post_query.first()
    
    # if the id doesn't exists throw an exception
    if not Post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail=f"post with id : {id} does not exist")
    
    # if the post doesn't belong to the current user
    if Post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Sorry! You're not authuorized to perform the requested action!")
    
    # else update the post with new details
    post_query.update(post.dict(), synchronize_session=False)
    
    # commit the changes to the db
    db.commit()

    return post_query.first()

