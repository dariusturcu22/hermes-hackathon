from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Backend OK"}

Base.metadata.create_all(bind=engine)
