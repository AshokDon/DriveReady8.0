# Java OOP & Advanced Concepts

## Tutorial 02 --- Classes, Objects, Constructors, References & Encapsulation

> Source: HackMD Lecture 2\
> https://hackmd.io/@7ZhgEFzKSUeDhAQFDVj8mw/Byizj2MzMe

------------------------------------------------------------------------

## 1. Abstraction: Principle vs Java Keyword

A useful way to think about OOP is:

``` text
Abstraction = represent a complex system using simpler concepts.
```

The three major mechanisms used to achieve this are:

``` text
Encapsulation  -> protects state
Inheritance    -> shares structure
Polymorphism   -> enables flexibility
```

Do not confuse the **abstraction principle** with Java's `abstract`
keyword. The keyword is one implementation mechanism; abstraction itself
is a broader design idea.

------------------------------------------------------------------------

# 2. Class vs Object

A class is a blueprint.

``` java
class Driver {
    String name;
    double rating;

    void acceptRide() {
        System.out.println("Ride accepted");
    }
}
```

An object is a real instance of that class.

``` java
Driver d1 = new Driver();
Driver d2 = new Driver();
```

Think:

``` text
Class
  |
  +---- object d1
  |
  +---- object d2
  |
  +---- object d3
```

Each object has its own instance state.

------------------------------------------------------------------------

# 3. Fields and Methods

A class contains members.

### Fields

Represent state.

``` java
class Driver {
    private String name;
    private double rating;
}
```

### Methods

Represent behaviour.

``` java
class Driver {
    public void acceptRide() {
        System.out.println("Ride accepted");
    }
}
```

The design goal is:

``` text
Data + behaviour that belongs to that data
```

------------------------------------------------------------------------

# 4. References and the Heap

Consider:

``` java
Driver d1 = new Driver("D001");
Driver d2 = d1;
```

There is only **one object**.

``` text
Stack                         Heap

d1 -----------------------> Driver Object
                              id = D001
d2 ----------------------->  same object
```

Changing through `d2` changes what `d1` observes.

``` java
d2.setName("Rahul");

System.out.println(d1.getName());
// Rahul
```

The number of objects is determined by `new`, not by the number of
reference variables.

------------------------------------------------------------------------

# 5. Stack and Heap

A simplified mental model:

``` text
Stack
--------------------------------
method frame
local variables
references
--------------------------------

Heap
--------------------------------
Driver object
Trip object
Payment object
--------------------------------
```

A local reference can disappear when a method returns while the heap
object may continue to exist as long as another reference points to it.

------------------------------------------------------------------------

# 6. Constructors

A constructor initializes an object.

Rules:

-   constructor name = class name
-   no return type
-   runs when `new` is used

``` java
class Driver {
    private String id;
    private String name;

    public Driver(String id, String name) {
        this.id = id;
        this.name = name;
    }
}
```

Usage:

``` java
Driver d = new Driver("D001", "Rahul");
```

------------------------------------------------------------------------

# 7. The `this` Keyword

`this` refers to the current object.

``` java
class Driver {
    private String name;

    public Driver(String name) {
        this.name = name;
    }
}
```

Here:

``` text
name       -> constructor parameter
this.name  -> object's field
```

Without `this`, the names can become ambiguous.

------------------------------------------------------------------------

# 8. Constructor Overloading

Multiple constructors can initialize objects in different ways.

``` java
class Driver {
    private String id;
    private String name;
    private double rating;

    public Driver() {
        this("UNKNOWN", "UNKNOWN", 0.0);
    }

    public Driver(String id, String name) {
        this(id, name, 0.0);
    }

    public Driver(String id, String name, double rating) {
        this.id = id;
        this.name = name;
        this.rating = rating;
    }
}
```

This avoids repeated initialization logic.

------------------------------------------------------------------------

# 9. `static`

Instance fields belong to objects.

``` java
class Driver {
    private String name;
}
```

A static field belongs to the class.

``` java
class Driver {
    private static int totalDrivers = 0;

    public Driver() {
        totalDrivers++;
    }

    public static int getTotalDrivers() {
        return totalDrivers;
    }
}
```

Usage:

``` java
Driver d1 = new Driver();
Driver d2 = new Driver();

System.out.println(Driver.getTotalDrivers());
// 2
```

Mental model:

``` text
instance field -> one copy per object

static field   -> one copy shared by the class
```

------------------------------------------------------------------------

# 10. Java Is Pass-by-Value

Java always passes arguments by value.

For primitives:

``` java
static void change(int x) {
    x = 100;
}

int a = 10;
change(a);

System.out.println(a);
// 10
```

The method receives a copy of `10`.

For objects, Java copies the **reference value**.

``` java
static void changeName(Driver d) {
    d.setName("Changed");
}
```

Both references can point to the same object.

However:

``` java
static void reassign(Driver d) {
    d = new Driver("D2", "Other");
}
```

does not change the caller's reference.

------------------------------------------------------------------------

# 11. `toString()`

Every Java class ultimately inherits from `Object`.

Without overriding `toString()`:

``` java
System.out.println(driver);
```

typically produces a class name plus an identity-style value.

A useful override is:

``` java
@Override
public String toString() {
    return "Driver{id='" + id + "', name='" + name + "'}";
}
```

Now:

``` java
System.out.println(driver);
```

prints meaningful information.

------------------------------------------------------------------------

# 12. Encapsulation

Encapsulation means:

> Keep state and behaviour together and control direct access to the
> state.

Bad:

``` java
class Driver {
    public double rating;
}
```

Any code can do:

``` java
driver.rating = -500;
```

Better:

``` java
class Driver {
    private double rating;

    public void updateRating(double rating) {
        if (rating < 0 || rating > 5) {
            throw new IllegalArgumentException("Invalid rating");
        }

        this.rating = rating;
    }

    public double getRating() {
        return rating;
    }
}
```

Now the class protects its own invariant.

------------------------------------------------------------------------

# 13. Getter Does Not Mean "Expose Everything"

A getter can transform data.

``` java
public String getMaskedPhone() {
    return phone.substring(0, 3)
            + "XXXXX"
            + phone.substring(8);
}
```

Also, not every field needs a setter.

For read-only state:

``` java
private final String driverId;

public String getDriverId() {
    return driverId;
}
```

------------------------------------------------------------------------

## Key Takeaways

-   Class = blueprint.
-   Object = instance.
-   References point to objects.
-   `this` means the current object.
-   Constructors establish valid initial state.
-   `static` represents class-level state/behaviour.
-   Java is always pass-by-value.
-   `toString()` provides useful object representation.
-   Encapsulation protects state and enforces rules.

## Practice

Create a `BankAccount` class with:

``` text
accountNumber
ownerName
balance
```

Implement:

``` text
deposit()
withdraw()
getBalance()
toString()
```

Do not allow invalid withdrawals or direct modification of `balance`.
