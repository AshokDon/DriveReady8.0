from abc import ABC, abstractmethod


class DatabaseConnection:
    """Dummy database connection."""

    def __init__(self, connection_id):
        self.connection_id = connection_id


class ConnectionPool(ABC):

    @abstractmethod
    def initialize_pool(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def release_connection(self, connection):
        pass

    @abstractmethod
    def get_available_connections_count(self):
        pass

    @abstractmethod
    def get_total_connections_count(self):
        pass
