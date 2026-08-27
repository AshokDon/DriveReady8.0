# LLD — SOLID Principles (Python)

### Bird System: From Brute Force to the Final SOLID Design

> **A note on Python.** Java enforces several of the fixes below at compile time. Python has no compile step, so the same guarantees arrive in one of two places instead: at **runtime** as a `TypeError` or `AttributeError`, or **statically from a type checker such as `mypy`**, which reads your type hints before you run anything. Each section below says which one applies. Running `mypy` is what turns a type hint into an actual guarantee.

---

## 1. What Are We Building?

We will design a Bird System that supports different birds and their behaviors.

```
Birds:
    Pigeon   → can fly
    Dove     → can fly
    Crow     → can fly
    Penguin  → cannot fly
    Later    → new birds and new behaviors
```

We will intentionally start with a bad design and improve it step by step using SOLID. This makes it easier to understand why each principle exists.

---

## 2. Why SOLID?

SOLID principles are design guidelines, not strict rules. They help us write code that is easier to change, extend, test, reuse and maintain.

```
Goal:
    Working code
         ↓
    Maintainable code
         ↓
    Extensible code
         ↓
    Testable + reusable code
```

---

## 3. Stage 1 — Brute-Force Design

The first instinct is to create one Bird class and put all bird-specific logic inside it.

```python
class Bird:
    def __init__(self, name, age, color, bird_type):
        self.name = name
        self.age = age
        self.color = color
        self.type = bird_type

    def fly(self):
        if self.type == "pigeon":
            print("Pigeon is flying")
        elif self.type == "dove":
            print("Dove is flying")
        elif self.type == "crow":
            print("Crow is flying")
        elif self.type == "penguin":
            print("Penguin cannot fly")

    def eat(self): ...
    def dance(self): ...
    def swim(self): ...
    def make_sound(self): ...
```

**Problems:**

- One class contains logic for many different birds.
- Many if/else or switch statements.
- Large methods become difficult to read and test.
- Multiple developers may need to modify the same class.
- Adding a new bird means modifying existing code.
- Unrelated changes can create regression.

---

## 4. SRP — Single Responsibility Principle

**SRP says:** A class should have one responsibility and one reason to change.

The problem with our brute-force Bird class is that it knows the detailed behavior of Pigeon, Dove, Crow, Penguin and potentially every future bird.

The class therefore has many reasons to change:

```
Pigeon requirement changes   → Bird changes
Dove requirement changes     → Bird changes
Crow requirement changes     → Bird changes
Penguin requirement changes  → Bird changes
```

### Solution: Separate responsibilities using inheritance

We make Bird an abstract base class containing only the common bird information/behavior. Each concrete bird becomes responsible for its own specific behavior.

```
abstract Bird
    name
    age
    color

    eat()

Pigeon extends Bird
    fly()

Dove extends Bird
    fly()

Crow extends Bird
    fly()

Penguin extends Bird
    ...
```

If flying is currently considered part of the Bird contract, we can declare it abstract and let each child implement it.

```
abstract class Bird
    name
    age
    color

    constructor(name, age, color)

    abstract fly()

    eat()
```

**Python:**

```python
from abc import ABC, abstractmethod


class Bird(ABC):
    def __init__(self, name: str, age: int, color: str):
        self._name = name
        self._age = age
        self._color = color

    @abstractmethod
    def fly(self) -> None: ...

    def eat(self) -> None:
        print("Eating")


class Pigeon(Bird):
    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age, color)

    def fly(self) -> None:
        print("Pigeon is flying")


class Dove(Bird):
    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age, color)

    def fly(self) -> None:
        print("Dove is flying")


class Crow(Bird):
    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age, color)

    def fly(self) -> None:
        print("Crow is flying")
```

`@abstractmethod` does nothing on its own — the class must inherit `ABC` for it to be enforced. With `ABC` in place, `Bird("x", 1, "grey")` raises `TypeError: Can't instantiate abstract class Bird without an implementation for abstract method 'fly'`, and a subclass that forgets `fly()` fails the same way when you try to create one.

