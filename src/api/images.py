from fastapi import APIRouter, UploadFile

from src.services.images import ImagesService
from src.utils.exceptions import NotAValidImageException, NotAValidImageHTTPException

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("/", summary="Загрузить фотографию")
async def upload_image(file: UploadFile):
    try:
        await ImagesService().upload_image(file)
    except NotAValidImageException as exc:
        raise NotAValidImageHTTPException from exc

    return { "status": "OK" }
