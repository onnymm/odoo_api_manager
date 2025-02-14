import os

class _Env():
    _username = 'ODOO_API_USERNAME'
    _token = 'ODOO_API_TOKEN'
    _password = 'ODOO_API_PASSWORD'
    _url = 'ODOO_API_URL'
    _api_db = 'ODOO_API_DB'
    _api_test_db = 'ODOO_API_ALT_DB'

    def __init__(self, alt_api_db: bool | str | None = None) -> None:
        self.username = os.environ.get(self._username)
        self.token = os.environ.get(self._token)
        self.password = os.environ.get(self._password)
        self.url = os.environ.get(self._url)

        if isinstance(alt_api_db, bool):
            if alt_api_db:
                self.api_db = os.environ.get(self._api_test_db)
            else:
                self.api_db = os.environ.get(self._api_db)
        elif isinstance(alt_api_db, str):
            self.api_db = os.environ.get(alt_api_db)
        else:
            self.api_db = os.environ.get(self._api_db)
