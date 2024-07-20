from fastapi import APIRouter

from memes_app.controllers.http.routers import meme


router = APIRouter()

router.include_router(meme.router, prefix='/memes', tags=['Memes'])
