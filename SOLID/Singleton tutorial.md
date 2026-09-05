# Design Patterns 01 — Singleton

**DriveReady 8.0 · AI Applied Engineer · Post-read**

Last module you learned SOLID: five principles that tell you *how to think* about a class.
This module is different. Design patterns don't tell you how to think — they hand you a
finished shape you can drop into a problem you've seen before.

We build one pattern in this post-read: **Singleton**. We start from a `DBConnection` class
that is written badly on purpose, and fix it one bug at a time. Every code sample appears in
both Java and Python, because the two languages break in different places and the differences
are the most interesting part.

---

## Contents

1. [What a design pattern actually is](#1-what-a-design-pattern-actually-is)
2. [The three families](#2-the-three-families)
3. [Singleton: what problem is it solving?](#3-singleton-what-problem-is-it-solving)
4. [Building one, step by step](#4-building-one-step-by-step)
5. [Eager or lazy?](#5-eager-or-lazy)
6. [Threads break it](#6-threads-break-it)
7. [The bug your language hides from you](#7-the-bug-your-language-hides-from-you)
8. [Saving and loading breaks it too](#8-saving-and-loading-breaks-it-too)
9. [The shortcuts: enum and module](#9-the-shortcuts-enum-and-module)
10. [Making a Singleton testable](#10-making-a-singleton-testable)
11. [Where it already runs in your code](#11-where-it-already-runs-in-your-code)
12. [Pitfalls, collected](#12-pitfalls-collected)
13. [Java ↔ Python glossary](#13-java--python-glossary)
14. [Interview questions](#14-interview-questions)
15. [Check yourself](#15-check-yourself)
16. [Homework](#16-homework)

---

## 1. What a design pattern actually is

A design pattern is a solution shape that enough engineers arrived at independently that it
got a name. Nobody invented Singleton. People kept writing the same six lines to solve the
same problem, someone noticed, and the shape got written down.

The 1994 book that collected 23 of these is by Gamma, Helm, Johnson and Vlissides, and
everybody calls it the **Gang of Four** book, or GoF, because writing out four surnames every
time is tiring. We'll cover about ten of the 23 in this module.

**Why bother learning the names?** Because of what happens in a design review. If you say
"let's put a Factory here," a teammate who knows the name understands the entire structure
you're proposing in about a second. Without the name you'd be drawing on a whiteboard for
five minutes. The pattern is the idea; the name is the compression.

**Two things people get wrong early:**

- Thinking patterns replace SOLID. They don't. A pattern is what SOLID looks like once you've
  applied it to a specific recurring problem. Singleton is not an alternative to SOLID — it's
  built out of it.
- Thinking you need to memorise all 23 names before you can write good code. You need to
  recognise the *problem*. The name is a label you attach afterwards.

---

## 2. The three families

The 23 patterns get sorted into three groups by the kind of problem they attack:

```
Creational   →  how and when objects get made
Structural   →  how classes and objects assemble into bigger things
Behavioural  →  how objects talk to each other and divide up work
```

This module is entirely **creational**:

```
Singleton    ← this post-read
Builder      ← next class
Prototype (+ Registry)
Factory (Simple / Method / Abstract)
```

Don't memorise which pattern sits in which family. The grouping is filing-cabinet
organisation, useful once you already know what each pattern does and useless before that.

---

## 3. Singleton: what problem is it solving?

```
Singleton
Guarantee that a class has exactly ONE object for the whole
program, and give everyone one agreed way to reach it.
```

Normally you can make as many objects of a class as you like. Singleton is the rule that says:
however many times anyone asks, hand back the *same* object. Not a copy, not an equivalent
one. If that object lives at memory address `200`, then every reference anywhere in the
program points at `200`.

### Why would you ever want that?

There are two separate reasons, and they're worth keeping separate in your head.

**Reason 1 — something shared sits behind the class.**

Think about the printer in an office. Everyone prints to the one machine. Buying five printers
doesn't make anyone's documents come out faster; it just costs four times as much and takes up
the room.

A database connection is the same. It's your app's open line to the database — the thing that
lets you actually read and write rows. Opening that line costs real work. Once it's open, it
can be reused indefinitely. If `UserService` opens one to save users and `OrderService` opens
another to save orders, you now have two lines doing one line's job, and you paid the setup
cost twice.

Loggers are the same shape. Five logger objects all writing to one file gains you nothing and
introduces the risk of them interleaving each other's output mid-line.

**Reason 2 — the object is genuinely expensive to build.**

Opening a fresh DB connection means sending host, username and password over the network,
opening a TCP connection, waiting for the server to accept it, and usually a handshake on top.
That is several network round-trips before you have run a single query.

Do that on every incoming HTTP request and your response times fall apart the moment real
traffic arrives. Build it once, reuse it forever. That's the entire economic argument.

```
Use Singleton when:
  1. A shared resource sits behind it   (DB connection, logger, cache client)
  2. Creating it is genuinely expensive (network, disk, heavy setup)

If neither is true, you're adding a restriction and buying nothing.
```

One more thing worth noticing: a Singleton is usually meant to be stable once built. It's the
one dependable thing everyone leans on, so it should not be changing shape underneath them.

**A common misreading:** people say Singleton is about "saving memory." It isn't, really. Objects
are cheap. It's about not repeating expensive setup, and not ending up with several competing
copies of something that was supposed to be shared.

---

## 4. Building one, step by step

We'll start with a class that isn't a Singleton at all and fix it one problem at a time.

### Step 1 — the broken starting point

**Java**

```java
public class DBConnection {
    String url;
    String userName;
    String password;
    List<Connection> pool;
}
```

**Python**

```python
class DBConnection:
    def __init__(self, url, user_name, password):
        self.url = url
        self.user_name = user_name
        self.password = password
        self.pool = []
```

Is this a Singleton? No. Nothing stops anyone doing this:

**Java**

```java
DBConnection db1 = new DBConnection();
DBConnection db2 = new DBConnection();   // nothing prevents this
```

**Python**

```python
db1 = DBConnection("localhost", "root", "secret")
db2 = DBConnection("localhost", "root", "secret")   # nothing prevents this
print(db1 is db2)   # False — two separate objects
```

The problem: the constructor is public, so any line of code anywhere can make a new one.

### Step 2 — block the constructor

The obvious first move is to stop outside code from calling the constructor.

**Java**

```java
public class DBConnection {
    String url;
    String userName;
    String password;
    List<Connection> pool;

    private DBConnection() { }        // now unreachable from outside
}
```

**Python**

```python
class DBConnection:
    _allow_construction = False

    def __init__(self):
        if not DBConnection._allow_construction:
            raise RuntimeError("Use DBConnection.get_instance()")
        self.pool = []
```

Note the difference already. Java has a real access modifier: `private` means *the compiler
will not let you*. Python has no private constructor — the convention is a leading underscore
and a promise, and if you want an actual block you have to raise an error yourself. Python
programmers usually don't bother, and you'll see why in step 3.

We've now traded "too many objects" for "zero objects," which is a different flavour of
broken. We need the class to call its own constructor exactly once and hand the result out.

### Step 3 — one stored instance, one way in

We need a method that is:

- **public**, so outside code can call it, and
- **static** (Java) / a **classmethod** (Python), so it can be called *before any object
  exists*. You can't call an instance method on an object you haven't created yet.

**Java**

```java
public class DBConnection {
    String url;
    String userName;
    String password;
    List<Connection> pool;

    private static DBConnection instance = null;

    private DBConnection() { }

    public static DBConnection getInstance() {
        if (instance == null) {
            instance = new DBConnection();
        }
        return instance;
    }
}
```

**Python**

```python
class DBConnection:
    _instance = None                       # class attribute, one per class

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)   # build without calling __init__
            cls._instance.pool = []
        return cls._instance
```

Trace two calls back to back:

- **First call** — `instance` is null, so an object is built and stored.
- **Second call** — `instance` already holds something, so it's returned as-is. No new object.

```
The three moves:
  1. Stop outside code constructing it
  2. Keep one stored reference to the single instance
  3. Expose one method that builds it only if it doesn't exist, then returns it
```

**Why not just make the field public and skip the method?** Because then nothing guards it.
Any code anywhere could overwrite the reference and quietly break the guarantee for everyone
else. The method exists precisely to be the only door.

### The more Pythonic version

Python programmers rarely write `get_instance()`. The usual approach is to override `__new__`,
which runs *before* `__init__` and decides which object to return, so that plain
`DBConnection()` already does the right thing:

**Python**

```python
class DBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


db1 = DBConnection()
db2 = DBConnection()
print(db1 is db2)   # True
```

This looks clean and it is what almost every Python tutorial shows you.
**It also has a serious bug, which we get to in Section 7.** Hold that thought.

---

## 5. Eager or lazy?

Everything above waits for the first `getInstance()` call before building anything. That's
**lazy loading** — do the work when someone actually asks.

The alternative is to build it the moment the class loads, before anyone asks. That's **eager
loading**.

**Java**

```java
public class DBConnection {
    String url;
    String userName;
    String password;
    List<Connection> pool;

    private static DBConnection instance = new DBConnection();   // at class load

    private DBConnection() { }

    public static DBConnection getInstance() {
        return instance;                 // nothing to check, it already exists
    }
}
```

**Python**

```python
class DBConnection:
    def __init__(self):
        self.pool = []


# built at import time — the module body runs once, on first import
instance = DBConnection()


def get_instance():
    return instance
```

Picture a restaurant that cooks every dish on the menu before opening. Nobody waits for food.
But if half the menu goes unordered, that effort is gone.

```
Eager
  + Dead simple, no locking to think about
  - Slower startup
  - Config is fixed at load time, before you know what you need

Lazy
  + Nothing built until it's needed
  + Can use config decided at runtime
  - Needs care once multiple threads exist
```

That second eager downside matters more than people expect. If your connection details depend
on which environment you're running in, and that's only known once the app boots and reads its
config, eager loading has already locked in the wrong values.

**Don't over-learn this.** Eager is not automatically worse. For a small cheap object it's
simpler and there is no locking to get wrong. The trade-off only bites for something genuinely
expensive.

Because of the config problem, we go back to lazy. Which raises the question the rest of this
document is really about: what happens when two threads call it at the same time?

---

## 6. Threads break it

A real server does not handle one request at a time. Requests arrive together and run on
separate threads. Two threads can both be inside `getInstance()` at the same moment.

Here is what goes wrong:

```
Thread A: checks instance == null  →  true
Thread B: checks instance == null  →  true    (A hasn't finished yet)
Thread A: creates instance #1
Thread B: creates instance #2

Two objects. Singleton broken.
```

Both threads look, both see nothing, both build. This is a **race condition**: the outcome
depends on thread timing, which you do not control.

### "Doesn't the GIL protect Python?"

No. This is the single most common misconception in the room. The GIL guarantees that one
*bytecode* runs at a time. It does not stop a thread being switched out between the `is None`
check and the assignment — those are separate bytecodes.

Here is the actual measurement, eight threads against an unlocked `__new__` singleton:

```
distinct objects created: 2   (should be 1)
```

Two objects, in Python, with the GIL doing exactly what it promises. The race is real.

### Fix 1 — lock the whole thing

**Java**

```java
public static synchronized DBConnection getInstance() {
    if (instance == null) {
        instance = new DBConnection();
    }
    return instance;
}
```

**Python**

```python
import threading


class DBConnection:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        with cls._lock:                      # every call waits for the lock
            if cls._instance is None:
                cls._instance = cls.__new__(cls)
            return cls._instance
```

This is correct. But count the cost: after ten million calls, every one of those calls still
takes the lock — to guard against a race that can only ever happen once, on the very first
call. You're paying forever for a one-time risk.

### Fix 2 — double-checked locking

```
Double-checked locking
  1. Check without the lock       — fast, and true almost every time
  2. Only if it looks empty       → take the lock
  3. Check AGAIN inside the lock  — someone may have finished while you waited
  4. Only now build it
```

**Java**

```java
public static DBConnection getInstance() {
    if (instance == null) {                          // outer check, no lock
        synchronized (DBConnection.class) {
            if (instance == null) {                  // inner check, inside lock
                instance = new DBConnection();
            }
        }
    }
    return instance;
}
```

**Python**

```python
import threading


class DBConnection:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:                    # outer check, no lock
            with cls._lock:
                if cls._instance is None:            # inner check, inside lock
                    cls._instance = cls.__new__(cls)
        return cls._instance
```

**Why check twice?** Because a second thread can pass the outer check and *then* get stuck
waiting for the lock. By the time it gets in, the first thread has already built the object.
The inner check is what catches that. Without it, two threads pass the outer check, queue up
politely, and create two objects one after the other instead of simultaneously — same bug,
slightly different timing.

The inner check is the most frequently omitted line in this entire pattern.

Tick by tick:

```
tick:        1            2       3            4        5
Thread A:  outer-null    lock    inner-null   CREATE   unlock
Thread B:  outer-null    wait    wait         wait     lock → inner NOT null → reuse
```

1. Both see null.
2. A takes the lock. B waits.
3. A re-checks inside the lock. Still null. Safe to build.
4. A builds it.
5. A releases. B gets in, re-checks, finds it *not* null, and reuses A's object.

Measured, sixteen threads against the locked version:

```
distinct objects created: 1   ✓
```

---

## 7. The bug your language hides from you

Both languages have one trap here that compiles fine, looks correct, passes review, and is
wrong. They are different traps.

### Java: the missing `volatile`

This line looks like one step:

```java
instance = new DBConnection();
```

It is three:

```
1. allocate memory for the object
2. run the constructor, filling in the fields
3. point `instance` at that memory
```

Without `volatile`, the compiler and CPU are allowed to reorder those for performance. Step 3
can happen before step 2 finishes. A second thread then checks `instance == null`, sees a real
non-null reference, and returns it — while the constructor is still running. It has a
reference to a **half-built object**: real memory, fields not filled in yet.

```java
private static volatile DBConnection instance;
```

```
volatile does two jobs:
  1. Forbids that reordering
  2. Makes every thread read the current value, not a stale cached copy
```

This is the keyword AI assistants drop. Ask for "a thread-safe Singleton in Java" and you'll
usually get correct double-checked locking. Ask again with "keep it simple" or "make it
minimal" and `volatile` tends to quietly vanish, because to a casual reading it looks like
optional extra. It isn't. And it won't fail your compile, your tests, or your code review —
only production, under load, occasionally.

### Python: `__init__` runs every single time

Python has no reordering problem at the language level, so there is nothing like `volatile` to
forget. Python's trap is somewhere else entirely, and it's arguably worse because it looks
completely fine.

`__new__` decides which object comes back. `__init__` then runs on whatever `__new__` returned
— **every time you call the class**, cached instance or not.

**Python**

```python
class DBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        print("connecting to the database...")   # the expensive part
        self.pool = ["conn"]


a = DBConnection()
b = DBConnection()
print(a is b)
```

Output:

```
connecting to the database...
connecting to the database...
True
```

One object — and the expensive setup ran twice. Under ten concurrent callers, measured:

```
expensive setup ran, __new__ singleton  : 10 times  (10 callers)
expensive setup ran, metaclass singleton:  1 time   (10 callers)
```

Read that again. The `__new__` version returns one object, so it passes the `is` test, so it
looks like a working Singleton — and it re-runs the connection setup for every caller. The
whole reason we built a Singleton was to do that work once. This version quietly does not.

### The fix: a metaclass

`__new__` is too late to intercept. You need to get in front of the call itself, which is what
a metaclass's `__call__` does — it wraps both `__new__` and `__init__`.

**Python**

```python
import threading


class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:                      # outer check
            with cls._lock:
                if cls not in cls._instances:              # inner check
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DBConnection(metaclass=SingletonMeta):
    def __init__(self, url="localhost", user="root"):
        print("connecting to the database...")
        self.url = url
        self.pool = ["conn"]


a = DBConnection()
b = DBConnection()
print(a is b)
```

Output:

```
connecting to the database...
True
```

Once. That is the same double-checked locking from Section 6, applied one level higher — and
it is the closest Python equivalent to the Java version being genuinely correct.

### The habit to build

```
1. Ask AI for the first draft. It's fast and the shape is usually right.
2. Then interrogate it:
     "What's the subtle bug here?"
     "What breaks this under concurrency?"
     "What would a senior reviewer flag?"
3. In Java, look for one word: volatile.
   In Python, ask one question: does __init__ re-run?

AI is good at the textbook shape. You own the line that makes it correct.
```

---

## 8. Saving and loading breaks it too

Double-checked locking handles threads. It does nothing about **serialization** — turning an
object into bytes to save or send, then rebuilding it later.

Both languages break here, but in genuinely different ways, and the difference is worth
understanding rather than memorising.

### Java: you get a second object

Java deserialization rebuilds the object straight from the saved bytes. It skips your private
constructor and it never calls `getInstance()`. So a deserialized Singleton is a brand-new
second object, and your guarantee is gone.

### Python: you keep one object, but its state gets overwritten

`pickle` calls `cls.__new__(cls)`, which *does* hit your custom `__new__`, so you get the same
object back. Identity survives. But pickle then restores the saved `__dict__` onto it — so an
old snapshot silently overwrites whatever the live object currently holds.

**Python**

```python
import pickle

conn = DBConnection()
conn.url = "prod-db"

blob = pickle.dumps(conn)        # snapshot taken here
conn.url = "changed-later"       # live object moves on

restored = pickle.loads(blob)
print(restored is conn)          # True  — identity is fine
print(conn.url)                  # 'prod-db'  — the live object got rolled back
```

Java hands you a second object. Python keeps the one object and rewinds it. Both are bugs;
Python's is harder to spot because the `is` check still passes.

The Python fix is to tell pickle to resolve to the singleton rather than rebuild it:

**Python**

```python
class DBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __reduce__(self):
        return (DBConnection, ())    # "to rebuild me, just call DBConnection()"
```

---

## 9. The shortcuts: enum and module

Both languages have a built-in construct that already guarantees one instance, so you can stop
hand-building the machinery entirely.

### Java: the enum Singleton

An enum is normally for a fixed set of constants like days of the week. But the JVM's
guarantees about enum values happen to solve all three of our problems at once.

**Java**

```java
public enum DBConnection {
    INSTANCE;

    private final List<Connection> pool = new ArrayList<>();

    public List<Connection> getPool() {
        return pool;
    }
}

// used as:
DBConnection.INSTANCE.getPool();
```

```
An enum Singleton gets, free, guaranteed by the JVM:
  - exactly one instance
  - thread safety
  - safety against serialization
```

No private constructor, no `getInstance()`, no double-checked locking, no `volatile`. This is
why experienced Java engineers often reach for it directly.

### Python: the module *is* the Singleton

Python imports a module once and caches it in `sys.modules`. Every later import gets the same
module object back. So a module already behaves exactly like a Singleton, with no class
involved at all.

**Python**

```python
# db_connection.py
_pool = []
_connected = False


def _connect():
    global _connected
    print("connecting to the database...")
    _pool.append("conn")
    _connected = True


def get_pool():
    if not _connected:
        _connect()
    return _pool
```

```python
# anywhere else
from db_connection import get_pool

pool = get_pool()      # connects on first call, reuses forever after
```

This is the most Pythonic answer and it is what you should reach for first. No metaclass, no
`__new__`, no lock (module import itself is already thread-safe in CPython). If you don't
actually need a class, don't build one.

Python also has enums, and their members are singletons too:

**Python**

```python
from enum import Enum


class DBConnection(Enum):
    INSTANCE = "db"


print(DBConnection.INSTANCE is DBConnection("db"))   # True
```

```
Pick your tool:

Java    →  enum, unless you need constructor arguments
Python  →  module-level functions, unless you genuinely need a class;
           metaclass if you do
```

---

## 10. Making a Singleton testable

Section 3 sold you on Singleton. Here's the bill.

Tests want a clean slate every time. A Singleton is built specifically to refuse that — it
hands back the same object it handed the last test. So test three inherits whatever test one
did to the shared object, and now your suite passes or fails depending on the order it runs in.

`reset_instance()` is the escape hatch: a small method whose only job is to forget the stored
instance, so the next request builds a fresh one. It is **not** part of the GoF pattern. It's
something working engineers add because the pattern is otherwise awkward to test.

Think of the stored instance as an answer written on a whiteboard. Singleton keeps pointing at
the same board. `reset_instance()` is the eraser.

**Java**

```java
public class DBConnection {
    private static volatile DBConnection instance;

    private DBConnection() { }

    public static DBConnection getInstance() {
        if (instance == null) {
            synchronized (DBConnection.class) {
                if (instance == null) {
                    instance = new DBConnection();
                }
            }
        }
        return instance;
    }

    // for tests only — never call this from production code
    public static synchronized void resetInstance() {
        instance = null;
    }
}
```

**Python**

```python
import threading


class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def reset_instance(cls):                  # for tests only
        with cls._lock:
            cls._instances.pop(cls, None)


class DBConnection(metaclass=SingletonMeta):
    def __init__(self, url="localhost"):
        self.url = url
        self.pool = []
```

Wiring it into a test suite:

**Java**

```java
@BeforeEach                       // runs before every test method
void setUp() {
    DBConnection.resetInstance();
}

@Test
void connectionIsFreshEachTest() {
    DBConnection conn = DBConnection.getInstance();
    // guaranteed brand new, not left over from an earlier test
}
```

**Python**

```python
import unittest


class TestDBConnection(unittest.TestCase):
    def setUp(self):                          # runs before every test method
        DBConnection.reset_instance()

    def test_connection_is_fresh_each_test(self):
        conn = DBConnection()
        # guaranteed brand new, not left over from an earlier test
```

Note that `reset_instance` sits on the *metaclass*, which is why `DBConnection.reset_instance()`
works as a class-level call without a decorator. If you built your singleton with `__new__`
instead, the equivalent is a `@classmethod` that sets `cls._instance = None`.

**The rule that matters:** `reset_instance()` belongs in tests and nowhere else. Call it from
production code while other parts of the app still hold the old reference, and you now have two
live "shared" objects — precisely the bug Singleton exists to prevent.

---

## 11. Where it already runs in your code

If you've ever put `@Service` or `@Component` on a Spring Boot class, you've shipped a
Singleton. Spring's default bean scope is singleton: one instance, shared app-wide. You didn't
write `getInstance()`; the framework did it for you.

```
Singleton, running in production right now, everywhere:

  Spring beans            default scope for @Service / @Component / @Repository
  Connection pools        HikariCP — one pool per data source
  Logging                 Log4j, SLF4J, Python's logging.getLogger(name)
  Config and cache        one shared config object in memory
  Redis / HTTP clients    one client, reused across the app
  Python modules          every import you have ever written
```

That last one is worth sitting with. `logging.getLogger("app")` returns the same logger object
every time you ask for that name — that's a registry of singletons, built into the standard
library. And the connection *pool manager* being a Singleton is just Section 3's argument one
level up: one pool coordinating many connections beats several pools each opening their own.

---

## 12. Pitfalls, collected

```
1.  Treating patterns as separate from SOLID
      They're a named shape for applying those principles to a recurring problem.

2.  Using Singleton for something cheap and unshared
      No shared resource, no setup cost → you've added a restriction and gained nothing.

3.  Blocking construction without providing a way in
      Zero objects is as broken as many, just in the other direction.

4.  Exposing the instance field instead of a method
      Any code anywhere can then overwrite the shared reference.

5.  Assuming eager is always worse than lazy
      Fine for small cheap objects. The trade-off only matters for expensive ones.

6.  Assuming the race will show up in local testing
      It needs unlucky timing. It shows up in production, under load.

7.  Assuming Python's GIL prevents the race
      It doesn't. Measured: 2 objects from 8 unlocked threads.

8.  Double-checked locking with only the outer check
      Two threads pass it, queue for the lock, and still make two objects.

9.  Java — trusting a Singleton without checking for volatile
      No compile error, no obvious bug. Fails only under unlucky concurrency.

10. Python — assuming __new__ alone is enough
      One object, but __init__ re-runs per caller. Measured: expensive setup ran
      10 times for 10 callers. Use a metaclass, or a module.

11. Assuming locking makes it fully safe
      Serialization still breaks it. Java gets a second object; Python keeps one
      object and overwrites its state.

12. Reaching for Singleton without thinking about tests
      A global shared instance is hard to substitute. This is why DI still matters.

13. Forgetting to reset between tests
      Tests silently share leftover state and start depending on run order.

14. Calling reset_instance() from production code
      Two live "shared" objects. The exact bug the pattern exists to prevent.
```

---

## 13. Java ↔ Python glossary

| Concept | Java | Python |
|---|---|---|
| Block outside construction | `private` constructor | override `__new__`, or a metaclass |
| Store the one instance | `private static` field | class attribute, or module-level variable |
| The one way in | `public static getInstance()` | `__new__` / metaclass `__call__`, so plain `Cls()` works |
| Lock a section | `synchronized` | `with threading.Lock():` |
| Prevent reordering | `volatile` | not needed — no equivalent problem |
| The trap to check for | missing `volatile` | `__init__` re-running per call |
| Free built-in singleton | `enum` | a module, or an `Enum` member |
| Serialization damage | creates a second object | keeps the object, overwrites its state |
| Serialization fix | use `enum` | define `__reduce__` |
| Reset for tests | `static void resetInstance()` | `@classmethod` or a metaclass method |
| Test hook | `@BeforeEach` | `setUp()` |

**Terms**

| Term | Plain meaning |
|---|---|
| Design pattern | A reusable solution shape for a problem that keeps recurring |
| GoF | The four authors of the 1994 book that collected 23 of them |
| Creational pattern | A pattern about how and when objects get made |
| Singleton | Exactly one object of a class, shared everywhere |
| Eager loading | Build it immediately, before anyone asks |
| Lazy loading | Build it on first request |
| Race condition | A bug whose outcome depends on thread timing |
| Double-checked locking | Check without a lock, then again inside it, to avoid locking forever |
| GIL | CPython's global lock — one bytecode at a time, not one *operation* at a time |
| Serialization | Turning an object into bytes to store or transmit |
| Metaclass | The class of a class; its `__call__` runs when you call the class |

---

## 14. Interview questions

**1. What is a design pattern?**
A reusable solution shape for a problem that recurs across different systems — not one person's
clever idea, but something many engineers arrived at independently, which then got a name.

**2. Why does Singleton exist?**
Two reasons. A shared resource sits behind the class (DB connection, logger), so multiple
objects duplicate one object's job. Or the object is expensive to build, so you want to pay
that cost once.

**3. What are the pieces of a Java Singleton?**
Private constructor, private static field holding the instance, and a public static
`getInstance()` that builds it only if it doesn't exist.

**4. Eager vs lazy?**
Eager builds at class-load time: simpler, no locking, but slower startup and config is locked
in before runtime. Lazy builds on first use: no wasted work, supports runtime config, but needs
thread-safety handling.

**5. How does a race condition break a Singleton?**
Two threads both check the instance, both see it empty because neither has finished, and both
create their own. Two objects.

**6. Does Python's GIL prevent that?**
No. The GIL serialises bytecodes, not logical operations. A thread can be switched out between
the `is None` check and the assignment. You still need a `threading.Lock`.

**7. Why is plain `synchronized` correct but not ideal?**
It works, but every call forever takes the lock, guarding against a race that can only happen
on the first call.

**8. Why does double-checked locking need two checks?**
The outer one avoids the lock in the common case. The inner one catches the thread that passed
the outer check and then waited for the lock while another thread finished building.

**9. Why does missing `volatile` break Java's version?**
Object creation is allocate, construct, assign. Without `volatile` those can be reordered, so
the reference can be assigned before the constructor finishes. Another thread can then get a
half-built object.

**10. What's the Python equivalent of that trap?**
There isn't a reordering one. Python's trap is that `__init__` runs on every call even when
`__new__` returns a cached object — so a `__new__`-based singleton returns one object while
re-running its expensive setup for every caller. A metaclass fixes it.

**11. How does serialization break it, in each language?**
Java's deserialization skips the private constructor and `getInstance()`, producing a second
object. Python's `pickle` returns the same object but restores an old `__dict__` over it, so
identity holds while state silently rolls back.

**12. Why do experienced Java engineers prefer the enum Singleton?**
The JVM guarantees exactly one instance, thread safety and serialization safety for free — all
three problems that otherwise need separate manual fixes.

**13. What's the most Pythonic Singleton?**
A module. It's imported once, cached in `sys.modules`, and every later import returns the same
object. If you don't need a class, module-level functions and variables are the answer.

**14. Why add `reset_instance()` when it isn't in the GoF pattern?**
Testability. Singleton hands every test the same object, so state leaks between tests and
results depend on run order. Resetting forces a fresh object per test.

**15. What's the risk of calling it in production?**
If the instance is cleared while other code still holds the old reference, two "shared" objects
are live at once — the exact failure Singleton was built to prevent.

---

## 15. Check yourself

1. Give the two reasons for limiting a class to one object, and an example of each.
2. Write the three steps of a basic Singleton in order, in both languages.
3. Explain why exposing the instance field instead of a method breaks the guarantee.
4. What is the main cost of eager loading, and when is it still the right choice?
5. Walk two threads through the unlocked version and show how two objects appear.
6. Why is double-checked locking preferred over locking the whole method?
7. Explain instruction reordering, and how it produces a half-built object.
8. What does `volatile` do, and why is it so easy to drop?
9. Why doesn't Python need `volatile`, and what does it need instead?
10. Explain why `__new__` alone is not enough for a Python Singleton. Predict the output of the
    ten-caller example before running it.
11. Describe how serialization breaks the pattern differently in each language.
12. Name three places Singleton already runs in code you've written without calling it that.
13. Write `reset_instance()` in both languages and say in one sentence what it fixes.
14. Explain why calling `reset_instance()` inside request-handling code is dangerous.

---

## 16. Homework

```
1. Implement DBConnection as a Singleton in BOTH languages:
     Java   — double-checked locking + volatile
     Python — metaclass with a lock
   Comment each one explaining the specific bug that line prevents.

2. Prove the Python bug to yourself. Write the __new__ version with a print()
   in __init__, call it 10 times, and record the output. Then swap to the
   metaclass and record it again. Put both outputs in your README.

3. Ask an AI assistant for a "simple thread-safe Singleton Logger" in each
   language. Find at least one real bug in each answer. Write down what was
   missing — for Java check volatile, for Python check __init__.

4. Rewrite the Java version as an enum and the Python version as a plain
   module. Which felt easier to get right? Which would you actually ship?

5. Push everything to GitHub — branch: singleton-lecture-complete
```

---

[Uploading singleton-tutorial.html…]()

