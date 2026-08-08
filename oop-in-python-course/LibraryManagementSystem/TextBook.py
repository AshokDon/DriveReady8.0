class TextBook(Book):

    def __init__(self, isbn, title, author, subject, edition):
        super().__init__(isbn, title, author)

        self.__subject = subject
        self.__edition = edition

    def display_book_details(self):
        print(
            f"TextBook | Title: {self.title}"
            f" | Author: {self.author}"
            f" | Subject: {self.__subject}"
            f" | Edition: {self.__edition}"
        )
