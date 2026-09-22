# Java OOP & Advanced Concepts

## Tutorial 05 --- OOP Lab: Library Management System

> Source: HackMD OOP-4 Lab\
> https://hackmd.io/@7ZhgEFzKSUeDhAQFDVj8mw/rJgHH0GpMze

------------------------------------------------------------------------

# 1. Goal

This lab combines the OOP concepts from the previous tutorials into one
system:

``` text
Abstraction
Encapsulation
Inheritance
Polymorphism
Interfaces
Composition
static
final
Constructor overloading
Constructor chaining
```

The domain is a Library Management System.

------------------------------------------------------------------------

# 2. Identify the Entities

A useful first model:

``` text
User
  |
  +-- Member
  +-- Librarian

Book
  |
  +-- PrintedBook
  +-- EBook

LibraryManagementSystem
  |
  +-- users
  +-- books
```

A book also has a lending capability.

``` java
interface Lendable {
    boolean lend(User user);
    void returnItem();
    boolean isAvailable();
}
```

------------------------------------------------------------------------

# 3. Abstract `User`

``` java
public abstract class User {

    private final String userId;
    private final String name;

    public User(String userId, String name) {
        this.userId = userId;
        this.name = name;
    }

    public String getUserId() {
        return userId;
    }

    public String getName() {
        return name;
    }

    public abstract boolean canBorrowBooks();
}
```

The common state belongs in the parent.

The rule that differs belongs in subclasses.

------------------------------------------------------------------------

# 4. Member and Librarian

``` java
public class Member extends User {

    private int borrowedBooks;

    public Member(String userId, String name) {
        super(userId, name);
    }

    @Override
    public boolean canBorrowBooks() {
        return borrowedBooks < 5;
    }

    public void incrementBorrowCount() {
        borrowedBooks++;
    }
}
```

Librarian:

``` java
public class Librarian extends User {

    public Librarian(String userId, String name) {
        super(userId, name);
    }

    @Override
    public boolean canBorrowBooks() {
        return true;
    }
}
```

One method call:

``` java
user.canBorrowBooks();
```

can produce different results depending on the actual object.

That is runtime polymorphism.

------------------------------------------------------------------------

# 5. `Book` as an Abstract Class

``` java
public abstract class Book implements Lendable {

    private final String isbn;
    private final String title;
    private User borrowedBy;

    public Book(String isbn, String title) {
        this.isbn = isbn;
        this.title = title;
    }

    @Override
    public boolean isAvailable() {
        return borrowedBy == null;
    }

    @Override
    public boolean lend(User user) {
        if (!isAvailable()) {
            return false;
        }

        if (!user.canBorrowBooks()) {
            return false;
        }

        borrowedBy = user;
        return true;
    }

    @Override
    public void returnItem() {
        borrowedBy = null;
    }
}
```

The book controls its own availability.

That is encapsulation.

------------------------------------------------------------------------

# 6. Library Management Service

The system class coordinates objects rather than directly modifying
their internals.

``` java
public boolean lendBook(Member member, Book book) {
    if (book.lend(member)) {
        member.incrementBorrowCount();
        return true;
    }

    return false;
}
```

Notice:

``` text
Library -> coordinates
Book    -> owns lending state
Member  -> owns borrowing count
```

This is good responsibility assignment.

------------------------------------------------------------------------

# 7. `static` Class-Level State

Suppose the application wants to know how many users have been created.

``` java
public abstract class User {

    private static int totalUsers = 0;

    public User(String userId, String name) {
        this.userId = userId;
        this.name = name;
        totalUsers++;
    }

    public static int getTotalUsers() {
        return totalUsers;
    }
}
```

Call:

``` java
System.out.println(User.getTotalUsers());
```

The value belongs to the class, not one user.

------------------------------------------------------------------------

# 8. `final` State

A user ID should normally not change.

``` java
private final String userId;
```

It is assigned in the constructor and cannot be reassigned later.

------------------------------------------------------------------------

# 9. Avoid `instanceof` When Polymorphism Fits

Bad:

``` java
if (user instanceof Member) {
    // ...
} else if (user instanceof Librarian) {
    // ...
}
```

Prefer:

``` java
user.canBorrowBooks();
```

and let each subclass implement the rule.

This keeps the caller independent of concrete types.

------------------------------------------------------------------------

# 10. Overloading

Search can support multiple forms:

``` java
public List<Book> searchBooks(String criteria) {
    // ...
}

public List<Book> searchBooks(String criteria, String type) {
    // ...
}
```

This is compile-time polymorphism.

------------------------------------------------------------------------

# 11. Interfaces

`Lendable` represents a capability.

``` java
public interface Lendable {
    boolean lend(User user);
    void returnItem();
    boolean isAvailable();
}
```

Anything that can be borrowed can implement it.

The interface describes **what** is possible, not the internal
implementation.

------------------------------------------------------------------------

# 12. Full Design

``` text
                 User (abstract)
                  /          \
             Member        Librarian
                |
                | uses
                v
             Book (abstract)
                |
        +-------+--------+
        |                |
 PrintedBook          EBook
        |
     Lendable
```

The management system coordinates these objects.

------------------------------------------------------------------------

## Design Checklist

Before coding:

``` text
[ ] Identify entities
[ ] Assign state ownership
[ ] Assign behaviour ownership
[ ] Decide IS-A relationships
[ ] Decide HAS-A relationships
[ ] Identify capabilities
[ ] Use interfaces where appropriate
[ ] Protect mutable state
[ ] Use polymorphism instead of type checks
```

------------------------------------------------------------------------

## Practice

Extend the system with:

1.  `ReferenceBook` that cannot be borrowed.
2.  `Notifiable` interface.
3.  Email notification for overdue books.
4.  Search by author.
5.  Search by ISBN.
6.  A copy constructor for `Book`-related state where meaningful.
