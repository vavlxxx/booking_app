import shutil
from pathlib import Path

from fastapi import UploadFile
from src.services.base import BaseService
from src.tasks.tasks import resize_image


class ImagesService(BaseService):
    
    async def upload_image(self, file: UploadFile):
        image_path = f"src/media/images/{file.filename}"
        base_dir = Path(__file__).parent.parent
        media_dir = base_dir / "media" / "images"
        media_dir.mkdir(parents=True, exist_ok=True)
        with open(image_path, "wb+") as image:
            shutil.copyfileobj(file.file, image)

        resize_image.delay(
            image_path, 
            "src/media/images/", 
            (300, 700, 1000)
        )
