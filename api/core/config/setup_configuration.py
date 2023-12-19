from .config import ProductionConfig, DevelopmentConfig, TestConfig

def setup_configuration(env: str) -> object:
    
    if env == 'production':
        config_class = ProductionConfig
    elif env == 'test':
        config_class = TestConfig
    elif env == 'development':
        config_class = DevelopmentConfig
    else:
        None

    return config_class
