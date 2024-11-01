import pandas as pd
import numpy as np
from typing import Literal
from odoo_api_manager._base_extension import APIManagerExtension
from odoo_api_manager._base_api_manager import APIManager
from odoo_api_manager._warnings import deprecated

class DataMethods(APIManagerExtension):
    """
    ## Extensión de la clase `OdooAPIManager`
    Subclase para el uso de métodos relacionados con la consulta de datos
    para su análisis o consulta.
    """

    fields_atts = [
        'name',
        'field_description',
        'model_id',
        'ttype',
        'state',
        'relation'
    ]



    def dataset(
        self,
        model: APIManager.odoo_models,
        search_criteria: list[tuple, str],
        fields: list,
        offset: int | None = None,
        limit: int | None = None,
        many2one_values: Literal["id_only", "name_only", "pair", "raw"] = "pair",
    ) -> pd.DataFrame:
        """
        ## Obtener un conjunto de datos desde el API de Odoo
        Este método realiza una solicitud `search_read` al API de Odoo
        y crea un DataFrame con el JSON recibido. Este método recibe los mismos
        parámetros que el método antes mencionado.

        Este método también separa las referencias de los campos `many2one`
        de `[5, 'nombre_del_registro']` a `5` y `'nombre_del_registro'` y
        asigna los valores a las columnas renombradas.

        Por ejemplo, si se especifica un `user_id`, se creará un DataFrame que
        no sólo contenga la columna `user_id` con los valores en fomato
        `[5, 'nombre_usuario']` sino que se crearán dos columnas llamadas
        `user_id` y `user_name` con los valores `5` y `'nombre_usuario'`. Este
        comportamiento se puede desactivar especificando el parámetro
        `many2one_values` con el valor `"raw"`.

        ### Ejemplo de uso
        >>> odoo.data.data_set("sale.order", [("state", "=", "cancel")], ["name", "user_id", "state"])
        >>> #    id       name        user_id     user_name   state
        >>> # 0  3        S00003      3           moderator  cancel
        >>> # 1  14       S00014      7           user 4     cancel
        >>> # 2  25       S00025      7           user 4     cancel
        >>> # 3  27       S00027      3           moderator  cancel
        >>> # 4  48       S00048      5           moderator  cancel

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

        ### Campos a retornar por el API
        A diferencia del método `search_read` en el que los campos a obtener
        del modelo se pueden o no incluir como argumento de la llamada a éste,
        en el método `dataset` este parámetro es obligatorio. Para conocer
        cuáles son los campos disponibles en el modelo, se puede utilizar el
        método `OdooAPIManager.data.model_fields`:
        >>> odoo.data.dataset(... ['name', 'state'])

        ----
        ### Desfase de registros para paginación
        Este parámetro sirve para realizar un slice de la lista de IDs
        retornada por el API pero directamente desde el API. Suponiendo que una
        búsqueda normal arrojarría los siguientes resultados:
        >>> odoo.data.dataset("sale.order", [("state", "=", "sale")])
        >>> # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14...]

        Se puede especificar que sólo se requiere el retorno de la lista de IDs
        a partir de un índice especificado, por ejemplo:
        >>> odoo.data.dataset("sale.order", [("state", "=", "sale")], offset=5)
        >>> # [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19...]

        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima en la cantidad de IDs
        retornada por el API, también directamente desde el API. Suponiendo que
        una búsqueda normal arrojarría los siguientes resultados:
        >>> odoo.data.dataset("sale.order", [("state", "=", "sale")])
        >>> # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14...]

        Se puede especificar que sólo se requiere obtener una cantidad máxima
        de registros a partir de un número provisto:
        >>> odoo.data.dataset("sale.order", [("state", "=", "sale")], limit=5)
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
        >>> odoo.data.dataset("sale.order", criteria, [...])

        ### Sugerencia de uso en listas de campos muy grandes
        Para estos casos, se recomienda almacenar la lista de campos en una
        variable con alguna de las siguientes dos estructuras:

        >>> # Ejemplo 1
        >>> fields = ['name', 'state', 'salesman_id', 'partner_id']
        >>> 
        >>> # Ejemplo 2
        >>> fields = [
        >>>     'name',
        >>>     'state',
        >>>     'salesman_id',
        >>>     'partner_id'
        >>> ]

        La ejecución del método entonces se vería así:
        >>> odoo.data.dataset("sale.order", [(...)], fields)
        """

        # Obtención de los datos desde el API
        _base_data = self._instance.search_read(model, search_criteria, fields, offset, limit)

        # Creación de la estructura de columnas del DataFrame
        _base_df = pd.DataFrame({ field: [] for field in ['id'] + fields })

        # Creación del DataFrame
        data = pd.DataFrame(_base_data)

        # Obtención de las filas de datos
        if len(data) and many2one_values != "raw":
            # Destructuración de valores en columnas many2one
            data = self._destruture_many2one_columns(data, many2one_values)
            return data
        else:
            return _base_df



    def model_fields(
        self,
        model: APIManager.odoo_models,
        atts: list[str] = fields_atts,
        fields: list = None,
        output: Literal["dataframe", "raw"] = "dataframe"
    ) -> pd.DataFrame:
        """
        ## Obtener información de los campos de un modelo
        Este método retorna la información más relevante de los campos, en 
        formato pandas.DataFrame, de un modelo especificado en la función.
        Todos los modelos están disponibles para su consulta.

        uso:
        ````py
        odoo.data.model_fields("sale.order")
        #         id                       name ...     ttype        relation
        # 0     9931               access_token ...      char           False
        # 1     9930                 access_url ...      char           False
        # 2     9932             access_warning ...      text           False
        # ...    ...                        ... ...       ...             ...
        #         id                       name ...     ttype        relation
        # 127   9993                 write_date ...  datetime           False
        # 128   9992                  write_uid ...  many2one       res.users
        ````

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
        ````py
        specific_atts = ["name", "field_description", "ttype"]
        odoo.data.model_fields("sale.order", atts=specific_atts)
        #                     name  field_description     ttype
        # 0           access_token     Security Token      char
        # 1             access_url  Portal Access URL      char
        # 2         access_warning     Access warning      text
        # ...                  ...                ...       ...
        # 126  website_message_ids   Website Messages  one2many
        # 127           write_date    Last Updated on  datetime
        # 128            write_uid    Last Updated by  many2one
        ````

        ## Especificación de campos
        Por defecto, el método `model_fields` retorna la lista completa de
        todos los campos del modelo. Sin embargo, si sólo se requieren ciertos
        campos, puede ser especificado en el parámetro `fields` en una lista:
        ````py
        specific_fields = ["id", "name", "state"]
        odoo.data.model_fields("sale.order", fields=specific_fields)
        #      id   name ...      ttype  relation
        # 0  9989     id ...    integer     False
        # 1  9933   name ...       char     False
        # 2  9936  state ...  selection     False
        ````

        ### Formato de retorno
        Por defecto, el método `model_fields` retorna la información en formato
        pandas.DataFrame. También existe la opción de retornar el objeto
        sin manipular retornado desde el API de Odoo, esto, especificado en el
        parámetro `output`. Los valores disponibles son:
        - `"dataframe"`: Formato en `pandas.DataFrame` (Opción por defecto).
        - `"raw"`: Objeto retornado desde el API de Odoo, sin manipular.
        """
        # Criterio inicial de búsqueda
        search_criteria = [('model_id', '=', model)]

        # Si se especificaron los campos, se rearma el criterio de búsqueda
        if (fields):
            # Se interta el operador 'and' al principio de la lista
            search_criteria.insert(0, "&")
            # Se añade la tupla de coincidencia por nombre
            search_criteria.append(("name", "in", fields))

        # Búsqueda de registros
        data = self._instance.search_read(
            model= "ir.model.fields",
            data= search_criteria,
            fields= atts
        )

        # Evaluación del tipo de salida
        if output == "dataframe":
            # Se convierte la respuesta a un pandas.DataFrame
            data = pd.DataFrame(data)

        return data



    def _map_dataframe_ref(self, data, field):
        """"
        ## Mapeo de referencias múltiples
        Método interno para mapear una referencia de un DataFrame en un
        subconjunto de datos perteneciente a una columna de un conjunto principal.
        """
        new_columns = self._rename_df_column_ref(field)
        df_map = pd.DataFrame(
            [byte[field] if byte[field] else [np.nan, np.nan] for byte in data],
            columns= new_columns
        )
        df_map = df_map.drop_duplicates(field)
        return df_map, new_columns



    def _rename_df_column_ref(self, reference: str) -> list:
        end = reference.find("_id")
        reference = reference[:end]
        return [reference + "_id", reference + "_name"]



    def _extract_id_from_list(self, sample: list | np.number) -> int | np.number:
        if sample:
            return sample[0]
        else:
            return sample



    def _destruture_many2one_columns(self, data: pd.DataFrame, get: Literal["id_only", "name_only", "pair"]) -> pd.DataFrame:
        """
        ## Destructuración de valores en columnas many2one
        Este método se encarga de dividir los valores contenidos en las
        columnas de campos de tipo many2one, que consisten en una lista de
        pares `id` y `name` o bien, valores booleanos `False`.

        Uso:
        >>> data = pd.DataFrame(
        >>>     {
        >>>         'id': [0, 1, 2],
        >>>         'user_id': [
        >>>             [0, 'admin'],
        >>>             [1, 'moderator'],
        >>>             [2, 'normal_user']
        >>>         ]
        >>>     }
        >>> )
        >>> #    id           user_id
        >>> # 0   0        [0, admin]
        >>> # 1   1    [1, moderator]
        >>> # 2   2  [2, normal_user]
        >>> 
        >>> self._destruture_many2one_columns(data, get= "pairs")
        >>> #    id  user_id    user_name
        >>> # 0   0        0        admin
        >>> # 1   1        1    moderator
        >>> # 2   2        2  normal_user
        >>> 
        >>> self._destruture_many2one_columns(data, get= "id_only")
        >>> #    id  user_id
        >>> # 0   0        0
        >>> # 1   1        1
        >>> # 2   2        2
        >>> 
        >>> self._destruture_many2one_columns(data, get= "name_only")
        >>> #    id    user_name
        >>> # 0   0        admin
        >>> # 1   1    moderator
        >>> # 2   2  normal_user
        """

        # Inicialización de lista para almacenamiento ordenado de nombres de columna
        columns_order = []

        # Condición para obtener columna de nombre
        _get_name_column = get == "pair" or get == "name_only"
        _get_id_column = get == "pair" or get == "id_only"
        
        # En la obtención de valores, primero se obtiene el nombre y luego la ID
        # En la obtención de columnas, primero se obtiene la ID y luego el nombre

        # Iteración por cada nombre de columna
        for column in data.columns:
            # Si el nombre de la columna termina en `_id` significa que es un campo many2one
            if column.endswith("_id"):

                # Obtención de valores de columnas

                # Si el caso incluye la extracción del nombre del valor, se ejecuta lo siguiente
                if _get_name_column:
                    # Obtención de nombres de referencias many2one
                    data[column.replace("_id", "_name")] = data[column].apply(self.transformation.get_many2one_name)
            
                # Si el caso incluye la extracción del ID del valor, se ejecuta lo siguiente
                if _get_id_column:
                    data[column] = data[column].apply(self.transformation.get_many2one_id)

                # Obtención de nombres de columnas

                # Si el caso incluye la extracción del ID del valor, se ejecuta lo siguiente
                if _get_id_column:
                    columns_order.append(column)
                # Si el caso incluye la extracción del nombre del valor, se ejecuta lo siguiente
                if _get_name_column:
                    columns_order.append(column.replace("_id", "_name"))

            # Si el campo no es many2one se conserva en su respectivo índice
            else:
                columns_order.append(column)

        # Retorno del DataFrame en el orden de columnas establecido
        return data[columns_order]



    @deprecated(new_method=dataset)
    def get_dataset(
        self,
        model: APIManager.odoo_models,
        search_criteria: list[tuple, str],
        fields: list,
        offset: int,
        limit: int,
        separate_many2one: bool= True,
        many2one_ids_only: bool= False
    ) -> pd.DataFrame:
        """
        ## Obtener un conjunto de datos desde el API de Odoo
        Este método realiza una solicitud `search_read` al API de Odoo
        y crea un DataFrame con el JSON recibido. Este método recibe los mismos
        parámetros que el método antes mencionado.

        Este método también separa las referencias de los campos `many2one`
        de `[5, 'nombre_del_registro']` a `5` y `'nombre_del_registro'` y
        asigna los valores a las columnas renombradas.

        Por ejemplo, si se especifica un `user_id`, se creará un DataFrame que
        no sólo contenga la columna `user_id` con los valores en fomato
        `[5, 'nombre_usuario']` sino que se crearán dos columnas llamadas
        `user_id` y `user_name` con los valores `5` y `'nombre_usuario'`. Este
        comportamiento se puede desactivar especificando el parámetro
        `separate_many2one` con el valor `False`.

        ### Ejemplo de uso
        ````py
        odoo.data.get_data_set("sale.order", [("state", "=", "cancel")], ["name", "user_id", "state"])
        #    id       name        user_id     user_name   state
        # 0  3        S00003      3           moderador  cancel
        # 1  14       S00014      7           usuario 4  cancel
        # 2  25       S00025      7           usuario 4  cancel
        # 3  27       S00027      3           moderador  cancel
        # 4  48       S00048      5           moderador  cancel
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

        ### Campos a retornar por el API
        A diferencia del método `search_read` en el que los campos a obtener
        del modelo se pueden o no incluir como argumento de la llamada a éste,
        en el método `get_dataset` este parámetro es obligatorio. Para conocer
        cuáles son los campos disponibles en el modelo, se puede utilizar el
        método `OdooAPIManager.data.model_fields`:
        ````py
        odoo.data.get_dataset(... ['name', 'state'])
        ````

        ----
        ### Desfase de registros para paginación
        Este parámetro sirve para realizar un slice de la lista de IDs
        retornada por el API pero directamente desde el API. Suponiendo que una
        búsqueda normal arrojarría los siguientes resultados:
        ````py
        odoo.data.get_dataset("sale.order", [("state", "=", "sale")])
        # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14...]
        ````

        Se puede especificar que sólo se requiere el retorno de la lista de IDs
        a partir de un índice especificado, por ejemplo:
        ````py
        odoo.data.get_dataset("sale.order", [("state", "=", "sale")], offset=5)
        # [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19...]
        ````

        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima en la cantidad de IDs
        retornada por el API, también directamente desde el API. Suponiendo que
        una búsqueda normal arrojarría los siguientes resultados:
        ````py
        odoo.data.get_dataset("sale.order", [("state", "=", "sale")])
        # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14...]
        ````

        Se puede especificar que sólo se requiere obtener una cantidad máxima
        de registros a partir de un número provisto:
        ````py
        odoo.data.get_dataset("sale.order", [("state", "=", "sale")], limit=5)
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
        odoo.data.get_dataset("sale.order", criteria, [...])
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
        odoo.data.get_dataset("sale.order", [(...)], fields)
        ````
        """

        # Se obtiene el JSON de la búsqueda
        data = self._instance.search_read(model, search_criteria, fields)
        # Se obtiene un DataFrame de los campos del modelo
        model_fields = self.model_fields(model)
        # Se crea el DataFrame base de los datos del JSON
        df = pd.DataFrame(data)

        # Obtener los subcampos de las referencias many2one
        if separate_many2one:

            # Se crea la lista de columnas ordenadas que ya inclue el ID como primera columna
            columns = ['id']

            # Se itera cada uno de los campos provistos en la función
            for field in fields:

                # Se valida si el campo es de tipo many2one
                if model_fields[model_fields["name"] == field].reset_index().at[0, "ttype"] == "many2one":

                    # Se obtienen los nombres de las columnas derivados del nombre del campo
                    df[field] = df[field].apply(self._extract_id_from_list)

                    # Se valida si sólo se requieren las IDs de los campos many2one
                    if not many2one_ids_only:
                        # Se crea un DataFrame con los IDs y los nombres de los valores de las referencias
                        (df_map, new_columns) = self._map_dataframe_ref(data, field)

                        # Se añaden estas columnas a la lista para mantener un orden
                        for i in new_columns:
                            columns.append(i)
                    
                        # Se fusiona el DataFrame base con estos registros mapeados a la ID del campo many2one
                        df = pd.merge(left=df, right=df_map, how='left')

                    else:
                        columns.append(field)

                # De no tratarse de un campo many2one no se hace nada y sólo se añade la columna
                else:
                    columns.append(field)
            # Al final del for se devuelve el DataFrame con las columnas ordenadas
            return df[columns]
        
        else:
            # Si no se activó el parámetro para sólo mantener las IDs de las referencias
            if many2one_ids_only:
                # Se extrae la ID de las listas de referencia many2one
                df[field] = df[field].apply(self._extract_id_from_list)

            # Se devuelve el DataFrame sin manipular en caso de que se haya desactivado el parámetro de separación de referencias
            return df



    class transformation():

        @classmethod
        def get_many2one_id(cls, value) -> int:
            if isinstance(value, list):
                return value[0]
            else:
                return value
        @classmethod
        def get_many2one_name(cls, value) -> str:
            if isinstance(value, list):
                return value[1]
            else:
                return value

