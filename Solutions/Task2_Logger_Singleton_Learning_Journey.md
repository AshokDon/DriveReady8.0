# Task 2 — Logger → Singleton → Double-Checked Locking

## Learning Journey

We will use the same e-commerce application throughout this task.

```text
E-Commerce Application

        ┌──────────────┐
        │ User Service │
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │ Order Service│
        └──────┬───────┘
               │
        ┌──────▼────────┐
        │Payment Service│
        └───────────────┘
```

---

# PART 1 — What is a Logger?

## Step 1: Our application is doing many things

Suppose a customer places an order.

```text
User Login
    ↓
Create Order
    ↓
Process Payment
    ↓
Payment Successful
    ↓
Order Confirmed
```

If payment fails, a developer needs to know what happened before the failure.

We need a way to **record what is happening inside the application**.

That is where a **Logger** comes in.

---

## Step 2: What does a Logger do?

A Logger records application events.

Examples:

```text
Application started
User logged in
Order created
Payment started
Payment failed
```

These messages are called **logs**.

```text
Application
     ↓
   Logger
     ↓
  Log file
```

For example:

```text
application.log
```

---

## Step 3: What does the log file look like?

```text
2026-09-17 10:20:15 [INFO] Application started
2026-09-17 10:20:18 [INFO] User logged in
2026-09-17 10:20:21 [DEBUG] Creating order
2026-09-17 10:20:25 [INFO] Order created
2026-09-17 10:20:30 [ERROR] Payment failed
```

Each log contains:

```text
Timestamp
    +
Log Level
    +
Message
```

For example:

```text
2026-09-17 10:20:30 [ERROR] Payment failed
│                    │       │
│                    │       └── Message
│                    └────────── Level
└────────────────────────────── Timestamp
```

---

## Step 4: What is Log Level?

Different messages have different importance.

```text
TRACE
DEBUG
INFO
WARN
ERROR
FATAL
```

Examples:

```text
[INFO] Application started
[DEBUG] Order ID = 101
[WARN] Payment service is slow
[ERROR] Payment failed
```

---

## Step 5: How does Python actually write into a file?

Forget Logger for a moment.

Python itself can write to a file:

```python
file = open("application.log", "a")

file.write("Application started\n")
file.write("Order created\n")

file.close()
```

The file becomes:

```text
application.log

Application started
Order created
```

Fundamentally:

```text
open()
   ↓
write()
   ↓
write()
   ↓
close()
```

A Logger is simply **organizing this file-writing process**.

---

# PART 2 — Build a Simple Logger

## Step 6: Hide file handling inside a class

```python
class Logger:

    def __init__(self):
        self.file = None

    def set_log_file(self, file_path):
        self.file = open(file_path, "a")

    def log(self, message):
        self.file.write(message + "\n")

    def close(self):
        self.file.close()
```

Client code:

```python
logger = Logger()

logger.set_log_file("application.log")

logger.log("Application started")
logger.log("Order created")
logger.log("Payment successful")

logger.close()
```

The Logger hides:

```text
open()
write()
close()
```

from the client.

---

## Step 7: Add Log Level and Timestamp

Instead of:

```python
logger.log("Payment failed")
```

we want:

```python
logger.log(LogLevel.ERROR, "Payment failed")
```

The Logger creates:

```text
2026-09-17 10:20:30 [ERROR] Payment failed
```

Internally:

```text
log(level, message)
       ↓
Get current time
       ↓
Add level
       ↓
Add message
       ↓
Create complete log line
       ↓
Write to file
```

---

# PART 3 — Logger is a Service

## Step 8: Multiple services need Logger

Our application now has:

```text
                 ┌──────────────┐
                 │ User Service │
                 └──────┬───────┘
                        │
                 ┌──────▼───────┐
                 │ Order Service│
                 └──────┬───────┘
                        │
                 ┌──────▼───────┐
                 │Payment Service│
                 └──────┬───────┘
                        │
                        ▼
                  ┌──────────┐
                  │  Logger  │
                  └────┬─────┘
                       │
                       ▼
                application.log
```

