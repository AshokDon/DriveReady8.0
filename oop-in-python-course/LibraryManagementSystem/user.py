from abc import ABC, abstractmethod


class User(ABC):
    __id_counter = 0
    __total_users = 0

    def __init__(self, name=None, contact_info=None):
        User.__id_counter += 1
        User.__total_users += 1

        self.__user_id = f"U-{User.__id_counter}"
        self.__name = name
        self.__contact_info = contact_info

    @property
    def user_id(self):
        return self.__user_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def contact_info(self):
        return self.__contact_info

    @contact_info.setter
    def contact_info(self, value):
        self.__contact_info = value

    @classmethod
    def get_total_users(cls):
        return User.__total_users

    @abstractmethod
    def display_dashboard(self):
        pass

    @abstractmethod
    def can_borrow_books(self):
        pass
