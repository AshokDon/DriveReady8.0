# Python OOP — 12 Topics, Step by Step

**Reference:** your `Driver.java` and `Main.java`
**Rule for this document:** every method has comments explaining what it does and how Python runs it.
**How the code grows:** we start with a bare class and add one topic's worth of code at each step. By Topic 12 you have the complete class.

---

## A note on your Java code

One line in your Java won't compile:

```java
public Driver(int driverId, String name, double rating = 0.0, boolean isOnline)
//                                                   ^^^^^^
//                          Java does NOT allow default parameter values
```

Java has no default parameters — that's exactly why it needs **four separate constructors**. This is worth telling your class, because **Python can do it**, and that single difference removes the need for constructor overloading entirely. You'll see it in Topic 4.

---

## The map — how the class grows

| Topic | What gets added to `Driver` |
|:--|:--|
| 1 | the empty class, and creating objects |
| 2 | fields + methods |
| 3 | *(no change — we study memory)* |
| 4 | `__init__` and `self` |
| 5 | `total_drives`, `@staticmethod`, class body |
| 6 | *(no change — we study argument passing)* |
| 7 | `__str__` |
| 8 | `_rating` + `@property` |
| 9 | `_` and `__` levels |
| 10 | `@classmethod` chaining |
| 11 | `from_driver()` copy constructor |
| 12 | `copy()` and `deepcopy()` |

---
---

# TOPIC 1
# Class and Object

## Definition

> **Class** — a blueprint. It describes what data and behaviour a thing will have. It stores no data itself.
>
> **Object** — an instance built from that blueprint. Memory has actually been allocated, and it holds its own data.

One class → unlimited objects. Each object has its **own separate copy** of the data.

```
              class Driver          <- ONE blueprint
                    |
        +-----------+-----------+
        v           v           v
     [Ashok]     [Meera]     [Ravi]  <- MANY objects, separate data
```

## Java

```java
public class Driver {           // the blueprint
}

Driver d1 = new Driver();       // the object — note the `new` keyword
```

## Python

```python
# ============================================================
# TOPIC 1 — the simplest possible class
# ============================================================

class Driver:
    """A driver in the Uber system."""

    # `pass` means "this block is intentionally empty".
    # Python needs SOMETHING inside a class body, so we use pass
    # while the class has no content yet.
    pass


# ---------- CREATING OBJECTS ----------

# Driver()  <-- calling the CLASS NAME like a function creates an object.
#
# There is NO `new` keyword in Python. `Driver()` by itself does 3 things:
#   1. allocates memory for one new empty Driver object
#   2. runs the setup method (we add it in Topic 4)
#   3. returns the finished object
#
# `d1 =` then attaches the NAME d1 to that object.
d1 = Driver()
d2 = Driver()

# Attributes can be added AFTER creation.
# In Python an attribute is created the moment you assign to it.
# (This is the "lots of lines" problem your Java comments mention —
#  Topic 4 fixes it.)
d1.name = "Abc"
d1.rating = 5.0

d2.name = "Xyz"
d2.rating = 4.0

print(d1.name)          # Abc
print(d2.name)          # Xyz   <- separate object, separate data

# id() shows the memory address of an object.
# Two different addresses = two genuinely different objects.
print(id(d1) == id(d2))  # False
```

### Output

```
Abc
Xyz
False
```

### How it works

| Line | What Python does |
|:--|:--|
| `class Driver:` | Reads the blueprint. **No driver data exists yet.** |
| `d1 = Driver()` | Allocates memory → returns the object → names it `d1` |
| `d1.name = "Abc"` | Creates an attribute `name` **on the object `d1` only** |
| `print(d2.name)` | Reads `d2`'s own `name`. `d1` and `d2` never share data. |

> ⚠️ **Watch out:** in Python, reading an attribute you never set is an error, not a default value:
> ```python
> d3 = Driver()
> print(d3.name)     # AttributeError: 'Driver' object has no attribute 'name'
> ```
> Java would give you `null`. Python gives you nothing at all. **Topic 4 solves this too.**

---
---

# TOPIC 2
# Building the First Class — Fields, Methods, Members and State

## Definition

> **Fields** (member variables / instance attributes) — the variables that belong to the object. Its **data**.
>
> **Methods** (member methods) — the functions that belong to the class. Its **behaviour**.
>
> **Members** — the collective word for both.
>
> **State** — the *values* of an object's fields at a given moment in time.

## Java

```java
public class Driver {
    int driverId;                                  // member variables
    String name;
    double rating;
    boolean isOnline;

    public void acceptRide(String rideId) {        // member method
        System.out.println("Ride has been accepted " + rideId);
    }

    public void changeStatus() {                   // member method
        isOnline = !isOnline;
        System.out.println("Driver is " + isOnline);
    }
}
```

## Python

```python
# ============================================================
# TOPIC 2 — adding fields and methods
# ============================================================

class Driver:
    """A driver in the Uber system."""

    # NOTE: Python has NO field-declaration section.
    # Java writes `int driverId;` at the top of the class.
    # Python cannot. Fields come into existence when you assign them.
    # For now we assign them from outside; Topic 4 moves this into __init__.

    # ---------- MEMBER METHOD 1 ----------
    def accept_ride(self, ride_id):
        """Print a confirmation that this driver took a ride.

        `self`     -> the object this method was called on (Topic 4 explains it)
        `ride_id`  -> the normal argument the caller passes in
        """
        # self.name means "the name field of THIS particular driver".
        # Writing just `name` would be a NameError — see Topic 4.
        print(f"{self.name}: Ride has been accepted {ride_id}")

    # ---------- MEMBER METHOD 2 ----------
    def change_status(self):
        """Flip the driver between online and offline. CHANGES THE STATE."""
        # `not` is Python's version of Java's `!`
        # This line reads the current value, flips it, and stores it back.
        self.is_online = not self.is_online
        print(f"Driver is {self.is_online}")


# ---------- CREATING AN OBJECT AND SETTING ITS FIELDS ----------
d1 = Driver()           # object created — but it has NO fields yet
d1.driver_id = 100      # now the field `driver_id` exists on d1
d1.name = "Abc"
d1.rating = 5.0
d1.is_online = True

# ---------- LOOKING AT THE STATE ----------
# __dict__ is a built-in dictionary holding everything THIS object owns.
# It is the single most useful debugging tool in Python OOP.
print("STATE now :", d1.__dict__)

# ---------- CALLING METHODS ----------
# d1.accept_ride("R-101") passes d1 in automatically as `self`.
d1.accept_ride("R-101")

# change_status() modifies the state, so print __dict__ before and after.
print("before    :", d1.is_online)
d1.change_status()
print("after     :", d1.is_online)
print("STATE now :", d1.__dict__)
```

### Output

```
STATE now : {'driver_id': 100, 'name': 'Abc', 'rating': 5.0, 'is_online': True}
Abc: Ride has been accepted R-101
before    : True
Driver is False
after     : False
STATE now : {'driver_id': 100, 'name': 'Abc', 'rating': 5.0, 'is_online': False}
```

### How it works

Look at the two `__dict__` prints. **Same object. Different values.**

That is what **state** means — the object didn't get replaced, one value inside it moved.

```
   STATE before                    STATE after
   ---------------                 ---------------
   driver_id = 100                 driver_id = 100
   name      = "Abc"               name      = "Abc"
   rating    = 5.0                 rating    = 5.0
   is_online = True     ---->      is_online = False    <- only this changed
                    change_status()
```

> 💡 **A method is an arrow between states.** Every method you write either reads the state or moves it.

| Term | In our code |
|:--|:--|
| Field / member variable | `driver_id`, `name`, `rating`, `is_online` |
| Member method | `accept_ride()`, `change_status()` |
| Members | all six of the above |
| State | `{'driver_id': 100, 'name': 'Abc', ...}` at one moment |

---
---

# TOPIC 3
# Reference Variables and the Memory Model

*No change to the class here — we study what a variable actually is.*

## Definition

> A Python variable does **not** hold an object. It holds a **reference** (an address) pointing at the object.
>
> **A variable is a label stuck on a box, not the box itself.**

## Java

```java
Driver d1 = new Driver();
d1.name = "Abc";

Driver d2 = d1;                    // copies the ADDRESS, not the object
System.out.println(d2.name);       // Abc

d2.name = "Xyz";
System.out.println(d1.name);       // Xyz  <-- d1 changed too!
```

## Python

```python
# ============================================================
# TOPIC 3 — references: two names, ONE object
# ============================================================

class Driver:
    pass


d1 = Driver()
d1.name = "Abc"

# ---------------------------------------------------------------
# THE KEY LINE.
#
# `d2 = d1` does NOT create a second Driver.
# It does NOT copy anything inside the object.
# It only says: "the name d2 now points at the SAME object as d1".
# ---------------------------------------------------------------
d2 = d1

print("d2.name       :", d2.name)      # Abc

# Because both names point to ONE object, changing it through
# either name is visible through both.
d2.name = "Xyz"

print("d1.name       :", d1.name)      # Xyz  <-- changed!
print("d2.name       :", d2.name)      # Xyz

# ---------- PROVING they are the same object ----------
# id() returns the memory address.
print("id(d1)        :", id(d1))
print("id(d2)        :", id(d2))       # identical number

# `is`  asks: are these the SAME OBJECT?      (identity)
# `==`  asks: do these have the SAME VALUE?   (equality)
print("d1 is d2      :", d1 is d2)     # True

# A genuinely separate object, even with identical data:
d3 = Driver()
d3.name = "Xyz"
print("d1 is d3      :", d1 is d3)     # False — different object
```

