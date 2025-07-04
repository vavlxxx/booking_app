import shutil

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image


router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("/", summary="Загрузить фотографию")
async def upload_image(file: UploadFile):
    image_path = f"src/media/images/{file.filename}"
    with open(image_path, "wb+") as image:
        shutil.copyfileobj(file.file, image)
    
    resize_image.delay(
        image_path, 
        "src/media/images/", 
        (300, 700, 1000)
    )

    return {"status": "OK"}
