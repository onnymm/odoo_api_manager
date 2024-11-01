from odoo_api_manager._base_api_manager import APIManager

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
            APIManager._registered_modules.append(
                {
                    "name": module_name,
                    "declaration": module
                }
            )

        return register_new_module