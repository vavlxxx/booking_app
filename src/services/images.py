import os
import shutil
from pathlib import Path

from PIL import Image
from fastapi import UploadFile

from src.services.base import BaseService
from src.tasks.tasks import resize_image
from src.utils.exceptions import NotAValidImageException


class ImagesService(BaseService):
    async def is_valid_image(self, image_path: UploadFile):
        try:
            with Image.open(image_path) as img:
                img.verify()
        except (IOError, SyntaxError):
            os.remove(image_path)
            raise NotAValidImageException

    async def upload_image(self, file: UploadFile):
        image_path = f"src/media/images/{file.filename}"

        base_dir = Path(__file__).parent.parent
        media_dir = base_dir / "media" / "images"
        media_dir.mkdir(parents=True, exist_ok=True)

        with open(image_path, "wb+") as image:
            shutil.copyfileobj(file.file, image)

        await self.is_valid_image(image_path)

        resize_image.delay(image_path, "src/media/images/", (300, 700, 1000))
