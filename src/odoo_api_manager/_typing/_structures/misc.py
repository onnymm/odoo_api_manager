from typing import Union
from .._base.aliases import RecordID
from .._base.generics import _T
from .._base.literals import (
    ComparisonOperator,
    MostCommonFields,
)

ListOrItem = _T | list[_T]

AltDatabaseArg = Union[str, bool]
"""
Argumento de base de datos alternativa.
"""

ModelField = Union[MostCommonFields | str]
"""
Campo de modelo/registro.
"""

SerializableValue = Union[None, int, float, str, RecordID]
"""
Valor seriañizable a JSON.
"""

_FieldSerializableValue = Union[int, float, str, bool, None]

_TripletValue = ListOrItem[_FieldSerializableValue]

Triplet = tuple[MostCommonFields, ComparisonOperator, _TripletValue]

RecordData = dict[ModelField, SerializableValue]
"""
Datos de registro.
"""
