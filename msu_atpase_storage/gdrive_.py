from io import BytesIO
from typing import Sequence

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from msu_atpase_storage.config import settings
from msu_atpase_storage.types_ import GDriveFile


class GDrive:
    def __init__(self):
        gauth = GoogleAuth(settings_file=settings.gdrive_settings_path)
        gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
        self.drive = GoogleDrive(gauth)

    def upload_content(self, content: BytesIO, file_name: str) -> GDriveFile:
        # TODO обрабатывать tmp файл
        file = self.drive.CreateFile({"parents": [{"id": settings.gdrive_folder_id}], "title": file_name})

        file.SetContentString(content.read().decode())
        file.Upload()
        file.InsertPermission({"type": "anyone", "value": "anyone", "role": "reader"})
        fobj = GDriveFile(id_=file["id"], filename=file_name, link=file["alternateLink"])
        return fobj

    def remove_file(self, file_id: str):
        file = self.drive.CreateFile({"id": file_id})
        file.Delete()

    def list_content(self) -> Sequence[str]:
        file_list = self.drive.ListFile({"q": f"'{settings.gdrive_folder_id}' in parents and trashed=false"}).GetList()
        return file_list  # Has title and id fields