Initially, we might create:

```text
User Service
     ↓
 Logger 1 ─────┐
               │
Order Service  │
     ↓         ├──→ application.log
 Logger 2 ─────┤
               │
Payment Service│
     ↓         │
 Logger 3 ─────┘
```

Now ask:

> **Do we really need three Logger objects?**

---

# PART 4 — Do We Need Multiple Logger Objects?

## Step 9: Think about the responsibility of Logger

Our Logger writes to:

```text
application.log
```

If the entire application uses one log file, why create:

```text
Logger 1
Logger 2
Logger 3
```

?

We can have:

```text
User Service ────┐
                 │
Order Service ───┼──→ ONE LOGGER ──→ application.log
                 │
Payment Service ─┘
```

Now the question becomes:

> **How can we make sure the application creates only one Logger object?**

---

# PART 5 — Convert Logger into Singleton

## Step 10: Normal class allows multiple objects

```python
class Logger:

    def __init__(self):
        self.file = None
```

This allows:

```python
logger1 = Logger()
logger2 = Logger()
logger3 = Logger()
```

And:

```python
logger1 is logger2
```

is:

```text
False
```

We want:

```python
logger1 = Logger.get_instance()
logger2 = Logger.get_instance()
logger3 = Logger.get_instance()
```

with:

```python
logger1 is logger2
logger2 is logger3
```

resulting in:

```text
True
```

---

## Step 11: Store the single object

Use a class variable:

```python
class Logger:

    _instance = None
```

Initially:

```text
Logger._instance
      ↓
    None
```

First request:

```text
get_instance()
      ↓
_instance == None
      ↓
Create Logger
      ↓
Store it in _instance
```

Next request:

```text
get_instance()
      ↓
_instance != None
      ↓
Return existing object
```

---

## Step 12: Simple Singleton first

```python
class Logger:

    _instance = None

    @classmethod
    def get_instance(cls):

        if cls._instance is None:
            cls._instance = cls()

        return cls._instance
```

First call:

```text
get_instance()
      ↓
_instance == None
      ↓
create object
      ↓
_instance = object
      ↓
return object
```

Second call:

```text
get_instance()
      ↓
_instance != None
      ↓
return existing object
```

---

# PART 6 — But There Is a Problem

## Step 13: Multiple threads

Imagine two threads request the Logger at the same time:

```text
Thread 1
    ↓
get_instance()

Thread 2
    ↓
get_instance()
```

Suppose:

```text
_instance = None
```

Both threads may see:

```text
_instance is None → True
```

Then:

```text
Thread 1 → creates Logger A
Thread 2 → creates Logger B
```

We could end up with:

```text
Thread 1 ──→ Logger A
Thread 2 ──→ Logger B
```

That breaks our Singleton requirement.

So ask:

> **How do we make Singleton creation safe when multiple threads request it at the same time?**

---

# PART 7 — Add a Lock

## Step 14: Use a lock

```python
import threading

class Logger:

    _instance = None
    _instance_lock = threading.Lock()
```

Then:

```python
with cls._instance_lock:
```

means:

> Only one thread can enter this section at a time.

Flow:

```text
Thread 1 ──┐
           │
           ▼
         LOCK
           │
           ▼
      Create Logger
           │
           ▼
        UNLOCK
```

Thread 2 waits until Thread 1 finishes.

---

# PART 8 — Why Double Check?

## Step 15: The simple lock version

We could write:

```python
@classmethod
def get_instance(cls):

    with cls._instance_lock:

        if cls._instance is None:
            cls._instance = cls()

        return cls._instance
```

This is thread-safe.

But there is a performance problem.

Every call to:

```python
Logger.get_instance()
```

would acquire the lock.

After the Logger already exists, we don't need the lock.

