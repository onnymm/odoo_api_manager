from typing import Literal
from ._base import ListOrItem
from ._literals import MostCommonFields

_LogicOperator = Literal["&", "|"]

_ComparisonOperator = Literal[
    "=",
    "!=",
    "in",
    "not in",
    "ilike",
    "not ilike",
    ">",
    "<",
    ">=",
    "<=",
]

_SerializableValue = int | float | str | bool | None

_TripletValue = ListOrItem[_SerializableValue]

Triplet = tuple[MostCommonFields, _ComparisonOperator, _TripletValue]

CriteriaStructure = list[_LogicOperator | Triplet]
