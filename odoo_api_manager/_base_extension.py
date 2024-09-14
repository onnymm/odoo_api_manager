from ._base_api_manager import APIManager

class APIManagerExtension():
    """
    ## Clase base para módulo de extensión
    Esta clase base se utiliza como el punto de partida para la creación de
    módulos de extensión de la librería `OdooAPIManager`.
    """

    def __init__(self, instance: APIManager):
        self._instance = instance