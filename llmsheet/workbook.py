
from typing import Any, Dict, List
import xlsxwriter
import attr

from llmsheet.worksheet import Worksheet


@attr.s(auto_attribs=True)
class Workbook:
    _sheets: List[Worksheet] = attr.Factory(list)
    _labels: Dict[str, str]= attr.Factory(dict)

    def add_sheet( self, id: str, worksheet: Worksheet):
        if id in self._labels:
            raise Exception(f"Already have a sheet with id {id}")
        label = worksheet.label
        if label in self._labels.values():
            raise Exception(f"Already have a sheet with label {label}")
        self._labels[id] = label
        self._sheets.append( worksheet )


    def render( self, filename: str ) -> None:
        workbook = xlsxwriter.Workbook("demo.xlsx")
        for sheet in self._sheets:
            sheet.render( workbook )
        workbook.close()
