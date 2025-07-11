from fastapi import APIRouter, UploadFile

from src.services.images import ImagesService
from src.utils.file_manager import FileManager

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("/", summary="Загрузить фотографию")
async def upload_image(file: UploadFile):
    await ImagesService().upload_image(FileManager(file))
    return {
        "status": "OK",
        "detail": "Фотография была успешно загружена"
    }
