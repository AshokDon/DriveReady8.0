class NovelBook(Book):

    def __init__(self, isbn, title, author, genre):
        super().__init__(isbn, title, author)
        self.__genre = genre

    def display_book_details(self):
        print(
            f"NovelBook | Title: {self.title}"
            f" | Author: {self.author}"
            f" | Genre: {self.__genre}"
        )
