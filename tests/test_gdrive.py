import tempfile
from pathlib import Path

from msu_atpase_storage.gdrive_ import GDrive


def test_create_and_delete_file():
    drive = GDrive()
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_file = Path(tmpdirname) / "tmp_file.txt"
        with tmp_file.open("w") as f:
            f.write("pup")

        file = drive.upload_file(tmp_file, "____01")
    drive.remove_file(file.id_)
