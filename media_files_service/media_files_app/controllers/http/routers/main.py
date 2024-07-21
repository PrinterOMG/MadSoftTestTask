from fastapi import APIRouter

from media_files_app.controllers.http.routers import file


router = APIRouter()

router.include_router(file.router, prefix='/files')
