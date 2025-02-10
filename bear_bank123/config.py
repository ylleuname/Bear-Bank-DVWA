import os

DB_CONFIG = {
    'host': 'db', # Usa 'db' como host do MySQL seguro
    'user': 'root',
    'password': 'admin',
    'database': 'bear_bank'
}

DB_CONFIG_VULNERABLE = {
    'host': 'db_vulnerable',
    'user': 'root',
    'password': 'admin',
    'database': 'bear_bank_v'
}
