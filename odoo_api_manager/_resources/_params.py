from typing import Optional
from .._typing import (
    CriteriaStructure,
    RecordData,
    RecordID,
    AccessRights,
    ListOrItem,
    ModelField,
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
    ) -> None:

        # Plantilla de args
        self.args = [record_ids, search_criteria, records_data, right_type]

        # Plantilla de kwargs
        self.kwargs = {
            'fields': fields,
            'offset': offset,
            'limit': limit,
            'raise_exception': raise_exception,
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

        # Construcción de kwargs sin valores nulos
        self.kwargs = {
            key: value
            for ( key, value ) in self.kwargs.items()
            if value is not None
        }
