import json


class Config:

    DB_FILENAME = None

    GIRO = None

    def build(mode):
        cfg = json.load()
        
        assert mode in ["DEV", "TEST", "PROD"], f"Mode \"{mode}\" is invalid"
        assert "DATABASE_FILENAMES" in cfg, "Database configuration missing"
        assert "GIRO" in cfg, "Giro configuration missing"
        assert "ACCOUNT_KEY" in cfg["GIRO"], "Account key for giro configuration missing"
        assert "TRANSACTION_MAPPING" in cfg["GIRO"], "Transaction mapping for giro configuration missing"

        Config.DB_FILENAME = cfg["DATABASE_FILENAMES"][mode]
        Config.GIRO = cfg["GIRO"]