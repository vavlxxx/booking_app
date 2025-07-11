from fastapi import UploadFile


class FileManager:
    
    def __init__(self, file_obj: UploadFile):
        self.file_obj = file_obj

    @property
    def file(self):
        return self.file_obj
    
    @property
    def filename(self):
        return self.file_obj.filename
    