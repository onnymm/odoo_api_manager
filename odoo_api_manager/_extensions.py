from ._base_api_manager import APIManager
from ._options import MODELS
import pandas as pd
import numpy as np
from typing import Literal
from datetime import datetime, timedelta

class DataMethods():
    """
    ## Extensión de la clase `OdooAPIManager`
    Subclase para el uso de métodos relacionados con la consulta de datos
    para su análisis o consulta.
    """
    def __init__(self, _instance: APIManager):
        self._instance = _instance

    def get_dataset(
        self,
        model: MODELS,
        search_criteria: list[tuple, str],
        fields: list,
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

    def model_fields(
        self,
        model: MODELS,
        atts: list[str] = [
                'name',
                'field_description',
                'model_id',
                'ttype',
                'state',
                'relation'
            ]
    ) -> pd.DataFrame:
        """
        Esto es una documentación
        """
        data = self._instance.search_read(
            model= "ir.model.fields",
            data= [('model_id', '=', model)],
            fields= atts
        )

        return pd.DataFrame(data)
    
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

class FixMethods():
    """
    ## Extensión de la clase `OdooAPIManager`
    Subclase para el uso de métodos relacionados con la corrección
    preestablecida para excepciones en procesos administrativos dentro de Odoo.
    """

    def __init__(self, _instance: APIManager):
        self._instance = _instance

    # ----- CIERRE DE CICLO DE VIDA EN ESTADOS DE ÓRDENES DE VENTA -----
    def close_sale_order_status(
        self,
        record_id: int
    ):
        execution = self._instance._write_single_record(
            model= "sale.order",
            record_id= record_id,
            changes_data= {
                "invoice_status": "invoiced"
            }
        )

        if execution:
            return self._instance.read(
                model= "sale.order",
                record_ids= [record_id],
                fields= ["invoice_status"]
            )
        else:
            "No fue posible actualizar el registro"

class ModelsMethods():
    """
    ## Submódulo para desencadenar acciones de modelos
    """

    _actions = {
        "sale.order": {
            "confirm": "action_confirm"
        },
        "account.move": {
            "update_payments": "l10n_mx_edi_cfdi_invoice_try_update_payments"
        }
    }

    def __init__(self, _instance: APIManager):
        self._instance = _instance

    def sale_order_exec(self, method: Literal["confirm"], record_id: int):
        actions = self._actions["sale.order"]
        self._instance._request("sale.order", actions[method], [[record_id]])

    def account_move_exec(self, method: Literal["update_payments"], record_id: int):
        actions = self._actions["account.move"]
        try:
            self._instance._request("account.move", actions[method], [[record_id]])
        except:
            pass

class UtilsMethods():

    local_time_difference_in_hours = -7

    def __init__(self, _instance: APIManager):
        self._instance = _instance

    def _to_datetime(self, string_date: str) -> datetime:
        [date, time] = string_date.split(" ")
        [year, month, day] = [int(i) for i in date.split("-")]
        [hour, minute, second] = [int(i) for i in time.split(":")]
        return datetime(year, month, day, hour, minute, second)
        # str(datetime(year, month, day, hour, minute, second) - timedelta(hours=7))

    def to_local_date(self, date: str):
        print(date)
        return str(self._to_datetime(date) + timedelta(hours=self.local_time_difference_in_hours))
    
class ExtensionsRegistry():
    """
    ## Registro de módulos externos
    Este módulo se integra a la superclase OdooAPIManager para registrar
    módulos externos en ésta y extender su funcionalidad.
    """

    def register_module(cls, module_name: str):
        """
        ## Registro de módulos de extensión de `OdooAPIManager`
        Este método se utiliza como decorador para la declaración de clases
        de Python que funcionarán como extensiones de la librería
        `OdooAPIManager` utilizando los métodos integrados de ésta extendiendo
        su funcionalidad con métodos personalizados.

        uso:
        ````py
        @OdooAPIManager.extension.register_module("my_custom_module"):
        class CustomModule()
            ...
        ````

        ### Registro de un nuevo módulo de extensión
        Para registrar un nuevo módulo de extensión se utiliza la llamada del
        método como decorador de la declaración de la clase contenedora de
        los métodos de extensión proporcionando el nombre con el que se
        accederá al módulo externo:
        ````py
        @OdooAPIManager.extension.register_module("my_custom_module")
        ````

        ### Declaración de la clase de extensión
        Para fines de estandarización se recomienda inicializar la clase con
        un argumento de entrada. El nombre sugerido es `api_manager`:
        ````py
        class CustomModule:
            def _init_(self, api_manager: OdooAPIManager): # Debe ser doble guión bajo
        ````

        Posteriormente se integra la instancia de la librería OdooAPIManger
        como parte de un atributo:
        ````py
        self._api_manager = api_manager
        ````

        De esta forma se pueden crear métodos extendidos que aprovechan las
        funciones de la librería y se utilizan de una forma más personalizada:
        ````py
        def count_product_items(self):
            count = self._api_manager.search_count("product.template", [])
            return count
        ````

        El ejemplo anterior permitiría hacer lo siguiente:
        ````py
        odoo = OdooAPIManager()

        odoo.my_custom_module.count_product_items()
        # Esto retorna algún número
        ````

        A continuación se muestra el ejemplo completo:
        >>> @OdooAPIManager.extension.register_module("my_custom_module"):
        >>> class CustomModule()
        >>>     def _init_(self, api_manager: OdooAPIManager): # Debe ser doble guión bajo
        >>>         self._api_manager = api_manager
        >>> 
        >>>     def count_product_items(self):
        >>>         count = self._api_manager.search_count("product.template", [])
        >>>         return count
        >>> 
        >>> odoo = OdooAPIManager()
        >>> 
        >>> odoo.my_custom_module.count_product_items()
        >>> # Esto retorna algún número
        """

        def register_new_module(module):
            APIManager.extension_modules.append(
                {
                    "name": module_name,
                    "declaration": module
                }
            )
            print("registro exitoso")

        return register_new_module

class ExtendMethods():

    def __init__(self, instance: APIManager):
        self._instance = instance

    def _initialize_modules(self):
        if len(self._instance.extension_modules) > 0:
            for module in self._instance.extension_modules:
                setattr(
                    self._instance,
                    module["name"],
                    module["declaration"](self._instance)
                )
