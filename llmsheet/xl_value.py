import abc
from typing import Union
import attr

@attr.define
class XLValue(abc.ABC):
    """
    Abstract class for something that can render into an Excel value
    """

    @abc.abstractmethod
    def __str__(self):
        pass

@attr.define
class XLConstant(XLValue):
    value: Union[str, int, float]

    def __str__(self):
        return str(self.value)