import shutil

from src.services.base import BaseService
from src.utils.file_manager import FileManager
from src.tasks.tasks import resize_image


class ImagesService(BaseService):
    
    async def upload_image(self, file: FileManager):
        image_path = f"src/media/images/{file.filename}"
        with open(image_path, "wb+") as image:
            shutil.copyfileobj(file.file, image)
        
        resize_image.delay(
            image_path, 
            "src/media/images/", 
            (300, 700, 1000)
        )
