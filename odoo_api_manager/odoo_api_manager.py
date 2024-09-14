import os
import xmlrpc.client
from ._base_api_manager import APIManager
from ._env_variables import ENV
from ._options import ACCESS_RIGHTS, API_METHODS
from ._base_extension import APIManagerExtension
from ._extensions import DataMethods, UtilsMethods, FixMethods, ModelsMethods, ExtensionsRegistry, ExtendMethods
from ._warnings import deprecated

class OdooAPIManager(APIManager):
    """
    ## Conexión al API de Odoo
    Creador de una conexión con el sistema de Odoo a través del API. Puede ser
    a la base de datos principal o a una base de datos de prueba provista en el
    archivo `.env`

    ### Forma de uso:
    ````py
    odoo = OdooAPIManager()
    ````

    Para crear una conexión a la base de datos de prueba, se debe proveer el
    valor `True` en el argumento `test_db`:
    ````py
    odoo_test = OdooAPIManager(test_db=True)
    ````

    Para proporcionar los datos de la conexión al API se debe contar con un
    archivo `.env` en la raíz del proyecto con la siguiente estructura:

    ````env
    ODOO_USERNAME_API = username_api@example.com
    ODOO_CLAVE_API = 1234567890abcdefghijklmnopqrstuvwxyz1234
    ODOO_PASSWORD_API = thisisapassword321
    ODOO_URL_API = https://your-database-name.odoo.com
    ODOO_DB_API = your-database-name
    ODOO_DB_PRUEBA_API = your-database-name-test
    ````

    ----
    ## Métodos disponibles
    ### • Revisión de permisos de acceso
    Método para verificar los permisos de acceso a un modelo
    especificado:
    ````py
    odoo.check_access_rights("res.partner", "write")
    ````

    ### • Búsqueda de registros
    Este método realiza una búsqueda en un modelo especificado y retorna
    una lista de IDs que cumplen con las condiciones especificadas.
    ````py
    odoo.search("sale.order", [("state", "=", "cancel")])
    # [52, 87, 129, 132]
    ````

    ### • Lectura de registros
    Este método realiza una lectura de IDs en donde retorna una lista
    de diccionarios, cada uno, con la información de un registro.
    ````py
    odoo.read("sale.order", [52, 87, 129, 132])
    # [{
    #     'id': 52,
    #     'name': 'S00052',
    #     ...
    #  },
    #  {
    #     'id': 89,
    #     'name': 'S00089',
    #     ...
    #  },
    #  {
    #     'id': 129,
    #     'name': 'S00129',
    #     ...
    #  },
    #  {
    #     'id': 132,
    #     'name': 'S00132',
    #     ...
    # }]
    ````

    ### • Búsqueda y lectura de registros
    Este método es la combinación de los métodos internos
    `OdooAPIManager.search` y `OdooAPIManager.read` optimizado para la
    ejecución de ambos en una misma solicitud al API.
    ````py
    odoo.search_read("sale.order", [("state", "=", "cancel")])
    # [{
    #     'id': 52,
    #     'name': 'S00052',
    #     ...
    #  },
    #  {
    #     'id': 89,
    #     'name': 'S00089',
    #     ...
    #  },
    #  {
    #     'id': 129,
    #     'name': 'S00129',
    #     ...
    #  },
    #  {
    #     'id': 132,
    #     'name': 'S00132',
    #     ...
    # }]
    ````

    ### • Conteo de registros en búsqueda
    Este método devuelve el conteo de la cantidad de registros que cumplen
    un criterio de búsqueda provisto. Es equivalente a usar la función
    `len()` a la lista de retorno del método `OdooAPIManager.search()`:
    ````py
    odoo.search_count("sale.order", [("state", "=", "cancel")])
    # 87
    ````
    """

    extensions = ExtensionsRegistry()

    # ----- INICIALIZACIÓN -----
    def __init__(self,
        test_db: bool = False
    ) -> None:
        
        db = {
            True: ENV["test_db"],
            False: ENV["api_db"],
        }
        
        # Obtención de la base de datos real o de prueba
        self._api_db = os.environ.get(db[test_db])

        # Obtención de las variables de entorno requeridas conexión al API de Odoo
        self._api_url = os.environ.get(ENV["url"])
        self._api_username = os.environ.get(ENV["username"])
        self._api_token = os.environ.get(ENV["token"])

        # Inicialización de la conexión
        self._common = xmlrpc.client.ServerProxy(f"{self._api_url}/xmlrpc/2/common")
        self._uid = self._common.authenticate(self._api_db, self._api_username, self._api_token, {})
        self._models = xmlrpc.client.ServerProxy(f"{self._api_url}/xmlrpc/2/object")

        # Módulos de extensión
        self.data = DataMethods(self)
        self.fix = FixMethods(self)
        self.models = ModelsMethods(self)
        self.utils = UtilsMethods(self)

        # Inicialización de módulos externos
        self._external_modules = ExtendMethods(self)
        self._external_modules._initialize_modules()

        # Información
        self._info = [
            f"base de datos: {self._api_db}",
            f"url de origen: {self._api_url}",
            f"usuario: {self._api_username}",
            f"token: {len(self._api_token) * "*"}",
        ]

    # ----- REVISIÓN DE DERECHOS DE ACCESO -----
    def check_access_rights(
        self,
        model: APIManager.odoo_models,
        right: ACCESS_RIGHTS,
    ) -> bool:
        """
        ## Método para verificar los permisos de acceso a un modelo
        especificado

        Ejemplo de uso:
        ````py
        odoo.check_access_rights("res.partner", "write")
        ````

        Permisos disponibles
        - `create`: Permiso de creación
        - `read`: Permiso de lectura
        - `write`: Permiso de lectura
        - `unlink`: Permiso de eliminación
        """

        return self._request(
            model= model,
            method= "check_access_rights",
            data= self._build_data(
                data= right
            ),
            params= self._build_params(
                raise_exception= False
            )
        )


    # ----- MÉTODO DE BÚSQUEDA -----
    def search(
        self,
        model: APIManager.odoo_models,
        search_criteria: APIManager.condition_structure,
        offset: int = None,
        limit: int = None
    ) -> list[int]:
        """
        ## Método de búsqueda
        Este método realiza una búsqueda en un modelo especificado y retorna
        una lista de IDs que cumplen con las condiciones especificadas.

        Ejemplo de uso:
        ````py
        odoo.search("sale.order", [("state", "=", "cancel")])
        # [52, 87, 129, 132]
        ````

        ### Condición de búsqueda
        Se provee al menos una tupla con la siguiente escructura:
        ````py
        ("nombre_del_campo", "=", "valor")
        ````

        Todo esto se encierra dentro de una lista:
        ````py
        [("nombre_del_campo", "=", "valor")]
        ````

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
        ````py
        ['&', (condicion_1...), (condicion_2...)]
        ````

        Los operadores lógicos disponibles son:
        - `&`: and
        - `|`: or

        ### Desfase de registros para paginación
        Este parámetro sirve para realizar un slice de la lista de IDs
        retornada por el API pero directamente desde el API. Suponiendo que una
        búsqueda normal arrojarría los siguientes resultados:
        ````py
        odoo.search("sale.order", [("state", "=", "sale")])
        # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14...]
        ````

        Se puede especificar que sólo se requiere el retorno de la lista de IDs
        a partir de un índice especificado, por ejemplo:
        ````py
        odoo.search("sale.order", [("state", "=", "sale")], offset=5)
        # [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19...]
        ````

        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima en la cantidad de IDs
        retornada por el API, también directamente desde el API. Suponiendo que
        una búsqueda normal arrojarría los siguientes resultados:
        ````py
        odoo.search("sale.order", [("state", "=", "sale")])
        # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14...]
        ````

        Se puede especificar que sólo se requiere obtener una cantidad máxima
        de registros a partir de un número provisto:
        ````py
        odoo.search("sale.order", [("state", "=", "sale")], limit=5)
        # [1, 2, 3, 4, 5]
        ````

        ----
        ### Sugerencia de uso en múltiples condiciones
        Para mejorar y facilitar una búsqueda con múltiples condiciones
        se recomienda asignar la lista a una variable y utilizar la siguiente
        estructura de identación dentro de la lista:
        ````py
        # Ejemplo 1
        criteria = [
            '&',
                (condicion_1...),
                (condicion_2...)
        ]

        # Ejemplo 2
        criteria = [
            '|',
                '&',
                    (condicion_1...),
                    (condicion_2...),
                (condicion_3...)
        ]
        ````

        En el primer ejemplo, la condición 1 y la condición 2 deben
        cumplirse para que un registro se incluya en la lista de resultados.

        En el segundo ejemplo, el resultado `True` de la condición 1 y la
        condición 2, todo esto o la condición 3 deben cumplirse para que un registro se
        incluya en la lista de resultados, es decir, algo como esto:
        ````py
        ((condicion_1 and condicion_2) or condicion_3)
        ````

        La ejecución del método entonces se vería así:
        ````py
        odoo.search("sale.order", criteria)
        ````
        """

        
        # Ejecución del método de solicitud al API
        return self._request(
            model= model,
            method= "search",
            data= self._build_data(
                data= search_criteria
            ),
            params= self._build_params(
                offset=offset,
                limit=limit
            )
        )


    # ----- MÉTODO DE LECTURA -----
    def read(
        self,
        model: APIManager.odoo_models,
        record_ids: list[int],
        fields: list[str] = None
    ) -> list[dict]:
        """
        ## • Método de lectura
        Este método realiza una lectura de IDs en donde retorna una lista
        de diccionarios, cada uno, con la información de un registro.

        ### Ejemplo de uso
        ````py
        odoo.read("sale.order", [52, 87, 129, 132])
        # [{
        #     'id': 52,
        #     'name': 'S00052',
        #     ...
        #  },
        #  {
        #     'id': 89,
        #     'name': 'S00089',
        #     ...
        #  },
        #  {
        #     'id': 129,
        #     'name': 'S00129',
        #     ...
        #  },
        #  {
        #     'id': 132,
        #     'name': 'S00132',
        #     ...
        # }]
        ````

        ### Espeficicación de campos a retornar por el API
        También se puede especificar una lista de campos para reducir
        el tamaño de los diccionarios en la lista para mayor rapidez en el
        tiempo de respuesta de la API:
        ````py
        odoo.read("sale.order", [52, 87, 129, 132], ['name', 'state'])
        ````

        ----
        ### Sugerencia de uso en listas de campos muy grandes
        Para estos casos, se recomienda almacenar la lista de campos en una
        variable con alguna de las siguientes dos estructuras:

        ````py
        # Ejemplo 1
        fields = ['name', 'state', 'salesman_id', 'partner_id']

        # Ejemplo 2
        fields = [
            'name',
            'state',
            'salesman_id',
            'partner_id'
        ]
        ````

        La ejecución del método entonces se vería así:
        ````py
        odoo.read("sale.order", [52, 87, 129, 132], fields)
        ````

        """
        
        # Ejecución del método de solicitud al API
        return self._request(
            model= model,
            method= "read",
            data= self._build_data(record_ids),
            params= self._build_params(
                fields= fields
            )
        )
    

    # ----- MÉTODO DE BÚSQUEDA Y LECTURA -----
    def search_read(
        self,
        model: APIManager.odoo_models,
        data: APIManager.condition_structure,
        fields: list[str] = None,
        offset: int = None,
        limit: int = None
    ):
        """
        ## Método de búsqueda y lectura
        Este método es la combinación de los métodos internos
        `OdooAPIManager.search` y `OdooAPIManager.read` optimizado para la
        ejecución de ambos en una misma solicitud al API.

        ### Ejemplo de uso

        ````py
        odoo.search_read("sale.order", [("state", "=", "cancel")])
        # [{
        #     'id': 52,
        #     'name': 'S00052',
        #     ...
        #  },
        #  {
        #     'id': 89,
        #     'name': 'S00089',
        #     ...
        #  },
        #  {
        #     'id': 129,
        #     'name': 'S00129',
        #     ...
        #  },
        #  {
        #     'id': 132,
        #     'name': 'S00132',
        #     ...
        # }]
        ````

        ### Condición de búsqueda
        Se provee al menos una tupla con la siguiente escructura:
        ````py
        ("nombre_del_campo", "=", "valor")
        ````

        Todo esto se encierra dentro de una lista:
        ````py
        [("nombre_del_campo", "=", "valor")]
        ````

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
        ````py
        ['&', (condicion_1...), (condicion_2...)]
        ````

        Los operadores lógicos disponibles son:
        - `&`: and
        - `|`: or

        ### Espeficicación de campos a retornar por el API
        También se puede especificar una lista de campos para reducir
        el tamaño de los diccionarios en la lista para mayor rapidez en el
        tiempo de respuesta de la API:
        ````py
        odoo.read("sale.order", [52, 87, 129, 132], ['name', 'state'])
        ````

        ### Desfase de registros para paginación
        Este parámetro sirve para realizar un slice de la lista de IDs
        retornada por el API pero directamente desde el API. Suponiendo que una
        búsqueda normal arrojarría los siguientes resultados:
        ````py
        odoo.search_read("sale.order", [("state", "=", "sale")])
        # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14...]
        ````

        Se puede especificar que sólo se requiere el retorno de la lista de IDs
        a partir de un índice especificado, por ejemplo:
        ````py
        odoo.search_read("sale.order", [("state", "=", "sale")], offset=5)
        # [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19...]
        ````

        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima en la cantidad de IDs
        retornada por el API, también directamente desde el API. Suponiendo que
        una búsqueda normal arrojarría los siguientes resultados:
        ````py
        odoo.search_read("sale.order", [("state", "=", "sale")])
        # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14...]
        ````

        Se puede especificar que sólo se requiere obtener una cantidad máxima
        de registros a partir de un número provisto:
        ````py
        odoo.search_read("sale.order", [("state", "=", "sale")], limit=5)
        # [1, 2, 3, 4, 5]
        ````

        ----
        ### Sugerencia de uso en múltiples condiciones
        Para mejorar y facilitar una búsqueda con múltiples condiciones
        se recomienda asignar la lista a una variable y utilizar la siguiente
        estructura de identación dentro de la lista:
        ````py
        # Ejemplo 1
        criteria = [
            '&',
                (condicion_1...),
                (condicion_2...)
        ]

        # Ejemplo 2
        criteria = [
            '|',
                '&',
                    (condicion_1...),
                    (condicion_2...),
                (condicion_3...)
        ]
        ````

        En el primer ejemplo, la condición 1 y la condición 2 deben
        cumplirse para que un registro se incluya en la lista de resultados.

        En el segundo ejemplo, el resultado `True` de la condición 1 y la
        condición 2, todo esto o la condición 3 deben cumplirse para que un registro se
        incluya en la lista de resultados, es decir, algo como esto:
        ````py
        ((condicion_1 and condicion_2) or condicion_3)
        ````

        La ejecución del método entonces se vería así:
        ````py
        odoo.search_read("sale.order", criteria)
        ````

        ### Sugerencia de uso en listas de campos muy grandes
        Para estos casos, se recomienda almacenar la lista de campos en una
        variable con alguna de las siguientes dos estructuras:

        ````py
        # Ejemplo 1
        fields = ['name', 'state', 'salesman_id', 'partner_id']

        # Ejemplo 2
        fields = [
            'name',
            'state',
            'salesman_id',
            'partner_id'
        ]
        ````

        La ejecución del método entonces se vería así:
        ````py
        odoo.read("sale.order", [52, 87, 129, 132], fields)
        ````
        """
        
        # Ejecución del método de solicitud al API
        return self._request(
            model= model,
            method= "search_read",
            data= self._build_data(data),
            params= self._build_params(
                fields= fields,
                offset= offset,
                limit= limit
            )
        )
    

    # ----- MÉTODO DE CONTEO DE UNA BÚSQUEDA -----
    def search_count(
        self,
        model: APIManager.odoo_models,
        data: APIManager.condition_structure
    ) -> int:
        """
        ## Método de conteo de una búsqueda
        Este método devuelve el conteo de la cantidad de registros que cumplen
        un criterio de búsqueda provisto. Es equivalente a usar la función
        `len()` a la lista de retorno del método `OdooAPIManager.search()`:
        ````py
        len(odoo.search("sale.order", [("state", "=", "cancel")]))
        ````

        Ejemplo de uso:
        ````py
        odoo.search_count("sale.order", [("state", "=", "cancel")])
        # 87
        ````

        ### Condición de búsqueda
        Se provee al menos una tupla con la siguiente escructura:
        ````py
        ("nombre_del_campo", "=", "valor")
        ````

        Todo esto se encierra dentro de una lista:
        ````py
        [("nombre_del_campo", "=", "valor")]
        ````

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
        ````py
        ['&', (condicion_1...), (condicion_2...)]
        ````

        Los operadores lógicos disponibles son:
        - `&`: and
        - `|`: or

        ----
        ### Sugerencia de uso en múltiples condiciones
        Para mejorar y facilitar una búsqueda con múltiples condiciones
        se recomienda asignar la lista a una variable y utilizar la siguiente
        estructura de identación dentro de la lista:
        ````py
        # Ejemplo 1
        criteria = [
            '&',
                (condicion_1...),
                (condicion_2...)
        ]

        # Ejemplo 2
        criteria = [
            '|',
                '&',
                    (condicion_1...),
                    (condicion_2...),
                (condicion_3...)
        ]
        """

        return self._request(
            model= model,
            method= "search_count",
            data= self._build_data(
                data= data
            ),
            params= self._build_params()
        )


    # ----- MÉTODO INTERNO DE ESCRITURA -----
    def _write_single_record(
        self,
        model: APIManager.odoo_models,
        record_id: list[dict],
        changes_data: dict[str, int, bool]
    ):
        return self._request(
            model= model,
            method= "write",
            data = self._build_data(
                data= record_id,
                data_args= changes_data,
            )
        )
    
    def session_info(self) -> None:
        """
        ## Información de la sesión
        Este método retorna una impresión de la información de la sesión actual:
        ````py
        odoo.session_info()
        # base de datos: your-database-name
        # url de origen: https://your-database-name.odoo.com
        # usuario: username_api@example.com
        # token: ****************************************
        ````
        """
        for i in self._info:
            print(i)


    # ----- SOLICITUD AL API -----
    def _request(
        self,
        model: APIManager.odoo_models,
        method: API_METHODS,
        data: APIManager.condition_structure,
        params: dict[list, int] ={}
    ):
        # Se realiza la solicitud al API
        return self._models.execute_kw(
            # Base de datos de la API
            self._api_db,
            # UUID de la cuenta
            self._uid,
            # Token de la cuenta
            self._api_token,
            # Modelo de Odoo
            model,
            # Método de solicitud
            method,
            # Matriz de argumentos
            data,
            # Diccionario de argumentos
            params
        )


    def _build_data(
        self,
        data: list[tuple, str, int],
        data_args: dict = None
    ):
        
        if data_args:
            return [data, data_args]
        else:
            return [data]
        

    # ----- CONSTRUIR EL DICCIONARIO DE ARGUMENTOS OPCIONALES -----
    def _build_params(
        self,
        fields: list[str] = None,
        offset: int = None,
        limit: int = None,
        raise_exception: bool = None
    ) -> dict[list[str], int]:
        """
        ## Método interno para la conversión de parámetros individuales en un
        diccionario con llaves opcionales. Retorna un diccionario vacío en caso
        de llamarlo sin proporcionarle argumentos.
        """
        
        # Se inicializa la variable como diccionario vacío
        params = dict()

        # Campos
        if fields:
            params["fields"] = fields
        # Desfase inicial
        if offset:
            params["offset"] = offset
        # Límite de resultados arrojados
        if limit:
            params["limit"] = limit
        # Arrojar error
        if not raise_exception is None:
            params["raise_exception"] = raise_exception

        # Retorno del diccionario construído
        return params
    

    @classmethod
    def extension_class_template(cls):
        """
        ## Generación de clase de extensión de `OdooAPIManager`
        Este método de clase retorna una plantilla de constructor para la
        creación de módulos externos.

        Uso:
        ````py
        ExtensionModule = OdooAPIManager.extension_class_template()

        @OdooAPIManager.extensions.register_module("iacele")
        class MyCustomModule(ExtensionModule):
            ...
        ````
        """
        return APIManagerExtension


    # ------ MÉTODOS DESCONTINUADOS --------

    @deprecated(new_method= session_info)
    def info(self) -> None:
        """
        **Obsoleto**: Este método está obsoleto y será removido en futuras versiones.
        Usar el método OdooAPIManager.session_info()
        """
        self.session_info()