`super().__init__(name, age, color)` is Python's `super(name, age, color)`. It runs the parent constructor so the parent part of the object is built first, exactly as in Java.

Unlike Java, Python does **not** force you to write these. A child with no `__init__` at all silently inherits the parent's, and `Pigeon("Pigeon", 13, "black")` still works. They are written out here so the parent/child construction is visible, and because the moment a child needs one extra field of its own — as `Dove` does in Section 10 — you have to write it anyway.

Now bird-specific logic is separated. Pigeon changes affect Pigeon, Dove changes affect Dove, and so on. The common Bird class owns common bird responsibilities.

---

## 5. OCP — Open/Closed Principle

**OCP says:** A class should be open for extension but closed for modification.

After SRP, our design is already much better. But now consider what happens when a new bird is introduced.

With the brute-force design, we would modify the existing `fly()` method:

```python
def fly(self):
    if self.type == "pigeon":
        ...
    elif self.type == "dove":
        ...
    elif self.type == "crow":
        ...
    elif self.type == "eagle":         # ← modify old code again
        ...
```

This is exactly what OCP tries to avoid.

### Solution: Extend using inheritance

Because Bird is an abstract class, a new bird can be added by creating a new subclass. We extend the system instead of repeatedly modifying the existing bird implementations.

```
Existing:
    Bird
     ├── Pigeon
     ├── Dove
     └── Crow

New requirement:
    Add Eagle

Extension:
    Bird
     ├── Pigeon
     ├── Dove
     ├── Crow
     └── Eagle        ← NEW CLASS
```

**Pseudocode:**

```
class Eagle extends Bird

    constructor(...)
        call super(...)

    fly()
        print "Eagle is flying"
```

**Python:**

```python
class Eagle(Bird):
    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age, color)

    def fly(self) -> None:
        print("Eagle is flying")
```

The important idea:

```
Before:
    New bird → modify existing Bird logic

After:
    New bird → create a new child class
```

At this stage, we have used inheritance to improve both SRP and OCP. However, inheritance introduces a new design problem: not every Bird can actually satisfy the `fly()` contract.

---

## 6. LSP — Liskov Substitution Principle

**LSP says:** A child object should be usable wherever its parent is expected without breaking the correctness of the program.

Our current hierarchy says every Bird must implement `fly()`. That works for Pigeon, Dove, Crow and Eagle.

```
Bird
    fly()

    Pigeon   → fly ✓
    Dove     → fly ✓
    Crow     → fly ✓
    Eagle    → fly ✓
    Penguin  → cannot fly ✗
```

If we add Penguin:

```python
class Penguin(Bird):
    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age, color)

    def fly(self) -> None:
        pass        # Penguin cannot fly
```

Now the parent contract is wrong. A Penguin is a Bird, but it cannot behave as a Bird that supports `fly()`.

A bad workaround is special handling:

```python
def make_bird_fly(bird: Bird) -> None:

    if isinstance(bird, Penguin):
        print("Sorry, not supported")
        return

    bird.fly()
```

The need for special handling tells us the abstraction is wrong.

### Solution: Separate capabilities from the Bird hierarchy

Bird should contain common bird behavior. Flying and dancing should be modeled as capabilities.

```
Bird
    eat()

Flyable
    fly()

Danceable
    dance()

Pigeon   → Bird + Flyable + Danceable
Dove     → Bird + Flyable
Penguin  → Bird + Danceable
```

**Java:**

```python
from abc import ABC, abstractmethod


class Bird(ABC):
    def __init__(self, name: str, age: int, color: str):
        self._name = name
        self._age = age
        self._color = color

    def eat(self) -> None:
        print("Eating")


class Flyable(ABC):
    @abstractmethod
    def fly(self) -> None: ...


class Danceable(ABC):
    @abstractmethod
    def dance(self) -> None: ...


class Pigeon(Bird, Flyable, Danceable):

    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age, color)

    def fly(self) -> None:
        print("Pigeon is flying")

    def dance(self) -> None:
        print("Pigeon is Dancing")


class Dove(Bird, Flyable):

    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age, color)

    def fly(self) -> None:
        print("Dove is flying")


class Penguin(Bird, Danceable):

    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age, color)

    def dance(self) -> None:
        print("Penguin is Dancing")
```

