import shutil

from fastapi import UploadFile
from src.services.base import BaseService
from src.tasks.tasks import resize_image


class ImagesService(BaseService):
    
    async def upload_image(self, file: UploadFile):
        image_path = f"src/media/images/{file.filename}"
        with open(image_path, "wb+") as image:
            shutil.copyfileobj(file.file, image)

        resize_image.delay(
            image_path, 
            "src/media/images/", 
            (300, 700, 1000)
        )
