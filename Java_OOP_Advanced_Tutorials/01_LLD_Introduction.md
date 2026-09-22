# Java OOP & Advanced Concepts

## Tutorial 01 --- Introduction to LLD, OOP Thinking & Entities

------------------------------------------------------------------------

## 1. What Is Low-Level Design?

Software design works at different levels of detail.

### High-Level Design (HLD)

HLD answers:

-   What components should exist?
-   How do those components communicate?
-   Where should data live?
-   How should the system scale?

Typical HLD components:

``` text
User
  |
Load Balancer
  |
+---------+---------+---------+
| App     | App     | App     |
| Server  | Server  | Server  |
+---------+---------+---------+
            |
        Database
```

### Low-Level Design (LLD)

LLD answers:

> How should each component be represented in clean, maintainable code?

LLD deals with:

-   classes
-   objects
-   interfaces
-   relationships
-   responsibilities
-   encapsulation
-   inheritance
-   polymorphism
-   design principles
-   design patterns

A useful mental model is:

``` text
HLD
"What components do we need?"
        |
        v
LLD
"How do we implement those components well?"
        |
        v
Code
```

------------------------------------------------------------------------

## 2. Scaling: Vertical vs Horizontal

A single server creates three common problems:

1.  **Single Point of Failure**
2.  **High latency under load**
3.  **Limited capacity**

### Vertical Scaling

Make one machine more powerful.

``` text
Small Server
    |
    v
Bigger Server
    |
    v
Even Bigger Server
```

Advantages:

-   simple
-   easy to operate

Limitations:

-   hardware has a ceiling
-   cost increases
-   the single point of failure remains

### Horizontal Scaling

Add more machines.

``` text
                 +--> App Server 1
                 |
User --> LB -----+--> App Server 2
                 |
                 +--> App Server 3
                         |
                         v
                     Database
```

Horizontal scaling improves capacity and availability, but introduces
new design problems such as shared state and coordination.

------------------------------------------------------------------------

## 3. Why Shared State Matters

Suppose a user logs in through Server 1.

``` text
Request 1 --> Server 1
             session stored here
```

The next request may reach Server 2.

``` text
Request 2 --> Server 2
             "Who is this user?"
```

The solution is to keep shared user state in a shared layer.

``` text
                +--> Server 1 --+
User --> LB ----+--> Server 2 --+--> Database
                +--> Server 3 --+
```

This is one reason scalable applications try to keep application servers
as stateless as practical.

------------------------------------------------------------------------

## 4. Good LLD

Good LLD makes code:

### Maintainable

Another developer can understand and modify it.

### Extensible

New requirements can be added without rewriting unrelated code.

### Reusable

Common behaviour is not duplicated unnecessarily.

The important question is not:

> "Can I write this code?"

It is:

> "Can this code survive the next six months of requirement changes?"

------------------------------------------------------------------------

# 5. Procedural Thinking vs Object-Oriented Thinking

### Procedural Style

The code is organized around functions.

``` text
data
 |
 +--> function(data)
 +--> anotherFunction(data)
 +--> anotherFunction(data)
```

The data is largely passive.

For example:

``` java
class StudentData {
    String name;
    int age;
}

static void printStudent(StudentData student) {
    System.out.println(student.name);
    System.out.println(student.age);
}
```

The external function controls the behaviour.

### Object-Oriented Style

The object owns the behaviour.

``` java
class Student {
    private String name;
    private int age;

    public void print() {
        System.out.println(name);
        System.out.println(age);
    }
}
```

Usage:

``` java
Student student = new Student();
student.print();
```

The important change is:

``` text
Procedural:
printStudent(student)

OOP:
student.print()
```

The entity becomes responsible for behaviour related to its own state.

------------------------------------------------------------------------

# 6. The Entity Mental Model

A useful first definition is:

``` text
Entity = Data + Behaviour
```

For a ride-booking system:

  Entity    Data                  Behaviour
  --------- --------------------- --------------------------------
  Driver    name, rating          acceptRide(), updateLocation()
  Rider     name, location        bookRide(), cancelRide()
  Trip      source, destination   calculateFare(), complete()
  Vehicle   model, registration   identifyVehicle()
  Payment   amount, status        process(), refund()

Do not create a class for every noun in a problem statement.

Ask:

1.  Does this concept have meaningful state?
2.  Does it own behaviour?
3.  Does it have a clear responsibility?

------------------------------------------------------------------------

## 7. Responsibility Assignment

A useful design question is:

> Whose data does this behaviour primarily operate on?

For example:

``` java
class Trip {
    private double distance;

    public double calculateFare() {
        return distance * 12;
    }
}
```

This is better than:

``` java
class DriverService {
    public double calculateTripFare(Trip trip) {
        return trip.getDistance() * 12;
    }
}
```

when the fare rule fundamentally belongs to the trip.

------------------------------------------------------------------------

# 8. LLD Interview Perspective

LLD questions usually test whether you can:

1.  clarify requirements
2.  identify entities
3.  assign responsibilities
4.  choose relationships
5.  define interfaces
6.  keep dependencies manageable
7.  write clean code

Avoid jumping immediately into code.

A strong process is:

``` text
Requirements
     |
     v
Entities
     |
     v
Responsibilities
     |
     v
Relationships
     |
     v
Interfaces / Abstractions
     |
     v
Classes
     |
     v
Implementation
```

------------------------------------------------------------------------

## 9. Key Takeaways

-   HLD defines system components and their connections.
-   LLD defines how those components are implemented.
-   Horizontal scaling introduces shared-state concerns.
-   OOP organizes software around entities.
-   An entity combines data and behaviour.
-   Good LLD optimizes for change, not just initial implementation.
-   Avoid premature abstraction.
-   Assign behaviour to the object that owns the relevant data.

------------------------------------------------------------------------

## Practice

Design a food-delivery system.

Identify at least four entities and write:

``` text
Entity
  - two important fields
  - two behaviours
```

Example:

``` text
Restaurant
  - name
  - location
  - acceptOrder()
  - updateMenu()
```
