class Librarian(User):

    def __init__(self, name, contact_info, employee_number):
        super().__init__(name, contact_info)
        self.__employee_number = employee_number

    def display_dashboard(self):
        print("--- Librarian Dashboard ---")
        print(f"Name: {self.name}")
        print(f"Employee #: {self.__employee_number}")

    def can_borrow_books(self):
        # Librarians have unrestricted borrowing access
        return True

    def add_new_book(self, book):
        # Implementation later
        pass

    def remove_book(self, book):
        # Implementation later
        pass
