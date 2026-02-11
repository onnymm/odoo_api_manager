## Conexión al API de Odoo
Creador de una conexión con la API de Odoo.

Instalación:
```bash
pip install git+https://github.com/onnymm/odoo_api_manager.git
```

Forma de uso:
```py
from odoo_api_manager import OdooAPIManager
odoo_api = OdooAPIManager()
```

## Índice
- **MÉTODOS DISPONIBLES**
    - [Información de la sesión](#información-de-la-sesión)
    - [Permisos de acceso](#permisos-de-acceso)
    - [Creación de registros](#creación-de-registros)
    - [Búsqueda de registros](#búsqueda-de-registros)
    - [Lectura de registros](#lectura-de-registros)
    - [Búsqueda y lectura de registros](#búsqueda-y-lectura-de-registros)
    - [Conteo de una búsqueda](#conteo-de-una-búsqueda)
    - [Actualización de registros](#actualización-de-registros)
    - [Eliminación de registros](#eliminación-de-registros)
    - [Ejecución de métodos](#ejecución-de-métodos)
    - [Obtener información de los campos de un modelo](#obtener-información-de-los-campos-de-un-modelo)
- **ACERCA DE...**
    - [Configuración del entorno de trabajo](#configuración-del-entorno-de-trabajo)
    - [Formato de retorno](#formato-de-retorno)
    - [Tipado de Criterio de búsqueda](#tipado-de-criterio-de-búsqueda)
    - [Desfase de resultados](#desfase-de-resultados)
    - [Límite de registros retornados](#límite-de-registros-retornados)

----

# Métodos disponibles

## Información de la sesión
Este método retorna una impresión de la información de la sesión actual:
```py
odoo_api.session_info()
# Base de datos: your-database-name
# URL de origen: https://your-database-name.odoo.com
# Usuario: username_api@example.com
# Token de API: ****************************************
```

> **PARÁMETROS**
> 
> No se requieren parámetros.

----

## Permisos de acceso
Método para verificar los permisos de acceso del usuario de la sesión a un modelo especificado.

Ejemplo de uso:
```py
odoo_api.check_access_rights("res.partner", "write")
```

> **PARÁMETROS**
> 
> - `model`*: Nombre del modelo.
> - `right_type`*  Permiso de acceso a consultar. Los permisos disponibles son:
>     - `"create"`: Permiso de creación
>     - `"read"`: Permiso de lectura
>     - `"write"`: Permiso de lectura
>     - `"unlink"`: Permiso de eliminación
> - `raise_exception`: Arrojar error si no se tiene el permiso. Su valor prestablecido es `False`.

----

## Creación de registros
Este método permite crear un registro en un modelo de Odoo y retorna la ID de su registro.

Ejemplo de uso:
```py
partner_id = odoo_api.create("res.partner", {"name": "Nombre de un contacto"})
# 32
```

### Estructura de los datos
Las llaves deben ser el nombre exacto del campo en el modelo de Odoo, en donde se desea realizar el registro. Por ejemplo, el modelo `res.partner` contiene un campo llamado `name` que es el nombre del contacto.
```py
{"name": "Nombre de un contacto"}
```

También se puede proporcionar una lista de registros a crear
```py
[
    {"name": "Nombre de un contacto"},
    {"name": "Nombre de otro contacto"},
]
```

> **PARÁMETROS**
> 
> - `model`*: Nombre del modelo.
> - `records_data`*  Diccionario o lista de diccionarios que contienen los datos de los registros a crear.

----

## Búsqueda de registros
Este método realiza una búsqueda en un modelo especificado y retorna
una lista de IDs que cumplen con las condiciones especificadas.

Ejemplo de uso:
```py
odoo_api.search("sale.order", [("state", "=", "cancel")])
# [52, 87, 129, 132]
```

> **PARÁMETROS**
> 
> - `model`*: Nombre del modelo.
> - `search_criteria` Criterio de búsqueda. Para saber más sobre cómo generar criterios de búsqueda, consulta [Tipado de Criterio de búsqueda](#tipado-de-criterio-de-búsqueda).
> - `offset`: Desfase de resultados. Para saber más sobre cómo funciona este parámetro, consulta [Desfase de resultados para paginación](#desfase-de-resultados).
> - `limit`: Límite de resultados retornados. Para saber más sobre cómo funciona este parámetro, consulta [Límite de resultados](#límite-de-registros-retornados).

----

## Lectura de registros
Este método realiza una lectura de IDs en donde retorna una lista
de diccionarios, cada uno, con la información de un registro.

Ejemplo de uso:
```py
odoo_api.read("sale.order", [52, 87, 129, 132])
#     id    name ...
# 0   52  S00052 ...
# 1   89  S00089 ...
# 2  129  S00129 ...
# 3  132  S00132 ...

odoo_api.read("sale.order", [52, 87, 129, 132], output="dict")
# [{
#     "id": 52,
#     "name": "S00052",
#     ...
#  },
#  {
#     "id": 89,
#     "name": "S00089",
#     ...
#  },
#  {
#     "id": 129,
#     "name": "S00129",
#     ...
#  },
#  {
#     "id": 132,
#     "name": "S00132",
#     ...
# }]
```

### Espeficicación de campos a retornar por el API
También se puede especificar una lista de campos para reducir
el tamaño de los diccionarios en la lista para mayor rapidez en el
tiempo de respuesta de la API:
```py
odoo_api.read("sale.order", [52, 87, 129, 132], ["name", "state"])
```

> **PARÁMETROS**
> 
> - `model`*: Nombre del modelo.
> - `record_ids`* ID o lista de IDs de registros a leer en el modelo.
> - `fields`: Lista de campos específicos a leer de los registros.
> - `output`: Formato de retorno para la ejecución. Para saber más sobre cómo funciona este parámetro, consulta [Formato de retorno](#formato-de-retorno).

----

## Búsqueda y lectura de registros
Este método es la combinación de los métodos internos
`OdooAPIManager.search` y `OdooAPIManager.read` optimizado para la
ejecución de ambos en una misma solicitud al API.

Ejemplo de uso:
```py
odoo_api.read("sale.order", [52, 87, 129, 132])
#     id    name ...
# 0   52  S00052 ...
# 1   89  S00089 ...
# 2  129  S00129 ...
# 3  132  S00132 ...

odoo_api.read("sale.order", [52, 87, 129, 132], output="dict")
# [{
#     "id": 52,
#     "name": "S00052",
#     ...
#  },
#  {
#     "id": 89,
#     "name": "S00089",
#     ...
#  },
#  {
#     "id": 129,
#     "name": "S00129",
#     ...
#  },
#  {
#     "id": 132,
#     "name": "S00132",
#     ...
# }]
```

> **PARÁMETROS**
> 
> - `model`*: Nombre del modelo.
> - `search_criteria` Criterio de búsqueda. Para saber más sobre cómo generar criterios de búsqueda, consulta [Tipado de Criterio de búsqueda](#tipado-de-criterio-de-búsqueda).
> - `fields`: Lista de campos específicos a leer de los registros.
> - `offset`: Desfase de resultados. Para saber más sobre cómo funciona este parámetro, consulta [Desfase de resultados para paginación](#desfase-de-resultados).
> - `limit`: Límite de resultados retornados. Para saber más sobre cómo funciona este parámetro, consulta [Límite de resultados](#límite-de-registros-retornados).
> - `output`: Formato de retorno para la ejecución. Para saber más sobre cómo funciona este parámetro, consulta [Formato de retorno](#formato-de-retorno).

----

## Conteo de una búsqueda
Este método retorna el conteo de la cantidad de registros que cumplen un criterio de búsqueda provisto. Es equivalente a usar la función `len()` a la lista de retorno del método `OdooAPIManager.search()`.

Ejemplo de uso:
```py
odoo_api.search_count("sale.order", [("state", "=", "cancel")])
# 3
```

> **PARÁMETROS**
> 
> - `model`*: Nombre del modelo.
> - `search_criteria` Criterio de búsqueda. Para saber más sobre cómo generar criterios de búsqueda, consulta [Tipado de Criterio de búsqueda](#tipado-de-criterio-de-búsqueda).

----

## Actualización de registros
Este método permite actualizar uno o varios registros en el modelo especificado de Odoo.

Ejemplo de uso:
```py
odoo_api.write("sale.order", 52, {"user_id": 3})
# True

odoo_api.write("res.partner", 45, {"name": "Nuevo Nombre", "phone": "123456789"})
# True
```

Múltiples registros pueden ser actualizados simultáneamente pero todos éstos obtendrán el mismo valor para todos los campos declarados:
```py
odoo_api.write("sale.order", [52, 87, 129], {"user_id": 5})
# True
```

> **PARÁMETROS**
> 
> - `model`*: Nombre del modelo.
> - `record_ids`* ID o lista de IDs de registros a modificar en el modelo.
> - `records_data`*  Diccionario que contiene los datos a modificar.

----

## Eliminación de registros
Este método permite eliminar uno o varios registros en el modelo especificado de Odoo. Es importante mencionar que ciertos registros en ciertos modelos no pueden ser eliminados directamente debido a su uso en otros modelos o por contener ciertos vínculos como un documento fiscal, etc..

Ejemplo de uso:
```py
odoo_api.unlink("sale.order", 52)
# True

odoo_api.unlink("sale.order", [52, 87, 129])
# True
```

> **PARÁMETROS**
> 
> - `model`*: Nombre del modelo.
> - `record_ids`* ID o lista de IDs de registros a eliminar en el modelo.
> - `records_data`*  Diccionario que contiene los datos a eliminar.

----

## Ejecución de métodos
Este método ejecuta el método de un modelo en Odoo.

Uso:
```py
odoo_api.execute('sale.order', 'action_confirm', [15])
```

Esto permite "presionar botones de interfaz" directamente desde la API.

> Nota: Exiten algunos métodos que abren una ventana para ser completados. La ejecución de de este tipo de métodos no está soportada por esta librería.

> **PARÁMETROS**
> 
> - `model`*: Nombre del modelo.
> - `method`* Nombre del método a ejecutar.
> - `record_ids`* ID o lista de IDs de registros sobre los que se ejecuta el método.
> - `kwargs` Diccionario de argumentos proporcionados al método a ejecutar.

----

## Obtener información de los campos de un modelo
Este método retorna la información más relevante de los campos, en 
formato, de un modelo especificado en la función. Todos los modelos
están disponibles para su consulta.

uso:
```py
odoo_api.model_fields("sale.order")
#         id                       name ...     ttype        relation
# 0     9931               access_token ...      char           False
# 1     9930                 access_url ...      char           False
# 2     9932             access_warning ...      text           False
# ...    ...                        ... ...       ...             ...
#         id                       name ...     ttype        relation
# 127   9993                 write_date ...  datetime           False
# 128   9992                  write_uid ...  many2one       res.users
```

### Atributos de los campos
Las columnas de atributos mostradas por defecto son las siguientes:
- `name`: Nombre del campo
- `field_description`: Descripción del campo
- `model_id`: ID del campo
- `ttype`: Tipo del campo
- `state`: Estado del campo (`base` para campos nativos y `manual` para campos personalizados)
- `relation`: Modelo de relación

> **PARÁMETROS**
> 
> - `model`*: Nombre del modelo.
> - `attributes` Nombres de los atributos a revisar en los campos.
> - `fields`: Lista de campos específicos a leer de los registros.
> - `output`: Formato de retorno para la ejecución. Para saber más sobre cómo funciona este parámetro, consulta [Formato de retorno](#formato-de-retorno).

----

# Acerca de...

## Configuración del entorno de trabajo

Para proporcionar los datos de la conexión al API se debe contar con un archivo `.env` en la raíz del proyecto con la siguiente estructura:

```env
ODOO_API_USERNAME = username_api@example.com
ODOO_API_TOKEN = 1234567890abcdefghijklmnopqrstuvwxyz1234
ODOO_API_URL = https://your-database-name.odoo.com
ODOO_API_DB = your-database-name
ODOO_API_ALT_DB = your-database-name-test
```

Para crear una conexión a una base de datos de prueba o una base de datos alternativa, se debe proveer el valor `True` (En caso de haberse declarado una base de datos alternativa en el archivo `env.` con el nombre de variable `ODOO_API_ALT_DB`. Esta es la principal base de datos alternativa):
```py
odoo_test = OdooAPIManager(alt_db=True)
```

Ahora también se pueden utilizar mútiples conexiones a bases de datos usando sufijos en variables de entorno. Por ejemplo:
```env
ODOO_API_ALT_DB_01 = your-database-name-TEST-01
ODOO_API_ALT_DB_02 = your-database-name-TEST-02
```

Múltiples conexiones simultáneas:
```py
odoo_api_test_01 = OdooAPIManager(alt_db="01")
odoo_api_test_02 = OdooAPIManager(alt_db="02")
```

----

## Formato de retorno
Existe la forma de personalizar el formato de retorno en lecturas de datos. Por defecto, éste está prestablecido en Pandas DataFrame pero puede usarse el formato de listas de diccionarios tal como se recibe desde la API:
```py
odoo_api = OdooAPIManager() # Formato de retorno en Pandas DataFrame
odoo_api.read(...) # Formato de retorno en Pandas DataFrame
odoo_api.read(..., output="dict") # Formato de retorno en listas de diccionarios.

# Puede prestablecerse el formato predeterminado en la inicialización
odoo_api = OdooAPIManager(output_format="dict") # Formato de retorno en listas de diccionarios
odoo_api.read(...) # Formato de retorno en listas de diccionarios
odoo_api.read(..., output="dataframe") # Formato de retorno en Pandas DataFrame.
```

----

## Tipado de Criterio de búsqueda
Los criterios de búsqueda utilizados en Odoo consisten de listas de tuplas y literales de operadores lógicos para construir desde simples filtros hasta los filtros más complejos que sean necesarios para filtrar datos.

Se provee al menos una tupla con la siguiente escructura:
```py
("nombre_del_campo", "=", "valor")
```

Esta tupla está conformada por:
1. Nombre de un campo
2. Operador de comparación
3. Valor

Todo esto se encierra dentro de una lista:
```py
[("nombre_del_campo", "=", "valor")]
```

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

Los valores pueden ser de tipo `str`, `int`, `float` o `bool` dependiendo del tipo de valor del campo.

También pueden ser de tipo `list` que contenga alguno de los tipos anteriores.

En relaciones tipo `many2one`, `one2many` y `many2many` la búsqueda se hace por ID o por lista de IDs.

### Búsqueda con varias condiciones provistas
También se puede incluir más de una condición. Para esto, se agrega un operador lógico antes de dos tuplas de condiciones:
```py
["&", (condicion_1...), (condicion_2...)]
```

Los operadores lógicos disponibles son:
- `&`: and
- `|`: or

### Sugerencia de uso en múltiples condiciones
Para mejorar y facilitar una búsqueda con múltiples condiciones se recomienda asignar la lista a una variable y utilizar la siguiente estructura de identación dentro de la lista:
```py
# Importación para tipado y autocompletado
from odoo_api_manager.typing import CriteriaStructure
# Ejemplo 1
criteria: CriteriaStructure = [
    "&",
        (condicion_1...),
        (condicion_2...)
]

# Ejemplo 2
criteria = [
    "|",
        "&",
            (condicion_1...),
            (condicion_2...),
        (condicion_3...)
]
```

En el primer ejemplo, la condición 1 y la condición 2 deben
cumplirse para que un registro se incluya en la lista de resultados.

En el segundo ejemplo, el resultado `True` de la condición 1 y la
condición 2, todo esto o la condición 3 deben cumplirse para que un registro se
incluya en la lista de resultados, es decir, algo como esto:
```py
((condicion_1 and condicion_2) or condicion_3)
```

La ejecución del método entonces se vería así:
```py
odoo_api.search("sale.order", criteria)
```

----

## Desfase de resultados
Este parámetro sirve para realizar un slice de la lista de IDs
retornada por el API pero directamente desde el API. Suponiendo que una
búsqueda normal arrojarría los siguientes resultados:

```py
odoo_api.search("sale.order", [("state", "=", "sale")])
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14...]
```

Se puede especificar que sólo se requiere el retorno de la lista de IDs
a partir de un índice especificado, por ejemplo:

```py
odoo_api.search("sale.order", [("state", "=", "sale")], offset=5)
# [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19...]
```

----

## Límite de registros retornados
También es posible establecer una cantidad máxima en la cantidad de IDs
retornada por el API, también directamente desde el API. Suponiendo que
una búsqueda normal arrojarría los siguientes resultados:
```py
odoo_api.search("sale.order", [("state", "=", "sale")])
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14...]
```

Se puede especificar que sólo se requiere obtener una cantidad máxima
de registros a partir de un número provisto:
```py
odoo_api.search("sale.order", [("state", "=", "sale")], limit=5)
# [1, 2, 3, 4, 5]
```
