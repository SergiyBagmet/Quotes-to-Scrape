from functools import wraps
from mongoengine import connect, disconnect
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure, OperationFailure, ConfigurationError


def mongo_connection(db_uri: str, db_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                connect(db=db_name, host=db_uri, alias='default')
                return func(*args, **kwargs)
            except ServerSelectionTimeoutError:
                print("Server selection timed out.")
            except ConnectionFailure:
                print("Failed to connect to the server.")
            except OperationFailure as e:
                print(f"Operation failed: {e}")
            except ConfigurationError as e:
                print(f"Configuration error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            finally:
                disconnect(alias='default')

        return wrapper

    return decorator
