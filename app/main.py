from fastapi import FastAPI
from .database import engine
from app.routers import auth, message, user
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message.router)
app.include_router(user.router)
app.include_router(auth.router)


