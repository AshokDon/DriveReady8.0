# Object-Oriented Programming in Python
## Chapter 1 — Introduction

**Running example:** Uber's dispatch system
**Scope:** Day 1 — entities, classes, objects, memory, `__init__`, `self`, class-level members, parameter passing, `__str__`, and an introduction to encapsulation.

---

## How this chapter is built

Every concept follows the same five beats:

| | |
|:--|:--|
| 📖 **Definition** | The formal one-liner — the sentence you write in an exam |
| 🌍 **The story** | Where this shows up in a real system |
| ❓ **Why we need it** | The problem it solves. Skip this and the concept is just syntax |
| ⚙️ **How Python does it** | The mechanism and its rules |
| 💻 **Code** | Small, runnable, Day-1 only |

Callouts you'll see:

> ⚠️ **Trap** — a mistake that will silently break your code
> 🎯 **Interview** — a question asked from this concept
> 🧠 **Deeper** — the engineering reason behind the rule

---

# Part 0 — One Button, Five Systems

You open Uber. You tap **Book Ride**. Fifteen seconds later a car is on its way.

You saw one button. Here is what happened behind it.

### Step 1 — "Where are you?" is harder than it sounds

There are millions of drivers on the platform. The naive way to find the closest is to measure the distance from you to every driver and sort:

```python
for driver in all_five_million_drivers:
    distance = haversine(rider.location, driver.location)
```

Five million distance calculations — each one a haversine formula with sines, cosines, and a square root. Per request. Thousands of requests per minute in one city. **This approach dies instantly.**

Uber's answer was to stop treating the Earth as a plane of coordinates. They built **H3** — a system that carves the globe into hexagonal cells, each with a compact 64-bit ID. A driver's GPS position isn't stored as latitude and longitude; it's stored as *which hexagon they're in*.

Now finding nearby drivers becomes: *look up my hexagon, and its 6 neighbours.* Seven cell lookups. Millions of comparisons collapse into dozens.

> **Why hexagons and not squares?** In a square grid, your 4 edge-neighbours are closer than your 4 corner-neighbours — "one cell away" means two different distances. Every hexagon has exactly **6 neighbours, all equidistant**. Radial search becomes uniform and predictable.

### Step 2 — The nearest driver is not the nearest driver

You now have 30 candidates within a kilometre. Pick the closest?

No. The closest driver by straight-line distance might be:

- on the **other side of a river**, 20 minutes away by the nearest bridge
- on a **one-way street** pointing away from you
- 200 metres away but stuck behind a **jammed junction**

Geographic distance is the wrong measure. **Travel time** is the right one.

So the candidate list goes to a **routing engine**, which models the city's road network as a **graph**: intersections are nodes, road segments are edges, and each edge is weighted by traversal time. Finding the fastest route becomes a shortest-path problem — Dijkstra's algorithm and its industrial descendants — over millions of edges, adjusted for one-way streets, turn restrictions, turn costs, and speed limits.

### Step 3 — Even the shortest path lies

The routing engine gives a mathematically optimal answer. Reality disagrees. It doesn't know the pickup point is inside a mall with a five-minute walk to the kerb, or that this junction floods at 6pm on Fridays.

So Uber layers a **machine-learning model** on top that doesn't predict the ETA — it predicts the *error* in the routing engine's ETA, and corrects it.

### Step 4 — Dispatch

Uber's dispatch service (internally **DISCO** — Dispatch Optimization) now has candidates sorted by real ETA. It offers the trip to the best driver, who has seconds to accept. If he doesn't, it moves on. Meanwhile the system is also considering drivers who aren't free yet but will be by the time they reach you.

### Step 5 — And then

Payment authorisation, fraud scoring, surge calculation, live location streaming, receipt generation, driver payout accounting.

---

### Now count what you saw.

**One button.**

Geospatial indexing, graph shortest-path algorithms, machine-learned corrections, a real-time bidding system, and a payments pipeline — reduced to a single tap that says *Book Ride*.

**That reduction has a name. It is called abstraction, and it is the reason object-oriented programming exists.**

Here's the thing, though. Before you can write `find_nearest_driver()`, something has to answer: **what is a driver?**

Not philosophically. In code. What data does a driver carry? What can a driver do? How does one live in memory? How do you create one, and how do you stop it being created broken?

**That is what this chapter is about.** Everything above is built on top of it.

---

# Part 1 — Why Objects?

Before objects, programs were a list of instructions over loose variables. Let's try our driver data that way.

```python
driver1_name = "Ashok"
driver1_rating = 4.8
driver1_is_online = True

driver2_name = "Meera"
driver2_rating = 4.9
driver2_is_online = False
# ... 4,999,998 more
```

Three things break immediately.

**1. The data is scattered.** Nothing connects `driver1_rating` to `driver1_name`. They're related only inside your head.

**2. The behaviour has nowhere to live.** Where does `accept_ride()` go? It becomes a loose function with eight parameters:

```python
def accept_ride(name, rating, is_online, ride_id, lat, lng, ...):
```

Add one field to a driver and every call site breaks.

**3. Nothing is protected.** Any line in any file can write `driver1_rating = -50`. Now the dispatch sort is poisoned and you will spend a night finding out why.

> **Object-Oriented Programming organises code so that data and the behaviour operating on that data live together as one unit, modelled on real-world things.**

That unit is the **object**. Every concept in this chapter exists to build one, describe one, or protect one.

---

# 1. Entity

### 📖 Definition

> **An entity is any person, place, thing, or concept from the real world that you want to represent inside your program.**

### 🌍 The story

Identifying entities is the first act of design — before a single line of code. You look at the system and ask: *what things exist here?*

For Uber:

```
                         UBER
                           │
      ┌────────┬───────────┼───────────┬─────────┐
      ▼        ▼           ▼           ▼         ▼
   Driver   Customer    Vehicle     Payment    Trip
```

Across other domains:

| System | Entities |
|:--|:--|
| Hospital | Patient, Doctor, Appointment, Prescription, Bill |
| College | Student, Faculty, Course, Batch, Exam |
| E-commerce | Product, Cart, Order, Payment, Seller |
| Airline | Flight, Passenger, Ticket, Crew, Aircraft |

### 🎯 The question that always comes up

> *"Does the real Uber system only have these 5 entities?"*

**No — and the answer is more interesting than just 'there are more'.**

Look back at Part 0. The dispatch flow needed a hexagonal grid index, a road-network graph, a shortest-path engine, an ETA correction model, and a bidding loop. **None of those five things is on the diagram.**

That's deliberate. You are not listing everything. You are choosing the **entry points** — the handful of concepts through which the whole system becomes discussable.

And notice: once `Driver` and `Trip` are real types in your code, the complicated parts get somewhere to attach:

```python
nearest = dispatch_service.find_nearest(customer.location)
trip = Trip(customer, nearest)
```

The H3 hexagons live inside `find_nearest`. The graph and Dijkstra live inside it too. But the *conversation* stays at the level of drivers, customers, and trips.

**Choosing the right five entities is what makes the other hundred manageable.**

