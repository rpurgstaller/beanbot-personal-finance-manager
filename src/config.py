class Config:
    DEBUG = False
    TEST = False
    DB_FILENAME = ""

class TestConfig(Config):
    DEBUG = True
    TEST = True
    DB_FILENAME = "test.db"

class DevConfig(Config):
    DEBUG = True
    TEST = False
    DB_FILENAME = "dev.db"

class ProductionConfig(Config):
    DEBUG = True
    TEST = False
    DB_FILENAME = "model.db"

config_by_name = dict(
    test=TestConfig,
    dev=DevConfig,
    prod=ProductionConfig
)