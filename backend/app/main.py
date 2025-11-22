from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine

from .applications.router import router as applications_router
from .events.router import router as events_router
from .organizations.router import router as organizations_router
from .points_history.router import router as points_history_router
from .users.router import router as users_router

app = FastAPI()

app.include_router(applications_router)
app.include_router(events_router)
app.include_router(organizations_router)
app.include_router(points_history_router)
app.include_router(users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Backend OK"}
