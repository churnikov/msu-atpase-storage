from pathlib import Path
from typing import Sequence

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from msu_atpase_storage.config import settings
from msu_atpase_storage.types_ import GDriveFile


class GDrive:
    """
    Wrapper for pydrive.
    """

    def __init__(self):
        gauth = GoogleAuth(settings_file=settings.gdrive_settings_path)
        gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
        self.drive = GoogleDrive(gauth)

    def upload_file(self, path: Path, file_id: str) -> GDriveFile:
        """
        Upload file from a `path`. File will be saved as `file_id.ext`.
        We will take extension from `path`

        :param path: path of a file
        :param file_id: string id of a file
        :return: Meta info of a file saved in gdrive
        """
        file_name = file_id + "".join(path.suffixes)
        file = self.drive.CreateFile({"parents": [{"id": settings.gdrive_folder_id}], "title": file_name})

        file.SetContentFile(path)
        file.Upload()
        file.InsertPermission({"type": "anyone", "value": "anyone", "role": "reader"})
        fobj = GDriveFile(id_=file["id"], filename=file_name, link=file["alternateLink"])
        return fobj

    def remove_file(self, file_id: str) -> None:
        """
        Delete file from gdrive folder.

        :param file_id: gdrive id of a file (not ours)
        """
        file = self.drive.CreateFile({"id": file_id})
        file.Delete()

    def list_files(self) -> Sequence[str]:
        """List all files in a folder."""
        file_list = self.drive.ListFile({"q": f"'{settings.gdrive_folder_id}' in parents and trashed=false"}).GetList()
        return file_list  # Has title and id fields
