# LLD 01 — SOLID Principles

**DriveReady 8.0 · AI Applied Engineer · Post-read**

This session is built around one running example: a `Bird` class hierarchy that starts out
badly written, then gets repaired one principle at a time. Nothing here is presented in the
abstract — every principle arrives because the previous design just broke.

Every sample is in Java and Python. That matters more than it sounds like it should, because
about half the guarantees in this session are enforced by the Java compiler, and Python has no
compiler. Where that changes the answer, the document says so instead of glossing over it.

Assumed from Module 1: encapsulation, inheritance, polymorphism, and the difference between
`extends`, `implements` and composition.

---

## Contents

1. [The naive Bird class, and where it breaks](#1-the-naive-bird-class-and-where-it-breaks)
2. [SRP — one reason to change](#2-srp--one-reason-to-change)
3. [OCP — open for extension, closed for modification](#3-ocp--open-for-extension-closed-for-modification)
4. [Refactoring Bird, and the Penguin problem](#4-refactoring-bird-and-the-penguin-problem)
5. [Splitting by capability, and class explosion](#5-splitting-by-capability-and-class-explosion)
6. [LSP — substitutability](#6-lsp--substitutability)
7. [ISP — keep interfaces small](#7-isp--keep-interfaces-small)
8. [DIP — depend on abstractions](#8-dip--depend-on-abstractions)
9. [Dependency Injection](#9-dependency-injection)
10. [ISP and DIP are one check, not two](#10-isp-and-dip-are-one-check-not-two)
11. [What Python actually changes](#11-what-python-actually-changes)
12. [Pitfalls, collected](#12-pitfalls-collected)
13. [Java ↔ Python glossary](#13-java--python-glossary)
14. [Interview questions](#14-interview-questions)
15. [Check yourself](#15-check-yourself)
16. [Extra read — the pattern hiding in Section 8](#16-extra-read--the-pattern-hiding-in-section-8)
17. [Homework](#17-homework)

---

## 1. The naive Bird class, and where it breaks

Given "design a `Bird` entity that stores different bird types, their attributes and their
behaviour," almost everyone's first instinct is one class holding everything. We're going to
build that version on purpose, so we can watch it fail rather than be told it fails.

**Start with attributes:**

**Java**

```java
public class Bird {
    private String name;
    private int age;
    private String color;
    private String type;      // "pigeon", "sparrow", "eagle" ...
}
```

**Python**

```python
class Bird:
    def __init__(self, name: str, age: int, color: str, kind: str):
        self.name = name
        self.age = age
        self.color = color
        self.kind = kind      # "pigeon", "sparrow", "eagle" ...
```

Note `kind` rather than `type` in Python — `type` is a builtin, and shadowing it inside a class
body causes real confusion later.

**Now add flight, branched on the type:**

**Java**

```java
public class Bird {
    private String name;
    private int age;
    private String color;
    private String type;

    public void fly() {
        if (type.equals("pigeon")) {
            // short bursts, close to the ground
        } else if (type.equals("sparrow")) {
            // quick, fluttery
        } else if (type.equals("eagle")) {
            // soars, long glides
        }
    }
}
```

**Python**

```python
class Bird:
    def __init__(self, name, age, color, kind):
        self.name, self.age, self.color, self.kind = name, age, color, kind

    def fly(self):
        if self.kind == "pigeon":
            print("short bursts, close to the ground")
        elif self.kind == "sparrow":
            print("quick, fluttery")
        elif self.kind == "eagle":
            print("soars, long glides")
```

Swapping the string for an enum is a reasonable instinct and it does remove a real
stringly-typed risk. But look at what it fixes: nothing about the branching. The `if-else`
chain is identical either way. The failure isn't in how the type is *represented*, it's in
every bird's behaviour being crammed into one method.

Add bird types and the chain grows one branch each time, until it's twenty near-identical
conditions that nobody wants to read or test.

**Two things to watch for:**

- Thinking an enum fixes this. It tidies the type and leaves the structure untouched.
- Assuming it scales fine. Five branches look manageable. Twenty is unreadable, awkward to test
  branch by branch, and starts growing duplicated logic between branches.

---

## 2. SRP — one reason to change

> **Single Responsibility Principle:** every unit of code should have one responsibility —
> meaning one reason to change.

Look at `fly()` above and count the reasons it might change:

```
the pigeon's flight style changes    → edit fly()
the sparrow's changes                → edit fly()
the eagle's changes                  → edit fly()
a new bird type is added             → edit fly()
```

Four reasons, none of which has anything to do with the others. That's the violation, and it
also points straight at the fix: each bird gets its own class with its own `fly()`.

### Not every conditional is a violation

This is the part people over-apply. A chain of `if-else` that walks through steps of one
coherent algorithm is fine. It becomes an SRP violation when the branches are doing genuinely
unrelated jobs, as the per-bird flight logic is.

The real test isn't line count or branch count. It's this: *would a change to one unrelated
concern force an edit to code responsible for a different unrelated concern?* A method that
both charges a payment and sends a confirmation email fails that test at four lines long.

### Trap — the monster method

**Java**

```java
public void saveToDatabase() {
    // connect, build query, execute, map result, close connection
}
```

**Python**

```python
def save_to_database(self):
    # connect, build query, execute, map result, close connection
    ...
```

The name promises one job. The body does five. Split it:

```
saveToDatabase()  →  connectToDatabase()
                     createQuery()
                     executeQuery()
                     mapToObject()
                     closeConnection()
```

### Trap — the garbage drawer

A `Utils.java` or `utils.py` that accumulates date logic, string logic and file logic over two
years becomes impossible to navigate, and guarantees that two engineers working on unrelated
features will collide in the same file.

```
Instead of one utils file:

  Java              Python
  DateUtils.java    utils/dates.py
  StringUtils.java  utils/strings.py
  FileUtils.java    utils/files.py
```

**Watch for:**

- Treating length as the test. It isn't. Unrelated reasons to change is the test.
- Chasing a mechanically perfect split. LLD is partly subjective. The goal is a codebase that's
  easier to work in, not a diagram that satisfies a rule.

---

## 3. OCP — open for extension, closed for modification

> **Open/Closed Principle:** a class should be open for extension but closed for modification.
> A new feature should mean new code, not edits to code that already works.

**Java**

```java
public void fly() {
    if (type.equals("eagle"))        flyLikeEagle();
    else if (type.equals("penguin")) flyLikePenguin();
    else if (type.equals("parrot"))  flyLikeParrot();
}
```

**Python**

```python
def fly(self):
    if self.kind == "eagle":     self.fly_like_eagle()
    elif self.kind == "penguin": self.fly_like_penguin()
    elif self.kind == "parrot":  self.fly_like_parrot()
```

Supporting a Falcon means wedging another `elif` into a method that already worked. That's a
modification, not an extension, no matter how small the insertion looks.

### Why this actually matters: regression

The concrete risk is a **regression** — a change made for one purpose breaking something
unrelated that used to work. You add the Falcon branch, and one of the twelve bird types
already handled by this method quietly stops working.

Note the counter-intuitive part: a method with *good* test coverage across many cases is
exactly where this is most dangerous, because it's carrying the most existing behaviour that
your edit can disturb.

```
Editing shared, working code risks a regression.
New feature  →  touch NEW code only.

Bird class          →  generic attributes and behaviour
Specific behaviour  →  specific bird classes
```

SRP told us to split responsibilities apart. It didn't tell us how to add a sixteenth bird
without touching anything. That's OCP's job, and Section 4 applies both at once.

**Watch for:**

- Calling "adding a branch" an extension. Inserting an `elif` into a working method is
  modification, full stop.

---

## 4. Refactoring Bird, and the Penguin problem

Apply SRP and OCP together: generic shared parts go on a base class, bird-specific behaviour
goes into subclasses.

**Java**

```java
public abstract class Bird {
    protected String name;
    protected int age;
    protected String color;

    public void eat() {
        // shared by every bird, so it stays concrete here
    }

    public abstract void fly();      // every bird MUST supply its own
}
```

**Python**

```python
from abc import ABC, abstractmethod


class Bird(ABC):
    def __init__(self, name: str, age: int, color: str):
        self.name = name
        self.age = age
        self.color = color

    def eat(self) -> None:
        print(f"{self.name} is eating")     # shared, stays concrete

    @abstractmethod
    def fly(self) -> None:                  # every bird MUST supply its own
        ...
```

`eat()` stays concrete because it genuinely works the same for every bird. `fly()` is abstract
precisely because it doesn't, which forces every subclass to supply one rather than leaving it
optional.

**Each bird supplies only its own flight logic:**

**Java**

```java
public class Pigeon extends Bird {
    @Override public void fly() { /* short bursts, low altitude */ }
}

public class Sparrow extends Bird {
    @Override public void fly() { /* quick, fluttery */ }
}

public class Eagle extends Bird {
    @Override public void fly() { /* soars, long glides */ }
}
```

**Python**

```python
class Pigeon(Bird):
    def fly(self) -> None: print("short bursts, low altitude")


class Sparrow(Bird):
    def fly(self) -> None: print("quick, fluttery")


class Eagle(Bird):
    def fly(self) -> None: print("soars, long glides")
```

A Falcon is now one new class and one `fly()`. `Bird`, `Pigeon`, `Sparrow` and `Eagle` need
zero edits. One new file, no edits to existing code — SRP and OCP satisfied together.

Notice the Python version dropped all the constructor boilerplate. Java needs a constructor in
each subclass just to forward arguments to `super`; Python inherits `__init__` automatically,
so only the behaviour that actually differs is written down.

### The Penguin problem

A Penguin cannot fly. `Bird` requires every subclass to implement `fly()`.

**Java**

```java
public class Penguin extends Bird {
    @Override public void fly() {
        throw new UnsupportedOperationException("Penguins can't fly!");
    }
}
```

**Python**

```python
class Penguin(Bird):
    def fly(self) -> None:
        raise NotImplementedError("Penguins can't fly!")
```

**Java**

```java
Bird b = new Pigeon();
b.fly();                    // fine

b = new Penguin();
b.fly();                    // UnsupportedOperationException — at RUNTIME
```

**Python**

```python
b: Bird = Pigeon("p", 2, "grey")
b.fly()                     # fine

b = Penguin("pg", 5, "black")
b.fly()                     # NotImplementedError — at runtime
```

Leaving the body empty instead of throwing is worse, not better. A caller who runs
`penguin.fly()` and sees nothing happen will reasonably conclude it worked. A silent failure
is harder to find than a loud one.

The deeper problem: from the calling side, nothing distinguishes the working `Pigeon` call
from the failing `Penguin` call. Both look identical. You only find out by running that exact
line.

**Watch for:**

- Thinking the exception is the fix. It turns a silent failure into a loud one, which is an
  improvement — but a bird is still being forced to implement something it can't honestly do.
- Assuming this is a `fly()` problem. Any abstract method forced onto every subclass has the
  same exposure.

---

## 5. Splitting by capability, and class explosion

The honest fix is that a bird which can't fly shouldn't *have* a `fly()` method at all. Split
`Bird` into flying and non-flying branches:

**Java**

```java
public abstract class Bird {
    protected String name;
    public void eat() { }
}

public abstract class FlyingBird extends Bird {
    public abstract void fly();
}

public abstract class NonFlyingBird extends Bird {
    // deliberately no fly() at all
}

public class Pigeon  extends FlyingBird    { public void fly() { /* ... */ } }
public class Penguin extends NonFlyingBird { /* fly() does not exist here */ }
```

**Python**

```python
class Bird(ABC):
    def eat(self) -> None: ...


class FlyingBird(Bird):
    @abstractmethod
    def fly(self) -> None: ...


class NonFlyingBird(Bird):
    pass                                 # deliberately no fly() at all


class Pigeon(FlyingBird):
    def fly(self) -> None: print("short bursts")


class Penguin(NonFlyingBird):
    pass                                 # fly() does not exist here
```

**Java**

```java
FlyingBird p = new Pigeon();
p.fly();                        // fine

NonFlyingBird pg = new Penguin();
// pg.fly();                    // won't even COMPILE
```

**Python**

```python
p = Pigeon()
p.fly()                         # fine

pg = Penguin()
# pg.fly()                      # AttributeError at runtime; mypy flags it before that
```

There's the first real difference between the two languages, and it's worth pausing on. Java
turns this into a compile error — the code cannot be built. Python has no compile step, so the
same mistake is an `AttributeError` when that line eventually runs, unless a type checker
catches it first. Section 11 goes into what that means in practice.

### Now add dancing

Apply the same can/cannot subclassing to a second independent behaviour and you need four
classes to cover the combinations:

```
FlyingDancingBird | FlyingNonDancingBird | NonFlyingDancingBird | NonFlyingNonDancingBird
```

Add swimming and it doubles again, because every existing class has to split into can/cannot
for the new behaviour:

```
2 behaviours →  4 classes
3 behaviours →  8 classes
4 behaviours → 16 classes
n behaviours → 2ⁿ classes
```

Subclassing "can or cannot do X" does not scale once behaviours accumulate. This is called
**class explosion** and it is the reason interfaces exist.

**Watch for:**

- Treating the flying/non-flying split as the destination. It's a step. It fixes one behaviour
  and immediately reveals a worse problem when a second one arrives.

---

## 6. LSP — substitutability

> **Liskov Substitution Principle:** anywhere a parent type is used, a child should be safely
> substitutable in its place, with everything still working and no special handling required.

Section 4's Penguin is the direct illustration. Code holding a `Bird` and calling `fly()` works
for a Pigeon and needs a `try-catch` or a type check for a Penguin. **That special handling is
itself the violation.** A Penguin isn't truly substitutable for a `Bird` if using it safely
requires the caller to know it's specifically a Penguin.

### The formal rule

"Safely swappable" is a working definition, not the real one. Liskov's actual rule — behavioural
subtyping — is stated in terms of contracts:

```
A subtype may not STRENGTHEN the preconditions it inherits.
A subtype may not WEAKEN the postconditions it inherits.
```

A **precondition** is what a method requires before it runs — what the caller must guarantee.
A **postcondition** is what the method guarantees afterwards — what the caller may rely on.

The rule exists to protect the caller. Someone who only knows the parent's contract should
never be surprised by a subtype demanding more up front, or delivering less afterwards.

Both of this session's examples fail on postconditions:

- **Penguin.** `Bird.fly()` implicitly promises the bird flies. `Penguin` overrides it to
  throw, which weakens that promise — flight is no longer guaranteed, and the caller has no way
  to know from the `Bird` type alone.
- **Square extends Rectangle.** `Rectangle` implicitly guarantees that `setWidth()` changes
  only the width. `Square` also changes the height, weakening that guarantee, and the caller
  gets an area it didn't ask for.

### Square and Rectangle, correctly

**Java**

```java
class Rectangle {
    protected int width, height;
    public void setWidth(int w)  { width = w; }
    public void setHeight(int h) { height = h; }
    public int getArea()         { return width * height; }
}

class Square extends Rectangle {
    @Override public void setWidth(int w)  { width = w; height = w; }
    @Override public void setHeight(int h) { width = h; height = h; }
}
```

**Python**

```python
class Rectangle:
    def __init__(self) -> None:
        self.width = 0
        self.height = 0

    def set_width(self, w: int) -> None:  self.width = w
    def set_height(self, h: int) -> None: self.height = h
    def area(self) -> int:                return self.width * self.height


class Square(Rectangle):
    def set_width(self, w: int) -> None:
        self.width = w
        self.height = w

    def set_height(self, h: int) -> None:
        self.width = h
        self.height = h
```

**Java**

```java
Rectangle r = new Square();
r.setWidth(5);
r.setHeight(10);
r.getArea();          // caller expects 50, gets 100
```

**Python**

```python
r: Rectangle = Square()
r.set_width(5)
r.set_height(10)
print(r.area())       # caller expects 50, gets 100
```

**Both setters have to be overridden.** This is worth stating explicitly because it's easy to
get wrong: if you override only `setWidth`, then `setHeight(10)` runs the parent's version, you
end up with width 5 and height 10, and the area is 50 — the same answer a real Rectangle gives.
The example would demonstrate nothing at all. Measured:

```
only set_width overridden   →  w=5  h=10  area=50    (no bug visible)
both setters overridden     →  w=10 h=10  area=100   (the violation)
```

`Square` silently changes more than the caller asked for. Nothing in the `Rectangle` type warns
about it. Same failure shape as `Penguin.fly()` throwing: a subtype that appears to fit and
quietly breaks a promise.

### The fix: capabilities, not family trees

`extends` locks a class into exactly one parent. Interfaces let "can fly" and "can dance"
become independent opt-in choices instead of forced branches in a tree.

**Java**

```java
public interface Flyable  { void fly(); }
public interface Dancable { void dance(); }
```

**Python**

```python
from abc import ABC, abstractmethod


class Flyable(ABC):
    @abstractmethod
    def fly(self) -> None: ...


class Dancable(ABC):
    @abstractmethod
    def dance(self) -> None: ...
```

`Bird` goes back to holding only generic attributes and `eat()`, with nothing about flying or
dancing on it.

**Java**

```java
public class Sparrow extends Bird implements Flyable, Dancable {
    @Override public void fly()   { /* fluttery */ }
    @Override public void dance() { /* hopping  */ }
}

public class Penguin extends Bird implements Dancable {
    @Override public void dance() { /* waddling */ }
    // Flyable not implemented at all
}
```

**Python**

```python
class Sparrow(Bird, Flyable, Dancable):
    def fly(self) -> None:   print("fluttery")
    def dance(self) -> None: print("hopping")


class Penguin(Bird, Dancable):
    def dance(self) -> None: print("waddling")
    # Flyable not inherited at all
```

Python has no `implements` keyword. Multiple inheritance from small ABCs is the direct
equivalent, and it reads almost identically.

**Java**

```java
List<Flyable> flyingThings = new ArrayList<>();
flyingThings.add(new Sparrow());
// flyingThings.add(new Penguin());   // won't compile — Penguin isn't Flyable

for (Flyable f : flyingThings) f.fly();   // completely safe
```

**Python**

```python
flying_things: list[Flyable] = []
flying_things.append(Sparrow(...))
flying_things.append(Penguin(...))        # mypy: error. Runtime: allowed.

for f in flying_things:
    f.fly()                               # AttributeError on the Penguin
```

Here is the difference again, measured. mypy on that exact code:

```
error: Argument 1 to "append" of "list" has incompatible type "Penguin";
       expected "Flyable"  [arg-type]
```

And the same code run without a type checker:

```
fluttery
AttributeError: 'Penguin' object has no attribute 'fly'
```

Java refuses to build. Python builds happily, gets one bird into the loop, and falls over on
the second. The design is equally correct in both — but in Python the guarantee is only as
real as your CI pipeline running mypy.

**Watch for:**

- Assuming that compiling means LSP is satisfied. Square/Rectangle compiles cleanly in Java and
  passes mypy in Python. The violation is behavioural, not syntactic.
- Treating a `try-catch` around one specific subtype as ordinary defensive coding. If one
  subtype needs handling its siblings don't, that's the signature of an LSP violation.

---

## 7. ISP — keep interfaces small

> **Interface Segregation Principle:** no client should be forced to depend on methods it does
> not use. Interfaces should be small and focused, ideally one capability each.

Interfaces solved class explosion in Section 5. But an interface can still be designed badly,
by bundling unrelated capabilities into one contract.

**Java**

```java
public interface Performable {
    void fly();
    void dance();
}

public class Sparrow extends Bird implements Performable {
    public void fly()   { /* ... */ }
    public void dance() { /* ... */ }
}
```

**Python**

```python
class Performable(ABC):
    @abstractmethod
    def fly(self) -> None: ...

    @abstractmethod
    def dance(self) -> None: ...


class Sparrow(Bird, Performable):
    def fly(self) -> None:   ...
    def dance(self) -> None: ...
```

An Ostrich dances but can't fly. Implementing `Performable` forces it to supply a `fly()`
anyway — empty or throwing. Neither is honest.

**This is the Penguin problem again**, relocated from an abstract class into a fat interface.
Same root cause both times: something was forced to implement a behaviour it never had. Only
the mechanism changed.

**The fix — one capability per interface:**

**Java**

```java
public interface Flyable  { void fly(); }
public interface Dancable { void dance(); }

public class Sparrow extends Bird implements Flyable, Dancable { }
public class Ostrich extends Bird implements Dancable { }
```

**Python**

```python
class Flyable(ABC):
    @abstractmethod
    def fly(self) -> None: ...


class Dancable(ABC):
    @abstractmethod
    def dance(self) -> None: ...


class Sparrow(Bird, Flyable, Dancable): ...
class Ostrich(Bird, Dancable): ...
```

### Python's smaller interface: Protocol

Python has a second option that Java doesn't, and it's arguably the purest expression of ISP.
With `typing.Protocol`, a class satisfies a capability just by *having the method*. No
inheritance, no declaration, no coupling at all.

**Python**

```python
from typing import Protocol


class Flyable(Protocol):
    def fly(self) -> None: ...


class Pigeon:                          # inherits nothing
    def fly(self) -> None:
        print("short bursts")


def launch(bird: Flyable) -> None:
    bird.fly()


launch(Pigeon())                       # accepted — Pigeon has fly()
```

This is structural typing: the interface describes a shape, and anything of that shape fits.
The class doesn't need to know the protocol exists.

```
When to use which, in Python:

  ABC       you want shared implementation, and a runtime guarantee that
            an unfinished subclass can't be instantiated at all

  Protocol  you only want to describe what a caller needs, with zero
            coupling from the implementing class back to you
```

**Watch for:**

- Bundling two behaviours into one interface because one class needs both. Sparrow needing
  `fly()` and `dance()` doesn't justify `Performable`. It can implement two small ones.
- Assuming a big general-purpose interface is more "complete." A `Machine` interface with
  `print()`, `scan()` and `fax()` forces a `SimplePrinter` to stub out two methods it will
  never support.

---

## 8. DIP — depend on abstractions

> **Dependency Inversion Principle:** two concrete classes should not depend on each other
> directly. They should depend through an abstraction.

Pigeon and Sparrow fly the same way — short, low bursts. Writing that logic in both classes
duplicates it.

### The formal definition

The one-liner above is a simplification. Robert C. Martin's original has two clauses:

```
A. High-level modules should not depend on low-level modules.
   Both should depend on abstractions.

B. Abstractions should not depend on details.
   Details should depend on abstractions.
```

A **high-level module** encodes policy — what should happen. A **low-level module** encodes a
concrete detail — how it's actually done. Here, `Pigeon` is high-level: its policy is "I fly by
delegating to whatever flying behaviour I was given." `PigeonSparrowFlyingBehaviour` is
low-level: one specific way of doing it.

Clause A explains the direction of the fix below. Clause B adds something the one-liner misses:
the abstraction itself must not be shaped around any single implementation. `FlyingBehaviour`
has to stay general enough that a `FastFlyingBehaviour` can honour it without the interface
changing. **The dependency always points from a detail toward an abstraction, never back.**

### Attempt 1 — extract the shared logic

**Java**

```java
public class PigeonSparrowFlyingBehaviour {
    public void fly() { /* short bursts, low altitude — written ONCE */ }
}

public class Pigeon extends Bird implements Flyable, Dancable {
    private PigeonSparrowFlyingBehaviour flyingBehaviour =
        new PigeonSparrowFlyingBehaviour();

    public void fly() { flyingBehaviour.fly(); }
}
```

**Python**

```python
class PigeonSparrowFlyingBehaviour:
    def fly(self) -> None:
        print("short bursts, low altitude")      # written ONCE


class Pigeon(Bird, Flyable, Dancable):
    def __init__(self, name, age, color):
        super().__init__(name, age, color)
        self._flying = PigeonSparrowFlyingBehaviour()    # concrete, hard-wired

    def fly(self) -> None:
        self._flying.fly()
```

The duplication is gone. But `Pigeon` is now welded to one concrete class. Introducing a
`FastFlyingBehaviour` later means going back into `Pigeon` and editing both the declared type
and the construction — which is modifying working code, the exact thing OCP warned about.

### Attempt 2 — invert onto an abstraction

**Java**

```java
public interface FlyingBehaviour { void fly(); }

public class PigeonSparrowFlyingBehaviour implements FlyingBehaviour {
    public void fly() { /* short bursts, low altitude */ }
}

public class Pigeon extends Bird implements Flyable, Dancable {
    private FlyingBehaviour flyingBehaviour = new PigeonSparrowFlyingBehaviour();
    public void fly() { flyingBehaviour.fly(); }
}
```

**Python**

```python
class FlyingBehaviour(ABC):
    @abstractmethod
    def fly(self) -> None: ...


class PigeonSparrowFlyingBehaviour(FlyingBehaviour):
    def fly(self) -> None:
        print("short bursts, low altitude")


class Pigeon(Bird, Flyable, Dancable):
    def __init__(self, name, age, color):
        super().__init__(name, age, color)
        self._flying: FlyingBehaviour = PigeonSparrowFlyingBehaviour()

    def fly(self) -> None:
        self._flying.fly()
```

`Pigeon` now depends on the `FlyingBehaviour` abstraction rather than on a concrete class.
That flip — a concrete class depending on an abstraction instead of another concrete class — is
what "Inversion" means in the name.

### Recognising a violation

| Declaration | DIP violation? |
|---|---|
| `private PaymentGateway gateway;` | No — interface type |
| `self._gateway: PaymentGateway` | No — annotated with the abstraction |
| `private RazorpayGateway gateway = new RazorpayGateway();` | **Yes** — names and builds a concrete class |
| `self._gateway = RazorpayGateway()` | **Yes** — same shape in Python |
| `interface PaymentGateway { void pay(double amount); }` | No — this *is* the abstraction |
| `class RazorpayGateway implements PaymentGateway` | No — correct implementation |

The violation is specifically a class naming *and constructing* a concrete implementation
instead of depending on the interface.

And notice: even after the fix, `PigeonSparrowFlyingBehaviour()` is still being constructed
*inside* `Pigeon`. DIP fixed **who** `Pigeon` depends on. It didn't change **who builds it**.
That's the next section.

**Watch for:**

- Thinking the interface is the finish line. The class still constructs its own dependency.
- Dismissing DIP as overhead on small code. Fair for a script that will never change. The value
  appears the moment an implementation needs swapping.
- Confusing "depends on an abstraction" with "depends on nothing." `Pigeon` still has a
  dependency. DIP changed its nature, not its existence.

---

## 9. Dependency Injection

Dependency Injection is **not** one of the five letters. It's the natural payoff of DIP.

In `self._flying = PigeonSparrowFlyingBehaviour()`, `Pigeon` decides which implementation gets
built, right there, with nobody else getting a say.

> **Dependency Injection:** a class should not create its own dependencies. They should be
> handed in from outside — usually through the constructor.

**Java**

```java
public class Pigeon extends Bird implements Flyable, Dancable {
    private final FlyingBehaviour flyingBehaviour;

    public Pigeon(FlyingBehaviour flyingBehaviour) {
        this.flyingBehaviour = flyingBehaviour;
    }

    public void fly() { flyingBehaviour.fly(); }
}
```

**Python**

```python
class Pigeon(Bird, Flyable, Dancable):
    def __init__(self, name, age, color, flying: FlyingBehaviour):
        super().__init__(name, age, color)
        self._flying = flying

    def fly(self) -> None:
        self._flying.fly()
```

**Java**

```java
FlyingBehaviour fb = new PigeonSparrowFlyingBehaviour();
Pigeon pigeon = new Pigeon(fb);
```

**Python**

```python
fb = PigeonSparrowFlyingBehaviour()
pigeon = Pigeon("Coo", 2, "grey", fb)

# swapping the implementation touches nothing inside Pigeon
fast = FastFlyingBehaviour()
pigeon = Pigeon("Coo", 2, "grey", fast)
```

No `new` for its own dependency anywhere in `Pigeon`. Whoever builds a Pigeon supplies one.

### Where manual wiring stops working

If `A` needs `B` and `C`, and `B` needs `D`, `E` and `F`, then constructing everything in the
right order — `D`, `E`, `F`, then `B`, then `C`, then `A` — is something you do by hand exactly
once before wanting a machine to do it.

```
Manual wiring:  b = B(d, e, f);  a = A(b, c)
                → unmanageable fast as the graph deepens

Framework:      you declare WHAT you need in the constructor.
                The framework works out creation order, builds
                everything, and hands it to you wired up.
```

In Java that's Spring's `@Component` and `@Autowired`. **In Python — and this is the one you'll
actually use in Week 5 — it's FastAPI's `Depends`:**

**Python**

```python
from fastapi import Depends, FastAPI

app = FastAPI()


def get_flying_behaviour() -> FlyingBehaviour:
    return PigeonSparrowFlyingBehaviour()


@app.get("/fly")
def fly_endpoint(flying: FlyingBehaviour = Depends(get_flying_behaviour)):
    flying.fly()
    return {"status": "ok"}
```

FastAPI resolves the dependency graph, builds what's needed, and passes it in — the same job
Spring does, in a form you can read in one screen. And in tests you override it with
`app.dependency_overrides[get_flying_behaviour] = lambda: FakeFlyingBehaviour()`, which is
exactly the swap that DI existed to make possible.

Understanding the manual version first is what stops the framework from looking like magic.

```
DIP  determines WHO a class depends on   →  an abstraction, not a concrete class
DI   determines HOW it gets there         →  handed in, not self-constructed
```

**Watch for:**

- Conflating DI with DIP. Different questions. A design can satisfy one without the other —
  the `Pigeon` at the end of Section 8 satisfies DIP and not DI.
- Assuming manual wiring scales. It works for a shallow graph and becomes error-prone fast.
- Treating framework injection as unrelated magic. It automates precisely the manual process
  shown above. Nothing conceptually new.

---

## 10. ISP and DIP are one check, not two

DIP says a high-level module should depend on an abstraction. It says nothing about the
*shape* of that abstraction. That's the gap ISP fills.

Suppose `FlyingBehaviour` had been designed fat:

**Java**

```java
public interface BirdBehaviour {
    void fly();
    void dance();
    void swim();
}
```

**Python**

```python
class BirdBehaviour(ABC):
    @abstractmethod
    def fly(self) -> None: ...

    @abstractmethod
    def dance(self) -> None: ...

    @abstractmethod
    def swim(self) -> None: ...
```

If `Pigeon` depends on `BirdBehaviour` instead of `FlyingBehaviour`, DIP is technically
satisfied — it depends on an interface, not a concrete class. And the fix is hollow. `Pigeon`
is now coupled to `dance()` and `swim()`, which it never uses, and every implementation must
supply all three. That's the Section 7 ISP violation, moved one level up into the abstraction
DIP told everyone to depend on.

```
DIP without ISP   "depend on an abstraction" is satisfied, but the
                  abstraction drags in obligations nobody wanted.

ISP without DIP   interfaces are small and focused, but a high-level
                  module is still wired straight to one concrete
                  implementation, bypassing them.

Both together     depend on an abstraction (DIP), AND make that
                  abstraction narrow enough that depending on it costs
                  nothing beyond what you use (ISP).
```

### How these violations compound

They fail independently but in a real codebase they feed each other:

- **A fat interface forces every implementer — including ones that can't honestly support every
  method — to stub or throw.** That recreates the Penguin problem for each of them, which is now
  also an **LSP violation**: none of them is safely substitutable without the caller
  special-casing it.
- **A high-level module depending on that interface inherits every one of those unsafe
  implementers as a plausible dependency.** Code written against the interface, trusting DIP's
  promise that any implementation works, now has no way to tell which ones are actually safe.
  The exact guarantee DIP existed to provide is gone.
- **The result is a redesign, not a local fix.** Narrowing the interface afterwards changes its
  signature, which ripples into every implementer and every consumer. What would have been one
  new class had the interface been narrow from the start becomes a coordinated multi-file
  change — precisely the shared-code edit OCP was introduced to avoid.

**The practical rule:** before depending on an abstraction, check that every current and
reasonably foreseeable implementer can honestly satisfy every method on it. That single check
covers ISP and keeps everyone substitutable under LSP at the same time.

---

## 11. What Python actually changes

Worth reading in one go, because it's scattered through the sections above.

**The principles are identical.** All five are about how responsibilities and dependencies are
arranged, and that reasoning doesn't care what language you're in. Nothing in Sections 2, 3, 8,
9 or 10 changes at all.

**What changes is when you find out you got it wrong.**

| | Java | Python |
|---|---|---|
| Calling a method a subtype doesn't have | Compile error | `AttributeError` at runtime |
| Putting a Penguin in a `List<Flyable>` | Compile error | Allowed; mypy flags it |
| Class with an unimplemented abstract method | Compile error | `TypeError` on instantiation |
| Square/Rectangle | Compiles, wrong at runtime | Runs, wrong at runtime |

Three of those four move from "cannot be built" to "fails while running." That is the entire
difference, and it has one practical consequence: **in Python, the compile-time guarantees in
this document are only as real as your type checker actually running.** Add mypy or pyright to
CI, or the annotations are documentation with no teeth.

Row three is the exception worth knowing. Python's ABCs give a real runtime guarantee, no type
checker required:

```
TypeError: Can't instantiate abstract class Broken without an
           implementation for abstract method 'fly'
```

You cannot create a half-finished subclass. That's genuine enforcement, and it's why ABC is
usually the better choice over Protocol when you're modelling a capability that subclasses must
actually provide.

**Three Python-specific notes:**

- **No `implements`.** Multiple inheritance from small ABCs is the equivalent, and it's the
  standard way to model capabilities.
- **No `private`.** A leading underscore is a convention, not enforcement. The encapsulation
  arguments in SRP still hold; they're just honour-system.
- **Duck typing is not a substitute for LSP.** "If it has `fly()`, call it" sounds like it
  removes the problem. It relocates it: the check moves from the compiler to the moment the
  method is called, which is exactly the Penguin failure. `Protocol` is the disciplined version
  of duck typing — the same flexibility, with a checker watching.

---

## 12. Pitfalls, collected

```
1.  Treating every long method or conditional chain as an SRP violation
      The test is whether the reasons to change are unrelated — not length.

2.  Adding a branch to a working method to support a new case
      That's modification, not extension, and it risks a regression in the
      branches that already worked.

3.  Treating a thrown exception as an adequate fix for a forced method
      It turns a silent failure loud, which helps. The subtype is still being
      forced into a capability it doesn't have.

4.  Assuming clean compilation means LSP is satisfied
      Square/Rectangle compiles fine and passes mypy. The violation is
      behavioural.

5.  Overriding only one setter in the Square/Rectangle example
      Then area comes out 50 — the same as a real Rectangle — and the example
      demonstrates nothing. Both setters have to be overridden.

6.  Bundling capabilities into one interface because one class needs both
      Every other implementer then inherits behaviour it may not have.

7.  Believing an interface-typed field completes DIP
      The class may still construct its own implementation with new / ().

8.  Conflating Dependency Injection with Dependency Inversion
      DIP is who you depend on. DI is how it gets to you.

9.  Python — assuming type hints enforce anything on their own
      They don't. Without mypy or pyright in CI they're comments. Three of the
      four compile-time guarantees in this document become runtime failures.

10. Python — treating duck typing as a reason to skip all this
      It moves the failure from the compiler to the call site. That is the
      Penguin problem, not a solution to it.

11. Applying a principle in isolation
      SRP and OCP produced the abstract class together. DIP set up DI. ISP is
      what makes DIP's abstraction worth depending on. They compound.
```

---

## 13. Java ↔ Python glossary

| Concept | Java | Python |
|---|---|---|
| Abstract base class | `abstract class` | `class X(ABC)` |
| Abstract method | `public abstract void fly();` | `@abstractmethod` + `def fly(self): ...` |
| Interface | `interface Flyable` | `class Flyable(ABC)` or `class Flyable(Protocol)` |
| Implement a capability | `implements Flyable, Dancable` | `class Pigeon(Bird, Flyable, Dancable)` |
| Single inheritance limit | one `extends`, many `implements` | multiple inheritance, no limit |
| Constructor forwarding | explicit in every subclass | inherited automatically |
| Private field | `private String name;` | `self._name` by convention only |
| Type-safe collection | `List<Flyable>` | `list[Flyable]` — checked by mypy, not at runtime |
| Structural typing | not available | `typing.Protocol` |
| DI framework | Spring `@Autowired` | FastAPI `Depends`, or just pass the argument |
| Where mistakes surface | compile time | run time, unless a checker runs first |

**Terms**

| Term | Plain meaning |
|---|---|
| SRP | One reason to change per unit of code |
| Monster method | A method whose name promises one job and whose body does five |
| OCP | Open for extension, closed for modification |
| Regression | A change for one purpose breaking something else that worked |
| The Penguin problem | A subtype forced to implement something it can't honestly support |
| Class explosion | 2ⁿ subclass growth from modelling n independent behaviours by subclassing |
| LSP | A subtype must work anywhere its parent is expected, with no special handling |
| Precondition | What a method requires before it runs |
| Postcondition | What a method guarantees after it runs |
| ISP | No client forced to depend on methods it doesn't use |
| DIP | Depend on abstractions, not on concrete classes |
| Tight coupling | Direct dependency on a specific implementation, hard to swap |
| Dependency Injection | Dependencies handed in from outside rather than self-constructed |
| Protocol | Python's structural interface — matched by shape, not by inheritance |

---

## 14. Interview questions

**1. What separates an SRP violation from just a long method?**
Length isn't the test. A long method built from sequential steps of one algorithm can satisfy
SRP fine. The violation is multiple *unrelated* reasons to change — a method that charges
payment and also sends a confirmation email fails at four lines.

**2. Explain OCP through the risk it avoids.**
It asks that a new requirement be met by adding code rather than editing working code. The risk
is regression: an edit for one new case breaking cases that already passed. Counter-intuitively,
well-tested shared methods are where this is most dangerous, because they carry the most
existing behaviour to disturb.

**3. Why is throwing from `Penguin.fly()` still an LSP violation?**
Throwing makes the failure visible, which beats a silent no-op, but it doesn't restore
substitutability. Code holding a `Bird` still has to special-case Penguin to use it safely, and
that special handling is the violation.

**4. Why does `Square extends Rectangle` violate LSP even though it compiles?**
`Square` overrides the setters so that setting one dimension changes both. A caller who calls
`setWidth(5)` then `setHeight(10)` on what it believes is a Rectangle gets area 100, not 50. The
type system says nothing — it's a broken invariant, not a syntax problem.

**5. How is an ISP violation different from the abstract-class Penguin problem?**
The underlying failure is identical: a type coerced into a capability it doesn't have. Only the
mechanism differs — an abstract method on a base class in one case, a fat interface bundling
unrelated capabilities in the other.

**6. What does DIP fix, and what does it leave open?**
It changes what a concrete class may depend on: an abstraction instead of another concrete
class. It doesn't change who constructs that dependency — a class can hold an interface type and
still `new` its own implementation. That gap is DI's.

**7. Is Dependency Injection one of the five? Justify it.**
No. SOLID is five, and DI isn't among them. DIP addresses the *direction* of a dependency; DI
addresses the *mechanism* by which it arrives. Related, distinct.

**8. Why doesn't subclassing scale for independent optional behaviours?**
Modelling n independent can/cannot behaviours by subclassing needs a class per combination:
2ⁿ. Two behaviours is four classes, three is eight. Interfaces scale because a class picks up
any subset independently.

**9. In a review, how do you tell a real violation from a style disagreement?**
A real one has a demonstrable failure mode: unrelated reasons to change (SRP), an edit to tested
working code (OCP), one subtype needing special handling (LSP), an implementer stubbing a method
(ISP), a concrete class named and constructed inside another (DIP). Style disagreements don't
point at any of those.

**10. Does any of this change in Python?**
The principles don't. The enforcement does. Java rejects a Penguin in a `List<Flyable>` at
compile time; Python accepts it and raises `AttributeError` when `fly()` is called, unless mypy
catches it first. The one real runtime guarantee Python keeps is that ABCs refuse to instantiate
a class with unimplemented abstract methods.

**11. Apply all five to a Notification system (Email, SMS, Push).**
Each channel gets its own class implementing a shared `NotificationSender` — that's SRP and OCP,
since a new channel is a new class rather than an edit. Every implementation must be usable
without the caller special-casing it (LSP). The interface exposes only `send()`, not unrelated
concerns (ISP). The orchestrating class depends on `NotificationSender` and receives the concrete
channel from outside (DIP and DI).

---

## 15. Check yourself

1. List three genuinely unrelated reasons the original `fly()` might change, and say why each is
   a valid SRP concern on its own.
2. `process_order()` validates an order, charges payment, updates inventory and emails a
   confirmation. Identify the violation and propose the split.
3. Using the idea of regression, explain why adding a seventh `elif` to an `apply_discount()`
   that already handles six is risky even when the new branch is correct.
4. Build a two-level `Vehicle` hierarchy with one abstract method not every vehicle can support,
   and identify your Penguin case.
5. Give a concrete LSP violation that is *not* Square/Rectangle and compiles cleanly.
6. Derive why n independent behaviours need 2ⁿ subclasses, and say how many three would need.
7. In the `Performable` interface, name exactly which class is forced into a method it can't
   support, and why.
8. `self._gateway = RazorpayGateway()` sits inside `OrderService`. Explain why that's a DIP
   violation and rewrite it.
9. Now rewrite the same class to receive its gateway by constructor injection instead.
10. State precisely what DIP guarantees versus what DI guarantees, using `Pigeon` and
    `FlyingBehaviour`.
11. Take the Section 6 Python example, run it once with mypy and once without, and record both
    outputs. Explain in two sentences what that difference means for a Python codebase.
12. Rewrite `Flyable` as a `Protocol` instead of an ABC. What does that change about who can
    satisfy it, and what does it cost you?

---

## 16. Extra read — the pattern hiding in Section 8

The design we reached — an interface capturing one piece of interchangeable logic, a concrete
implementation of it, and a class holding a reference to the interface rather than implementing
the logic itself — is a named pattern in its own right: **Strategy**.

Its defining idea is that a family of interchangeable behaviours is extracted behind a common
interface, so the behaviour a class uses can be selected or swapped independently of the class
using it.

Mapping our code onto the pattern's vocabulary:

```
FlyingBehaviour                 →  the strategy interface
PigeonSparrowFlyingBehaviour    →  a concrete strategy
Pigeon                          →  the context (uses a strategy without
                                   knowing which one it was given)
```

The constructor-injection version of `Pigeon` from Section 9 is already the textbook form of
Strategy: the context receives its strategy from outside instead of choosing one internally.

Worth noticing: we arrived at this shape by working through DIP and DI in sequence, driven by
problems rather than by looking up a pattern. Getting to the same place from both directions is
good evidence the reasoning holds, not just the name.

The way Spring or FastAPI resolves an entire dependency graph automatically is also a named
pattern — a form of Inversion of Control container — and it's the second subject of the next
class.

---

## 17. Homework

```
1. New domain — design a Notification system (Email / SMS / Push) in BOTH
   languages. Apply all five principles. Write down explicitly which
   principle fixed which problem.

2. Extend the Bird hierarchy with a third independent behaviour
   (Swimmable). Show the class-explosion math for subclassing, then the
   interface-based fix.

3. Take your Pigeon + FlyingBehaviour code and refactor to constructor
   injection. Note exactly what would change to swap in a different
   FlyingBehaviour.

4. Python only — write the Section 6 list[Flyable] example, append a
   Penguin to it, and run mypy. Paste the error into your README, then
   run the same file without mypy and paste what happens instead.
   Two sentences on what that gap means for a real codebase.

5. Push to GitHub — branch: solid-lecture-complete
```

---

*Post-read · LLD 01 · Next class: Design Patterns — Strategy and the IoC container*
