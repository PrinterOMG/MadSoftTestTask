from fastapi import HTTPException, UploadFile, status


async def image_checker(image: UploadFile) -> UploadFile:
    if image.content_type not in ('image/png', 'image/jpeg'):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail='Unsupported media type. Only PNG and JPEG are supported',
        )

    max_size = 20 * 1024 * 1024  # 20 MB
    if image.size > max_size:  # Или можно использовать Middleware
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail='Request entity too large. Max size is 20 MB',
        )

    return image
