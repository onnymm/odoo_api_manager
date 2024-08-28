import xmlrpc.client
from ._options import MODELS, ACCESS_RIGHTS, API_METHODS

class APIManager():
    
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
        model: MODELS,
        right: ACCESS_RIGHTS
    ) -> bool:
        ...


    def search(
        self,
        model: MODELS,
        search_criteria: list[tuple, str],
        offset: int = ...,
        limit: int = ...
    ) -> list[int]:
        ...


    def read(
        self,
        model: MODELS,
        record_ids: list[int],
        fields: list[str] = ...
    ) -> list[dict]:
        ...


    def search_read(
        self,
        model: MODELS,
        data: list[tuple, str],
        fields: list[str] = ...,
        offset: int = ...,
        limit: int = ...
    ):
        ...
    

    def search_count(
        self,
        model: MODELS,
        data: list[tuple, str]
    ) -> int:
        ...


    def _write_single_record(
        self,
        model: MODELS,
        record_id: list[dict],
        changes_data: dict[str, int, bool]
    ):
        ...


    def _request(
        self,
        model: MODELS,
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
