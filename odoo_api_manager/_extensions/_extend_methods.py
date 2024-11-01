from odoo_api_manager._base_extension import APIManagerExtension

class ExtendMethods(APIManagerExtension):

    def _initialize_modules(self):
        if len(self._instance._registered_modules) > 0:
            print("Se inicializa")
            for module in self._instance._registered_modules:
                setattr(
                    self._instance,
                    module["name"],
                    module["declaration"](self._instance)
                )