Java needs `extends` for the class and `implements` for the interfaces because it forbids multiple inheritance. Python allows a class to inherit from several bases directly, so `Bird` and the capabilities are listed together in one line. The idea is identical: `Bird` carries the shared state, and each capability is a separate, optional contract.

Note that `Bird` is no longer abstract in behaviour — it has no `@abstractmethod` left — so `Bird("x", 1, "grey")` would now succeed. Keep `ABC` in the base if you want to keep blocking that.

---

## 7. Class Explosion

Once we start adding many behaviors, trying to model every combination with inheritance can produce class explosion.

```
FlyingBird
NonFlyingBird
HighFlyingBird
LowFlyingBird
FlyingSwimmingBird
FlyingDancingBird
SwimmingDancingBird
...
```

Capabilities avoid this by allowing behaviors to be composed independently.

```
Bird
 │
 ├── Flyable
 ├── Danceable
 ├── Swimmable
 └── ...
```

---

## 8. ISP — Interface Segregation Principle

**ISP says:** Clients should not be forced to depend on methods they do not need.

Now that we have introduced interfaces, we should keep them small.

```python
# Bad
class BirdBehavior(ABC):
    @abstractmethod
    def fly(self) -> None: ...
    @abstractmethod
    def dance(self) -> None: ...
    @abstractmethod
    def swim(self) -> None: ...
    @abstractmethod
    def hunt(self) -> None: ...
    @abstractmethod
    def sing(self) -> None: ...
```

A Penguin should not be forced to implement `fly()` just because it needs `dance()`.

```python
# Better
class Flyable(ABC):
    @abstractmethod
    def fly(self) -> None: ...

class Danceable(ABC):
    @abstractmethod
    def dance(self) -> None: ...

class Swimmable(ABC):
    @abstractmethod
    def swim(self) -> None: ...

class Singable(ABC):
    @abstractmethod
    def sing(self) -> None: ...
```

Python makes the cost of the fat version very concrete: a `Penguin` that inherits `BirdBehavior` and omits `fly()` raises `TypeError: Can't instantiate abstract class Penguin without an implementation for abstract method 'fly'`. The only way to make it usable is to write a dishonest `fly()`.

Our birds implement only the capabilities they actually support.

---

## 9. DIP — Dependency Inversion Principle

**DIP says:** High-level modules should not directly depend on low-level concrete implementations. Both should depend on abstractions.

Now imagine Dove can fly at different altitudes. We do not want Dove tightly coupled to one concrete flying implementation.

```
Bad:
    Dove
     ↓
    LowFlyingBird

Change requirement:
    Dove
     ↓
    HighFlyingBird

    Dove must change.
```

Introduce the Flyer abstraction:

```
            Flyer
           /     \
  LowFlyingBird   HighFlyingBird

    Dove
     ↓
    Flyer
```

```python
class Flyer(ABC):
    @abstractmethod
    def fly_altitude(self) -> None: ...


class HighFlyingBird(Flyer):
    def high_fly(self) -> None:
        print("this bird flies high")

    def fly_altitude(self) -> None:
        self.high_fly()


class LowFlyingBird(Flyer):
    def low_fly(self) -> None:
        print("This bird flies low")

    def fly_altitude(self) -> None:
        self.low_fly()
```

Dove now depends on Flyer, not on a concrete flying strategy.

---

## 10. DI — Dependency Injection

Dependency Injection is not a SOLID principle. It is a technique commonly used to implement Dependency Inversion.

Instead of Dove creating the dependency itself, the client creates it and injects it.

```python
# Bad
class Dove(Bird, Flyable):
    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age, color)
        self._flyer = HighFlyingBird()      # Dove chooses for itself

# Better
class Dove(Bird, Flyable):
    def __init__(self, name: str, age: int, color: str, flyer: Flyer):
        super().__init__(name, age, color)
        self._flyer = flyer                 # handed in from outside
```

**Python:**

