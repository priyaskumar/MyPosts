from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote

origins = ['*']

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# includes all path operations of posts
app.include_router(post.router)

# includes all path operations of users
app.include_router(user.router)

# includes all path operations of users
app.include_router(auth.router)

# includes all path operations of votes
app.include_router(vote.router)

# home page (GET REQUEST --> from webpage to user)
@app.get("/")
async def root():
    return {"message":"Welcome to my API"}







