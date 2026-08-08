from abc import ABC, abstractmethod


class Lendable(ABC):

    @abstractmethod
    def lend(self, user):
        pass

    @abstractmethod
    def return_item(self, user):
        pass

    @abstractmethod
    def is_available(self):
        pass