> ⚠️ **How to know you picked wrong.** If explaining your system requires you to keep saying "and then there's this other thing that…", your entity list is missing something. If you can narrate the main flow using only your entities, you picked well.

---

# 2. The Four Properties: 3 Pillars + 1 Principle

Textbooks list **four pillars of OOP**. That's a convenient simplification that hides something important.

```
   ┌──────────────────┐
   │  Encapsulation   │──┐
   ├──────────────────┤  │
   │  Inheritance     │──┼──►   THE 3 PILLARS
   ├──────────────────┤  │      mechanisms · things you type · the HOW
   │  Polymorphism    │──┘
   └──────────────────┘

   ┌──────────────────┐
   │  Abstraction     │──────►  THE PRINCIPLE
   └──────────────────┘         the outcome · the goal · the WHY
```

| | The 3 Pillars | Abstraction |
|:--|:--|:--|
| What is it? | Mechanisms | A goal, an outcome |
| Do you type it? | Yes | **No syntax exists for it** |
| Relationship | The tools | What the tools are *for* |

Read it as a sentence:

> **We use encapsulation, inheritance, and polymorphism *in order to achieve* abstraction.**

Abstraction is not a fourth tool standing beside the other three. It is the reason they exist.

> 🎯 **Interview: "How many pillars does OOP have?"**
> A strong answer: *"Four properties are normally listed. Three of them — encapsulation, inheritance, polymorphism — are mechanisms you actually write. Abstraction is the principle you achieve by applying those three."*
> This is correct, and shows you understand the relationship rather than having memorised a list.

---

# 3. Abstraction — The Principle

### 📖 Definition

> **Abstraction is representing a complex system through a simple, high-level interface, hiding the internal complexity from whoever uses it.**

Compressed: **representing a complex system in a few working steps.**

### 🌍 The story — in code

Here's abstraction as an Uber engineer experiences it:

```python
eta_minutes = routing_service.get_eta(driver.location, rider.location)
```

One line. Behind it: a road network graph with millions of weighted edges, a shortest-path search, real-time traffic data, turn restrictions, and a neural network correcting the result.

The engineer calling `get_eta` needs to know **none of it**. They need to know: *two points in, minutes out.*

### 🧠 Deeper — the payoff you can't see

Uber originally built ETAs on an open-source routing engine, then replaced it with their own. The internals changed completely — different algorithms, different data structures, different traffic modelling.

**How many lines of dispatch code had to change?**

If the interface stayed `get_eta(from, to) → minutes`, then: **almost none.**

This is the real prize. Abstraction isn't only about making things easy to *use*. It's about making them **safe to change**. A good interface is a wall: complexity stays on one side, and you can rebuild that side without anyone on the other side noticing.

### 🌍 Two more angles

**A research paper's abstract.** One paragraph tells you the problem, method, and result. You understand what the paper *does* without reading 40 pages of methodology. That's exactly the relationship an interface has to an implementation.

**Attending an online class.** Your experience:

```
   login  ──►  dashboard  ──►  join
```

Three steps. Is Microsoft Teams' backend three steps?

```
   login      →  credential validation, password hashing, token issue,
                 session creation, 2FA
   dashboard  →  auth on every request, database queries, permissions,
                 caching, API fan-out
   join       →  WebSocket handshake, media server allocation,
                 codec negotiation, bandwidth adaptation, load balancing
```

**No. But for you, it is an abstraction of those three steps.**

### ❓ Why we need it

Software systems are enormously complex, but **we want to visualise them in very simple steps.** Two payoffs:

1. **Usability** — you can use something without understanding it.
2. **Changeability** — the implementation can be rewritten without breaking its users.

### ⚙️ How we achieve it

**By using the three pillars.**

- **Encapsulation** hides *data* behind methods.
- **Inheritance** lets you say "this is a kind of that" without repeating details.
- **Polymorphism** lets you call one operation on many types without knowing which one you hold.

Today we begin with the raw materials, and end with the first pillar.

---

# 4. Class — The Blueprint

### 📖 Definition

> **A class is a blueprint or template that defines the structure (data) and behaviour (methods) that all objects of that type will have.**

### 🌍 The story

To build a house you don't start laying bricks. You draw a **blueprint**: 3 bedrooms, 2 bathrooms, 1200 sq ft.

Two things about that blueprint:

1. **Nobody can live in it.** It's paper. No address, no land.
2. **You can build 50 houses from it** — each a separate, real house.

The blueprint is the **class**. Each house is an **object**.

| Blueprint (class) | Real thing (object) |
|:--|:--|
| Cookie cutter | Each cookie |
| Blank passport form | Each issued passport |
| Recipe | Each dish cooked |
| `Driver` class | Ashok, Meera, and 5 million others |

### ❓ Why we need it

Define the shape **once**, create unlimited objects from it. Without a class you'd redescribe "what a driver is" every time you needed one.

### Designing a class — two questions

**Question 1: What data will every driver carry?**

```
                        Driver
     ┌──────────┬─────────┬────────┬────────────┐
     ▼          ▼         ▼        ▼            ▼
  driver_id   name     rating   is_online   (location)
```

At this moment, has anyone signed up? **No.** You are deciding: *if I build this system, this is what I will store for every driver.*

**Question 2: What will a driver DO?** → **behaviour**

```
   accept_ride()
   change_status()
   complete_trip()
```

**A class = data + behaviour, bundled.** That bundling is where encapsulation begins.

### 💻 Code

```python
class Driver:
    """A driver in the ride-hailing system."""

    def __init__(self, driver_id, name, rating, is_online):
        # ---- data: instance attributes ----
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online

    # ---- behaviour: methods ----
    def accept_ride(self, ride_id):
        print(f"Ride has been accepted {ride_id}")

    def change_status(self):
        self.is_online = not self.is_online
        print(f"Driver is {self.is_online}")
```

> ⚙️ **Python has no field-declaration section.** There's no place to write "a driver has a name of type str." An attribute springs into existence the moment you assign to it — which you do inside `__init__`.
>
> This reflects a real difference in philosophy. A Java class body is a *contract* checked by a compiler. **A Python class body is executable code that runs top to bottom.** This isn't a detail — it explains several behaviours later in this chapter.

> **File rule:** none. Unlike some languages, Python lets you put any number of classes in one file, named anything. `models.py` can hold `Driver`, `Trip`, and `Customer` together.

---

# 5. Object — The Instance

### 📖 Definition

> **An object is an instance of a class — a concrete entity that exists in memory with its own copy of the data.**

Said another way, and both halves matter:

> **A real-world entity in the system is called an object.**
> **In computer science, "real" means: memory has been allocated.**

### ❓ Why the distinction matters

When you have only *written* the class, what exists? A class object holding some function definitions. No name is stored, no rating exists, no online status — because there is no *particular* driver yet.

```python
class Driver: ...            # a description. No driver data anywhere.

d1 = Driver(1, "Ashok", 4.8, True)     # NOW an object exists in memory
d2 = Driver(2, "Meera", 4.9, True)     # a DIFFERENT object, separate data
```

