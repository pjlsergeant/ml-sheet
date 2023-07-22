
from typing import Any, Dict
import xlsxwriter
import attr

class Worksheet:
    def __init__(self, label: str):
        self.label = label

    def render( self, workbook: xlsxwriter.Workbook ) -> None:
        worksheet = workbook.add_worksheet(self.label)
