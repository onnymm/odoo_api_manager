from typing import Optional
from .._typing import (
    CriteriaStructure,
    RecordData,
    RecordID,
    AccessRights,
    ListOrItem,
    ModelField,
    SerializableValue,
)

class Params:

    def __init__(
        self,
        /,
        record_ids: Optional[RecordID] = None,
        search_criteria: Optional[CriteriaStructure] = None,
        records_data: ListOrItem[RecordData] | None = None,
        fields: Optional[list[ModelField]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        raise_exception: Optional[bool] = None,
        right_type: Optional[AccessRights] = None,
        kwargs: dict[str, SerializableValue] = None,
    ) -> None:

        # Plantilla de args
        self.args = [record_ids, search_criteria, records_data, right_type]

        # Plantilla de kwargs
        self.kwargs = {
            'fields': fields,
            'offset': offset,
            'limit': limit,
            'raise_exception': raise_exception,
            'kwargs': kwargs,
        }

        # Construcción de args y kwargs
        self._build_args()
        self._build_kwargs()

    def _build_args(
        self,
    ) -> list:
        """
        ### Construcción de args
        Este método construye una lista de args que tienen valores diferentes a `None`
        para ser usados en solicitud al API.
        """

        # Construcción de args sin nulos
        self.args = [
            item
            for item in self.args
            if item is not None
        ]

    def _build_kwargs(
        self,
    ) -> dict:
        """
        ## Construcción de kwargs
        Este método interno construye un diccionario de kwargs que tienen valores
        diferentes a None para ser usados en solicitudes al API.
        """

        # Si existen valores en llave 'kwargs'...
        if self.kwargs['kwargs'] is not None:
            # Se toma una copia de ésta
            kwargs = self.kwargs['kwargs'].copy()
            # Se transcriben los argumentos al objeto
            for ( k, v ) in kwargs.items():
                self.kwargs[k] = v
            # Se elimina la referencia
            del self.kwargs['kwargs']

        # Construcción de kwargs sin valores nulos
        self.kwargs = {
            key: value
            for ( key, value ) in self.kwargs.items()
            if value is not None
        }
