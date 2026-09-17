from abc import ABC, abstractmethod
from enum import Enum


class LogLevel(Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Logger(ABC):

    @abstractmethod
    def log(self, level, message):
        pass

    @abstractmethod
    def set_log_file(self, file_path):
        pass

    @abstractmethod
    def get_log_file(self):
        pass

    @abstractmethod
    def flush(self):
        pass

    @abstractmethod
    def close(self):
        pass
