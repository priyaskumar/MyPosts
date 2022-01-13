from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

# to perform adding and deleting vote on a post
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # finding the post with the required id
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    # if the post doesn't exist throw an exception
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {vote.post_id} doesn't exist!")

    # find the entry in vote table with the required post id and current user id
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id , models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    # if the dir of vote request is 1
    if (vote.dir == 1):

        # if the entry already exist raise an exception (the user has already voted)
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")

        # else add the new vote to the votes table
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)

        # commit the changes in the db
        db.commit()
        
        return {"message": "successfully added vote"}

    # if the dir of vote request is 0
    else:

        # if the entry doesn't exist throw an exception (user hasn't voted yet)
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exist")

        # else delete the vote
        vote_query.delete(synchronize_session=False)
        
        # commit the changes to db
        db.commit()

        return {"message" : "successfully deleted the vote"}

