## Conexión al API de Odoo
Creador de una conexión con el sistema de Odoo a través del API. Puede ser
a la base de datos principal o a una base de datos de prueba provista en el
archivo `.env`

Instalación:
```bash
pip install git+https://github.com/onnymm/odoo_api_manager.git
```

### Forma de uso:
```py
odoo = OdooAPIManager()
```

Para crear una conexión a la base de datos de prueba, se debe proveer el
valor `True` en el argumento `test_db`:
```py
odoo_test = OdooAPIManager(test_db=True)
```

Para proporcionar los datos de la conexión al API se debe contar con un
archivo `.env` en la raíz del proyecto con la siguiente estructura:

```env
ODOO_USERNAME_API = username_api@example.com
ODOO_CLAVE_API = 1234567890abcdefghijklmnopqrstuvwxyz1234
ODOO_PASSWORD_API = thisisapassword321
ODOO_URL_API = https://your-database-name.odoo.com
ODOO_DB_API = your-database-name
ODOO_DB_PRUEBA_API = your-database-name-test
```

----
## Métodos disponibles
### • Revisión de permisos de acceso
Método para verificar los permisos de acceso a un modelo
especificado:
```py
odoo.check_access_rights("res.partner", "write")
```

### • Búsqueda de registros
Este método realiza una búsqueda en un modelo especificado y retorna
una lista de IDs que cumplen con las condiciones especificadas.
```py
odoo.search("sale.order", [("state", "=", "cancel")])
# [52, 87, 129, 132]
```

### • Lectura de registros
Este método realiza una lectura de IDs en donde retorna una lista
de diccionarios, cada uno, con la información de un registro.
```py
odoo.read("sale.order", [52, 87, 129, 132])
```

```py
[{
    'id': 52,
    'name': 'S00052',
    ...
 },
 {
    'id': 89,
    'name': 'S00089',
    ...
 },
 {
    'id': 129,
    'name': 'S00129',
    ...
 },
 {
    'id': 132,
    'name': 'S00132',
    ...
}]
```

### • Búsqueda y lectura de registros
Este método es la combinación de los métodos internos
`OdooAPIManager.search` y `OdooAPIManager.read` optimizado para la
ejecución de ambos en una misma solicitud al API.
```py
odoo.search_read("sale.order", [("state", "=", "cancel")])
```

```py
[{
    'id': 52,
    'name': 'S00052',
    ...
 },
 {
    'id': 89,
    'name': 'S00089',
    ...
 },
 {
    'id': 129,
    'name': 'S00129',
    ...
 },
 {
    'id': 132,
    'name': 'S00132',
    ...
}]
```

### • Conteo de registros en búsqueda
Este método devuelve el conteo de la cantidad de registros que cumplen
un criterio de búsqueda provisto. Es equivalente a usar la función
`len()` a la lista de retorno del método `OdooAPIManager.search()`:
```py
odoo.search_count("sale.order", [("state", "=", "cancel")])
```

```py
# Respuesta
87
```