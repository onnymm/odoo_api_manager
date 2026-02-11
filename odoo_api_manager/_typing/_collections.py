from typing import Union
from ._literals import MostCommonFields
from ._aliases import RecordID

ModelField = Union[MostCommonFields | str]
"""
Campo de modelo/registro.
"""

SerializableValue = Union[None, int, float, str, RecordID]
"""
Valor seriañizable a JSON.
"""

RecordData = dict[ModelField, SerializableValue]
"""
Datos de registro.
"""
