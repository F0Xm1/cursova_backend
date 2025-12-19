from starlette import status
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

import models
from fastapi import FastAPI, Depends
from database import engine
from typing import Annotated
import auth
import articles
import polls
import profile
import subscription
import admin
from auth import get_user
from dependencies import db_dependency

app = FastAPI(title="Медіа-платформа API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(articles.router)
app.include_router(polls.router)
app.include_router(profile.router)
app.include_router(subscription.router)
app.include_router(admin.router)

models.Base.metadata.create_all(bind=engine)

user_dependency = Annotated[dict, Depends(get_user)]


@app.get("/", status_code=status.HTTP_200_OK)
async def root(user: user_dependency = None, db: db_dependency = None):
    """Головна сторінка API"""
    if user is None:
        return {
            "message": "Ласкаво просимо до Медіа-платформи API",
            "docs": "/docs",
            "status": "Для доступу до API потрібна авторизація"
        }
    return {
        "message": "Ласкаво просимо до Медіа-платформи API",
        "user": user,
        "docs": "/docs"
    }
