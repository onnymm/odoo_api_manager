import pandas as pd
from xmlrpc import client
from typing import Any
from ._typing import (
    API_METHODS,
    ACCESS_RIGHTS,
    odoo_names,
    OutputOptions,
    CriteriaStructure,
)
from ._env import _Env

class OdooAPIManager():
    """
    # Conexión al API de Odoo
    Creador de una conexión con el sistema de Odoo a través del API. Puede ser
    a la base de datos principal o a una base de datos de prueba provista en el
    archivo `.env`

    Forma de uso:
    >>> odoo = OdooAPIManager()

    Para crear una conexión a una base de datos de prueba o una base de datos
    alternativa, se debe proveer el valor `True` (En caso de haberse declarado
    una base de datos alternativa en el archivo `env.`) o el nombre de la base
    de datos alternativa en el argumento `alt_db`:
    >>> odoo_test = OdooAPIManager(test_db=True)

    Para proporcionar los datos de la conexión al API se debe contar con un
    archivo `.env` en la raíz del proyecto con la siguiente estructura:

    ```env
    ODOO_API_USERNAME = username_api@example.com
    ODOO_API_TOKEN = 1234567890abcdefghijklmnopqrstuvwxyz1234
    ODOO_API_PASSWORD = thisisapassword321
    ODOO_API_URL = https://your-database-name.odoo.com
    ODOO_API_DB = your-database-name
    ODOO_API_TEST_DB = your-database-name-test
    ```
    ----
    # Métodos disponibles
    ## Permisos de acceso
    Método para verificar los permisos de acceso a un modelo especificado.

    Ejemplo de uso:
    >>> odoo.check_access_rights('res.partner', 'write')

    Permisos disponibles
    - `create`: Permiso de creación
    - `read`: Permiso de lectura
    - `write`: Permiso de lectura
    - `unlink`: Permiso de eliminación

    ----
    ## Creación de registro
    Este método permite crear un registro en un modelo de Odoo y retorna la
    ID de su registro.

    Ejemplo de uso:
    >>> partner_id = odoo.create('res.partner', {'name': 'Nombre de un cliente'})
    >>> # 32

    ### Estructura de los datos
    Las llaves deben ser el nombre exacto del campo en el modelo de Odoo,
    en donde se desea realizar el registro. Por ejemplo, el modelo
    `res.partner` contiene un campo llamado `name` que es el nombre del
    cliente.
    >>> {'name': 'Nombre de un cliente'}

    ----
    ## Búsqueda de registros
    Este método realiza una búsqueda en un modelo especificado y retorna
    una lista de IDs que cumplen con las condiciones especificadas.

    Ejemplo de uso:
    >>> odoo.search("sale.order", [("state", "=", "cancel")])
    >>> # [52, 87, 129, 132]

    ### Condición de búsqueda
    Se provee al menos una tupla con la siguiente escructura:
    >>> ("nombre_del_campo", "=", "valor")

    Todo esto se encierra dentro de una lista:
    >>> [("nombre_del_campo", "=", "valor")]

    Los operadores de comparación pueden ser alguno de los siguientes:
    - `=`: Igual a
    - `!=`: Diferente de
    - `in`: Está en
    - `not in`: No está en
    - `ilike`: Contiene
    - `not ilike`: No contiene
    - `>`: Es mayor a
    - `<`: Es menor a
    - `>=`: Es mayor o igual a
    - `<=`: Es menor o igual a

    Los valores pueden ser de tipo `str`, `int`, `float` o `bool`
    dependiendo del tipo de valor del campo.

    ----
    ## Lectura de registros
    Este método realiza una lectura de IDs en donde retorna una lista
    de diccionarios, cada uno, con la información de un registro.

    Ejemplo de uso:
    >>> odoo.read("sale.order", [52, 87, 129, 132])
    >>> #     id    name ...
    >>> # 0   52  S00052 ...
    >>> # 1   89  S00089 ...
    >>> # 2  129  S00129 ...
    >>> # 3  132  S00132 ...
    >>> 
    >>> odoo.read("sale.order", [52, 87, 129, 132], output='dict')
    >>> # [{
    >>> #     'id': 52,
    >>> #     'name': 'S00052',
    >>> #     ...
    >>> #  },
    >>> #  {
    >>> #     'id': 89,
    >>> #     'name': 'S00089',
    >>> #     ...
    >>> #  },
    >>> #  {
    >>> #     'id': 129,
    >>> #     'name': 'S00129',
    >>> #     ...
    >>> #  },
    >>> #  {
    >>> #     'id': 132,
    >>> #     'name': 'S00132',
    >>> #     ...
    >>> # }]

    ----
    ## Búsqueda y lectura de registros
    Este método es la combinación de los métodos internos
    `OdooAPIManager.search` y `OdooAPIManager.read` optimizado para la
    ejecución de ambos en una misma solicitud al API.

    Ejemplo de uso:
    >>> odoo.read("sale.order", [52, 87, 129, 132])
    >>> #     id    name ...
    >>> # 0   52  S00052 ...
    >>> # 1   89  S00089 ...
    >>> # 2  129  S00129 ...
    >>> # 3  132  S00132 ...
    >>> 
    >>> odoo.read("sale.order", [52, 87, 129, 132], output='dict')
    >>> # [{
    >>> #     'id': 52,
    >>> #     'name': 'S00052',
    >>> #     ...
    >>> #  },
    >>> #  {
    >>> #     'id': 89,
    >>> #     'name': 'S00089',
    >>> #     ...
    >>> #  },
    >>> #  {
    >>> #     'id': 129,
    >>> #     'name': 'S00129',
    >>> #     ...
    >>> #  },
    >>> #  {
    >>> #     'id': 132,
    >>> #     'name': 'S00132',
    >>> #     ...
    >>> # }]

    ----
    ## Conteo de una búsqueda
    Este método retorna el conteo de la cantidad de registros que cumplen
    un criterio de búsqueda provisto. Es equivalente a usar la función
    `len()` a la lista de retorno del método `OdooAPIManager.search()`:
    >>> len(odoo.search("sale.order", [("state", "=", "cancel")]))

    Ejemplo de uso:
    >>> odoo.search_count("sale.order", [("state", "=", "cancel")])
    >>> # 87

    ### Condición de búsqueda
    Se provee al menos una tupla con la siguiente escructura:
    >>> ("nombre_del_campo", "=", "valor")

    Todo esto se encierra dentro de una lista:
    >>> [("nombre_del_campo", "=", "valor")]

    ----
    ## Actualización de registros
    Este método permite actualizar uno o varios registros en el modelo
    especificado de Odoo.

    Ejemplo de uso:
    >>> odoo.write("sale.order", 52, {"state": "cancel"})
    >>> # True
    >>> 
    >>> odoo.write("res.partner", 45, {"name": "Nuevo Nombre", "phone": "123456789"})
    >>> # True

    Múltiples registros pueden ser actualizados simultáneamente pero todos
    éstos obtendrán el mismo valor para todos los campos declarados.
    >>> odoo.write("sale.order", [52, 87, 129], {"state": "done"})
    >>> # True

    ----
    ## Eliminación de registros
    Este método permite eliminar uno o varios registros en el modelo
    especificado de Odoo. Es importante mencionar que ciertos registros en
    ciertos modelos no pueden ser eliminados directamente debido a su uso
    en otros modelos o por contener ciertos vínculos como un documento
    fiscal, etc..

    Ejemplo de uso:
    >>> odoo.unlink("sale.order", 52)
    >>> # True

    >>> odoo.unlink("sale.order", [52, 87, 129])
    >>> # True

    ----
    ## Obtener información de los campos de un modelo
    Este método retorna la información más relevante de los campos, en 
    formato, de un modelo especificado en la función. Todos los modelos
    están disponibles para su consulta.

    uso:
    >>> odoo.data.model_fields("sale.order")
    >>> #         id                       name ...     ttype        relation
    >>> # 0     9931               access_token ...      char           False
    >>> # 1     9930                 access_url ...      char           False
    >>> # 2     9932             access_warning ...      text           False
    >>> # ...    ...                        ... ...       ...             ...
    >>> #         id                       name ...     ttype        relation
    >>> # 127   9993                 write_date ...  datetime           False
    >>> # 128   9992                  write_uid ...  many2one       res.users

    ## Atributos de los campos
    Las columnas de atributos mostradas por defecto son las siguientes:
    - `name`: Nombre del campo
    - `field_description`: Descripción del campo
    - `model_id`: ID del campo
    - `ttype`: Tipo del campo
    - `state`: Estado del campo (`base` para campos nativos y `manual` para campos personalizados)
    - `relation`: Modelo de relación

    ----
    ## Información de la sesión
    Este método retorna una impresión de la información de la sesión actual:
    >>> odoo.session_info()
    >>> # base de datos: your-database-name
    >>> # url de origen: https://your-database-name.odoo.com
    >>> # usuario: username_api@example.com
    >>> # token: ****************************************
    """

    fields_atts = [
        'name',
        'field_description',
        'model_id',
        'ttype',
        'state',
        'relation'
    ]

    def __init__(self,
        alt_db: bool | str | None = None,
        default_output: OutputOptions = 'dataframe',
    ) -> None:

        # Obtención de las variables de entorno
        self._env = _Env(alt_db)
        # Creación de la conexión common para autenticar el usuario
        self._common = client.ServerProxy(f"{self._env.url}/xmlrpc/2/common")
        # Token de autenticación
        self._uid = (
            self._common
            .authenticate(
                self._env.api_db,
                self._env.username,
                self._env.token,
                {}
            )
        )
        # Creación de la conexión models para realizar solicitudes
        self._models = client.ServerProxy(f"{self._env.url}/xmlrpc/2/object")

        # Se configura el formato de salida de la información
        self._default_output = default_output

        # Información
        self._info = [
            f"base de datos: {self._env.api_db}",
            f"url de origen: {self._env.url}",
            f"usuario: {self._env.username}",
            f"token: {len(self._env.token) * '*'}",
        ]

    @property
    def version(self) -> dict:
        """
        Versión del sistema Odoo con el que se tiene conexión.
        """
        return self._common.version()

    def check_access_rights(
        self,
        model: odoo_names.MODELS,
        right_type: ACCESS_RIGHTS,
        raise_exception: bool= False
    ) -> bool:
        """
        ## Permisos de acceso
        Método para verificar los permisos de acceso a un modelo especificado.

        Ejemplo de uso:
        >>> odoo.check_access_rights('res.partner', 'write')

        Permisos disponibles
        - `create`: Permiso de creación
        - `read`: Permiso de lectura
        - `write`: Permiso de lectura
        - `unlink`: Permiso de eliminación
        """

        # Ejecución del método de solicitud al API
        return self._request(
            model= model,
            method= 'check_access_rights',
            data= [right_type],
            params= {'raise_exception': raise_exception}
        )

    def create(
        self,
        model: odoo_names.MODELS,
        data: dict[str, Any],
    ) -> int:
        """
        ## Creación de registro
        Este método permite crear un registro en un modelo de Odoo y retorna la
        ID de su registro.

        Ejemplo de uso:
        >>> partner_id = odoo.create('res.partner', {'name': 'Nombre de un cliente'})
        >>> # 32

        ### Estructura de los datos
        Las llaves deben ser el nombre exacto del campo en el modelo de Odoo,
        en donde se desea realizar el registro. Por ejemplo, el modelo
        `res.partner` contiene un campo llamado `name` que es el nombre del
        cliente.
        >>> {'name': 'Nombre de un cliente'}

        Para conocer los nombres de los campos de un modelo en específico se
        puede realizar una consulta a Odoo desde el método
        `OdooAPIManager.model_fields`.
        """

        # Ejecución del método de solicitud al API
        return self._request(
            model= model,
            method= 'create',
            data= [data],
        )

    def search(
        self,
        model: odoo_names.MODELS,
        search_criteria: CriteriaStructure = [],
        offset: int | None = None,
        limit: int | None = None
    ) -> list[int]:
        """
        ## Búsqueda de registros
        Este método realiza una búsqueda en un modelo especificado y retorna
        una lista de IDs que cumplen con las condiciones especificadas.

        Ejemplo de uso:
        >>> odoo.search("sale.order", [("state", "=", "cancel")])
        >>> # [52, 87, 129, 132]

        ### Condición de búsqueda
        Se provee al menos una tupla con la siguiente escructura:
        >>> ("nombre_del_campo", "=", "valor")

        Todo esto se encierra dentro de una lista:
        >>> [("nombre_del_campo", "=", "valor")]

        Los operadores de comparación pueden ser alguno de los siguientes:
        - `=`: Igual a
        - `!=`: Diferente de
        - `in`: Está en
        - `not in`: No está en
        - `ilike`: Contiene
        - `not ilike`: No contiene
        - `>`: Es mayor a
        - `<`: Es menor a
        - `>=`: Es mayor o igual a
        - `<=`: Es menor o igual a

        Los valores pueden ser de tipo `str`, `int`, `float` o `bool`
        dependiendo del tipo de valor del campo.

        También pueden ser de tipo `list` que contenga alguno de los tipos
        anteriores.

        En relaciones tipo `many2one`, `one2many` y `many2many` la búsqueda se
        hace por ID o por lista de IDs.

        ### Búsqueda con varias condiciones provistas
        También se puede incluir más de una condición. Para esto, se agrega un
        operador lógico antes de dos tuplas de condiciones:
        >>> ['&', (condicion_1...), (condicion_2...)]

        Los operadores lógicos disponibles son:
        - `&`: and
        - `|`: or

        ### Desfase de registros para paginación
        Este parámetro sirve para realizar un slice de la lista de IDs
        retornada por el API pero directamente desde el API. Suponiendo que una
        búsqueda normal arrojarría los siguientes resultados:
        >>> odoo.search("sale.order", [("state", "=", "sale")])
        >>> # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14...]

        Se puede especificar que sólo se requiere el retorno de la lista de IDs
        a partir de un índice especificado, por ejemplo:
        >>> odoo.search("sale.order", [("state", "=", "sale")], offset=5)
        >>> # [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19...]

        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima en la cantidad de IDs
        retornada por el API, también directamente desde el API. Suponiendo que
        una búsqueda normal arrojarría los siguientes resultados:
        >>> odoo.search("sale.order", [("state", "=", "sale")])
        >>> # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14...]

        Se puede especificar que sólo se requiere obtener una cantidad máxima
        de registros a partir de un número provisto:
        >>> odoo.search("sale.order", [("state", "=", "sale")], limit=5)
        >>> # [1, 2, 3, 4, 5]

        ----
        ### Sugerencia de uso en múltiples condiciones
        Para mejorar y facilitar una búsqueda con múltiples condiciones
        se recomienda asignar la lista a una variable y utilizar la siguiente
        estructura de identación dentro de la lista:
        >>> # Ejemplo 1
        >>> criteria = [
        >>>     '&',
        >>>         (condicion_1...),
        >>>         (condicion_2...)
        >>> ]
        >>> 
        >>> # Ejemplo 2
        >>> criteria = [
        >>>     '|',
        >>>         '&',
        >>>             (condicion_1...),
        >>>             (condicion_2...),
        >>>         (condicion_3...)
        >>> ]

        En el primer ejemplo, la condición 1 y la condición 2 deben
        cumplirse para que un registro se incluya en la lista de resultados.

        En el segundo ejemplo, el resultado `True` de la condición 1 y la
        condición 2, todo esto o la condición 3 deben cumplirse para que un registro se
        incluya en la lista de resultados, es decir, algo como esto:
        >>> ((condicion_1 and condicion_2) or condicion_3)

        La ejecución del método entonces se vería así:
        >>> odoo.search("sale.order", criteria)
        """

        # Ejecución del método de solicitud al API
        return self._request(
            model= model,
            method= 'search',
            data= [search_criteria],
            params= self._build_params(
                offset= offset,
                limit= limit
            )
        )

    def read(
        self,
        model: odoo_names.MODELS,
        record_ids: int | list[int],
        fields: list[str] | None = None,
        output: OutputOptions | None = None,
    ) -> list[dict] | pd.DataFrame:
        """
        ## Lectura de registros
        Este método realiza una lectura de IDs en donde retorna una lista
        de diccionarios, cada uno, con la información de un registro.

        Ejemplo de uso:
        >>> odoo.read("sale.order", [52, 87, 129, 132])
        >>> #     id    name ...
        >>> # 0   52  S00052 ...
        >>> # 1   89  S00089 ...
        >>> # 2  129  S00129 ...
        >>> # 3  132  S00132 ...
        >>> 
        >>> odoo.read("sale.order", [52, 87, 129, 132], output='dict')
        >>> # [{
        >>> #     'id': 52,
        >>> #     'name': 'S00052',
        >>> #     ...
        >>> #  },
        >>> #  {
        >>> #     'id': 89,
        >>> #     'name': 'S00089',
        >>> #     ...
        >>> #  },
        >>> #  {
        >>> #     'id': 129,
        >>> #     'name': 'S00129',
        >>> #     ...
        >>> #  },
        >>> #  {
        >>> #     'id': 132,
        >>> #     'name': 'S00132',
        >>> #     ...
        >>> # }]

        ### Espeficicación de campos a retornar por el API
        También se puede especificar una lista de campos para reducir
        el tamaño de los diccionarios en la lista para mayor rapidez en el
        tiempo de respuesta de la API:
        >>> odoo.read("sale.order", [52, 87, 129, 132], ['name', 'state'])

        ----
        ### Sugerencia de uso en listas de campos muy grandes
        Para estos casos, se recomienda almacenar la lista de campos en una
        variable con alguna de las siguientes dos estructuras:

        Ejemplo:
        >>> fields = [
        >>>     'name',
        >>>     'state',
        >>>     'salesman_id',
        >>>     'partner_id',
        >>> ]

        La ejecución del método entonces se vería así:
        >>> odoo.read("sale.order", [52, 87, 129, 132], fields)
        """

        # Conversión a lista de enteros si la entrada es una ID en entero
        if isinstance(record_ids, int):
            record_ids = [record_ids]

        # Obtención de los datos a partir del método de solicitud al API
        response = self._request(
            model= model,
            method= 'read',
            data= [record_ids],
            params= self._build_params(
                fields= fields,
            )
        )

        # Retorno en formato de salida configurado
        return self._build_output(response, output)

    def get_value(
        self,
        model: odoo_names.MODELS,
        record_id: int,
        field: str,
    ) -> Any:
        """
        ## Obtención del valor de un registro
        Este método obtiene el valor de un campo de un registro especificado.

        Uso:
        >>> odoo.get_value('product.template', 53, 'list_price')
        >>> # 7.40
        """

        # Obtención del registro
        response = self.read(
            model,
            [record_id],
            [field],
            output= 'dict'
        )

        # Si no existe el registro se retorna un None para evitar errores
        if not response:
            return None

        else:
            # Se destructura el registro de la lista
            [ record ] = response

        # Se retorna el valor del registro
        return record[field]

    def get_values(
        self,
        model: odoo_names.MODELS,
        record_ids: list[int],
        fields: list[str]
    ) -> tuple[Any]:
        """
        ## Obtención de valores de un registro
        Este método obtiene los valores de los campos especificados de un
        registro especificado.

        Uso:
        >>> odoo.get_values('product.template', 53, ['name', 'list_price'])
        >>> # ('Café', 7.40)
        
        Los valores también pueden ser destructurados para ser guardados
        directamente en variables:
        >>> name, price = odoo.get_values('product.template', 53, ['name', 'list_price'])
        >>> name
        >>> # 'Café'
        >>> price
        >>> # 7.40
        """

        # Obtención del registro
        response = self.read(
            model,
            record_ids,
            fields,
            output= 'dict'
        )

        # Si no existe el registro se retorna un None para evitar errores
        if not response:
            return None

        else:
            # Se destructura el registro de la lista
            [ record ] = response

        return tuple([record[field] for field in fields])

    def search_read(
        self,
        model: odoo_names.MODELS,
        data: CriteriaStructure = [],
        fields: list[str] = None,
        offset: int = None,
        limit: int = None,
        output: OutputOptions | None = None,
    ):
        """
        ## Búsqueda y lectura de registros
        Este método es la combinación de los métodos internos
        `OdooAPIManager.search` y `OdooAPIManager.read` optimizado para la
        ejecución de ambos en una misma solicitud al API.

        Ejemplo de uso:
        >>> odoo.read("sale.order", [52, 87, 129, 132])
        >>> #     id    name ...
        >>> # 0   52  S00052 ...
        >>> # 1   89  S00089 ...
        >>> # 2  129  S00129 ...
        >>> # 3  132  S00132 ...
        >>> 
        >>> odoo.read("sale.order", [52, 87, 129, 132], output='dict')
        >>> # [{
        >>> #     'id': 52,
        >>> #     'name': 'S00052',
        >>> #     ...
        >>> #  },
        >>> #  {
        >>> #     'id': 89,
        >>> #     'name': 'S00089',
        >>> #     ...
        >>> #  },
        >>> #  {
        >>> #     'id': 129,
        >>> #     'name': 'S00129',
        >>> #     ...
        >>> #  },
        >>> #  {
        >>> #     'id': 132,
        >>> #     'name': 'S00132',
        >>> #     ...
        >>> # }]

        ### Condición de búsqueda
        Se provee al menos una tupla con la siguiente escructura:
        >>> ("nombre_del_campo", "=", "valor")

        Todo esto se encierra dentro de una lista:
        >>> [("nombre_del_campo", "=", "valor")]

        Los operadores de comparación pueden ser alguno de los siguientes:
        - `=`: Igual a
        - `!=`: Diferente de
        - `in`: Está en
        - `not in`: No está en
        - `ilike`: Contiene
        - `not ilike`: No contiene
        - `>`: Es mayor a
        - `<`: Es menor a
        - `>=`: Es mayor o igual a
        - `<=`: Es menor o igual a

        Los valores pueden ser de tipo `str`, `int`, `float` o `bool`
        dependiendo del tipo de valor del campo.

        También pueden ser de tipo `list` que contenga alguno de los tipos
        anteriores.

        En relaciones tipo `many2one`, `one2many` y `many2many` la búsqueda se
        hace por ID o por lista de IDs.

        ### Búsqueda con varias condiciones provistas
        También se puede incluir más de una condición. Para esto, se agrega un
        operador lógico antes de dos tuplas de condiciones:
        >>> ['&', (condicion_1...), (condicion_2...)]

        Los operadores lógicos disponibles son:
        - `&`: and
        - `|`: or

        ### Espeficicación de campos a retornar por el API
        También se puede especificar una lista de campos para reducir
        el tamaño de los diccionarios en la lista para mayor rapidez en el
        tiempo de respuesta de la API:
        >>> odoo.search_read("sale.order", [52, 87, 129, 132], ['name', 'state'])

        ### Desfase de registros para paginación
        Este parámetro sirve para realizar un slice de la lista de IDs
        retornada por el API pero directamente desde el API. Suponiendo que una
        búsqueda normal arrojarría los siguientes resultados:
        >>> odoo.search_read("sale.order", [("state", "=", "sale")])
        >>> # [{'id': 1, ...}, {'id': 2, ...}, {'id': 3, ...}, {'id': 4, ...}, ...]

        Se puede especificar que sólo se requiere el retorno de la lista de IDs
        a partir de un índice especificado, por ejemplo:
        >>> odoo.search_read("sale.order", [("state", "=", "sale")], offset=3)
        >>> # [{'id': 4, ...}, {'id': 5, ...}, {'id': 6, ...}, {'id': 7, ...}, ...]

        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima en la cantidad de IDs
        retornada por el API, también directamente desde el API. Suponiendo que
        una búsqueda normal arrojarría los siguientes resultados:
        >>> odoo.search_read("sale.order", [("state", "=", "sale")])
        >>> # [{'id': 1, ...}, {'id': 2, ...}, {'id': 3, ...}, {'id': 4, ...}, ...]

        Se puede especificar que sólo se requiere obtener una cantidad máxima
        de registros a partir de un número provisto:
        >>> odoo.search_read("sale.order", [("state", "=", "sale")], limit=3)
        >>> # [{'id': 1, ...}, {'id': 2, ...}, {'id': 3, ...}]

        ----
        ### Sugerencia de uso en múltiples condiciones
        Para mejorar y facilitar una búsqueda con múltiples condiciones
        se recomienda asignar la lista a una variable y utilizar la siguiente
        estructura de identación dentro de la lista:
        >>> # Ejemplo 1
        >>> criteria = [
        >>>     '&',
        >>>         (condicion_1...),
        >>>         (condicion_2...)
        >>> ]
        >>> 
        >>> # Ejemplo 2
        >>> criteria = [
        >>>     '|',
        >>>         '&',
        >>>             (condicion_1...),
        >>>             (condicion_2...),
        >>>         (condicion_3...)
        >>> ]

        En el primer ejemplo, la condición 1 y la condición 2 deben
        cumplirse para que un registro se incluya en la lista de resultados.

        En el segundo ejemplo, el resultado `True` de la condición 1 y la
        condición 2, todo esto o la condición 3 deben cumplirse para que un registro se
        incluya en la lista de resultados, es decir, algo como esto:
        >>> ((condicion_1 and condicion_2) or condicion_3)

        La ejecución del método entonces se vería así:
        >>> odoo.search_read("sale.order", criteria)

        ### Sugerencia de uso en listas de campos muy grandes
        Para estos casos, se recomienda almacenar la lista de campos en una
        variable con alguna de las siguientes dos estructuras:

        Ejemplo:
        >>> fields = [
        >>>     'name',
        >>>     'state',
        >>>     'salesman_id',
        >>>     'partner_id',
        >>> ]

        La ejecución del método entonces se vería así:
        >>> odoo.search_read("sale.order", [(...)], fields)
        """

        # Obtención de los datos a partir del método de solicitud al API
        response = self._request(
            model= model,
            method= 'search_read',
            data= [data],
            params= self._build_params(
                fields= fields,
                offset= offset,
                limit= limit
            )
        )

        # Retorno en formato de salida configurado
        return self._build_output(response, output)

    def search_count(
        self,
        model: odoo_names.MODELS,
        data: CriteriaStructure
    ) -> int:
        """
        ## Conteo de una búsqueda
        Este método retorna el conteo de la cantidad de registros que cumplen
        un criterio de búsqueda provisto. Es equivalente a usar la función
        `len()` a la lista de retorno del método `OdooAPIManager.search()`:
        >>> len(odoo.search("sale.order", [("state", "=", "cancel")]))

        Ejemplo de uso:
        >>> odoo.search_count("sale.order", [("state", "=", "cancel")])
        >>> # 87

        ### Condición de búsqueda
        Se provee al menos una tupla con la siguiente escructura:
        >>> ("nombre_del_campo", "=", "valor")

        Todo esto se encierra dentro de una lista:
        >>> [("nombre_del_campo", "=", "valor")]

        Los operadores de comparación pueden ser alguno de los siguientes:
        - `=`: Igual a
        - `!=`: Diferente de
        - `in`: Está en
        - `not in`: No está en
        - `ilike`: Contiene
        - `not ilike`: No contiene
        - `>`: Es mayor a
        - `<`: Es menor a
        - `>=`: Es mayor o igual a
        - `<=`: Es menor o igual a

        Los valores pueden ser de tipo `str`, `int`, `float` o `bool`
        dependiendo del tipo de valor del campo.

        También pueden ser de tipo `list` que contenga alguno de los tipos
        anteriores.

        En relaciones tipo `many2one`, `one2many` y `many2many` la búsqueda se
        hace por ID o por lista de IDs.

        ### Búsqueda con varias condiciones provistas
        También se puede incluir más de una condición. Para esto, se agrega un
        operador lógico antes de dos tuplas de condiciones:
        >>> ['&', (condicion_1...), (condicion_2...)]

        Los operadores lógicos disponibles son:
        - `&`: and
        - `|`: or

        ----
        ### Sugerencia de uso en múltiples condiciones
        Para mejorar y facilitar una búsqueda con múltiples condiciones
        se recomienda asignar la lista a una variable y utilizar la siguiente
        estructura de identación dentro de la lista:
        >>> # Ejemplo 1
        >>> criteria = [
        >>>     '&',
        >>>         (condicion_1...),
        >>>         (condicion_2...)
        >>> ]
        >>> 
        >>> # Ejemplo 2
        >>> criteria = [
        >>>     '|',
        >>>         '&',
        >>>             (condicion_1...),
        >>>             (condicion_2...),
        >>>         (condicion_3...)
        >>> ]

        En el primer ejemplo, la condición 1 y la condición 2 deben
        cumplirse para que un registro se incluya en la lista de resultados.

        En el segundo ejemplo, el resultado `True` de la condición 1 y la
        condición 2, todo esto o la condición 3 deben cumplirse para que un registro se
        incluya en la lista de resultados, es decir, algo como esto:
        >>> ((condicion_1 and condicion_2) or condicion_3)

        La ejecución del método entonces se vería así:
        >>> odoo.search_read("sale.order", criteria)
        """

        # Ejecución del método de solicitud al API
        return self._request(
            model= model,
            method= 'search_count',
            data= [data],
        )

    def write(
        self,
        model: odoo_names.MODELS,
        record_ids: int | list[int],
        data: dict[str, Any]
    ) -> bool:
        """
        ## Actualización de registros
        Este método permite actualizar uno o varios registros en el modelo
        especificado de Odoo.

        Ejemplo de uso:
        >>> odoo.write("sale.order", 52, {"state": "cancel"})
        >>> # True
        >>> 
        >>> odoo.write("res.partner", 45, {"name": "Nuevo Nombre", "phone": "123456789"})
        >>> # True

        Múltiples registros pueden ser actualizados simultáneamente pero todos
        éstos obtendrán el mismo valor para todos los campos declarados.
        >>> odoo.write("sale.order", [52, 87, 129], {"state": "done"})
        >>> # True
        """

        # Conversión a lista de enteros si la entrada es una ID en entero
        if isinstance(record_ids, int):
            record_ids = [record_ids]

        # Ejecución del método de solicitud al API
        return self._request(
            model= model,
            method= 'write',
            data= [record_ids, data]
        )

    def unlink(
        self,
        model: odoo_names.MODELS,
        record_ids: int | list[int],
    ) -> bool:
        """
        ## Eliminación de registros
        Este método permite eliminar uno o varios registros en el modelo
        especificado de Odoo. Es importante mencionar que ciertos registros en
        ciertos modelos no pueden ser eliminados directamente debido a su uso
        en otros modelos o por contener ciertos vínculos como un documento
        fiscal, etc..

        Ejemplo de uso:
        >>> odoo.unlink("sale.order", 52)
        >>> # True

        >>> odoo.unlink("sale.order", [52, 87, 129])
        >>> # True
        """

        # Conversión a lista de enteros si la entrada es una ID en entero
        if isinstance(record_ids, int):
            record_ids = [record_ids]

        # Ejecución del método de solicitud al API
        return self._request(
            model= model,
            method= 'unlink',
            data= [record_ids]
        )

    def model_fields(
        self,
        model: odoo_names.MODELS,
        attributes: list[str] = fields_atts,
        fields: list[str] | None = None,
        output: OutputOptions | None = None,
    ) -> pd.DataFrame | list[dict]:
        """
        ## Obtener información de los campos de un modelo
        Este método retorna la información más relevante de los campos, en 
        formato, de un modelo especificado en la función. Todos los modelos
        están disponibles para su consulta.

        uso:
        >>> odoo.data.model_fields("sale.order")
        >>> #         id                       name ...     ttype        relation
        >>> # 0     9931               access_token ...      char           False
        >>> # 1     9930                 access_url ...      char           False
        >>> # 2     9932             access_warning ...      text           False
        >>> # ...    ...                        ... ...       ...             ...
        >>> #         id                       name ...     ttype        relation
        >>> # 127   9993                 write_date ...  datetime           False
        >>> # 128   9992                  write_uid ...  many2one       res.users

        ## Atributos de los campos
        Las columnas de atributos mostradas por defecto son las siguientes:
        - `name`: Nombre del campo
        - `field_description`: Descripción del campo
        - `model_id`: ID del campo
        - `ttype`: Tipo del campo
        - `state`: Estado del campo (`base` para campos nativos y `manual` para campos personalizados)
        - `relation`: Modelo de relación

        Sin embargo se pueden obtener datos de otros atributos,
        específicándolos en el parámetro `atts` como una lista:
        >>> specific_atts = ["name", "field_description", "ttype"]
        >>> odoo.data.model_fields("sale.order", atts=specific_atts)
        >>> #                     name  field_description     ttype
        >>> # 0           access_token     Security Token      char
        >>> # 1             access_url  Portal Access URL      char
        >>> # 2         access_warning     Access warning      text
        >>> # ...                  ...                ...       ...
        >>> # 126  website_message_ids   Website Messages  one2many
        >>> # 127           write_date    Last Updated on  datetime
        >>> # 128            write_uid    Last Updated by  many2one

        ## Especificación de campos
        Por defecto, el método `model_fields` retorna la lista completa de
        todos los campos del modelo. Sin embargo, si sólo se requieren ciertos
        campos, puede ser especificado en el parámetro `fields` en una lista:
        >>> specific_fields = ["id", "name", "state"]
        >>> odoo.data.model_fields("sale.order", fields=specific_fields)
        >>> #      id   name ...      ttype  relation
        >>> # 0  9989     id ...    integer     False
        >>> # 1  9933   name ...       char     False
        >>> # 2  9936  state ...  selection     False
        """

        # Criterio inicial de búsqueda
        search_criteria: CriteriaStructure = [('model_id', '=', model)]

        # Si se especificaron los campos, se rearma el criterio de búsqueda
        if (fields):
            # Se interta el operador 'and' al principio de la lista
            search_criteria.insert(0, '&')
            # Se añade la tupla de coincidencia por nombre
            search_criteria.append(('name', 'in', fields))

        # Obtención de los datos a partir del método de solicitud al API
        response = self.search_read(
            model= 'ir.model.fields',
            data= search_criteria,
            fields= attributes
        )

        # Retorno en formato de salida configurado
        return self._build_output(response, output)

    def session_info(self) -> None:
        """
        ## Información de la sesión
        Este método retorna una impresión de la información de la sesión actual:
        >>> odoo.session_info()
        >>> # base de datos: your-database-name
        >>> # url de origen: https://your-database-name.odoo.com
        >>> # usuario: username_api@example.com
        >>> # token: ****************************************
        """
        for i in self._info:
            print(i)

    def _build_output(self, response: dict, output: OutputOptions | None) -> list[dict] | pd.DataFrame:
        """
        ## Formateo de salida
        Este método interno formatea la salida de las funciones de lectura
        desde el API de Odoo. Si se estableció un formato de salida en la
        inicialización de la instancia, éste se mantiene. De lo contrario se
        utiliza el formateo especificado en la ejecución de la función de
        lectura. En caso de no haberlo se utiliza el formato de salida por
        defecto que es Pandas DataFrame.
        """

        # Si no se especificó formato de salida en la función...
        if not output:
            # Formato de salida en DataFrame
            if self._default_output == 'dataframe':
                return pd.DataFrame(response)

        # Si el formato de salida por fecto es DataFrame...
        if output == 'dataframe':
                return pd.DataFrame(response)

        # Retorno de información en lista de diccionarios
        return response

    def _build_params(self, **args) -> dict:
        """
        ## Construcción de parámetros
        Este método interno construye un diccionario de parámetros que tienen
        valores diferentes a None para ser usados en solicitudes al API.
        """

        # Inicialización del diccionario a retornar
        built_params = {}

        # Iteración por llave y valor
        for ( key, value ) in args.items():
            # Si el valor es diferente a None
            if not ( value is None ):
                # Se añade la tupla al diccionaio a retornar
                built_params.update({ key: value })

        # Retorno del diccionario de parámetros
        return built_params

    def _request(
        self,
        model: odoo_names.MODELS,
        method: API_METHODS,
        data: CriteriaStructure,
        params: dict[list, int] ={}
    ):

        # Se realiza la solicitud al API
        return self._models.execute_kw(
            # Base de datos de la API
            self._env.api_db,
            # UUID de la cuenta
            self._uid,
            # Token de la cuenta
            self._env.token,
            # Modelo de Odoo
            model,
            # Método de solicitud
            method,
            # Criterio de búsqueda
            data,
            # Diccionario de parámetros
            params
        )
