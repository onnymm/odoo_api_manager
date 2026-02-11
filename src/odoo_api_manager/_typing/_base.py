from typing import TypeVar

_T = TypeVar('_T')
_O = TypeVar('_O')

ListOrItem = _T | list[_T]
