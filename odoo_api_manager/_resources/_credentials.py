from typing import (
    Any,
    Optional,
)
from .._constants import VARIABLE_NAME
from .._core import env
from .._errors import DatabaseNotDefinedError
from .._settings import CREDENTIALS_CONFIG
from .._typing import AltDatabaseArg

class Credentials():

    def __init__(
        self,
        alt_db: Optional[AltDatabaseArg] = None,
    ) -> None:

        # Se guardan los valores
        self.username = CREDENTIALS_CONFIG.USERNAME
        self.token = CREDENTIALS_CONFIG.TOKEN
        self.url = CREDENTIALS_CONFIG.URL

        # Si el argumento de base de datos alternativa fue especificado...
        if alt_db is not None:
            # Se carga el nombre de la base de datos alternativa
            self._load_alternative_database(alt_db)
        # Si el argumento de base de datos alternativas no fue especificado...
        else:
            # Se carga el nombre de la base de datos principal
            self.db = CREDENTIALS_CONFIG.DB

    def _load_alternative_database(
        self,
        alt_db: AltDatabaseArg,
    ) -> None:

        # Si el tipo de dato del argumento es booleano
        if isinstance(alt_db, bool):
            # Si es True...
            if alt_db:
                # Si el valor desde el entorno es None
                if CREDENTIALS_CONFIG.ALT_DB is None:
                    # Se lanza error
                    raise DatabaseNotDefinedError('¡Define una base de datos alternativa primero!')
                # Se establece el nombre de la base de datos alternativa
                self.db = CREDENTIALS_CONFIG.ALT_DB
            # Si es False...
            else:
                # Se usa la base de datos de producción
                self.db = CREDENTIALS_CONFIG.DB
        # Si el tipo de dato es cualquier otra cosa...
        else:
            # Se carga una base de datos personalizada
            self._load_custom_database(alt_db)

    def _load_custom_database(
        self,
        suffix: Any,
    ) -> None:

        # Construcción del nombre de variable
        build_name = f'{VARIABLE_NAME.ALT_DB}_{suffix}'
        # Obtención del nombre de la base de datos
        self.db = env.variable(build_name, str, ...)
