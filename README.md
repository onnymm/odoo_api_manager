## Conexión al API de Odoo
Creador de una conexión con el sistema de Odoo a través del API. Puede ser a la base de datos principal o a una base de datos de prueba provista en el archivo `.env`

Instalación:
```bash
pip install git+https://github.com/onnymm/odoo_api_manager.git
```

Forma de uso:
```py
odoo = OdooAPIManager()
```

Para crear una conexión a una base de datos de prueba o una base de datos alternativa, se debe proveer el valor `True` (En caso de haberse declarado una base de datos alternativa en el archivo `env.`) o el nombre de la base de datos alternativa en el argumento `alt_db`:
```py
odoo_test = OdooAPIManager(test_db=True)
```


Para proporcionar los datos de la conexión al API se debe contar con un archivo `.env` en la raíz del proyecto con la siguiente estructura:

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
```py
odoo.check_access_rights('res.partner', 'write')
```

Permisos disponibles
- `create`: Permiso de creación
- `read`: Permiso de lectura
- `write`: Permiso de lectura
- `unlink`: Permiso de eliminación

----
## Creación de registro
Este método permite crear un registro en un modelo de Odoo y retorna la ID de su registro.

Ejemplo de uso:
```py
partner_id = odoo.create('res.partner', {'name': 'Nombre de un cliente'})
# 32
```

### Estructura de los datos
Las llaves deben ser el nombre exacto del campo en el modelo de Odoo, en donde se desea realizar el registro. Por ejemplo, el modelo `res.partner` contiene un campo llamado `name` que es el nombre del cliente.
```py
{'name': 'Nombre de un cliente'}
```

----
## Búsqueda de registros
Este método realiza una búsqueda en un modelo especificado y retorna
una lista de IDs que cumplen con las condiciones especificadas.

Ejemplo de uso:
```py
odoo.search("sale.order", [("state", "=", "cancel")])
# [52, 87, 129, 132]
```

### Condición de búsqueda
Se provee al menos una tupla con la siguiente escructura:
```py
("nombre_del_campo", "=", "valor")
```

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

Los valores pueden ser de tipo `str`, `int`, `float` o `bool`
dependiendo del tipo de valor del campo.

----
## Lectura de registros
Este método realiza una lectura de IDs en donde retorna una lista
de diccionarios, cada uno, con la información de un registro.

Ejemplo de uso:
```py
odoo.read("sale.order", [52, 87, 129, 132])
#     id    name ...
# 0   52  S00052 ...
# 1   89  S00089 ...
# 2  129  S00129 ...
# 3  132  S00132 ...

odoo.read("sale.order", [52, 87, 129, 132], output='dict')
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
```

----
## Búsqueda y lectura de registros
Este método es la combinación de los métodos internos
`OdooAPIManager.search` y `OdooAPIManager.read` optimizado para la
ejecución de ambos en una misma solicitud al API.

Ejemplo de uso:
```py
odoo.read("sale.order", [52, 87, 129, 132])
#     id    name ...
# 0   52  S00052 ...
# 1   89  S00089 ...
# 2  129  S00129 ...
# 3  132  S00132 ...

odoo.read("sale.order", [52, 87, 129, 132], output='dict')
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
```

----
## Conteo de una búsqueda
Este método retorna el conteo de la cantidad de registros que cumplen
un criterio de búsqueda provisto. Es equivalente a usar la función
`len()` a la lista de retorno del método `OdooAPIManager.search()`:
```py
len(odoo.search("sale.order", [("state", "=", "cancel")]))
```

Ejemplo de uso:
```py
odoo.search_count("sale.order", [("state", "=", "cancel")])
# 87
```

### Condición de búsqueda
Se provee al menos una tupla con la siguiente escructura:
```py
("nombre_del_campo", "=", "valor")
```

Todo esto se encierra dentro de una lista:
```py
[("nombre_del_campo", "=", "valor")]
```

----
## Actualización de registros
Este método permite actualizar uno o varios registros en el modelo
especificado de Odoo.

Ejemplo de uso:
```py
odoo.write("sale.order", 52, {"state": "cancel"})
# True

odoo.write("res.partner", 45, {"name": "Nuevo Nombre", "phone": "123456789"})
# True
```

Múltiples registros pueden ser actualizados simultáneamente pero todos
éstos obtendrán el mismo valor para todos los campos declarados.
```py
odoo.write("sale.order", [52, 87, 129], {"state": "done"})
# True
```

----
## Eliminación de registros
Este método permite eliminar uno o varios registros en el modelo
especificado de Odoo. Es importante mencionar que ciertos registros en
ciertos modelos no pueden ser eliminados directamente debido a su uso
en otros modelos o por contener ciertos vínculos como un documento
fiscal, etc..

Ejemplo de uso:
```py
odoo.unlink("sale.order", 52)
# True

odoo.unlink("sale.order", [52, 87, 129])
# True
```

----
## Obtener información de los campos de un modelo
Este método retorna la información más relevante de los campos, en 
formato, de un modelo especificado en la función. Todos los modelos
están disponibles para su consulta.

uso:
```py
odoo.data.model_fields("sale.order")
#         id                       name ...     ttype        relation
# 0     9931               access_token ...      char           False
# 1     9930                 access_url ...      char           False
# 2     9932             access_warning ...      text           False
# ...    ...                        ... ...       ...             ...
#         id                       name ...     ttype        relation
# 127   9993                 write_date ...  datetime           False
# 128   9992                  write_uid ...  many2one       res.users
```

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
```py
odoo.session_info()
# base de datos: your-database-name
# url de origen: https://your-database-name.odoo.com
# usuario: username_api@example.com
# token: ****************************************
```