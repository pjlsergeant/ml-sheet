import re
from typing import Tuple
from typing import Optional

pattern = re.compile(r'^(?:(?P<sheet>[^!]+)!)?(?P<column>[A-Z]+)(?P<row>[0-9]+)$')

def col_to_idx(col: str) -> int:
    num = 0
    for i in range(len(col)):
        num = num * 26 + (ord(col[i]) - ord("A") + 1)
    return num


def idx_to_col(idx: int) -> str:
    col = ""
    while idx > 0:
        (idx, remainder) = divmod(idx - 1, 26)
        col = chr(65 + remainder) + col
    return col


def parse_position(ref: str) -> Tuple[str, int, Optional[str]]:
    match = pattern.match(ref)
    if not match:
        raise ValueError(f"Ref {ref} isn't a valid Excel reference")

    items = match.groupdict()
    sheet = items.get("sheet", None)
    if sheet:
        sheet = sheet.replace("'", '')

    return (items["column"], int(items["row"]), sheet )
