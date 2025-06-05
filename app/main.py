from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.auth import auth_router
from app.routers.reccomendation import recommendation_router

app = FastAPI()
app.mount("/home", StaticFiles(directory="frontend/home", html=True), name="static")
app.mount("/login", StaticFiles(directory="frontend/login", html=True), name="static")
app.mount("/pictures", StaticFiles(directory="frontend/pictures", html=True), name="static")

app.include_router(auth_router)
app.include_router(recommendation_router)