So ask:

> **Can we check before taking the lock?**

Yes.

---

# PART 9 — Double-Checked Locking

## Step 16: Check before the lock

First check:

```python
if cls._instance is None:
```

If the object already exists:

```text
_instance exists
      ↓
return it
```

No lock is required.

Only when it doesn't exist:

```text
_instance == None
       ↓
     LOCK
       ↓
   CHECK AGAIN
       ↓
 create object
```

That's why it is called:

> **Double-Checked Locking**

We check `_instance` twice.

---

## Step 17: Final `get_instance()`

```python
@classmethod
def get_instance(cls):

    # First check
    if cls._instance is None:

        with cls._instance_lock:

            # Second check
            if cls._instance is None:
                cls._instance = cls()

    return cls._instance
```

Flow:

```text
             get_instance()
                   │
                   ▼
        Is instance already there?
             /           \
           YES            NO
            │              │
            │             LOCK
            │              │
            │              ▼
            │      Is instance still None?
            │          /        \
            │        NO          YES
            │        │            │
            │        │       Create object
            │        │            │
            │        │            ▼
            │        │      Store instance
            │        │            │
            └────────┴────────────┘
                         │
                         ▼
                  Return instance
```

---

# PART 10 — Why Do We Need the Second Check?

This is the most important part of Double-Checked Locking.

Suppose two threads arrive together:

```text
_instance = None
```

### Thread 1

```text
First check → None
      ↓
gets LOCK
```

### Thread 2

```text
First check → None
      ↓
waits for LOCK
```

Thread 1:

```text
LOCK
 ↓
Second check → None
 ↓
Create Logger A
 ↓
_instance = Logger A
 ↓
UNLOCK
```

Now Thread 2 gets the lock.

If there were no second check:

```text
Thread 2
   ↓
gets lock
   ↓
creates Logger B
```

Now we have two objects.

With the second check:

```text
Thread 2
   ↓
gets lock
   ↓
Second check
   ↓
_instance already exists
   ↓
DO NOT CREATE
   ↓
return Logger A
```

Correct.

---

# Final Learning Journey

```text
                    LOGGER
                       │
                       ▼
        What problem does Logger solve?
                       │
                       ▼
        Application needs to record events
                       │
                       ▼
              Write logs to a file
                       │
                       ▼
          Timestamp + Level + Message
                       │
                       ▼
                Build Logger
                       │
                       ▼
        Logger is used by many services
                       │
                       ▼
       Do we need multiple Logger objects?
                       │
                       ▼
                      NO
                       │
                       ▼
          One Logger → One log file
                       │
                       ▼
             How to ensure one?
                       │
                       ▼
                  SINGLETON
                       │
                       ▼
          _instance = None
                       │
                       ▼
              get_instance()
                       │
                       ▼
          But what about threads?
                       │
                       ▼
                     LOCK
                       │
                       ▼
       But do we need lock every time?
                       │
                       ▼
             First check before lock
                       │
                       ▼
       Second check inside the lock
                       │
                       ▼
          DOUBLE-CHECKED LOCKING
```

# Final Mental Model

### Layer 1 — Logger

> How do I write application events?

```text
Logger
   ↓
Format message
   ↓
Write to file
```

### Layer 2 — Singleton

> How many Logger objects do I need?

```text
One Logger
   ↓
Shared by services
```

### Layer 3 — Double-Checked Locking

> What if many threads request the Logger at the same time?

```text
Multiple Threads
       ↓
     Lock
       ↓
Safely create ONE
       ↓
Reuse that instance
```

## Key Idea

Do not start by memorizing:

```python
__new__()
threading.Lock()
```

First understand the problem:

> **We have one Logger service writing to one shared log file, so we want one shared Logger object. When multiple threads may create it simultaneously, we need thread-safe Singleton creation. Double-checked locking gives us a fast path after the instance already exists and a safe creation path when it doesn't.**
