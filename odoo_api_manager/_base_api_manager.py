import xmlrpc.client
from ._options import MOST_COMMON_FIELDS, MODELS, ACCESS_RIGHTS, API_METHODS
from typing import Union, Literal, Tuple

class APIManager():

    # Valores para tipado
    odoo_models = MODELS
    condition_structure = Union[
        list[
            Union[
                MOST_COMMON_FIELDS,
                Tuple[
                    MOST_COMMON_FIELDS,
                    # Operaciones disponibles
                    Literal["=", "!=", "in", "not in", "ilike", "not ilike", ">", "<", ">=", "<="],
                    Union[int, str, bool, list[int, str]]
                ]
            ]
        ]
    ]

    # Lista de módulos externos registrados
    _registered_modules = []

    def __init__(self) -> None:
        self._common: xmlrpc.client.ServerProxy
        self._models: xmlrpc.client.ServerProxy
        self._uid: xmlrpc.client._Method
        self._api_db: str
        self._api_url: str
        self._api_username: str
        self._api_token: str


    def check_access_rights(
        self,
        model: odoo_models,
        right: ACCESS_RIGHTS
    ) -> bool:
        ...


    def search(
        self,
        model: odoo_models,
        search_criteria: list[tuple, str],
        offset: int = ...,
        limit: int = ...
    ) -> list[int]:
        ...


    def read(
        self,
        model: odoo_models,
        record_ids: list[int],
        fields: list[str] = ...
    ) -> list[dict]:
        ...


    def search_read(
        self,
        model: odoo_models,
        data: list[tuple, str],
        fields: list[str] = ...,
        offset: int = ...,
        limit: int = ...
    ):
        ...
    

    def search_count(
        self,
        model: odoo_models,
        data: list[tuple, str]
    ) -> int:
        ...

    def session_info(self) -> None:
        ...


    def _write_single_record(
        self,
        model: odoo_models,
        record_id: list[dict],
        changes_data: dict[str, int, bool]
    ):
        ...


    def _request(
        self,
        model: odoo_models,
        method: API_METHODS,
        data: list[tuple, str, list, dict],
        params: dict[list, int] ={}
    ):
        ...


    def _build_data(
        self,
        data: list[tuple, str, int],
        data_args: dict = None
    ):
        ...


    def _build_params(
        self,
        fields: list[str] = None,
        offset: int = None,
        limit: int = None,
        raise_exception: bool = None
    ) -> dict[list[str], int]:
        ...
