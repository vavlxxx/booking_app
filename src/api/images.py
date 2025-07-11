from fastapi import APIRouter, UploadFile

from src.services.images import ImagesService

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("/", summary="Загрузить фотографию")
async def upload_image(file: UploadFile):
    await ImagesService().upload_image(file)
    return {
        "status": "OK",
        "detail": "Фотография была успешно загружена"
    }
