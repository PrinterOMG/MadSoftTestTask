from fastapi import APIRouter

from memes_app.controllers.http.routers import meme, file


router = APIRouter()

router.include_router(meme.router, prefix='/memes', tags=['Memes'])
router.include_router(file.router, prefix='/files', tags=['Files'])
