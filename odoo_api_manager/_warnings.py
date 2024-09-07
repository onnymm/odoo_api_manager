import warnings

def deprecated(new_method):

    def deprecation_warning(callback):
        warning_text = (
            f"\nEl método {callback.__name__} está obsoleto y será removido en futuras versiones.\n"
            f"El nuevo método disponible es 'OdooAPIManager.{new_method.__name__}'.\n"
        )

        def wrapper(*args, **kwargs):
            warnings.warn(
                warning_text,
                category = DeprecationWarning,
                stacklevel= 2
            )

            return callback(*args, **kwargs)
        
        return wrapper
    
    return deprecation_warning
