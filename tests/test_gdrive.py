from io import BytesIO

from msu_atpase_storage.gdrive_ import GDrive


def test_create_and_delete_file():
    drive = GDrive()
    file = drive.upload_content(BytesIO(b"rstrst"), "test_file.txt")
    drive.remove_file(file.id_)
