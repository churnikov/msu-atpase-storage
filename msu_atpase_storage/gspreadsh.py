from typing import Optional

import gspread

from msu_atpase_storage.config import settings
from msu_atpase_storage.types_ import GSheetRow


class GSheet:
    """Google spreadsheets wrapper"""

    def __init__(self):
        gc = gspread.service_account(settings.gsheet_service_account_path)
        self.sh = gc.open(settings.gsheet_name).sheet1

    def get_next_free_row_id(self):
        """Get next free id from table and its' first sheet."""
        values_list = self.sh.col_values(1)
        return len(values_list) + 1

    def add_row(self, data: GSheetRow, row_id: Optional[int] = None):
        """Add new row to google spreadsheet"""
        next_row_id = self.get_next_free_row_id() if row_id is None else row_id
        col_list = self.sh.range(f"A{next_row_id}:F{next_row_id}")
        for cl, value in zip(col_list, data):
            cl.value = value
        self.sh.update_cells(col_list)
