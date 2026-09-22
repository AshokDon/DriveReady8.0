# Java OOP & Advanced Concepts

## Tutorial 03 --- Access Modifiers, `final`, Immutability, Copying & Inheritance

------------------------------------------------------------------------

# 1. Access Modifiers

Java provides four levels of access:

  Modifier        Same Class   Same Package   Subclass   Everywhere
  ------------- ------------ -------------- ---------- ------------
  `private`                ✓              ✗          ✗            ✗
  default                  ✓              ✓          ✗            ✗
  `protected`              ✓              ✓          ✓            ✗
  `public`                 ✓              ✓          ✓            ✓

Default means no keyword:

``` java
class Driver {
    String name; // package-private
}
```

For encapsulated entity state, `private` is normally the safest starting
point.

------------------------------------------------------------------------

# 2. Constructor Chaining

Two keywords are important:

``` text
this(...)  -> another constructor in the same class
super(...) -> constructor of the parent class
```

Both must be the first statement of a constructor.

Example:

``` java
class Driver {
    private String id;
    private String name;
    private double rating;

    public Driver(String id) {
        this(id, "Unknown", 0.0);
    }

    public Driver(String id, String name, double rating) {
        this.id = id;
        this.name = name;
        this.rating = rating;
    }
}
```

The first constructor delegates to the second.

------------------------------------------------------------------------

# 3. `final`

`final` has three common meanings.

### Final variable

``` java
private final String driverId;
```

It can be assigned once.

### Final method

``` java
public final String getDriverId() {
    return driverId;
}
```

A subclass cannot override it.

### Final class

``` java
public final class Fare {
}
```

No class can extend it.

Remember:

``` text
final variable -> cannot reassign
final method   -> cannot override
final class    -> cannot extend
```

------------------------------------------------------------------------

# 4. Immutability

An immutable object cannot change after construction.

A typical immutable class:

``` java
public final class Fare {
    private final double amount;
    private final String currency;

    public Fare(double amount, String currency) {
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }

        this.amount = amount;
        this.currency = currency;
    }

    public double getAmount() {
        return amount;
    }

    public String getCurrency() {
        return currency;
    }
}
```

There are:

-   no setters
-   final fields
-   controlled construction
-   no subclassing

Immutable objects are easier to reason about and safer to share.

------------------------------------------------------------------------

# 5. Shallow vs Deep Copy

Suppose:

``` java
class Trip {
    private Fare fare;
    private Route route;
}
```

A shallow copy may copy references:

``` java
this.fare = other.fare;
this.route = other.route;
```

Now both objects point to the same nested objects.

For mutable state, this can create unwanted coupling.

A deep copy creates a new nested object:

``` java
this.route = new Route(other.route);
```

A useful rule:

``` text
Immutable object -> sharing reference is usually safe
Mutable object   -> consider creating a new object
```

------------------------------------------------------------------------

# 6. Copy Constructor

A copy constructor accepts another object of the same type.

``` java
public Trip(Trip other) {
    this.fare = other.fare;          // Fare is immutable
    this.route = new Route(other.route); // Route is mutable
}
```

This gives controlled copying.

------------------------------------------------------------------------

# 7. Inheritance

Inheritance represents an **IS-A** relationship.

``` java
class Vehicle {
    protected String vehicleId;

    public void register() {
        System.out.println("Vehicle registered");
    }
}

class Car extends Vehicle {
    private int seatingCapacity;
}
```

Now:

``` java
Car car = new Car();

car.register();
```

The child inherits accessible behaviour from the parent.

------------------------------------------------------------------------

# 8. `super`

The child constructor can call the parent constructor.

``` java
class Vehicle {
    private String id;

    public Vehicle(String id) {
        this.id = id;
    }
}

class Car extends Vehicle {
    private int seats;

    public Car(String id, int seats) {
        super(id);
        this.seats = seats;
    }
}
```

The parent portion must be initialized before the child portion.

Conceptually:

``` text
new Car(...)
   |
   v
Vehicle constructor
   |
   v
Car constructor body
```

------------------------------------------------------------------------

# 9. `protected`

A `protected` member is accessible:

-   inside the same class
-   inside the same package
-   from subclasses

Example:

``` java
class Vehicle {
    protected String vehicleId;
}
```

A subclass can use it:

``` java
class Car extends Vehicle {
    public void printId() {
        System.out.println(vehicleId);
    }
}
```

Private fields cannot be accessed directly by subclasses.

Use methods when you want controlled access:

``` java
class Vehicle {
    private String vehicleId;

    protected String getVehicleId() {
        return vehicleId;
    }
}
```

------------------------------------------------------------------------

# 10. The `Object` Class

Every Java class ultimately extends `Object`.

Important methods include:

``` java
toString()
equals()
hashCode()
```

### `equals()`

Used for logical equality.

``` java
@Override
public boolean equals(Object obj) {
    if (this == obj) return true;
    if (!(obj instanceof Driver)) return false;

    Driver other = (Driver) obj;
    return driverId.equals(other.driverId);
}
```

### `hashCode()`

If two objects are equal according to `equals()`, they must have the
same hash code.

``` java
@Override
public int hashCode() {
    return driverId.hashCode();
}
```

This matters heavily for:

``` text
HashSet
HashMap
HashTable-like structures
```

------------------------------------------------------------------------

# 11. Inheritance Design Rule

Inheritance is useful when the child truly is a specialized version of
the parent.

``` text
Vehicle
  |
  +-- Car
  +-- Bike
  +-- Auto
```

Do not use inheritance simply to reuse a few methods.

That problem is better addressed with composition.

------------------------------------------------------------------------

## Key Takeaways

-   Use access modifiers to control visibility.
-   `this(...)` chains constructors in the same class.
-   `super(...)` invokes a parent constructor.
-   `final` can lock variables, methods, or classes.
-   Immutable objects are safe to share.
-   Copy mutable nested objects when independent state is required.
-   Inheritance models IS-A relationships.
-   Every Java class ultimately inherits from `Object`.
-   Override `equals()` and `hashCode()` together.

## Practice

Build:

``` text
Vehicle
  |
  +-- Car
  +-- Bike
  +-- Auto
```

Add:

-   parent constructor
-   child constructors
-   `protected` access
-   `toString()`
-   `equals()`
-   `hashCode()`