```python
class Dove(Bird, Flyable):

    def __init__(self, name: str, age: int, color: str, flyer: Flyer):
        super().__init__(name, age, color)
        self._flyer = flyer

    def fly(self) -> None:
        self._flyer.fly_altitude()
        print("Dove is flying")
```

**Client:**

```python
flyer = HighFlyingBird()

dove = Dove("Dove", 10, "white", flyer)

dove.fly()
```

**Changing the strategy:**

```python
flyer = LowFlyingBird()

dove = Dove("Dove", 10, "white", flyer)
```

Dove does not need to change.

---

## 11. Final Client

```python
def make_bird_fly(bird: Flyable) -> None:
    print("Bird is flying")
    bird.fly()


if __name__ == "__main__":
    pigeon = Pigeon("Pigeon", 13, "black")
    dove = Dove("Dove", 10, "white", HighFlyingBird())

    make_bird_fly(pigeon)
    make_bird_fly(dove)

    penguin = Penguin("Penguin", 15, "blue")
    # make_bird_fly(penguin)
    # Not allowed — Penguin is not Flyable
```

**Output:**

```
Bird is flying
Pigeon is flying
Bird is flying
this bird flies high
Dove is flying
```

The client does not need an `isinstance(bird, Penguin)` check. The type system prevents invalid usage — with one Python-specific caveat.

In Java that last line would not compile. In Python it is caught in one of two places:

```
mypy    → Argument 1 to "make_bird_fly" has incompatible type "Penguin";
          expected "Flyable"  [arg-type]

runtime → AttributeError: 'Penguin' object has no attribute 'fly'
```

`mypy` reports it before you run anything, which is the equivalent of Java's compile error. Without `mypy`, the type hint is documentation and the failure waits until that line executes. Either way the `isinstance` check is gone — a Penguin simply has no `fly()` to call.

---

## 12. Final System

```
                    Bird
                     │
        ┌────────────┼────────────┐
        │            │            │
     Pigeon        Dove        Penguin
        │            │            │
   ┌────┴────┐    Flyable     Danceable
   │         │       │
Flyable  Danceable  Flyer
                   /     \
           LowFlying    HighFlying


Bird                   → common bird responsibility
Flyable / Danceable    → capabilities
Flyer                  → flying-strategy abstraction
LowFlying / HighFlying → concrete implementations
Client                 → depends on abstractions
```

---

## 13. Complete Teaching Flow

```
BRUTE FORCE
    One Bird class contains every bird's logic
         ↓
Problems
    Large class + if/else + conflicts + testing difficulty
         ↓
SRP
    Separate bird-specific responsibilities
         ↓
SOLUTION: INHERITANCE
    Make Bird abstract
    Create Pigeon, Dove, Crow, etc.
         ↓
OCP
    New birds should extend the system
    without modifying existing bird logic
         ↓
SOLUTION: INHERITANCE
    Add Eagle as a new child class
         ↓
LSP
    Penguin cannot satisfy Bird.fly()
         ↓
SOLUTION: CAPABILITIES / INTERFACES
    Flyable + Danceable
         ↓
ISP
    Keep each interface small and focused
         ↓
DIP
    Dove depends on Flyer abstraction
    instead of concrete flying classes
         ↓
DI
    Inject HighFlyingBird / LowFlyingBird
    from outside
         ↓
FINAL DESIGN
    Flexible + maintainable + testable + extensible
```

---

## 14. One-Line Memory Trick

| Concept | Question |
|---|---|
| **SRP** | What is this class responsible for, and what makes it change? |
| **OCP** | Can I add a new bird without modifying stable existing logic? |
| **LSP** | Can I safely replace the parent with the child? |
| **ISP** | Am I forcing a class to depend on methods it does not need? |
| **DIP** | Am I depending on a concrete implementation unnecessarily? |
| **DI** | Who creates and provides the dependency? |

---

## 15. Final Mental Model

```
SRP  → Separate responsibilities
OCP  → Extend through new implementations
LSP  → Preserve substitutability
ISP  → Keep interfaces small
DIP  → Depend on abstractions
DI   → Inject dependencies from outside
```
