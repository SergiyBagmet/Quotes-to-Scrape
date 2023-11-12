from functools import wraps
from mongoengine import connect, disconnect
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure, OperationFailure, ConfigurationError


class MongoDBError(Exception):
    pass


class MongoDBConnection:
    def __init__(self, db_uri: str, ):
        self.db_uri = db_uri

    def __call__(self, db_name: str):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    connect(db=db_name, host=self.db_uri, alias='default')
                    func(*args, **kwargs)
                except ServerSelectionTimeoutError:
                    raise MongoDBError("Server selection timed out.")
                except ConnectionFailure:
                    raise MongoDBError("Failed to connect to the server.")
                except OperationFailure as e:
                    raise MongoDBError(f"Operation failed: {e}")
                except ConfigurationError as e:
                    raise MongoDBError(f"Configuration error: {e}")
                except Exception as e:
                    raise MongoDBError(f"[{type(e).__name__}]An unexpected error occurred: {e}")
                finally:
                    disconnect(alias='default')

            return wrapper

        return decorator
