import configparser
from pathlib import Path

import pika
import redis


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
    f"mongodb+srv://{username}:{password}@{domain}/"
    f"?retryWrites={retry_writes}&w=majority&ssl={ssl}"
)


redis_host = config.get('REDIS', 'HOST')
redis_port = config.getint('REDIS', 'PORT')
redis_password = config.get('REDIS', 'PASSWORD', fallback=None)

client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)


host_rmq = config.get('rabbitmq', 'host')
port_rmq = config.getint('rabbitmq', 'port')
username_rmq = config.get('rabbitmq', 'username')
password_rmq = config.get('rabbitmq', 'password')




