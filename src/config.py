import configparser
from pathlib import Path

file_config = Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')
retry_writes = config.get('DB', 'RETRY_WRITES')
ssl = config.get('DB', 'SSL')

mongo_uri = (
    f"mongodb+srv://{username}:{password}@{domain}/{db_name}"
    f"?retryWrites={retry_writes}&w=majority&ssl={ssl}"
)