**One class. Unlimited objects. Each with its own independent copy of the data.**

### 🌍 The story

When Uber's dispatch service is running, millions of `Driver` objects are alive across a fleet of servers. Ashok's object holds `rating = 4.8`. Meera's holds `rating = 4.9`. Same class, same methods, **completely independent data**.

That's the leverage: you wrote `Driver` once, and it describes five million distinct things.

### 💻 Code

```python
d1 = Driver(1, "Ashok", 4.8, True)
d2 = Driver(2, "Meera", 4.9, True)

print(d1.name)      # Ashok
print(d2.name)      # Meera

d1.is_online = False
print(d1.is_online)  # False
print(d2.is_online)  # True    ← untouched, separate object
```

### ⚙️ Creating an object

```python
d1 = Driver(1, "Ashok", 4.8, True)
```

**There is no `new` keyword in Python.** Calling the class name like a function *is* the object creation. Behind that call, Python:

1. **Allocates** a new empty object
2. **Runs `__init__`**, passing the new object in as `self`
3. **Returns** the finished object

> ⚠️ **Python has no default field values.** If `__init__` doesn't set an attribute, the attribute simply *does not exist* — and touching it raises `AttributeError`:
>
> ```python
> class Driver:
>     def __init__(self, name):
>         self.name = name
>
> d = Driver("Ashok")
> print(d.rating)      # AttributeError: 'Driver' object has no attribute 'rating'
> ```
>
> **Set every attribute your class needs inside `__init__`.** Every one. This is the single best habit you can build today, because an attribute that only exists sometimes is a bug that only appears sometimes.

---

# 6. Members and State

### 📖 Definitions

> **Instance attributes (fields):** the variables belonging to an object.
> **Methods:** the functions belonging to a class.
> **State:** the values of an object's attributes at a given moment in time.

"Members" is the collective term — everything belonging to the class.

### 🌍 The story — state is what dispatch actually queries

Take Ashok. Right now:

```
   driver_id = 4021
   name      = "Ashok"
   rating    = 4.8
   is_online = False      ← asleep
```

That set of values is his **state**. Dispatch skips him — he's offline.

Two hours later he opens the app:

```
   is_online = True       ← state changed
```

Same object. Same identity. Different state. Now he appears in the candidate list.

**An object's lifetime is a sequence of states, and methods are what move it between them.**

A driver's realistic state machine:

```
   OFFLINE ──► ONLINE ──► ASSIGNED ──► ON_TRIP ──► ONLINE
                  ▲                                    │
                  └────────────────────────────────────┘
```

### ❓ Why the term matters

**Almost every serious bug in object-oriented code is a state bug** — the object reached a combination of values that should have been impossible:

- a driver who is `is_online = False` but has an active trip
- a driver assigned to **two trips at once**
- a bank account with a negative balance
- a rating of `-50`

Preventing impossible states is precisely the job of **encapsulation**, the first pillar.

### 💻 Code

```python
class Driver:
    def __init__(self, driver_id, name, rating):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = False

    def change_status(self):
        self.is_online = not self.is_online
        print(f"Driver is {self.is_online}")


d1 = Driver(4021, "Ashok", 4.8)

print(d1.is_online)     # False   ← state before
d1.change_status()
print(d1.is_online)     # True    ← state after
```

> 🧠 **`__dict__` shows you an object's state directly.** This is the most useful debugging tool in the language:
> ```python
> print(d1.__dict__)
> # {'driver_id': 4021, 'name': 'Ashok', 'rating': 4.8, 'is_online': True}
> ```

---

# 7. Reference Variables and the Memory Model

This section explains the most confusing behaviour in the language. Take it slowly — it pays for itself.

### 📖 Definition

> **A variable does not hold the object. It holds a reference to the object.**

### ⚙️ The mental model: labels, not boxes

Most people picture a variable as a **box holding a value**. In Python that picture is wrong and will mislead you.

**A Python name is a label stuck onto an object.**

```python
d1 = Driver(1, "Abc", 5.0, True)
```

```
              ┌────────────────────┐
   d1 ───────►│   Driver object    │
              │   name = "Abc"     │
              └────────────────────┘
```

`d1` is not the object. `d1` is a sticker pointing at it. You can see the address:

```python
print(id(d1))       # e.g. 140234891234567 — the object's address in memory
```

### ⚙️ Everything is an object

Some languages split the world into *primitives* (which hold values directly) and *objects* (reached by reference). **Python has no primitives.**

```python
x = 10
print(type(x))      # <class 'int'>
print(id(x))        # it has an address, like everything else
```

`10` is an object. `"Abc"` is an object. A function is an object. A class is an object. **The consequence: a name is always a reference — there is no other kind of variable.**

### 🌍 The story — why this matters in dispatch

The same `Driver` object is referenced from several places at once: the geo-index tracking his position, the active `Trip`, and the dispatch candidate list.

```python
ashok = Driver(4021, "Ashok", 4.8, True)

geo_index.add(ashok)          # reference #1
trip.driver = ashok           # reference #2
candidates.append(ashok)      # reference #3
```

**There is still exactly one Ashok in memory.** Three references, one object. Update his rating through any of them and all three see it — because there's nothing to keep in sync.

### The demonstration you must be able to predict

```python
d1 = Driver(1, "Abc", 5.0, True)
d2 = d1                      # copies the REFERENCE, not the object

print(d2.name)               # Abc

d2.name = "Xyz"
print(d1.name)               # Xyz   ← d1 changed too!
print(d2.name)               # Xyz
```

```
   BEFORE  d2 = d1                 AFTER  d2 = d1
   ─────────────────               ──────────────────────
   d1 ──► [ Driver ]               d1 ──┐
                                        ├──► [ Driver ]     ONE object
                                   d2 ──┘                   TWO labels
```

**There was never a second `Driver`.** `d2 = d1` moved a label. Both names lead to one object, so a change through either is visible through both.

> **Assignment in Python never copies an object.** It only ever attaches another name. Once you internalise this, an entire category of confusion disappears.

> 🌍 You write your home address on a slip of paper and hand a **photocopy** to a friend. Two slips — **one house**. If your friend goes there and repaints the door, you come home to a repainted door.

### ⚠️ `is` vs `==`

| Question | Operator |
|:--|:--|
| Same object in memory? (identity) | `is` |
| Same value? (equality) | `==` |

```python
d1 = Driver(1, "Abc", 5.0, True)
d2 = d1
d3 = Driver(1, "Abc", 5.0, True)     # separate object, identical data

d1 is d2      # True   → one object, two labels
d1 is d3      # False  → two different objects
d1 == d3      # compares by value, if the class defines how
```

**Use `is` only for `None`:**

```python
if x is None:        # ✅ the idiomatic check
if x == None:        # ❌ works, but nobody writes this
```

### Interning — Python's version of a string pool

```python
s1 = "Abc"
s2 = "Abc"
print(s1 is s2)      # True  — identical short literals are interned (shared)

a = 100
b = 100
print(a is b)        # True  — small integers (-5 to 256) are pre-cached
```

