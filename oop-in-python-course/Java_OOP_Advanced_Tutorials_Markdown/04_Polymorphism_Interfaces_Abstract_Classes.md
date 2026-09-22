# Java OOP & Advanced Concepts

## Tutorial 04 --- Polymorphism, Abstract Classes, Interfaces & Composition

> Source: HackMD Lecture 4\
> https://hackmd.io/@7ZhgEFzKSUeDhAQFDVj8mw/Bk0Qmcqzfl

------------------------------------------------------------------------

# 1. Polymorphism

Polymorphism means:

> One interface, many forms.

There are two major forms in Java:

``` text
Compile-time polymorphism -> overloading
Runtime polymorphism      -> overriding
```

------------------------------------------------------------------------

# 2. Runtime Polymorphism

Consider:

``` java
abstract class Vehicle {
    public abstract double getBaseRate();

    public double calculateFare(double km) {
        return km * getBaseRate();
    }
}

class Car extends Vehicle {
    @Override
    public double getBaseRate() {
        return 12.0;
    }
}

class Bike extends Vehicle {
    @Override
    public double getBaseRate() {
        return 5.0;
    }
}
```

Now:

``` java
List<Vehicle> fleet = new ArrayList<>();

fleet.add(new Car());
fleet.add(new Bike());

for (Vehicle vehicle : fleet) {
    System.out.println(vehicle.calculateFare(10));
}
```

The reference type is `Vehicle`, but the actual object may be `Car` or
`Bike`.

``` text
Reference type -> what methods can be called
Actual type    -> which overridden implementation runs
```

------------------------------------------------------------------------

# 3. Why `@Override` Matters

This is dangerous:

``` java
public double calculatFare(double km) {
    return km * 12;
}
```

A typo creates a new method instead of overriding the parent method.

Use:

``` java
@Override
public double calculateFare(double km) {
    return km * 12;
}
```

Now the compiler verifies your intention.

Rule:

> If you intend to override a method, always write `@Override`.

------------------------------------------------------------------------

# 4. Rules for Overriding

An overriding method must have:

-   same name
-   same parameter list
-   compatible return type
-   same or wider access
-   child-parent relationship

You cannot do:

``` java
class Child extends Parent {
    @Override
    private void process() {
    }
}
```

if the parent method was `public`.

You cannot reduce accessibility.

------------------------------------------------------------------------

# 5. Compile-Time Polymorphism: Overloading

Overloading means same method name but different parameter lists.

``` java
class CabBookingService {

    Ride bookRide(String pickup, String drop) {
        return new Ride();
    }

    Ride bookRide(String pickup, String drop, Date time) {
        return new Ride();
    }

    Ride bookRide(
            String pickup,
            String drop,
            Date time,
            String coupon) {
        return new Ride();
    }
}
```

The compiler selects the method based on the arguments.

Valid differences:

``` text
number of parameters
parameter types
order of parameter types
```

Not valid:

``` text
return type only
parameter variable names only
access modifier only
```

------------------------------------------------------------------------

# 6. Abstract Classes

An abstract class represents an incomplete/general concept.

``` java
public abstract class Vehicle {

    private String vehicleId;

    public Vehicle(String vehicleId) {
        this.vehicleId = vehicleId;
    }

    public abstract double getBaseRate();

    public double calculateFare(double km) {
        return km * getBaseRate();
    }
}
```

You cannot do:

``` java
Vehicle v = new Vehicle("V001"); // compile error
```

But you can do:

``` java
Vehicle v = new Car("V001");
```

An abstract class can contain:

-   fields
-   constructors
-   concrete methods
-   abstract methods

------------------------------------------------------------------------

# 7. Abstract Methods Create Obligations

If:

``` java
public abstract double getBaseRate();
```

then every concrete subclass must implement it.

``` java
class Car extends Vehicle {
    @Override
    public double getBaseRate() {
        return 12.0;
    }
}
```

This is stronger than a comment saying:

``` text
"Children should implement getBaseRate()."
```

The compiler enforces the rule.

------------------------------------------------------------------------

# 8. Interfaces

An interface represents a capability or contract.

``` java
public interface PaymentGateway {
    void pay(double amount);
}
```

Implementations:

``` java
class RazorpayGateway implements PaymentGateway {
    @Override
    public void pay(double amount) {
        System.out.println("Razorpay payment");
    }
}

class UpiGateway implements PaymentGateway {
    @Override
    public void pay(double amount) {
        System.out.println("UPI payment");
    }
}
```

The service depends on the contract:

``` java
class PaymentService {
    private final PaymentGateway gateway;

    public PaymentService(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    public void process(double amount) {
        gateway.pay(amount);
    }
}
```

Now:

``` java
PaymentService service =
        new PaymentService(new RazorpayGateway());

service.process(1000);
```

Changing the provider does not require changing `PaymentService`.

------------------------------------------------------------------------

# 9. Abstract Class vs Interface

Use an abstract class when the relationship is:

``` textis-a
```

Example:

`textCar IS A Vehicle`

Use an interface when the relationship is:

``` textcan-do
```

Example:

`textDriver CAN BE DISPATCHED RazorpayGateway CAN PROCESS PAYMENTS`

Quick comparison:

  Abstract Class      Interface
  ------------------- --------------------
  shared identity     shared capability
  can contain state   primarily contract
  has constructors    no constructors
  one parent class    many interfaces
  `extends`           `implements`

------------------------------------------------------------------------

# 10. Composition vs Inheritance

Suppose:

``` java
class Driver extends Person {
}
```

The IS-A relationship may be technically true.

But inheritance gives `Driver` everything `Person` has.

If `Person` later gains:

``` java
retire()
getMarried()
payTaxes()
applyForVisa()
```

the `Driver` class inherits those too.

Composition is more selective:

``` java
class Driver {
    private Person person;
    private Vehicle vehicle;
    private DriverLicense license;
}
```

Now:

``` text
Driver HAS A Person
Driver HAS A Vehicle
Driver HAS A DriverLicense
```

The driver uses only what it needs.

------------------------------------------------------------------------

# 11. Three-Question Heuristic

When deciding a relationship, ask in order:

``` text
IS A TYPE OF?
    |
    +--> extends / abstract class

CAN DO?
    |
    +--> implements / interface

HAS A?
    |
    +--> field / composition
```

Examples:

``` text
Car IS A Vehicle        -> extends
Driver CAN BE dispatched -> implements
Trip HAS A Fare         -> field
Driver HAS A Person     -> field
```

When inheritance and composition are both possible, composition often
creates less coupling.

------------------------------------------------------------------------

# 12. Complete OOP Picture

``` text
User (abstract)
 |
 +-- Driver
 |
 +-- Rider

Vehicle (abstract)
 |
 +-- Car
 +-- Bike
 +-- Auto

PaymentGateway (interface)
 |
 +-- RazorpayGateway
 +-- UpiGateway

Driver implements Dispatchable
```

These structures combine:

``` text
Encapsulation -> protects state
Inheritance   -> shares structure
Polymorphism  -> enables flexibility
Interfaces    -> define capabilities
Composition   -> controls dependencies
```

------------------------------------------------------------------------

## Practice

Build a payment system:

``` text
PaymentGateway
  |
  +-- RazorpayGateway
  +-- PaytmGateway
  +-- UpiGateway
```

Then write:

``` java
PaymentService
```

that depends only on `PaymentGateway`.

Add a new gateway without modifying `PaymentService`.
