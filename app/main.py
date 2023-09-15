from fastapi import FastAPI
# The dot is current directory
from . import models
from .database import engine
from .routers import posts, users, auth, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


# Don't need this anymore because of alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

#This is to manage cors, for now it's set to everyone( Don't do this usually)
origins = ["*"]

# Middleware is function before running a requests
# Allow_origins = all domains that can talk to api
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)      
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