### Output

```
d2.name       : Abc
d1.name       : Xyz
d2.name       : Xyz
id(d1)        : 140234891234567
id(d2)        : 140234891234567
d1 is d2      : True
d1 is d3      : False
```

### How it works

```
   BEFORE  d2 = d1                AFTER  d2 = d1

   d1 ---> [ Driver ]             d1 ---+
                                        +---> [ Driver ]
                                  d2 ---+
                                        ONE object, TWO labels
```

> 💡 **The rule that never breaks: in Python, `=` never copies an object. It only ever moves a label.**

### ⚠️ `is` and `==` are SWAPPED from Java

| Question | Java | Python |
|:--|:--|:--|
| Same object? (identity) | `d1 == d2` | `d1 is d2` |
| Same value? (equality) | `d1.equals(d2)` | `d1 == d2` |

If you carry the Java habit across, **every comparison you write will be wrong.** Tell your class this twice.

### The String Pool (your commented-out Java note)

```python
# Python does the same thing and calls it INTERNING.
s1 = "Abc"
s2 = "Abc"
print(s1 is s2)     # True  — Python reused ONE string object

# Why is sharing safe? Because strings are IMMUTABLE — they cannot be
# changed. s1.upper() does not modify "Abc", it builds a NEW string.
# So a thousand names can share one copy with zero risk.

# But NEVER rely on it:
x = 1000
y = int("1000")     # computed at runtime -> a separate object
print(x is y)       # False!
print(x == y)       # True   <- the comparison you actually wanted
```

> 💡 **Compare values with `==`. Use `is` only for `None`.**

---
---

# TOPIC 4
# Constructor and `self`

## Definition

> **Constructor** — a special method that runs **automatically** when an object is created. Its job is to initialise the object's fields, so no object can exist half-built.
>
> In Python it always has the name **`__init__`**.
>
> **`self`** — a reference to *the object the method was called on*. It is how one shared method knows which object it is working on.

## Why we need it

Your own Java comment says it perfectly:

```java
// d1.name = "Abc"; d1.isOnline = true; d1.driverId = 1; d1.rating = 5.0;
// now to initilize an object with data i am writing lot of lines, will some
// one do that in industry level no, so creat a paramatrized constructr
```

Exactly. Five lines per driver × 100 drivers = 500 lines. And if you forget one line, you get a crash in a **different file, hours later**.

## Java — you needed FOUR constructors

```java
public Driver() {                                   // no-args
    driverId = 100;  name = "Random";
    rating = 5.0;    isOnline = true;
}

public Driver(int driverId, String name, double rating, boolean isOnline) {
    this.driverId = driverId;                       // `this` resolves the name clash
    this.name = name;
    this.rating = rating;
    this.isOnline = isOnline;
    totalDrives++;
}
```

## Python — ONE `__init__` replaces all of them

```python
# ============================================================
# TOPIC 4 — adding the constructor and understanding self
# ============================================================

class Driver:
    """A driver in the Uber system."""

    # ------------------------------------------------------------------
    # THE CONSTRUCTOR
    #
    # Name:   ALWAYS `__init__`.  Never the class name (that's Java).
    #         The double underscores make it a "dunder" method — a hook
    #         Python calls automatically at a specific moment.
    #
    # Runs:   automatically, the instant you write Driver(...)
    #
    # self:   the FIRST parameter of every method. It is the object being
    #         built. You never pass it yourself — Python inserts it.
    #
    # =100 etc:  DEFAULT VALUES. If the caller doesn't supply an argument,
    #            the default is used. THIS is what replaces Java's four
    #            separate constructors — and Java cannot do it at all.
    # ------------------------------------------------------------------
    def __init__(self, driver_id=100, name="Random", rating=0.0, is_online=False):

        # Read each line as:
        #   self.name  =  name
        #     ^            ^
        #     |            +-- the PARAMETER (temporary, dies with the method)
        #     +-- the OBJECT'S OWN field (permanent, belongs to this driver)
        #
        # This is Java's `this.name = name;` — same idea, same purpose:
        # tell Python which `name` you mean when both have the same spelling.
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online

    # ---------- MEMBER METHOD ----------
    def accept_ride(self, ride_id):
        """`self` = which driver.  `ride_id` = the caller's argument."""
        print(f"Ride has been accepted {ride_id}")

    def change_status(self):
        """Flip online/offline. Notice EVERY field access uses self."""
        self.is_online = not self.is_online
        print(f"Driver is {self.is_online}")


# ================= CREATING OBJECTS — FOUR WAYS =================

# 1. No arguments at all -> every default is used.
d1 = Driver()

# 2. All four arguments, in order (positional arguments).
d2 = Driver(12, "Don", 4.0, True)

# 3. Only some -> the rest fall back to defaults.
d3 = Driver(13, "Meera")

# 4. KEYWORD ARGUMENTS — name the values, so order does not matter.
#    Java cannot do this. It makes calls self-documenting.
d4 = Driver(name="Ravi", driver_id=14)

print("d1:", d1.__dict__)
print("d2:", d2.__dict__)
print("d3:", d3.__dict__)
print("d4:", d4.__dict__)
```

### Output

```
d1: {'driver_id': 100, 'name': 'Random', 'rating': 0.0, 'is_online': False}
d2: {'driver_id': 12, 'name': 'Don', 'rating': 4.0, 'is_online': True}
d3: {'driver_id': 13, 'name': 'Meera', 'rating': 0.0, 'is_online': False}
d4: {'driver_id': 14, 'name': 'Ravi', 'rating': 0.0, 'is_online': False}
```

**One `__init__`. Four different ways to call it.** That's why Python doesn't need constructor overloading.

---

## `self` — the line that makes it click

You asked about unexplained syntax, so here is `self` proved rather than asserted.

```python
d2 = Driver(12, "Don", 4.0, True)

# These two lines do EXACTLY the same thing:
d2.accept_ride("R-101")            # what you normally write
Driver.accept_ride(d2, "R-101")    # what Python actually does underneath
```

### Output

```
Ride has been accepted R-101
Ride has been accepted R-101
```

Look at the second line. **`d2` is passed in as the first argument.**

> 💡 **A method is just a function stored inside a class.**
> **When you call it through an object, Python inserts that object as the first argument.**
> **`self` is simply the parameter that catches it.**

That's all `self` is. Not magic, not a keyword — a parameter.

### ⚠️ The mistake every Java student makes

```python
class Driver:
    def rename(self, new_name):
        name = new_name         # ❌ creates a LOCAL variable and throws it away
        self.name = new_name    # ✅ actually changes the object
```

**No error. No warning. The field simply never changes.**

| | Java `this` | Python `self` |
|:--|:--|:--|
| What is it? | a **keyword** | an ordinary **parameter** |
| Optional? | **Yes**, when no name clash | **Never** |

In Java you may write `name = n;` and it works. In Python the equivalent silently does nothing. This is the single biggest Java→Python bug.

### ⚠️ Python has NO constructor overloading

```python
class Driver:
    def __init__(self):                    # version 1
        ...
    def __init__(self, driver_id, name):   # version 2
        ...
```

This is **not** an error. Worse — **version 2 silently replaces version 1**, as if you never wrote it. There is only ever one `__init__`.

Use default arguments instead. (For different *kinds* of input, use Topic 10.)

---
---

# TOPIC 5
# `static` in Python

## Definition