**Why is sharing safe?** Because **strings and ints are immutable**. Nobody can modify `"Abc"`, so a thousand names can share one copy with no risk. This is also why `s.upper()` returns a *new* string rather than changing `s`.

> ⚠️ **Never use `is` to compare numbers or strings for equality.**
> ```python
> x = 1000
> y = int("1000")
> print(x is y)      # False!
> print(x == y)      # True  ← the one you wanted
> ```
> Interning is an implementation detail that varies. Compare values with `==`.

### 🧠 Deeper — garbage collection

```python
d1 = Driver(1, "Abc", 5.0, True)
d1 = Driver(2, "Xyz", 4.0, True)     # the first object now has NO labels
```

The first `Driver` is unreachable. Python counts how many references point at each object; when the count hits zero, the memory is freed automatically. You never write `free()` or `delete`.

---

# 8. The Constructor — `__init__`

### 📖 Definition

> **`__init__` is a special method that runs automatically when an object is created. Its job is to initialise the object's attributes.**

### 🌍 The story

Before you become a patient in a hospital's system you fill an **admission form**: name, age, blood group, emergency contact. You are not admitted until it's complete.

`__init__` is that form. **No object is handed back to you without it running.** It's the one moment where the class can guarantee every object begins life valid.

Think about what a broken `Driver` does to dispatch: a driver with `driver_id = 0` and no name gets returned as the nearest match, and the crash happens three services away from the bug.

### ❓ Why we need it — the problem

Watch object creation without one:

```python
d1 = Driver()
d1.driver_id = 1
d1.name = "Abc"
d1.rating = 5.0
d1.is_online = True
```

Five lines for **one** driver. For a hundred drivers, five hundred lines. And if you forget line 4, the attribute doesn't exist at all — you get an `AttributeError` somewhere completely unrelated, hours later.

> *"To initialise an object with data I am writing a lot of lines. Will anyone do that at industry level? No. → write a parameterised constructor."*

With one:

```python
d1 = Driver(1, "Abc", 5.0, True)
```

One line. **Impossible to forget a field** — Python raises `TypeError` immediately if you miss a required argument. That is the whole justification.

### ⚙️ The rules

| Rule | Detail |
|:--|:--|
| **Name** | Always `__init__`. Never the class name |
| **When does it run?** | Automatically, when you call `Driver(...)` |
| **First parameter** | Always `self` |
| **Return value** | Nothing. It fills in `self`; it must not `return` a value |
| **If you write none** | Python provides no default field values — you get an object with no attributes |
| **How many?** | **Exactly one.** Python has no overloading |

### 💻 Code

```python
class Driver:
    def __init__(self, driver_id, name, rating, is_online):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online


d1 = Driver(1, "Abc", 5.0, True)
```

### Default arguments — Python's answer to overloading

Some languages let you write several constructors with different parameter lists. **Python allows only one `__init__`** — writing a second silently replaces the first. Instead, use **default arguments**:

```python
class Driver:
    def __init__(self, driver_id=100, name="Random", rating=5.0, is_online=True):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online
```

```python
d1 = Driver()                            # all defaults → 100, "Random", 5.0, True
d2 = Driver(12, "Don", 4.0, True)        # all supplied
d3 = Driver(12, "Don")                   # partial — rest use defaults
```

**One `__init__` covers every case.** And Python adds something extra — **keyword arguments**:

```python
d4 = Driver(name="Meera", driver_id=13)   # order doesn't matter
```

Compare readability:

```python
Driver(13, "Meera", 4.9, False)           # what is False?
Driver(13, "Meera", 4.9, is_online=False) # oh, that.
```

### Two rules for defaults

**1. Defaults must come after non-defaults.**

```python
def __init__(self, name, rating=5.0):     # ✅
def __init__(self, rating=5.0, name):     # ❌ SyntaxError
```

**2. ⚠️ Never use a mutable default.**

```python
def __init__(self, rides=[]):        # ❌ THE LIST IS CREATED ONCE
    self.rides = rides
```

The default list is built **a single time, when the function is defined** — not per call. Every `Driver` created without an explicit `rides` argument shares the *same list*:

```python
d1 = Driver()
d2 = Driver()
d1.rides.append("R-101")
print(d2.rides)          # ['R-101']  😱
```

**Fix:**

```python
def __init__(self, rides=None):      # ✅
    self.rides = rides if rides is not None else []
```

This bug is famous, it is silent, and it will happen to you once. Now it won't.

> 🎯 **Interview: "Does Python have a constructor?"**
> The precise answer: *"`__init__` is technically an **initialiser** — the object already exists by the time it runs, which is why it receives `self`. The actual constructor is `__new__`, which allocates the object. In everyday code you only write `__init__`."*
> You will rarely touch `__new__`, but knowing the distinction marks you out.

---

# 9. `self` — Referring to the Current Object

### 📖 Definition

> **`self` is a reference to the current object — the specific object on which the method was called.**

### ❓ Why we need it — the problem

One class. Five million driver objects. **One copy of the method code**, shared by all of them. When dispatch calls:

```python
ashok.change_status()
```

...the method body must know **whose** status. Something has to identify the object.

That something is `self`.

### ⚙️ How it actually works — the demonstration that makes it click

```python
d1 = Driver(1, "Ashok", 4.8, True)

d1.accept_ride("R-101")              # what you write
Driver.accept_ride(d1, "R-101")      # what Python actually does
```

**Both lines do exactly the same thing.**

A method is just a function stored inside the class. When you call it through an object, **Python inserts that object as the first argument.** `self` is simply the parameter that catches it.

Once you see this, `self` stops feeling like clutter and starts looking inevitable.

### 🌍 The story

A hotel prints one "Room Service" card and puts an identical copy in all 200 rooms. It reads: *"Dial 9 to order food to **this room**."*

The words **this room** are `self`. **The card is identical everywhere, but means something different depending on which room you're standing in.**

### The main use — naming attributes after their parameters

```python
class Driver:
    def __init__(self, driver_id, name, rating, is_online):
        self.driver_id = driver_id      # self.attribute = parameter
        self.name = name
        self.rating = rating
        self.is_online = is_online
```

