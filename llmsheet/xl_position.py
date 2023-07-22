import re
from attrs import define
from typing import Optional

from llmsheet.geometry import col_to_idx, idx_to_col, parse_position

@define
class XLPosition():
    col: str
    row: int
    sheet: Optional[str] = None

    def __str__(self):
        sheet = f"'{self.sheet}'!" if self.sheet else ''
        return f"{sheet}{self.col}{self.row}"

    @classmethod
    def from_str(cls, ref: str) -> "XLPosition":
        (col, row, sheet) = parse_position(ref)
        return cls(col, row, sheet)

    def from_offset(self, col: int, row: int) -> "XLPosition":
        new_col = _col_offset( self.col, col )
        new_row = self.row + row

        if new_row < 1:
            raise ValueError(f"offset {row} to column {self.row} would be before 1")

        return XLPosition(new_col, new_row)

def _col_offset( col: str, offset: int ) -> str:
    # Turn current col into a number first
    num = col_to_idx(col)

    # Do the math
    num = num + offset
    if num < 1:
        raise ValueError(f"offset {offset} to column {col} would be before A")

    # And back again to a string
    return idx_to_col(num)