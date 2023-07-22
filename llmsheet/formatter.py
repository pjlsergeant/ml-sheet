# xlsxwriter makes formatting pretty hard for what feel like they should be
# quite straight-forward operations; I suspect this is due to the underlying
# implementation. This file provides some abstractions meant to help with that

from typing import Any, Dict, Tuple
import attr
from attr import define

FormatKey = Tuple[Tuple[str, str]]
FormatAttr = Dict[str, str]

def key_for_attributes( x: FormatAttr ) -> FormatKey:
    return tuple(sorted(x.items()))

@define
class Formatter():
    workbook: Any
    _formats: Dict[FormatKey, Any] = attr.ib(factory=dict)

    @classmethod
    def lazy(cls, workbook: Any):
        obj = cls(workbook)
        def _find_or_create_format(format_attrs: FormatAttr):
            return obj.find_or_create_format(format_attrs)
        return _find_or_create_format

    def find_or_create_format(self, format_attrs: FormatAttr):
        key = key_for_attributes( format_attrs )
        if not key in self._formats:
            self._formats[key] = self.workbook.add_format( format_attrs )
        return self._formats[key]
