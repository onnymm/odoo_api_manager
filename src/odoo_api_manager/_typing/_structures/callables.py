from typing import (
    Any,
    Callable,
)
from .._base.generics import _T

SeriesApply = Callable[[_T], Any]
"""
Función a aplicar en Pandas Series

El tipado recibe un genérico, por ejemplo, `int`.

>>> fn: SeriesApply[int] = lambda value: ...
>>> 
>>> # Esto es exactamente lo mismo
>>> def fn(value: int):
>>>     ...

El retorno se tipa en base al retorno de la misma función.
"""
