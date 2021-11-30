class BaseConfig(object):
    """Baseconfig

    Parameters
    ----------
    object : [type]
        [description]
    """
    SECRET_KEY = 'Key'
    DEBUG = True
    TESTING = False
class ProductionConfig(BaseConfig):
    'Produccion configuracion'
    DEBUG = False
class DevelopmentConfig(BaseConfig):
    'Desarrollo configuracion'
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'Desarrollo key'