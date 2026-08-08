from abc import ABC, abstractmethod


class Book(Lendable):

    def __init__(self, isbn=None, title=None, author=None):
        self.__isbn = isbn
        self.__title = title
        self.__author = author
        self.__is_available = True

    def lend(self, user):
        if self.__is_available and user.can_borrow_books():
            self.__is_available = False
            return True

        return False

    def return_item(self, user):
        self.__is_available = True

    def is_available(self):
        return self.__is_available

    @property
    def isbn(self):
        return self.__isbn

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    @abstractmethod
    def display_book_details(self):
        pass