Read it as: **`self.name` (the object's attribute) `=` `name` (the value just passed in).**

### ⚠️ The trap — `self` is never optional

Some languages let you drop `this` when there's no name collision. **Python does not.** An assignment without `self.` creates a *local variable* that vanishes when the method ends:

```python
class Driver:
    def rename(self, new_name):
        name = new_name           # ❌ creates a local variable. Does nothing.
        self.name = new_name      # ✅ sets the attribute
```

**No error. No warning.** The attribute simply never changes. If a value "isn't updating," this is the first thing to check.

The same applies to *reading*:

```python
def accept_ride(self, ride_id):
    print(f"{name} took {ride_id}")        # ❌ NameError: name is not defined
    print(f"{self.name} took {ride_id}")   # ✅
```

### The four rules of `self`

1. **Every instance method's first parameter is `self`.** No exceptions.
2. **You never pass it when calling.** Python inserts it.
3. **Every attribute access goes through `self.`** — reading and writing.
4. **`self` is a convention, not a keyword** — you *could* rename it. Never do; it's universal.

### 💻 Code

```python
class Driver:
    def __init__(self, driver_id, name, rating=5.0, is_online=True):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online

    def accept_ride(self, ride_id):
        print(f"{self.name} accepted ride {ride_id}")

    def change_status(self):
        self.is_online = not self.is_online
        print(f"{self.name} is online: {self.is_online}")


d1 = Driver(4021, "Ashok", 4.8)
d2 = Driver(4088, "Meera", 4.9)

d1.accept_ride("R-101")     # Ashok accepted ride R-101
d2.accept_ride("R-102")     # Meera accepted ride R-102
```

Same method. Two objects. Different output — because `self` was different each time.

---

# 10. Class Attributes — Members That Belong to the Class

### 📖 Definition

> **A class attribute belongs to the class itself, not to any object. There is exactly one copy, shared by every object of that class.**

This is what other languages call a **static** member.

### ❓ Why we need it — the problem

> **Requirement: track the total number of drivers registered in the system.**

**Attempt 1** — make it a normal attribute and increment it in `__init__`:

```python
class Driver:
    def __init__(self, name):
        self.name = name
        self.total_drivers = 0
        self.total_drivers += 1      # every object counts to 1. Useless.
```

**Will it work? No.**

> **Because it is a separate copy for every object. This should be a single variable which every object shares.**

```
       WITHOUT a class attribute                WITH one
   ┌───────────┐  ┌───────────┐          ┌───────────┐  ┌───────────┐
   │    d1     │  │    d2     │          │    d1     │  │    d2     │
   │ total = 1 │  │ total = 1 │          └─────┬─────┘  └─────┬─────┘
   └───────────┘  └───────────┘                └───────┬──────┘
     ✗ each has its own copy                     ┌─────▼─────┐
       nobody knows the real total                │  Driver   │  total = 2
                                                  │  (class)  │  ✓ ONE copy
                                                  └───────────┘
```

The total isn't a fact about *any one driver*. It's a fact about **the class as a whole**. So it must live on the class.

### 🌍 The story

A college has 3,000 students.

- **Roll number** — belongs to each student. 3,000 copies. **Instance.**
- **College name** — belongs to the college. Shared by all. 1 copy. **Class-level.**

The test: *"If this value changes, should it change for everyone at once?"* Yes → class attribute.

| Instance (per object) | Class-level (per class) |
|:--|:--|
| Driver's name, rating | Total driver count |
| Account balance | Bank's interest rate |
| Product price | Company's GST number |
| Trip fare | Maximum allowed rating (5.0) |

### ⚙️ How Python does it — position decides

```python
class Driver:
    total_drivers = 0                     # ← in the CLASS BODY = class attribute

    def __init__(self, name):
        self.name = name                  # ← starts with self. = instance attribute
        Driver.total_drivers += 1
```

**There is no keyword.** Where you write it decides what it is. That's the whole rule.

```python
d1 = Driver("Ashok")
d2 = Driver("Meera")
print(Driver.total_drivers)      # 2
```

### The lookup rule

When you write `obj.x`, Python searches:

```
   1. the instance      (obj.__dict__)
   2. then the class    (Driver.__dict__)
   3. → AttributeError
```

**Reading falls through to the class. Writing never does** — `obj.x = 1` always writes to the instance.

That asymmetry is the source of the next two traps. Understand it once and both become obvious.

### ⚠️ TRAP 1 — the counter that silently breaks

```python
def __init__(self, name):
    self.total_drivers += 1        # ❌ SILENTLY BROKEN
```

This looks correct. It runs without error. It does not work.

`self.total_drivers += 1` expands to `self.total_drivers = self.total_drivers + 1`. Split it:

```
   READ  (right side):  self.total_drivers
         → not on the instance
         → falls back to the class, finds 0
         → computes 0 + 1 = 1

   WRITE (left side):   self.total_drivers = 1
         → assignment through self ALWAYS writes to the instance
         → creates a NEW instance attribute on this one object
```

**You have accidentally recreated the exact bug the class attribute was meant to fix.** Every object gets a private copy set to 1; the class attribute never moves.

```python
d1 = Driver("Ashok")
d2 = Driver("Meera")

print(Driver.total_drivers)      # 0    ← never changed!
print(d1.total_drivers)          # 1
print(d2.total_drivers)          # 1
print(d1.__dict__)               # {'name': 'Ashok', 'total_drivers': 1}  ← proof
```

| Operation | Through `self` | Through the class name |
|:--|:--|:--|
| **Reading** a class attribute | ✅ works (falls through) | ✅ works |
| **Writing** a class attribute | ❌ creates an instance copy | ✅ correct |

> ✅ **Always write class attributes through the class name: `Driver.total_drivers += 1`.**

### ⚠️ TRAP 2 — mutable class attributes

```python
class Driver:
    rides = []                    # ❌ ONE list shared by every driver ever created

    def __init__(self, name):
        self.name = name

    def add_ride(self, ride_id):
        self.rides.append(ride_id)


d1 = Driver("Ashok")
d2 = Driver("Meera")
d1.add_ride("R-101")
print(d2.rides)                   # ['R-101']  😱
```

Why didn't `self.rides.append(...)` create an instance copy, the way `+=` did?

**Because there is no assignment.** `append` *mutates* the object that lookup found — the class's list. Only `=` writes to the instance.

**Fix — mutable state belongs in `__init__`:**

```python
class Driver:
    def __init__(self, name):
        self.name = name
        self.rides = []           # ✅ a fresh list for every object
```

> **Rule of thumb: class attributes should hold immutable values only** — `int`, `str`, `float`, `bool`. Anything mutable goes in `__init__`.

### Static methods

> **A static method belongs to the class and can be called without creating any object.**

### ❓ The reasoning — why `register()` must be static

> *"If a driver wants to **register**, do you think his object already exists in memory?"*
>
> **No.** He has no account yet — registering is what *creates* it.
>
> *"Then how will he call a method?"* → **make `register()` static.**

That reasoning generalises. **A normal method needs an object to be called on. But registration is what produces the object — so it cannot require one to already exist.** The sign-up button has to work before you have an account.

```python
class Driver:
    total_drivers = 0

    def __init__(self, name):
        self.name = name
        Driver.total_drivers += 1

    def accept_ride(self, ride_id):          # needs a specific driver → instance
        print(f"{self.name} took {ride_id}")

    @staticmethod
    def register():                          # no specific driver → static
        print("This is Register Method")
```

```python
Driver.register()          # called on the CLASS. No object anywhere.
```

**Two things to notice:**

1. `@staticmethod` is a **decorator** — the `@` line modifies the function below it. For now, read it as a label meaning *"this method receives no `self`."*
2. **There is no `self` parameter**, because there is no object to receive.

And the rule that follows: **a static method cannot touch instance attributes.** Not because Python forbids it, but because there is no `self` to touch them through. There is no object.

### The class body runs like a static block

Some languages have a *static block* — code that runs once, at class-loading time, before any object exists.

**Python needs no such construct, because the class body already is one.**

```python
class Driver:
    total_drivers = 15
    print("This is executed at time of Driver class definition")
```

Everything written directly inside `class Driver:` — not inside a method — executes **once**, the moment Python reads the class definition. That `print` fires on import, before any object exists.

Watch the order:

```python
class Driver:
    total_drivers = 0
    print("class body")                      # 1️⃣ ONCE, at definition

    def __init__(self, name):
        print("__init__")                    # 2️⃣ EVERY object
        self.name = name
        Driver.total_drivers += 1


print("--- creating objects ---")
Driver("Ashok")
Driver("Meera")
```

Output:
```
class body                ← once, before anything else
--- creating objects ---
__init__                  ← first object
__init__                  ← second object
```

**The class body never runs again**, no matter how many objects you create.

> **Coming later:** Python also has `@classmethod`, which receives the class as `cls`. It matters once inheritance is involved. For Day 1, `@staticmethod` plus `Driver.total_drivers` covers everything.

---

# 11. How Arguments Are Passed

### 📖 Definition

> **Python passes arguments by object reference — often called *call by sharing*. The function receives a copy of the reference, not a copy of the object.**

### 🌍 The story — the house address again

You hand a friend a **photocopy** of a slip with your home address.

**Case A — your friend drives there and repaints the door.**
You come home to a repainted door. ✅ **You see the change.** → this is **mutation**.

**Case B — your friend scratches out the address on their copy and writes a different one.**
Your slip is untouched. Your house is untouched. ❌ **You see nothing.** → this is **rebinding**.

That single analogy predicts every case in Python.

### 💻 The demonstration

```python
def add(x):
    x = x + 30                    # rebinds a local name

def change_name(driver):
    driver.name = "Xyz"           # mutates the object

def replace(driver):
    driver = Driver(9, "New")     # rebinds a local name
    driver.name = "Zzz"


x = 10
add(x)
print(x)                          # 10   ← UNCHANGED

d1 = Driver(1, "Abc", 5.0, True)
change_name(d1)
print(d1.name)                    # Xyz  ← CHANGED

replace(d1)
print(d1.name)                    # Xyz  ← replace() was completely invisible
```

### Why the difference

```
   add(x)                                change_name(d1)
   ────────────────────────────          ──────────────────────────────────
   x (caller)   ──► [ 10 ]               d1     (caller) ──┐
   x (function) ──► [ 10 ]  same object                    ├──► [ Driver ]
   x (function) ──► [ 40 ]  ← REBOUND    driver (function)─┘
   x (caller)   ──► [ 10 ]  ← untouched     ▲
                                            └── a copy of the REFERENCE,
                                                pointing at the SAME object
                                                → the edit is visible to both
```

`10` is an **immutable** `int`. `x = x + 30` cannot change it — it builds a new object and points the *local* name at it.
`d1` refers to a **mutable** object. `driver.name = "Xyz"` reaches through the reference and edits the real thing.

### The dividing line: mutable vs immutable

| Immutable — cannot be changed in place | Mutable — can be changed in place |
|:--|:--|
| `int`, `float`, `bool`, `str`, `tuple` | `list`, `dict`, `set`, **every class you write** |

### The rule

| What the function does | Does the caller see it? |
|:--|:--|
| **Mutates** the object — `obj.attr = ...`, `lst.append(...)` | ✅ **Yes** |
| **Rebinds** the parameter — `obj = something_new` | ❌ **No** |

### ⚠️ The same trap with lists

```python
def f(nums):
    nums.append(4)          # ✅ MUTATES → caller sees it

def g(nums):
    nums = nums + [4]       # ❌ REBINDS → new list, caller sees nothing

lst = [1, 2, 3]
f(lst); print(lst)          # [1, 2, 3, 4]
g(lst); print(lst)          # [1, 2, 3, 4]   ← g did nothing
```

Same intent. Opposite result. The only difference is whether you changed the existing object or built a new one.

### 🌍 Why this matters in real code

```python
def assign_trip(driver, trip):
    driver.is_online = False           # ✅ the caller's driver IS updated
    driver = find_backup_driver()      # ❌ the caller sees nothing — silent bug
```

The second line looks like it swaps in a different driver. It swaps the *local name*. The caller keeps the original driver, now marked offline, assigned to nothing. **This is a real class of production bug**, and it comes entirely from misunderstanding this section.

---

# 12. `__str__` — Printing an Object

### 📖 Definition

> **`__str__` defines how an object should be represented as a human-readable string.**

### ❓ Why we need it

Print an object without it:

```python
print(d1)      # <__main__.Driver object at 0x7f8b2c0d1a90>
```

The class name and a memory address. Technically correct, **humanly useless**.

### 🌍 The story

It is 2am. Dispatch is failing in one city. You open the logs:

```
ERROR  Failed to assign trip: <__main__.Driver object at 0x7f8b2c0d1a90>
ERROR  Failed to assign trip: <__main__.Driver object at 0x7f8b2c0d1b40>
ERROR  Failed to assign trip: <__main__.Driver object at 0x7f8b2c0d1cf0>
```

You have learned nothing. Now with `__str__`:

```
ERROR  Failed to assign trip: Driver(id=4021, name='Ashok', rating=4.8, online=False)
ERROR  Failed to assign trip: Driver(id=4088, name='Meera', rating=4.9, online=False)
ERROR  Failed to assign trip: Driver(id=4103, name='Ravi',  rating=4.7, online=False)
```

**Every one of them is offline.** You found the bug in three seconds — dispatch is selecting offline drivers. `__str__` isn't cosmetic; it's the difference between a debuggable system and an opaque one.

### ⚙️ How it works

`__str__` is a **dunder** (double-underscore) method — Python's mechanism for hooking your class into built-in behaviour. You met your first one already: `__init__` hooks into object creation. `__str__` hooks into `print()` and `str()`.

You never call it yourself. `print(d1)` calls it for you.

### 💻 Code

```python
class Driver:
    def __init__(self, driver_id, name, rating, is_online):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online

    def __str__(self):
        return (f"Driver(id={self.driver_id}, name='{self.name}', "
                f"rating={self.rating}, online={self.is_online})")


d1 = Driver(4021, "Ashok", 4.8, True)

print(d1)
# Driver(id=4021, name='Ashok', rating=4.8, online=True)

print(f"Assigned to {d1}")     # f-strings call it too
```

> ⚠️ **`__str__` must RETURN a string, not print one.**
> ```python
> def __str__(self):
>     print("Ashok")        # ❌ wrong
>     return "Ashok"        # ✅ right
> ```
> Returning a non-string raises `TypeError`.

> **Coming later:** Python has a second, developer-facing twin called `__repr__`, used in debuggers and when objects appear inside lists. We'll cover it once `__str__` is comfortable.

---

# 13. Encapsulation — Pillar 1 (Introduction)

*The first pillar, and the bridge into the next chapter.*

### 📖 Definition

> **Encapsulation is bundling data and the methods that operate on that data into a single unit, while restricting direct access to that data from outside.**

Two halves, both essential:

1. **Bundling** — data and behaviour in one class. *You have been doing this all chapter.*
2. **Restricting access** — the outside world cannot reach in and change the data directly.

### 🌍 The story

A **medicine capsule**. The powder is sealed inside a shell. You can't reach in and remove half the dose — you take it as designed. (The word is literal: *encapsulate*, to enclose in a capsule.)

Or an **ATM**. There is no slot that lets you reach into the vault. You get a fixed set of operations — withdraw, deposit, check balance — and the machine validates every one. You cannot withdraw ₹5,000 from a ₹200 balance, because the machine won't let you.

### ❓ Why we need it

Without restriction, anything can put your object into an impossible state:

```python
d1 = Driver(4021, "Ashok", 4.8, True)

d1.rating = -50        # 😱 a rating of minus fifty
d1.rating = "hello"    # 😱 a rating that is a word
d1.driver_id = -1      # 😱
```

Nothing stops it. `Driver` *knows* a rating must be between 0 and 5 — but it has no way to enforce that, because the attribute is wide open.

Now think about what that does to Part 0. The dispatch service sorts candidates by rating and ETA. A driver with `rating = -50` sorts to one end of every list and either never gets a trip or always does. **The bug isn't in dispatch. The bug is a line somewhere else that was allowed to write nonsense into an attribute, and you will spend a night finding it.**

**Encapsulation makes the class responsible for its own validity** — instead of trusting every other file in the project to be careful.

### ⚙️ How Python does it

**Python has no `private` keyword.** There is no compiler standing guard. Instead there is a naming convention that every Python developer understands:

| Written as | Means |
|:--|:--|
| `self.name` | **Public.** Part of the API. Use freely |
| `self._rating` | **Internal.** "Don't rely on this — it may change without warning" |
| `self.__secret` | **Name-mangled** to `_Driver__secret`. Avoids collisions in inheritance |

```python
class Driver:
    def __init__(self, driver_id, name, rating):
        self.driver_id = driver_id       # public
        self.name = name                 # public
        self._rating = rating            # internal by convention
```

### ⚠️ The underscore enforces nothing

```python
d1._rating = -50        # runs perfectly. Nothing stops you.
```

Python's philosophy is often summarised as **"we are all consenting adults here."** Access control is a documented agreement between developers, not a locked door. In some languages the compiler stops you; in Python your teammate stops you at code review.

**Does that make encapsulation weaker in Python?** In enforcement, yes. In practice, much less than you'd expect — because the convention is universal, tooling flags violations, and the real protection comes from the next piece.

### The controlled path in

The Day-1 version: give the class a method that validates, and mark the raw attribute internal.

```python
class Driver:
    def __init__(self, driver_id, name, rating):
        self.driver_id = driver_id
        self.name = name
        self._rating = rating
        self.is_online = False

    def get_rating(self):
        return self._rating

    def set_rating(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Rating must be a number")
        if not 0 <= value <= 5:
            raise ValueError("Rating must be between 0 and 5")
        self._rating = value
```

```python
d1 = Driver(4021, "Ashok", 4.8)

d1.set_rating(4.5)       # ✅ validated
d1.set_rating(-50)       # ❌ ValueError: Rating must be between 0 and 5
print(d1.get_rating())   # 4.5
```

The impossible state is now blocked — **provided everyone uses the method.**

### 🧠 Deeper — and why the next chapter matters

Two things to notice.

**First:** there is no `set_driver_id()`. That's intentional. A driver's ID should never change after creation. **Encapsulation lets you make something read-only** simply by offering a getter and no setter.

**Second:** this connects straight back to abstraction. Once callers go through `get_rating()` instead of touching the attribute, you can change how rating is stored — compute it live from the last 100 trips, cache it, fetch it from another service — **without breaking a single caller.**

But look at the code again. `d1.set_rating(4.5)` is clumsy compared to `d1.rating = 4.5`. And in Python, writing `get_x` / `set_x` for every attribute is considered **bad style** — you'll be marked down for it in a code review.

Python resolves this with a feature called `@property`, which lets you keep the clean `d1.rating = 4.5` syntax while running validation behind it. It is the reason Python developers start with plain public attributes and add protection only when it's actually needed.

> **Next chapter:** encapsulation in depth — `@property`, read-only attributes, and why "add a getter and setter for every field" is not actually encapsulation.

---

# The complete Day-1 class

Everything from this chapter in one runnable file.

```python
class Driver:
    """A driver in the Uber dispatch system."""

    # ---- class body: runs ONCE, at class definition ----
    total_drivers = 0
    print("Driver class loaded")

    # ---- constructor: one __init__, defaults cover every case ----
    def __init__(self, driver_id=100, name="Random", rating=5.0, is_online=True):
        self.driver_id = driver_id           # instance attributes
        self.name = name
        self.rating = rating
        self.is_online = is_online
        Driver.total_drivers += 1            # class name, NOT self

    # ---- instance methods ----
    def accept_ride(self, ride_id):
        print(f"{self.name} accepted ride {ride_id}")

    def change_status(self):
        self.is_online = not self.is_online
        print(f"{self.name} is online: {self.is_online}")

    # ---- static method: callable with no object ----
    @staticmethod
    def register():
        print("This is Register Method")

    # ---- printable form ----
    def __str__(self):
        return (f"Driver(id={self.driver_id}, name='{self.name}', "
                f"rating={self.rating}, online={self.is_online})")


# ---- module-level functions: argument passing ----
def add(x):
    x = x + 30                      # rebinds a local name


def change_name(driver):
    driver.name = "Xyz"             # mutates the real object


def replace(driver):
    driver = Driver()               # rebinds — invisible outside
    driver.name = "Zzz"


def main():
    # --- static method, before any object exists ---
    Driver.register()

    # --- objects ---
    d1 = Driver(4021, "Ashok", 4.8, True)
    d2 = Driver(4088, "Meera", 4.9, True)
    d3 = Driver()

    print(d1)                       # __str__
    print(d2)
    print(d3)

    # --- class attribute ---
    print("Total drivers:", Driver.total_drivers)      # 3

    # --- self: same method, different objects ---
    d1.accept_ride("R-101")
    d2.accept_ride("R-102")

    # --- state ---
    d1.change_status()

    # --- references: two names, one object ---
    d4 = d1
    d4.name = "Xyz"
    print(d1.name)                  # Xyz  ← d1 changed too
    print(d1 is d4)                 # True ← same object

    # --- argument passing ---
    x = 10
    add(x)
    print("x =", x)                 # 10   ← unchanged

    change_name(d2)
    print(d2.name)                  # Xyz  ← changed

    replace(d2)
    print(d2.name)                  # Xyz  ← replace was invisible


if __name__ == "__main__":
    main()
```

**Run it:**

```bash
python3 driver.py
```

> **What is `if __name__ == "__main__":`?** It means *run `main()` only when this file is executed directly, not when another file imports it.* Without it, your test code fires every time someone imports your module.

---

# Glossary

| Term | Meaning |
|:--|:--|
| **Entity** | A real-world person, place, thing, or concept to represent in code |
| **Class** | A blueprint defining structure and behaviour |
| **Object** | An instance of a class; memory has been allocated for it |
| **Instance** | Another word for object — "an instance *of* a class" |
| **Instance attribute** | A variable belonging to one object (`self.x`) |
| **Class attribute** | A variable belonging to the class, shared by all objects |
| **Method** | A function belonging to a class |
| **State** | The values of an object's attributes at a given moment |
| **Reference** | A name pointing at an object; never the object itself |
| **`self`** | A reference to the current object |
| **`__init__`** | The initialiser, run automatically on object creation |
| **Dunder method** | A `__double_underscore__` method hooking into built-in behaviour |
| **Decorator** | An `@name` line that modifies the function below it |
| **Mutable / Immutable** | Whether an object can be changed in place |
| **Mutation** | Changing an existing object's contents |
| **Rebinding** | Pointing a name at a different object |
| **Interning** | Sharing one copy of identical immutable literals |
| **`__dict__`** | An object's own attributes, as a dictionary |
| **Abstraction** | Representing a complex system through a simple interface |
| **Encapsulation** | Bundling data with its methods and restricting outside access |

---

# The Day-1 mistake list

| # | Mistake | Fix |
|:--|:--|:--|
| 1 | Forgetting `self` in the method signature | `def f(self, x)` |
| 2 | `name = x` instead of `self.name = x` | Always prefix with `self.` |
| 3 | `self.counter += 1` for a class attribute | `Driver.counter += 1` |
| 4 | Mutable class attribute (`rides = []`) | Move it into `__init__` |
| 5 | Mutable default argument (`def f(x=[])`) | `def f(x=None)` then build inside |
| 6 | Writing two `__init__` methods | Use default arguments |
| 7 | Using `==` to check identity | `is` for identity, `==` for value |
| 8 | Using `is` to compare numbers or strings | Use `==` |
| 9 | Setting some attributes outside `__init__` | Initialise every attribute in `__init__` |
| 10 | `__str__` printing instead of returning | `return f"..."` |
| 11 | `camelCase` names | `snake_case` for methods and variables |
| 12 | Mixing tabs and spaces | 4 spaces, always |

---

# Practice

### Conceptual

1. Explain the difference between a class and an object using an analogy that is **not** blueprint/house.
2. Why is abstraction called a *principle* rather than a *pillar*?
3. When you have written a class but created no objects, what exists in memory and what doesn't?
4. Why does a static method have no `self` parameter? Answer from first principles.
5. Why must `register()` be a static method? Connect it to any app's sign-up flow.
6. Uber replaced its entire routing engine. Why did dispatch code barely change? Name the property that made this possible.

### Predict the output

7. ```python
   d1 = Driver(1, "Abc")
   d2 = d1
   d2.name = "Xyz"
   print(d1.name)
   ```

8. ```python
   class Counter:
       count = 0
       def __init__(self):
           self.count += 1

   a, b = Counter(), Counter()
   print(Counter.count, a.count, b.count)
   ```
   Predict all three values, explain the mechanism, then fix the class.

9. ```python
   class Driver:
       rides = []
       def add(self, r):
           self.rides.append(r)

   d1, d2 = Driver(), Driver()
   d1.add("R-101")
   print(d2.rides)
   ```
   Why does this happen, and why doesn't it happen in question 8's fixed version?

10. `add(x)` leaves `x` at 10, but `change_name(d1)` does change `d1`. Explain both using only the words *mutation* and *rebinding*.

### Write code

11. Build a `Student` class for a College Management System: attributes `name`, `email`, `phone`, `grad_year`; methods `join_class()` and `give_contest()`; a class attribute counting total students; a static `admission_open()`; a print statement in the class body; and `__str__`.

12. Write a `BankAccount` class with a class attribute `interest_rate` shared by all accounts and an instance attribute `balance`. Create three accounts, change `BankAccount.interest_rate` once, and prove all three see the new rate.

13. Take the `Driver` class from this chapter and add validation: store the rating as `_rating`, and add `set_rating()` that rejects anything outside 0–5 and anything that isn't a number. Then demonstrate that `d1._rating = -50` still gets through, and explain why that's acceptable in Python.

### Design

14. List the 5 high-level entities for a **Hospital Management System**. Then list 5 more you deliberately left out, and justify the split using the reasoning from Section 1.

15. Part 0 described finding the nearest driver. Sketch the method signature you'd put on a `DispatchService` class — what does it take, what does it return? Now argue why the caller should not need to know that H3 hexagons exist.

---

# Appendix — Quick map for Java learners

If you're also studying OOP in Java, here is the direct translation.

| Concept | Java | Python |
|:--|:--|:--|
| Define class | `public class Driver { }` | `class Driver:` |
| Declare field | `int driverId;` | *(none — assign in `__init__`)* |
| Create object | `Driver d = new Driver();` | `d = Driver()` |
| Constructor | `public Driver(...)` | `def __init__(self, ...)` |
| Current object | `this` (keyword) | `self` (explicit parameter) |
| Overloading | Multiple constructors | Default arguments |
| Class variable | `static int total;` | `total = 0` in the class body |
| Class-level init | `static { ... }` | The class body itself |
| Static method | `static void register()` | `@staticmethod` |
| Print an object | `toString()` | `__str__` |
| Private field | `private int x;` | `self._x` (convention only) |
| Getter/setter | `getX()` / `setX()` | Plain attribute → `@property` later |
| Identity check | `d1 == d2` | `d1 is d2` |
| Value check | `d1.equals(d2)` | `d1 == d2` |
| Null | `null` | `None` |
| Argument passing | Pass by value | Call by sharing — same behaviour |

> ⚠️ **Two differences that cause the most bugs when moving from Java:**
>
> **1. `==` and `is` are swapped.** Java's `==` is identity; Python's `==` is value. Java's `.equals()` is value; Python's `is` is identity.
>
> **2. `self` is never optional.** Java lets you drop `this` when there's no name collision. In Python, an assignment without `self.` creates a local variable and silently does nothing.

---

## Sources for the Uber engineering details

- H3: Uber's Hexagonal Hierarchical Spatial Index — https://www.uber.com/en-IN/blog/h3/
- H3 documentation — https://h3geo.org/
- Engineering Routing Engine at Uber — https://www.uber.com/en-IN/blog/engineering-routing-engine/
- DeepETA: How Uber Predicts Arrival Times Using Deep Learning — https://www.uber.com/en-IN/blog/deepeta-how-uber-predicts-arrival-times/
- Scaling Uber's Real-time Market Platform (DISCO) — https://highscalability.com/how-uber-scales-their-real-time-market-platform/

---

*Next chapter: **Encapsulation in depth** — `@property`, read-only attributes, and designing a class that cannot be misused.*