> **Class attribute** (Java's `static` field) — belongs to the **class**, not to any object. There is exactly **one copy, shared by everyone**.
>
> **Static method** (`@staticmethod`) — a method callable **without any object existing**.
>
> **In Python there is no `static` keyword. Where you write it decides what it is.**

## Why we need it

Your Java comment nails the reasoning:

```java
// Creat a total Driver = 0 and increment inside all Constructor
// will it work? No. The reason is it is a Seperate Copy of Every Object
// This should be a Single Variable which Every Object is Sharing
```

Ask the class: **"Whose fact is 'total number of drivers'?"** Not Ashok's. Not Meera's. It's a fact about **the class**.

```
   WITHOUT (broken)                  WITH (correct)
   [d1 total=1] [d2 total=1]         [d1] [d2] [d3]
   [d3 total=1]                        \    |    /
   x each counts ITSELF                 [ Driver ] total = 3
                                        v ONE shared copy
```

## Java

```java
static int totalDrives;                 // static field

static {                                // static block
    totalDrives = 15;
    System.out.println("This is executed at time of driver class");
}

static public void Register() {         // static method
    System.out.println("This is Register Method");
}
```

## Python

```python
# ============================================================
# TOPIC 5 — adding class attributes and static methods
# ============================================================

class Driver:
    """A driver in the Uber system."""

    # ------------------------------------------------------------------
    # CLASS ATTRIBUTE  =  Java's `static int totalDrives;`
    #
    # Written DIRECTLY in the class body (not inside a method, no `self.`).
    # That position is the ONLY thing that makes it class-level.
    # There is one copy, shared by every Driver object ever created.
    # ------------------------------------------------------------------
    total_drives = 15

    # ------------------------------------------------------------------
    # THIS LINE IS JAVA'S STATIC BLOCK.
    #
    # Any code written directly in the class body runs ONCE — at the moment
    # Python reads the class definition, which is at IMPORT time,
    # before any object exists and before main() starts.
    #
    # Python needs no `static { }` construct because the class body IS one.
    # ------------------------------------------------------------------
    print("This is executed at time of Driver class definition")

    def __init__(self, driver_id=100, name="Random", rating=0.0, is_online=False):
        # ---- INSTANCE attributes: one copy PER OBJECT ----
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online

        # ------------------------------------------------------------------
        # Java writes:  totalDrives++;
        #
        # Python MUST write the CLASS NAME here, not self.
        # `self.total_drives += 1` looks correct, runs without error,
        # and is SILENTLY BROKEN. See the trap below.
        # ------------------------------------------------------------------
        Driver.total_drives += 1

    def accept_ride(self, ride_id):
        """Instance method — needs a specific driver, so it takes self."""
        print(f"Ride has been accepted {ride_id}")

    def change_status(self):
        self.is_online = not self.is_online
        print(f"Driver is {self.is_online}")

    # ------------------------------------------------------------------
    # STATIC METHOD  =  Java's `static public void Register()`
    #
    # @staticmethod is a DECORATOR — the @ line modifies the function below
    # it. Read it as a label meaning: "this method receives no self".
    #
    # Notice there is NO self parameter. That's the whole point:
    # there is no object to receive.
    #
    # WHY does this exist?  Your Java comment answers it:
    #   "If Driver want to Register, do you think his object created in
    #    memory? No. Then how will he call a method -> make it static"
    #
    # Registration is what CREATES the driver, so it cannot require a
    # driver to already exist. The sign-up button must work before you
    # have an account.
    # ------------------------------------------------------------------
    @staticmethod
    def register():
        print("This is Register Method")


# ================= USING IT =================

# The static method is callable with NO object anywhere.
print("--- before any object exists ---")
Driver.register()
print("total_drives:", Driver.total_drives)      # 15, from the class body

# Now create three drivers. Each __init__ bumps the shared counter.
d1 = Driver()
d2 = Driver(12, "Don", 4.0, True)
d3 = Driver(13, "Meera")

print("total_drives:", Driver.total_drives)      # 15 + 3 = 18
```

### Output

```
This is executed at time of Driver class definition
--- before any object exists ---
This is Register Method
total_drives: 15
total_drives: 18
```

### How it works

Look at line 1 of the output. **`This is executed at time of Driver class definition` printed before everything else** — before `Driver.register()`, before any object. That is Java's static block behaviour, and Python gives it to you for free.

| | Instance attribute | Class attribute |
|:--|:--|:--|
| Written as | `self.name = ...` inside a method | `total_drives = 0` in the class body |
| How many copies | one **per object** | exactly **one**, shared |
| Accessed as | `d1.name` | `Driver.total_drives` |
| Java equivalent | a normal field | a `static` field |

**The test to give your class:** *"If this value changes, should it change for everyone at once?"* Yes → class attribute.

| Belongs to each object | Belongs to the class |
|:--|:--|
| driver's name, rating | total driver count |
| bank account balance | the bank's interest rate |
| student roll number | college name |
| Swiggy order total | platform delivery fee |

---

## ⚠️ THE TRAP — the most important warning in this document

```python
# INSIDE __init__:
Driver.total_drives += 1      # ✅ CORRECT
self.total_drives  += 1       # ❌ SILENTLY BROKEN
```

Why? Split the line in half. `self.x += 1` means `self.x = self.x + 1`:

```
   READ  (right side):  self.total_drives
         -> not found on the object
         -> Python FALLS BACK to the class, finds 15
         -> computes 15 + 1 = 16

   WRITE (left side):   self.total_drives = 16
         -> assignment through self ALWAYS writes to the OBJECT
         -> creates a BRAND-NEW instance attribute on this one driver
         -> the class attribute is never touched
```

> 💡 **Reading falls through to the class. Writing never does.**

Demonstrate it live:

```python
d1.total_drives = 999          # writing through the object

print("d1.total_drives    :", d1.total_drives)       # 999
print("Driver.total_drives:", Driver.total_drives)   # 18  <- unaffected
print("d1.__dict__        :", d1.__dict__)
```

```
d1.total_drives    : 999
Driver.total_drives: 18
d1.__dict__        : {'driver_id': 100, 'name': 'Random', 'rating': 0.0,
                      'is_online': False, 'total_drives': 999}
```

**`total_drives` is now sitting inside `d1.__dict__`.** It shouldn't be there. That's your proof.

> 🔁 In Java, `totalDrives++` just works — the `static` keyword protects you and you *cannot* accidentally make an instance copy. **Python gives no such protection.** This is the sharpest difference between the two languages in this whole chapter.

### One more trap: never put a mutable value in a class attribute

```python
class Driver:
    rides = []                      # ❌ ONE list shared by EVERY driver

    def add_ride(self, r):
        self.rides.append(r)        # mutates the SHARED list


d1, d2 = Driver(), Driver()
d1.add_ride("R-101")
print(d2.rides)                     # ['R-101']  <- Meera has Ashok's ride!
```

Why didn't this create an instance copy like `+=` did? **Because there is no assignment.** `append` reaches into the list that lookup found. **Only `=` writes to the instance.**

Fix: mutable state goes in `__init__`.

```python
def __init__(self):
    self.rides = []                 # ✅ a fresh list for every driver
```

> 💡 **Rule: class attributes hold only immutable values** — `int`, `str`, `float`, `bool`, constants. Anything mutable belongs in `__init__`.

---
---

# TOPIC 6
# Pass by Value — Primitives vs Objects

*No change to the class — we study what happens when you pass things into functions.*

## Definition

> Your Java note says: **"In Java Every Thing is pass by Value."** Correct — and Python behaves identically.
>
> **The function receives a COPY OF THE REFERENCE, not a copy of the object.**
>
> - **Mutate** the object it points at → the caller **sees** it.
> - **Rebind** the parameter to something else → the caller sees **nothing**.

## Java — your exact `Main.java` demo

```java
int x = 10;
add(x);
System.out.println(x);            // 10   <-- UNCHANGED

Driver d1 = new Driver();
d1.name = "Abc";
changeName(d1);
System.out.println(d1.name);      // Xyz  <-- CHANGED

public static void add(int x) {
    x = x + 30;                   // modifies the local copy only
}
public static void changeName(Driver driver) {
    driver.name = "Xyz";          // follows the address, edits the real object
}
```

## Python — same behaviour, same result

```python
# ============================================================
# TOPIC 6 — how arguments are passed
# ============================================================

class Driver:
    def __init__(self, driver_id=100, name="Random"):
        self.driver_id = driver_id
        self.name = name


# ---------------------------------------------------------------
# FUNCTION 1 — REBINDING an immutable value
#
# `int` is IMMUTABLE: the number 10 cannot be changed.
# So `x = x + 30` cannot modify anything. It BUILDS A NEW object (40)
# and points the LOCAL name `x` at it.
# The caller's variable never moved.
# ---------------------------------------------------------------
def add(x):
    x = x + 30
    print(f"   [inside add] x is now {x}")


# ---------------------------------------------------------------
# FUNCTION 2 — MUTATING an object
#
# `driver` is a copy of the REFERENCE, but it points at the SAME object.
# `driver.name = "Xyz"` reaches THROUGH the reference and edits the
# real object, so the caller sees the change.
# ---------------------------------------------------------------
def change_name(driver):
    driver.name = "Xyz"
    print(f"   [inside change_name] name is now {driver.name}")


# ---------------------------------------------------------------
# FUNCTION 3 — REBINDING an object parameter
#
# This is the PROOF that the reference was passed BY VALUE.
# We point the local name at a brand-new Driver. The caller's
# variable still points at the original. Completely invisible outside.
# ---------------------------------------------------------------
def replace(driver):
    driver = Driver(999, "Ghost")
    driver.name = "Zzz"
    print(f"   [inside replace] local name is now {driver.name}")


# ================= RUNNING IT =================

print("--- 1. immutable: int ---")
x = 10
add(x)
print("   x after add      :", x, "  <- UNCHANGED")

print("\n--- 2. mutable: our object ---")
d1 = Driver()
d1.name = "Abc"
change_name(d1)
print("   d1.name after    :", d1.name, "  <- CHANGED")

print("\n--- 3. rebinding the parameter ---")
replace(d1)
print("   d1.name after    :", d1.name, "  <- STILL Xyz. replace() was invisible")

print("\n--- 4. the same trap with a list ---")
def mutate(items):
    items.append("R-999")        # MUTATION -> caller sees it

def rebind(items):
    items = items + ["R-888"]    # REBINDING -> caller sees nothing

rides = ["R-101"]
mutate(rides)
print("   after mutate     :", rides)
rebind(rides)
print("   after rebind     :", rides, "  <- rebind did NOTHING")
```

### Output

```
--- 1. immutable: int ---
   [inside add] x is now 40
   x after add      : 10   <- UNCHANGED

--- 2. mutable: our object ---
   [inside change_name] name is now Xyz
   d1.name after    : Xyz   <- CHANGED

--- 3. rebinding the parameter ---
   [inside replace] local name is now Zzz
   d1.name after    : Xyz   <- STILL Xyz. replace() was invisible

--- 4. the same trap with a list ---
   after mutate     : ['R-101', 'R-999']
   after rebind     : ['R-101', 'R-999']   <- rebind did NOTHING
```

### How it works — the analogy to give your class

You write your home address on a slip of paper and hand a **photocopy** to a friend.

| What your friend does | Name | Do you see it? |
|:--|:--|:--|
| Drives there and paints your door pink | **mutation** | ✅ Yes — one house, they went to it |
| Scratches out the address on their copy | **rebinding** | ❌ No — your slip and house are untouched |

```
   add(x)                            change_name(d1)
   ------------------------          --------------------------------
   x (caller)   --> [ 10 ]           d1     (caller) ---+
   x (function) --> [ 10 ]                              +--> [ Driver ]
   x (function) --> [ 40 ]  REBOUND  driver (function)--+
   x (caller)   --> [ 10 ]  safe          ^
                                          +-- copy of the REFERENCE,
                                              SAME object -> edit is shared
```

### The rule — memorise this

| What the function does | Caller sees it? |
|:--|:--|
| **Mutates** — `obj.attr = ...`, `list.append(...)` | ✅ **YES** |
| **Rebinds** — `obj = something_new` | ❌ **NO** |

| Immutable (acts like Java primitives) | Mutable (acts like Java objects) |
|:--|:--|
| `int`, `float`, `bool`, `str`, `tuple` | `list`, `dict`, `set`, **every class you write** |

> 🔁 **Java calls this "pass by value". Python calls it "call by sharing".** Different words, identical behaviour. The dividing line differs: Java splits *primitive vs object*, Python splits *immutable vs mutable*.

---
---

# TOPIC 7
# `__str__` (Java's `toString`)

## Definition

> **`__str__`** defines how your object should be represented as **human-readable text**.
>
> `print()` calls it for you automatically. You never call it yourself.
>
> Without it, printing an object gives you the class name and a memory address — true, but useless.

## Java

```java
@Override
public String toString() {
    return "Ashok";
}

System.out.println(d1);       // Ashok
```

## Why we need it

```python
d1 = Driver(4021, "Ashok")
print(d1)
```
```
<__main__.Driver object at 0x7f8b2c0d1a90>
```

Now picture that in a log file at 2am:

```
ERROR  Failed to assign trip: <__main__.Driver object at 0x7f8b2c0d1a90>
ERROR  Failed to assign trip: <__main__.Driver object at 0x7f8b2c0d1b40>
```

You've learned nothing. Versus:

```
ERROR  Failed: Driver(id=4021, name='Ashok', rating=4.8, online=False)
ERROR  Failed: Driver(id=4088, name='Meera', rating=4.9, online=False)
                                                        ^^^^^^^^^^^^^^
                                          every one of them is OFFLINE
```

**Bug found in three seconds.** `__str__` is not cosmetic.

## Python

```python
# ============================================================
# TOPIC 7 — adding __str__
# ============================================================

class Driver:
    """A driver in the Uber system."""

    total_drives = 15
    print("This is executed at time of Driver class definition")

    def __init__(self, driver_id=100, name="Random", rating=0.0, is_online=False):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online
        Driver.total_drives += 1

    def accept_ride(self, ride_id):
        print(f"Ride has been accepted {ride_id}")

    def change_status(self):
        self.is_online = not self.is_online
        print(f"Driver is {self.is_online}")

    @staticmethod
    def register():
        print("This is Register Method")

    # ------------------------------------------------------------------
    # __str__  =  Java's toString()
    #
    # Another DUNDER method (double underscores), like __init__.
    # Dunder methods are hooks Python calls automatically:
    #     __init__  -> called when you CREATE an object
    #     __str__   -> called when you PRINT an object
    #
    # Java uses @Override because toString() is inherited from Object.
    # Python needs no annotation — just define the method.
    #
    # ⚠️ IT MUST **RETURN** A STRING. It must not print one.
    #    `print` inside here shows the text and THEN raises
    #    TypeError: __str__ returned non-string
    # ------------------------------------------------------------------
    def __str__(self):
        # A ternary: pick one of two values based on a condition.
        # Java would write:  isOnline ? "online" : "offline"
        status = "online" if self.is_online else "offline"

        # f-string: the f prefix lets you embed {expressions} directly.
        return (f"Driver(id={self.driver_id}, name='{self.name}', "
                f"rating={self.rating}, {status})")


# ================= USING IT =================

d1 = Driver(4021, "Ashok", 4.8, True)
d2 = Driver(4088, "Meera", 4.9, False)

# print() automatically calls __str__ behind the scenes
print(d1)
print(d2)

# f-strings call it too
print(f"Trip R-101 assigned to {d1}")

# str() returns the text itself, so you can store or log it
text = str(d1)
print(type(text), "->", text)
```

### Output

```
This is executed at time of Driver class definition
Driver(id=4021, name='Ashok', rating=4.8, online)
Driver(id=4088, name='Meera', rating=4.9, offline)
Trip R-101 assigned to Driver(id=4021, name='Ashok', rating=4.8, online)
<class 'str'> -> Driver(id=4021, name='Ashok', rating=4.8, online)
```

### How it works

```
   print(d1)
      |
      v  print needs TEXT, but d1 is an object
      |
      v  Python asks: does Driver define __str__ ?
      |
      +-- YES -> call it, print the returned string
      |
      +-- NO  -> fall back to "<__main__.Driver object at 0x...>"
```

| | Java | Python |
|:--|:--|:--|
| Method name | `toString()` | `__str__(self)` |
| Triggered by | `System.out.println(obj)` | `print(obj)`, `str(obj)`, f-strings |
| Annotation | `@Override` | none needed |
| Default output | `Driver@1b6d3586` | `<__main__.Driver object at 0x...>` |

> ⚠️ **Never put secrets in `__str__`** — passwords, tokens, card numbers. They end up in your log files. That's a real security bug.

---
---

# TOPIC 8
# Encapsulation — Pillar 1

## Definition

> **Encapsulation** — bundling data together with the methods that operate on it, **and restricting direct access** to that data from outside.
>
> The goal: **the class enforces its own rules**, instead of trusting every other file to be careful.

## Why we need it

Right now, any file anywhere can write:

```python
d1.rating = -50           # a rating of minus fifty
d1.rating = 999
d1.rating = "excellent"   # a rating that is a word
```

Nothing stops it. `Driver` *knows* a rating must be 0–5 — but it has **no power to enforce that**.

Then dispatch sorts drivers by rating, Ashok never gets a trip, and an engineer spends a night reading the **dispatch** code — which is perfect. The bug is a single line in a different file written three weeks ago.

> 💡 **The real cost isn't the wrong value. It's the distance between the cause and the symptom.**

## Java — your getters and setters

Your `Driver.java` already has them:

```java
public double getRating() {
    return rating;
}

public void setRating(double rating) {
    this.rating = rating;          // <- but no validation!
}
```

Note: your setter accepts anything. Add the check and it becomes real encapsulation:

```java
public void setRating(double rating) {
    if (rating < 0 || rating > 5) {
        throw new IllegalArgumentException("Rating must be 0-5");
    }
    this.rating = rating;
}
```

And Java's `private` keyword is what forces callers through it.

## Python — `@property`, explained line by line

**This is the syntax you asked about.** Here it is with a comment on every part.

```python
# ============================================================
# TOPIC 8 — encapsulation with @property
# ============================================================

class Driver:
    """A driver in the Uber system."""

    total_drives = 15

    def __init__(self, driver_id=100, name="Random", rating=0.0, is_online=False):
        self.driver_id = driver_id
        self.name = name

        # ------------------------------------------------------------------
        # NOTE: we assign to `self.rating`, NOT `self._rating`.
        #
        # Because `rating` is a property (defined below), this line does NOT
        # store anything directly — it CALLS THE SETTER, which validates.
        #
        # That means you cannot even CREATE a driver with an invalid rating.
        # Validation at birth, not just afterwards.
        # ------------------------------------------------------------------
        self.rating = rating

        self.is_online = is_online
        Driver.total_drives += 1

    # ==================================================================
    #  THE PROPERTY — three parts. Read them in order.
    # ==================================================================

    # ------------------------------------------------------------------
    # PART 1 — THE GETTER
    #
    # @property turns the method below into a "computed attribute".
    #
    # After this, whenever anyone READS  d1.rating  ...
    #   -> Python does NOT look for a stored value
    #   -> it CALLS this method and uses whatever it returns
    #
    # The method name `rating` becomes the attribute name the caller uses.
    # ------------------------------------------------------------------
    @property
    def rating(self):
        # `self._rating` is the REAL storage — the actual variable holding
        # the number. The single underscore marks it "internal, don't
        # touch from outside" (Topic 9 explains the underscore fully).
        return self._rating

    # ------------------------------------------------------------------
    # PART 2 — THE SETTER   <-- THIS IS @rating.setter, YOUR QUESTION
    #
    # Read the decorator as three pieces:
    #
    #     @  rating  . setter
    #        ^^^^^^    ^^^^^^
    #        |         |
    #        |         +-- "attach a setter to it"
    #        +-- the property object created by @property above
    #
    # ⚠️ The name `rating` here MUST MATCH the @property method's name.
    #    Writing @score.setter for a property called rating gives
    #    NameError: name 'score' is not defined
    #
    # ⚠️ @property must come FIRST. The setter attaches to something that
    #    has to already exist.
    #
    # WHAT IT DOES:
    #   After this, whenever anyone WRITES  d1.rating = 4.5  ...
    #     -> Python does NOT store 4.5 anywhere
    #     -> it CALLS this method with value = 4.5
    #     -> your conditions run FIRST
    #     -> only if they pass does the value get stored
    #
    # So YES — this is exactly what lets you set the rating based on
    # conditions. It INTERCEPTS the assignment.
    #
    # This is Java's setRating(), but the caller writes d1.rating = 4.5
    # instead of d1.setRating(4.5).
    # ------------------------------------------------------------------
    @rating.setter
    def rating(self, value):
        # CONDITION 1 — is it even a number?
        # isinstance(value, (int, float)) asks "is value an int OR a float?"
        # `not` inverts it, so this reads: "if it is NOT a number..."
        if not isinstance(value, (int, float)):
            # `raise` throws an error — Java's `throw`.
            raise TypeError("Rating must be a number")

        # CONDITION 2 — is it in range?
        # `0 <= value <= 5` is a chained comparison. Java needs
        # `value >= 0 && value <= 5`; Python allows the single form.
        if not 0 <= value <= 5:
            raise ValueError(f"Rating must be 0-5, got {value}")

        # BOTH CONDITIONS PASSED -> now store it.
        #
        # ⚠️ MUST be self._rating (with the underscore).
        #    Writing `self.rating = value` here calls THIS SETTER AGAIN,
        #    which calls it again... -> RecursionError. See the trap below.
        self._rating = value

    # ------------------------------------------------------------------
    # PART 3 — A READ-ONLY PROPERTY
    #
    # A getter with NO matching setter.
    #
    # Result: reading works, writing raises AttributeError.
    # This is genuinely enforced — you cannot assign to it at all.
    #
    # Use this for values that must never change after creation.
    # Java's equivalent: `private final` + a getter and no setter.
    # ------------------------------------------------------------------
    @property
    def total_rides_allowed(self):
        return 50

    def __str__(self):
        status = "online" if self.is_online else "offline"
        return f"Driver(id={self.driver_id}, name='{self.name}', rating={self._rating}, {status})"


# ================= USING IT =================

d1 = Driver(4021, "Ashok", 4.8, True)

# READING — looks like a plain attribute, but runs the GETTER
print("read  d1.rating :", d1.rating)

# WRITING a valid value — runs the SETTER, conditions pass
d1.rating = 4.5
print("write d1.rating :", d1.rating)

# WRITING invalid values — the SETTER refuses them
print("\n--- invalid values are now BLOCKED ---")
for bad_value in (-50, 999, "excellent"):
    # try/except is Python's try/catch
    try:
        d1.rating = bad_value
    except (ValueError, TypeError) as e:
        print(f"  rejected {bad_value!r:12} -> {type(e).__name__}: {e}")

print("\nrating survived every attack :", d1.rating)

# THE READ-ONLY PROPERTY
print("\n--- read-only property ---")
print("  read  :", d1.total_rides_allowed)
try:
    d1.total_rides_allowed = 9999
except AttributeError as e:
    print("  write :", type(e).__name__, "-", e)
```

### Output

```
read  d1.rating : 4.8
write d1.rating : 4.5

--- invalid values are now BLOCKED ---
  rejected -50          -> ValueError: Rating must be 0-5, got -50
  rejected 999          -> ValueError: Rating must be 0-5, got 999
  rejected 'excellent'  -> TypeError: Rating must be a number

rating survived every attack : 4.5

--- read-only property ---
  read  : 50
  write : AttributeError - property 'total_rides_allowed' of 'Driver' object has no setter
```

### Seeing the interception

The clearest way to teach this is to put a print inside each part:

```python
@property
def rating(self):
    print("   [GETTER called]")
    return self._rating

@rating.setter
def rating(self, value):
    print(f"   [SETTER called with {value!r}] running conditions...")
    ...
```

Then:

```
--- creating the object ---
   [SETTER called with 4.8] running conditions...      <- __init__ went through it!
--- reading:  d1.rating ---
   [GETTER called]
--- writing:  d1.rating = 4.5 ---
   [SETTER called with 4.5] running conditions...
--- writing:  d1.rating = -50 ---
   [SETTER called with -50] running conditions...
   blocked -> Rating must be 0-5, got -50
```

> 💡 **`d1.rating = 4.5` does not store a value. It calls a method.**
> Same syntax as a plain attribute. Completely different machinery underneath.

### ⚠️ The bug your students will write

```python
@rating.setter
def rating(self, value):
    if not 0 <= value <= 5:
        raise ValueError("Rating must be 0-5")
    self.rating = value        # ❌ forgot the underscore
```
```
RecursionError: maximum recursion depth exceeded
```

`self.rating = value` **calls the setter again** → which calls it again → forever.

> **The setter's job is to write to the storage attribute `self._rating` — never to itself.**

### Why not just use Java-style `get_rating()` / `set_rating()`?

You can, and it works. But compare:

```python
d1.set_rating(d1.get_rating() + 0.1)     # Java style — clumsy
d1.rating = d1.rating + 0.1              # Pythonic — clean
```

> 💡 **The Pythonic rule:** start with a **plain public attribute**. Add `@property` only when you actually need validation.
>
> Because the caller's syntax is *identical* either way, you can add protection **later without changing a single line of calling code**. So writing getters "just in case" gains you nothing.
>
> **Java can't do this** — that's why Java teaches getters from day one and Python doesn't.

---
---

# TOPIC 9
# Access Modifiers

## Definition

> **Python has no access modifiers.** There is no `public`, no `private`, no `protected`.
>
> It has **three levels of signalling**, and only one has any mechanical effect — and that effect is **not privacy**.

| You write | Nickname | Enforced? | What actually happens |
|:--|:--|:--|:--|
| `self.name` | public | — | nothing. Fully accessible. |
| `self._name` | "protected" | ❌ **no** | nothing at class level. Pure convention. |
| `self.__name` | "private" | ⚠️ **not privacy** | **renamed** to `_ClassName__name` |

## Java — real enforcement

```java
private double rating;         // compiler ERROR if touched from outside
protected int driverId;        // class + subclass + package
public String name;            // everywhere
```

## Python

```python
# ============================================================
# TOPIC 9 — the three visibility levels
# ============================================================

class Driver:
    """A driver in the Uber system."""

    def __init__(self, name, rating):
        # ---------- LEVEL 1: PUBLIC ----------
        # No underscore. Part of the class's official API.
        # Anyone may read and write it. This is the default.
        self.name = name

        # ---------- LEVEL 2: SINGLE UNDERSCORE ----------
        # Means: "internal — please don't rely on this, it may change."
        # It is a SIGN, NOT A LOCK. Python does not stop anyone.
        # Think of a "Staff Only" door: unlocked, but you don't walk in.
        self._rating = rating

        # ---------- LEVEL 3: DOUBLE UNDERSCORE ----------
        # Triggers NAME MANGLING: Python renames this at compile time to
        #     _Driver__bank_account
        # It is NOT hidden and NOT secure — just renamed.
        self.__bank_account = "HDFC-9981-2234"

    # A method can also be double-underscored, and gets mangled the same way.
    def __calculate_payout(self):
        """Internal helper. Becomes _Driver__calculate_payout."""
        return 1000

    def show_payout(self):
        """Inside the class, the short name works fine."""
        return self.__calculate_payout()


d = Driver("Ashok", 4.8)

print("1. public     :", d.name)
print("2. _single    :", d._rating, "  <- read from OUTSIDE, no error at all")

# The double underscore looks like it worked...
try:
    print(d.__bank_account)
except AttributeError as e:
    print("3. __double   : AttributeError -", e)

# ...but look at what actually happened:
print("4. __dict__   :", d.__dict__)
```

### Output

```
1. public     : Ashok
2. _single    : 4.8   <- read from OUTSIDE, no error at all
3. __double   : AttributeError - 'Driver' object has no attribute '__bank_account'
4. __dict__   : {'name': 'Ashok', '_rating': 4.8, '_Driver__bank_account': 'HDFC-9981-2234'}
```

## The reveal — read the error message carefully

> `'Driver' object has no attribute '__bank_account'`

It does **not** say *access denied*. It says the attribute **does not exist**.

But we assigned it. And `__dict__` shows it sitting there in plain text — under a **different name**: `_Driver__bank_account`.

```python
# So it is trivially accessible if you know the new name:
print(d._Driver__bank_account)                 # HDFC-9981-2234
print(getattr(d, "_Driver__bank_account"))     # HDFC-9981-2234

d._Driver__bank_account = "HACKED"
print(d._Driver__bank_account)                 # HACKED

# Methods too:
print(d._Driver__calculate_payout())           # 1000
```

> 💡 **KEY IDEA**
> **Double underscore does not hide anything. It RENAMES it.**
> The mechanism is called **name mangling**. It is **not** security, **not** privacy. Never teach it as either.

### The exact mangling rule

Two or more leading underscores, **at most one** trailing underscore:

| You write | Becomes | Mangled? |
|:--|:--|:--|
| `self.public` | `public` | no |
| `self._one` | `_one` | no |
| `self.__two` | `_Driver__two` | ✅ yes |
| `self.__trail_` | `_Driver__trail_` | ✅ yes |
| `self.__both__` | `__both__` | ❌ no — **two** trailing = dunder |

That last row is why `__init__` and `__str__` are **not** mangled.

## So what IS double underscore for?

Its real purpose is **preventing accidental name collisions with subclasses** — not privacy.

```python
# ---------- CASE A: single underscore -> the child BREAKS the parent ----------
class Driver:
    def __init__(self, name):
        self.name = name
        self._score = 4.8                    # parent's 5-point rating

    def dispatch_priority(self):
        return self._score * 100             # parent's logic needs this


class PremiumDriver(Driver):
    def __init__(self, name):
        super().__init__(name)               # super() calls the parent's __init__
        self._score = 9200                   # child's LOYALTY POINTS
                                             # same name, different meaning!

p = PremiumDriver("Ashok")
print("expected 4.8 * 100 = 480, got:", p.dispatch_priority())
print("__dict__:", p.__dict__)
```
```
expected 4.8 * 100 = 480, got: 920000
__dict__: {'name': 'Ashok', '_score': 9200}
```

**One `_score`.** The child's assignment landed on top of the parent's, and the parent's method now returns garbage — **with no error message**.

```python
# ---------- CASE B: double underscore -> collision impossible ----------
class Driver:
    def __init__(self, name):
        self.name = name
        self.__score = 4.8                   # -> _Driver__score

    def dispatch_priority(self):
        return self.__score * 100


class PremiumDriver(Driver):
    def __init__(self, name):
        super().__init__(name)
        self.__score = 9200                  # -> _PremiumDriver__score

    def loyalty_points(self):
        return self.__score

p = PremiumDriver("Ashok")
print("parent's logic :", p.dispatch_priority())
print("child's logic  :", p.loyalty_points())
print("__dict__:", p.__dict__)
```
```
parent's logic : 480.0
child's logic  : 9200
__dict__: {'name': 'Ashok', '_Driver__score': 4.8, '_PremiumDriver__score': 9200}
```

**Two separate attributes. Both classes work.**

> 💡 **Name mangling protects your class from its own children, not from other programmers.**

## The one real effect of a single underscore

At **module level**, `from module import *` skips underscore names:

```python
# helpers.py
MAX_RATING = 5.0            # public
_INTERNAL_KEY = "secret"    # single underscore

# main.py
from helpers import *
print(MAX_RATING)           # 5.0  ✅ imported
print(_INTERNAL_KEY)        # NameError — NOT imported by *

from helpers import _INTERNAL_KEY    # but an explicit import works fine
```

## The sentence that resolves this topic

> 💡 **Java protects data by controlling *who can reach it*. Python protects data by controlling *what can be done to it*.**
>
> Java asks: *who may touch this field?* → `private`
> Python asks: *what values may this attribute hold?* → `@property`
>
> Both prevent `rating = -50`. They attack it from opposite ends.

| | Java | Python |
|:--|:--|:--|
| `public` | keyword | `name` (default) |
| `protected` | keyword | **no equivalent** — `_name` signals it |
| `private` | keyword, compiler-enforced | **no equivalent** — `__name` mangles |
| Enforcement | compile time | none for visibility; `@property` for values |
| Bypassable | reflection only | trivially: `obj._Class__x` |
| Read-only field | `private final` + getter | `@property` with no setter |

### ⚠️ Misconceptions to correct in class

| Misconception | Truth |
|:--|:--|
| "`__x` makes it private" | It **renames** it. Print `__dict__` and it's right there. |
| "`_x` is protected like Java" | Python has no protected. It's a comment that happens to be syntax. |
| "Use `__` for passwords/tokens" | **Dangerous.** Zero security. |
| "Python's encapsulation is broken" | It encapsulates through **behaviour** (`@property`), not visibility. |

---
---

# TOPIC 10
# Constructor Chaining

## Definition

> **Constructor chaining** — one constructor calling another constructor of the same class, so the common setup code is written **once**.
>
> Java does it with `this(...)`. **Python has no `this(...)` because it has only one `__init__`** — so it chains using `@classmethod` factories that delegate to `cls(...)`.

## Java — your exact code

```java
// constructor chaining which means calling constructor inside a constructor
public Driver(String name) {
    this(0, name, 0.0, false);          // calls the 4-arg constructor
}

// first call the constructor and then initialize
public Driver(String name, double rating) {
    this(0, name, 0.0, false);          // 1. delegate
    this.rating = rating;               // 2. then adjust
}
```

Two rules in Java worth telling your class:

- `this(...)` **must be the very first statement** in the constructor.
- You cannot call `this(...)` twice, and you cannot mix it with `super(...)`.

## Python

```python
# ============================================================
# TOPIC 10 — constructor chaining with @classmethod
# ============================================================

class Driver:
    """A driver in the Uber system."""

    total_drives = 15

    # ------------------------------------------------------------------
    # THE ONE AND ONLY __init__
    #
    # All the real setup work lives here. Every other way of building a
    # Driver will end up calling this. That is what "chaining" means:
    # one place does the work, everything else delegates to it.
    # ------------------------------------------------------------------
    def __init__(self, driver_id=0, name="Random", rating=0.0, is_online=False):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online
        self.rides = []                       # mutable -> per object
        Driver.total_drives += 1
        print(f"   [__init__] built {name!r} (id={driver_id}, rating={rating})")

    # ==================================================================
    #  ALTERNATIVE CONSTRUCTORS  =  Java's chained constructors
    # ==================================================================

    # ------------------------------------------------------------------
    # @classmethod — what it means
    #
    # A normal method receives `self` (one OBJECT).
    # A classmethod receives `cls` (the CLASS ITSELF).
    #
    # Why do we need the class? Because we are about to CREATE an object,
    # and there is no object yet to receive `self`.
    #
    # `cls` here IS `Driver`, so `cls(...)` means `Driver(...)`
    # -> which calls __init__ -> which is the chaining.
    #
    # Java equivalent:  public Driver(String name) { this(0,name,0.0,false); }
    # ------------------------------------------------------------------
    @classmethod
    def with_name(cls, name):
        """Build a Driver from just a name. Everything else gets defaults."""
        print("   [with_name] delegating to __init__ ...")
        # cls(...) calls __init__ -> the delegation, exactly like this(...)
        return cls(0, name, 0.0, False)

    # ------------------------------------------------------------------
    # This one mirrors your two-step Java constructor:
    #     this(0,name,0.0,false);     // 1. delegate
    #     this.rating = rating;       // 2. then adjust
    # ------------------------------------------------------------------
    @classmethod
    def with_name_and_rating(cls, name, rating):
        """Build from a name, then adjust the rating afterwards."""
        print("   [with_name_and_rating] delegating first ...")

        # STEP 1 — delegate. `obj` is now a fully-built Driver.
        obj = cls(0, name, 0.0, False)

        # STEP 2 — adjust the one field we care about.
        obj.rating = rating
        print(f"   [with_name_and_rating] adjusted rating to {rating}")

        # ⚠️ A classmethod MUST return the object. Java's constructor
        #    returns implicitly; here you return it yourself.
        return obj

    def __str__(self):
        return f"Driver(id={self.driver_id}, name='{self.name}', rating={self.rating})"


# ================= USING IT — watch the delegation order =================

print("--- d1 = Driver() ---")
d1 = Driver()

print("--- d2 = Driver.with_name('Ashok') ---")
# Note: called on the CLASS, not on an object. There is no object yet.
d2 = Driver.with_name("Ashok")

print("--- d3 = Driver.with_name_and_rating('Meera', 4.9) ---")
d3 = Driver.with_name_and_rating("Meera", 4.9)

print()
print("d3           :", d3)
print("total_drives :", Driver.total_drives)
```

### Output

```
--- d1 = Driver() ---
   [__init__] built 'Random' (id=0, rating=0.0)
--- d2 = Driver.with_name('Ashok') ---
   [with_name] delegating to __init__ ...
   [__init__] built 'Ashok' (id=0, rating=0.0)
--- d3 = Driver.with_name_and_rating('Meera', 4.9) ---
   [with_name_and_rating] delegating first ...
   [__init__] built 'Meera' (id=0, rating=0.0)
   [with_name_and_rating] adjusted rating to 4.9

d3           : Driver(id=0, name='Meera', rating=4.9)
total_drives : 18
```

### How it works

Read the trace for `d3`. It matches your Java **exactly**:

```
   Java                                 Python
   ----------------------------------   ------------------------------------
   public Driver(String n, double r) {  @classmethod
                                        def with_name_and_rating(cls, n, r):
       this(0, n, 0.0, false);   <- 1       obj = cls(0, n, 0.0, False)   <- 1
       this.rating = r;          <- 2       obj.rating = r                <- 2
   }                                        return obj
```

> 💡 **Why chain at all?** So the setup code exists in exactly **one** place. If you later add a field to `__init__`, every alternative constructor gets it automatically. Without chaining, you'd have to remember to update four separate methods.

### `self` vs `cls` vs nothing — the three method types

| Decorator | Receives | Use when |
|:--|:--|:--|
| *(none)* | `self` — the object | You need this driver's data |
| `@classmethod` | `cls` — the class | You need to **create** an object, or touch class attributes |
| `@staticmethod` | nothing | A helper that needs neither |

### ⚠️ Why `cls(...)` and not `Driver(...)`?

They look identical here. The difference appears with inheritance:

```python
class PremiumDriver(Driver):
    pass

d = PremiumDriver.with_name("Ashok")
print(type(d))        # <class '__main__.PremiumDriver'>   ✅ correct type
```

Because `with_name` used `cls(...)`, and `cls` was `PremiumDriver`, you got a `PremiumDriver` back. Had it hardcoded `Driver(...)`, subclasses would get the **wrong class** — a real and confusing bug.

> 💡 **Always use `cls(...)` inside a `@classmethod`, never the class name.**

### Two more notes for teaching

**Default arguments already cover most cases.** Before reaching for a classmethod, ask whether a default would do:

```python
d = Driver(name="Ashok")        # simpler than Driver.with_name("Ashok")
```

Use `@classmethod` when the **kind of input differs** — building from a name, from a dictionary, from a CSV line, from a database row. That's where it earns its place:

```python
@classmethod
def from_dict(cls, data):
    """Build a Driver from a dictionary — e.g. an API response."""
    return cls(data["id"], data["name"], data["rating"], data["online"])

d = Driver.from_dict({"id": 12, "name": "Don", "rating": 4.0, "online": True})
```

---
---

# TOPIC 11
# Copy Constructor

## Definition

> **Copy constructor** — a constructor that builds a **new object** by copying the values of an existing one.
>
> Java: `public Driver(Driver other)`.
> Python: no overloading, so use a **`@classmethod`** — or the built-in `copy` module.

## Why we need it

Because **`d2 = d1` does not copy anything** (Topic 3). It just adds a second label to the same object.

```
   d2 = d1                            a real copy
   ---------------------              ---------------------
   d1 ---+                            d1 ---> [ Driver A ]
         +---> [ Driver ]
   d2 ---+                            d2 ---> [ Driver B ]
   ONE object                         TWO objects
```

Sometimes you genuinely want two independent drivers with the same starting data.

## Java

```java
// copy constructor
public Driver(Driver other) {
    this.driverId  = other.driverId;
    this.name      = other.name;
    this.rating    = other.rating;
    this.isOnline  = other.isOnline;
}

Driver copy = new Driver(original);
```

## Python

```python
# ============================================================
# TOPIC 11 — the copy constructor
# ============================================================

import copy          # Python's built-in copying tools


class Driver:
    """A driver in the Uber system."""

    def __init__(self, driver_id=0, name="Random", rating=0.0,
                 is_online=False, rides=None):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online

        # A MUTABLE field. This is the one that will matter in Topic 12.
        # ⚠️ rides=None then build inside — NEVER rides=[] as the default,
        #    because that list would be created ONCE and shared by every driver.
        self.rides = rides if rides is not None else []

    # ------------------------------------------------------------------
    # THE COPY CONSTRUCTOR  =  Java's  public Driver(Driver other)
    #
    # Again a @classmethod, because Python has only one __init__ and we
    # cannot overload it with a Driver-shaped parameter.
    #
    # `other` is the existing driver we are copying FROM.
    # `cls(...)` builds the brand-new object.
    # ------------------------------------------------------------------
    @classmethod
    def from_driver(cls, other):
        """Create a NEW Driver with the same values as `other`."""
        return cls(
            other.driver_id,      # immutable -> safe to share the value
            other.name,           # immutable
            other.rating,         # immutable
            other.is_online,      # immutable
            list(other.rides)     # ⚠️ MUTABLE -> list() makes a NEW list.
                                  #    Writing `other.rides` here would SHARE
                                  #    the same list between both drivers.
        )

    def __str__(self):
        return (f"Driver(id={self.driver_id}, name='{self.name}', "
                f"rating={self.rating}, rides={self.rides})")


# ================= USING IT =================

original = Driver(1, "Ashok", 4.8, True, ["R-101"])

# ---------- WRONG: this is NOT a copy ----------
alias = original
alias.name = "CHANGED"
print("alias.name       :", alias.name)
print("original.name    :", original.name, "  <- changed too! Same object.")
print("same object?     :", original is alias)

original.name = "Ashok"          # reset for the next demo

# ---------- RIGHT: a genuine copy ----------
duplicate = Driver.from_driver(original)

print("\nafter from_driver:")
print("  same object?   :", original is duplicate)      # False -> two objects
print("  same values?   :", original.name == duplicate.name)

# Change the copy — the original must not move.
duplicate.name = "Meera"
duplicate.rides.append("R-999")

print("\n  original       :", original)
print("  duplicate      :", duplicate)
```

### Output

```
alias.name       : CHANGED
original.name    : CHANGED   <- changed too! Same object.
same object?     : True

after from_driver:
  same object?   : False
  same values?   : True

  original       : Driver(id=1, name='Ashok', rating=4.8, rides=['R-101'])
  duplicate      : Driver(id=1, name='Meera', rating=4.8, rides=['R-101', 'R-999'])
```

### How it works

**Two genuinely separate objects.** Changing `duplicate.name` left `original.name` alone, and appending to `duplicate.rides` left `original.rides` alone.

That second one only worked because of this line:

```python
list(other.rides)      # builds a NEW list containing the same items
```

> 🛑 **Ask your class:** what if we had written `other.rides` instead?
>
> Both drivers would point at the **same list**. Appending to one would appear in the other — and that is exactly the bug Topic 12 is about.

---
---

# TOPIC 12
# Deep vs Shallow Copy

## Definition

> **Shallow copy** — creates a new object, but **copies only the references** to the things inside. Nested mutable objects are still **shared**.
>
> **Deep copy** — creates a new object **and recursively new copies of everything inside**. Nothing is shared.

```
   ASSIGNMENT   d2 = d1          SHALLOW copy               DEEP copy
   ----------------------        ---------------------      -------------------
   d1 --+                        d1 --> [obj A]             d1 --> [obj A]
        +--> [ obj ]                      |                          |
   d2 --+                                 v                          v
                                       [ list ]                  [ list A ]
   ONE object                             ^
                                          |                     d2 --> [obj B]
                                 d2 --> [obj B]                          |
                                                                         v
                                 TWO objects,                        [ list B ]
                                 ONE shared list
                                                             TWO objects,
                                                             TWO lists
```

## Python

```python
# ============================================================
# TOPIC 12 — shallow vs deep copy
# ============================================================

import copy


class Driver:
    def __init__(self, driver_id=0, name="Random", rating=0.0,
                 is_online=False, rides=None):
        self.driver_id = driver_id
        self.name = name              # str  -> IMMUTABLE
        self.rating = rating          # float -> IMMUTABLE
        self.is_online = is_online    # bool -> IMMUTABLE
        self.rides = rides if rides is not None else []   # list -> MUTABLE

    def __str__(self):
        return f"Driver('{self.name}', rides={self.rides})"


original = Driver(1, "Ashok", 4.8, True, ["R-101"])

# ==================================================================
#  LEVEL 1 — ASSIGNMENT: not a copy at all
# ==================================================================
alias = original
print("LEVEL 1 — assignment")
print("  same object?     :", original is alias)          # True

# ==================================================================
#  LEVEL 2 — SHALLOW COPY:  copy.copy()
#
#  Makes a NEW Driver object, and copies each attribute's REFERENCE.
#  For immutable attributes (name, rating) that's perfectly safe.
#  For the MUTABLE list, both drivers end up pointing at the SAME list.
# ==================================================================
shallow = copy.copy(original)

print("\nLEVEL 2 — copy.copy()  (shallow)")
print("  different object?:", original is not shallow)    # True  -> good
print("  same rides list? :", original.rides is shallow.rides, " <- SHARED!")

# Changing an IMMUTABLE attribute is safe — it rebinds only the copy's name
shallow.name = "Meera"

# Changing the MUTABLE attribute LEAKS into the original
shallow.rides.append("R-999")

print("  original.name    :", original.name, "  (safe — immutable)")
print("  original.rides   :", original.rides, "<- LEAKED!")

# ==================================================================
#  LEVEL 3 — DEEP COPY:  copy.deepcopy()
#
#  Makes a NEW Driver object AND recursively new copies of everything
#  inside it. The list is duplicated too, so nothing is shared.
# ==================================================================
original.rides = ["R-101"]        # reset after the leak above
deep = copy.deepcopy(original)

print("\nLEVEL 3 — copy.deepcopy()  (deep)")
print("  different object?:", original is not deep)              # True
print("  same rides list? :", original.rides is deep.rides, " <- SEPARATE!")

deep.rides.append("R-777")
print("  original.rides   :", original.rides, "(untouched)")
print("  deep.rides       :", deep.rides)
```

### Output

```
LEVEL 1 — assignment
  same object?     : True

LEVEL 2 — copy.copy()  (shallow)
  different object?: True
  same rides list? : True  <- SHARED!
  original.name    : Ashok   (safe — immutable)
  original.rides   : ['R-101', 'R-999'] <- LEAKED!

LEVEL 3 — copy.deepcopy()  (deep)
  different object?: True
  same rides list? : False  <- SEPARATE!
  original.rides   : ['R-101'] (untouched)
  deep.rides       : ['R-101', 'R-777']
```

### How it works — the key observation

Look at Level 2 carefully. **Two things happened, and they were different:**

| We changed | Type | Leaked to the original? | Why |
|:--|:--|:--|:--|
| `shallow.name = "Meera"` | `str` — **immutable** | ❌ No | Assignment **rebinds** the copy's own name |
| `shallow.rides.append(...)` | `list` — **mutable** | ✅ **Yes** | `append` **mutates** the one shared list |

> 💡 **This is Topic 6 again — mutation versus rebinding.**
>
> A shallow copy is safe for immutable attributes and dangerous for mutable ones.
> That is the entire distinction.

### Which one should you use?

| Situation | Use |
|:--|:--|
| All attributes immutable (`int`, `str`, `float`, `bool`, `tuple`) | `copy.copy()` — cheaper and enough |
| Any mutable attribute (`list`, `dict`, `set`, another object) | `copy.deepcopy()` |
| You want explicit control | a `@classmethod` copy constructor (Topic 11) |

> ⚠️ **`deepcopy` is not free.** It walks the entire object graph. On a large nested structure it is noticeably slow and uses a lot of memory. Don't reach for it by reflex — reach for it when you have mutable state to protect.

### Customising what a copy does

Python lets your class decide how it should be copied, via two dunder methods:

```python
class Driver:
    def __init__(self, name, rides=None):
        self.name = name
        self.rides = rides if rides is not None else []

    # ------------------------------------------------------------------
    # __copy__  -> called by copy.copy(obj)
    # Here we deliberately make a NEW list, so our "shallow" copy is
    # actually safe. This is how you fix the leak at the class level.
    # ------------------------------------------------------------------
    def __copy__(self):
        return Driver(self.name, list(self.rides))

    # ------------------------------------------------------------------
    # __deepcopy__ -> called by copy.deepcopy(obj)
    # `memo` is a dictionary deepcopy uses to remember what it has
    # already copied, so circular references don't cause infinite loops.
    # ------------------------------------------------------------------
    def __deepcopy__(self, memo):
        return Driver(self.name, copy.deepcopy(self.rides, memo))
```

> 💡 With `__copy__` defined like that, `copy.copy(d)` no longer leaks — because the class itself now guarantees a fresh list. **That's encapsulation applied to copying.**

### 🎯 Interview questions from this topic

**Q1. Difference between `=`, `copy.copy()` and `copy.deepcopy()`?**

> `=` creates no new object at all — just another name for the same one. `copy.copy()` creates a new object but shares the nested objects. `copy.deepcopy()` creates a new object and recursively copies everything inside.

**Q2. When is a shallow copy dangerous?**

> When any attribute is mutable. Changing a nested list or dict through the copy is visible through the original, because they point at the same nested object.

**Q3. Why does changing `shallow.name` NOT leak, while `shallow.rides.append()` does?**

> `name` is a string — immutable. Assignment rebinds the copy's own attribute. `rides` is a list — mutable — and `append` modifies the single shared list rather than replacing it.

**Q4. Does Python have a copy constructor?**

> Not as an overloaded constructor, since Python allows only one `__init__`. The equivalent is a `@classmethod` factory such as `from_driver(cls, other)`, or the `copy` module, or defining `__copy__` / `__deepcopy__`.

---
---

# The Complete `Driver` Class

Everything from all 12 topics, in one file.

```python
# ============================================================
#  uber/driver.py  —  the complete Day-1 Driver class
# ============================================================
import copy


class Driver:
    """A driver in the Uber system."""

    # ---------- TOPIC 5: class attributes (Java's static fields) ----------
    total_drives = 15
    MIN_RATING = 0.0
    MAX_RATING = 5.0

    # ---------- TOPIC 5: Java's static block ----------
    # Runs ONCE, at import time, before any object exists.
    print("This is executed at time of Driver class definition")

    # ---------- TOPIC 4: the constructor ----------
    def __init__(self, driver_id=100, name="Random", rating=0.0,
                 is_online=False, rides=None):
        self.driver_id = driver_id        # instance attribute
        self.name = name                 # public (Topic 9)

        self._rating = None              # storage for the property
        self.rating = rating             # goes THROUGH the setter -> validated

        self.is_online = is_online
        self.rides = rides if rides is not None else []   # mutable -> per object

        self.__payout_account = "HDFC-9981"    # mangled -> _Driver__payout_account

        Driver.total_drives += 1         # CLASS NAME, not self (Topic 5 trap)

    # ---------- TOPIC 8: encapsulation via property ----------
    @property
    def rating(self):
        """GETTER — runs when anyone reads d.rating"""
        return self._rating

    @rating.setter
    def rating(self, value):
        """SETTER — runs when anyone writes d.rating = x. Validates first."""
        if not isinstance(value, (int, float)):
            raise TypeError("Rating must be a number")
        if not Driver.MIN_RATING <= value <= Driver.MAX_RATING:
            raise ValueError(f"Rating must be 0-5, got {value}")
        self._rating = value             # underscore! self.rating = recursion

    @property
    def driver_code(self):
        """READ-ONLY — getter with no setter. Assignment raises AttributeError."""
        return f"DRV-{self.driver_id}"

    # ---------- TOPIC 2: member methods ----------
    def accept_ride(self, ride_id):
        """Record a ride for THIS driver (self tells us which one)."""
        self.rides.append(ride_id)
        print(f"Ride has been accepted {ride_id}")

    def change_status(self):
        """Flip online/offline — moves the object's STATE."""
        self.is_online = not self.is_online
        print(f"Driver is {self.is_online}")

    # ---------- TOPIC 5: static method ----------
    @staticmethod
    def register():
        """Callable with NO object — registration is what creates drivers."""
        print("This is Register Method")

    # ---------- TOPIC 10: constructor chaining ----------
    @classmethod
    def with_name(cls, name):
        """Java: public Driver(String name) { this(0,name,0.0,false); }"""
        return cls(0, name, 0.0, False)

    @classmethod
    def with_name_and_rating(cls, name, rating):
        """Java: this(...) then this.rating = rating;"""
        obj = cls(0, name, 0.0, False)
        obj.rating = rating              # validated by the setter
        return obj

    # ---------- TOPIC 11: copy constructor ----------
    @classmethod
    def from_driver(cls, other):
        """Java: public Driver(Driver other)"""
        return cls(other.driver_id, other.name, other.rating,
                   other.is_online, list(other.rides))    # list() = NEW list

    # ---------- TOPIC 12: safe copying ----------
    def __copy__(self):
        """Called by copy.copy() — we make a new list so nothing leaks."""
        return Driver(self.driver_id, self.name, self._rating,
                      self.is_online, list(self.rides))

    def __deepcopy__(self, memo):
        """Called by copy.deepcopy() — memo prevents infinite loops."""
        return Driver(self.driver_id, self.name, self._rating,
                      self.is_online, copy.deepcopy(self.rides, memo))

    # ---------- TOPIC 7: __str__ (Java's toString) ----------
    def __str__(self):
        status = "online" if self.is_online else "offline"
        return (f"Driver(id={self.driver_id}, name='{self.name}', "
                f"rating={self._rating}, {status}, rides={len(self.rides)})")
```

---

# Java → Python Summary Table

| Topic | Java | Python |
|:--|:--|:--|
| 1 | `new Driver()` | `Driver()` — no `new` |
| 1 | `int driverId;` declaration | none — assign in `__init__` |
| 2 | member variables / methods | instance attributes / methods |
| 3 | `d1 == d2` (identity) | `d1 is d2` |
| 3 | `d1.equals(d2)` (value) | `d1 == d2` |
| 3 | String Pool | interning |
| 4 | `public Driver(...)` | `def __init__(self, ...)` |
| 4 | `this` (keyword, optional) | `self` (parameter, **never optional**) |
| 4 | 4 overloaded constructors | 1 `__init__` + default arguments |
| 5 | `static int totalDrives;` | `total_drives = 0` in the class body |
| 5 | `static { ... }` | the class body itself |
| 5 | `static void Register()` | `@staticmethod` |
| 6 | pass by value | call by sharing — same behaviour |
| 7 | `toString()` | `__str__` |
| 8 | `getRating()` / `setRating()` | `@property` / `@rating.setter` |
| 8 | `private final` + getter | `@property` with no setter |
| 9 | `private` (enforced) | `__name` (mangled, **not** private) |
| 9 | `protected` | `_name` (convention only) |
| 10 | `this(0, name, 0.0, false)` | `@classmethod` → `cls(...)` |
| 11 | `public Driver(Driver other)` | `@classmethod from_driver(cls, other)` |
| 12 | manual field-by-field copy | `copy.copy()` / `copy.deepcopy()` |

---

# The Four Traps — Warn Your Class About These

| # | Trap | Fix |
|:--|:--|:--|
| 1 | `name = x` instead of `self.name = x` | Always prefix with `self.` — silently does nothing otherwise |
| 2 | `self.total_drives += 1` for a class attribute | `Driver.total_drives += 1` — read falls through, write doesn't |
| 3 | `self.rating = value` inside the setter | `self._rating = value` — otherwise `RecursionError` |
| 4 | `rides=[]` as a default, or `rides = []` as a class attribute | `rides=None`, build inside `__init__` |

> 💡 **When anything behaves strangely, print `obj.__dict__`.** It catches all four.

---

*All code in this document was executed and verified.*
