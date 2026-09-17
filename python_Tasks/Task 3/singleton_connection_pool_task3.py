import threading

from connection_pool import ConnectionPool, DatabaseConnection


class ConnectionPoolImpl(ConnectionPool):

    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, max_connections):
        # TODO:
        # Implement Singleton creation.
        # Remember that get_instance() receives max_connections.
        pass

    def __init__(self, max_connections):
        # TODO:
        # Initialize the pool only once.
        #
        # You will need:
        # - maximum number of connections
        # - available connections
        # - connections currently in use
        # - a lock for pool operations
        pass

    @classmethod
    def get_instance(cls, max_connections):
        # TODO:
        # Return the Singleton instance.
        pass

    @classmethod
    def reset_instance(cls):
        # TODO:
        # Reset the Singleton instance.
        pass

    def initialize_pool(self):
        # TODO:
        # Create max_connections DatabaseConnection objects
        # and place them into the available pool.
        pass

    def get_connection(self):
        # TODO:
        # 1. Make the operation thread-safe.
        # 2. Get an available connection.
        # 3. Move it to the in-use collection.
        # 4. Return it.
        pass

    def release_connection(self, connection):
        # TODO:
        # 1. Make the operation thread-safe.
        # 2. Move the connection from in-use to available.
        pass

    def get_available_connections_count(self):
        # TODO:
        pass

    def get_total_connections_count(self):
        # TODO:
        pass
