from .._constants import VARIABLE_NAME
from .._core import env

class CREDENTIALS_CONFIG:
    USERNAME = env.variable(VARIABLE_NAME.USERNAME, str, ...)
    TOKEN = env.variable(VARIABLE_NAME.TOKEN, str, ...)
    TOKEN = env.variable(VARIABLE_NAME.TOKEN, str, ...)
    URL = env.variable(VARIABLE_NAME.URL, str, ...)
    DB = env.variable(VARIABLE_NAME.DB, str, ...)
    ALT_DB = env.variable(VARIABLE_NAME.ALT_DB, str, ...)
