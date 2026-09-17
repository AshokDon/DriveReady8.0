# Task 3 Solution — Singleton Connection Pool

## 1. Understand the Story

The application now needs database access.

A simple approach is:

```text
Request
   ↓
Create Database Connection
   ↓
Use it
   ↓
Close it
```

For every request.

This can be expensive because creating a database connection involves resource allocation, networking, authentication, and setup.

So we introduce a **Connection Pool**.

---

# 2. What Is a Connection Pool?

A connection pool is simply a collection of reusable database connections.

Suppose the maximum number is 5:

```text
Pool

┌────┬────┬────┬────┬────┐
│ C1 │ C2 │ C3 │ C4 │ C5 │
└────┴────┴────┴────┴────┘
```

The application creates these connections once.

A service can borrow one:

```text
Service
   │
   └── get_connection()
             ↓
            C1
```

When finished:

```text
Service
   │
   └── release_connection(C1)
             ↓
       C1 becomes available
```

The connection is reused.

---

# 3. The Important State

Every connection is in one of two states:

```text
AVAILABLE
IN USE
```

For five connections:

```text
C1 → Available
C2 → Available
C3 → In Use
C4 → Available
C5 → In Use
```

Therefore:

```text
Total      = 5
Available  = 3
In Use     = 2
```

This gives us the central pool idea:

```text
Total = Available + In Use
```

---

# 4. Why Singleton?

Suppose each service creates its own pool.

```text
User Service
     ↓
Pool #1 → 5 connections

Order Service
     ↓
Pool #2 → 5 connections
```

Now we have 10 database connections.

Instead, we want:

```text
                    ONE Connection Pool
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
        User Service   Order Service   Payment Service
```

All services share the same pool.

This is another Singleton problem.

---

# 5. Define the Database Connection

The assignment gives a dummy `DatabaseConnection`.

For the Python version, we can give each connection an ID so that we can see which connection is being used.

```python
class DatabaseConnection:

    def __init__(self, connection_id):
        self.connection_id = connection_id
```

For example:

```text
DatabaseConnection(1)
DatabaseConnection(2)
DatabaseConnection(3)
```

---

# 6. Define the Pool Interface

The required operations are:

```text
initialize_pool()
get_connection()
release_connection()
get_available_connections_count()
get_total_connections_count()
```

Python:

```python
from abc import ABC, abstractmethod


class ConnectionPool(ABC):

    @abstractmethod
    def initialize_pool(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def release_connection(self, connection):
        pass

    @abstractmethod
    def get_available_connections_count(self):
        pass

    @abstractmethod
    def get_total_connections_count(self):
        pass
```

---

# 7. Choose the Data Structures

We need to track two groups:

```text
Available Connections
Connections In Use
```

A simple design is:

```python
self.available_connections = []
self.in_use_connections = set()
```

Conceptually:

```text
Pool
│
├── available_connections
│      ├── C1
│      ├── C2
│      └── C3
│
└── in_use_connections
       ├── C4
       └── C5
```

This makes the state easy to understand.

---

# 8. Singleton Creation

As in the previous tasks:

```python
_instance = None
```

But this task also has a parameter:

```python
get_instance(max_connections)
```

So the constructor receives:

```python
max_connections
```

We still control creation through `__new__()`.

Because the application can have multiple threads, protect Singleton creation with a lock.

```python
_instance_lock = threading.Lock()
```

---

# 9. Implement `__new__()`

```python
def __new__(cls, max_connections):

    if cls._instance is None:

        with cls._instance_lock:

            if cls._instance is None:
                cls._instance = super().__new__(cls)

    return cls._instance
```

The first call:

```python
pool1 = ConnectionPoolImpl.get_instance(5)
```

creates the object.

The next call:

```python
pool2 = ConnectionPoolImpl.get_instance(5)
```

returns the same object.

---

# 10. Initialize the Pool Object

The Singleton needs:

```text
max_connections
available_connections
in_use_connections
pool lock
```

Implementation:

```python
def __init__(self, max_connections):

    if hasattr(self, "_initialized"):
        return

    self.max_connections = max_connections
    self.available_connections = []
    self.in_use_connections = set()
    self._pool_lock = threading.Lock()

    self._initialized = True
```

The `hasattr()` check prevents resetting the pool every time `get_instance()` is called.

---

# 11. Why a Separate Pool Lock?

We now have two different shared concerns.

```text
_instance_lock
      ↓
Protect creation of Singleton

_pool_lock
      ↓
Protect available/in-use connection state
```

This is the same reasoning used in Task 2.

Do not think:

> "Thread safety means one lock everywhere."

Instead ask:

> "What shared state am I protecting?"

---

# 12. Initialize the Pool

Suppose:

```text
max_connections = 5
```

We create:

```python
for i in range(self.max_connections):
    connection = DatabaseConnection(i + 1)
    self.available_connections.append(connection)
```

After initialization:

```text
Available:

C1 C2 C3 C4 C5

In Use:

empty
```

Counts:

```text
Total = 5
Available = 5
```

---

# 13. Avoid Accidental Double Initialization

If:

```python
pool.initialize_pool()
pool.initialize_pool()
```

we should not create another five connections unless the design explicitly wants that.

A simple guard is:

```python
if self.available_connections or self.in_use_connections:
    return
```

Then initialization happens once for the current pool.

---

# 14. Get a Connection

The operation is:

```python
connection = pool.get_connection()
```

Before:

```text
Available:
C1 C2 C3 C4 C5

In Use:
empty
```

Take one:

```python
connection = self.available_connections.pop()
```

Then:

```python
self.in_use_connections.add(connection)
```

After:

```text
Available:
C1 C2 C3 C4

In Use:
C5
```

Return:

```python
return connection
```

---

# 15. What If There Are No Connections?

Suppose:

```text
Total = 5
Available = 0
In Use = 5
```

A new caller asks:

```python
pool.get_connection()
```

There is nothing to return.

For this assignment, a straightforward approach is:

```python
raise RuntimeError("No available connections")
```

A production pool might wait until another connection is released, but that is a more advanced requirement and is not necessary for this task.

---

# 16. Release a Connection

The caller returns:

```python
pool.release_connection(connection)
```

We need to move it:

```text
In Use
  ↓
Available
```

Implementation idea:

```python
if connection in self.in_use_connections:

    self.in_use_connections.remove(connection)
    self.available_connections.append(connection)
```

---

# 17. Why Check Ownership?

Imagine somebody passes an object that did not come from this pool.

We should not blindly add it.

At minimum:

```python
if connection not in self.in_use_connections:
    return
```

This ensures only a connection currently owned by the pool is released.

---

# 18. Count Available Connections

Simple:

```python
def get_available_connections_count(self):

    with self._pool_lock:
        return len(self.available_connections)
```

---

# 19. Count Total Connections

We can calculate:

```text
Total = Available + In Use
```

So:

```python
def get_total_connections_count(self):

    with self._pool_lock:
        return (
            len(self.available_connections)
            + len(self.in_use_connections)
        )
```

This is useful because it directly represents the pool's state.

---

# 20. Reset Singleton

As before:

```python
@classmethod
def reset_instance(cls):
    cls._instance = None
```

For a simple dummy connection, this is enough.

In a real database pool, reset/shutdown would normally also close all actual database connections.

That is beyond the dummy `DatabaseConnection` supplied by this assignment.

---

# 21. Complete `connection_pool.py`

```python
from abc import ABC, abstractmethod


class DatabaseConnection:

    def __init__(self, connection_id):
        self.connection_id = connection_id


class ConnectionPool(ABC):

    @abstractmethod
    def initialize_pool(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def release_connection(self, connection):
        pass

    @abstractmethod
    def get_available_connections_count(self):
        pass

    @abstractmethod
    def get_total_connections_count(self):
        pass
```

---

# 22. Complete `singleton_connection_pool.py`

```python
import threading

from connection_pool import (
    ConnectionPool,
    DatabaseConnection
)


class ConnectionPoolImpl(ConnectionPool):

    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, max_connections):

        if cls._instance is None:

            with cls._instance_lock:

                if cls._instance is None:
                    cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, max_connections):

        if hasattr(self, "_initialized"):
            return

        if max_connections <= 0:
            raise ValueError(
                "max_connections must be greater than 0"
            )

        self.max_connections = max_connections
        self.available_connections = []
        self.in_use_connections = set()

        self._pool_lock = threading.Lock()

        self._initialized = True

    @classmethod
    def get_instance(cls, max_connections):
        return cls(max_connections)

    @classmethod
    def reset_instance(cls):

        with cls._instance_lock:
            cls._instance = None

    def initialize_pool(self):

        with self._pool_lock:

            if (
                self.available_connections
                or self.in_use_connections
            ):
                return

            for i in range(self.max_connections):

                connection = DatabaseConnection(i + 1)

                self.available_connections.append(
                    connection
                )

    def get_connection(self):

        with self._pool_lock:

            if not self.available_connections:
                raise RuntimeError(
                    "No available connections"
                )

            connection = (
                self.available_connections.pop()
            )

            self.in_use_connections.add(connection)

            return connection

    def release_connection(self, connection):

        with self._pool_lock:

            if connection not in self.in_use_connections:
                return

            self.in_use_connections.remove(connection)

            self.available_connections.append(
                connection
            )

    def get_available_connections_count(self):

        with self._pool_lock:
            return len(self.available_connections)

    def get_total_connections_count(self):

        with self._pool_lock:
            return (
                len(self.available_connections)
                + len(self.in_use_connections)
            )
```

---

# 23. Client

```python
from singleton_connection_pool import (
    ConnectionPoolImpl
)


def main():

    pool1 = ConnectionPoolImpl.get_instance(5)

    pool1.initialize_pool()

    print(
        "Total connections:",
        pool1.get_total_connections_count()
    )

    print(
        "Available connections:",
        pool1.get_available_connections_count()
    )

    connection = pool1.get_connection()

    print(
        "Available connections after get:",
        pool1.get_available_connections_count()
    )

    pool1.release_connection(connection)

    print(
        "Available connections after release:",
        pool1.get_available_connections_count()
    )

    pool2 = ConnectionPoolImpl.get_instance(5)

    print(
        "Same instance:",
        pool1 is pool2
    )

    ConnectionPoolImpl.reset_instance()

    pool3 = ConnectionPoolImpl.get_instance(5)

    print(
        "New instance after reset:",
        pool1 is pool3
    )


if __name__ == "__main__":
    main()
```

---

# 24. Walk Through the Client

First:

```python
pool1 = ConnectionPoolImpl.get_instance(5)
```

Creates one Singleton pool.

Then:

```python
pool1.initialize_pool()
```

creates:

```text
C1 C2 C3 C4 C5
```

Therefore:

```text
Total = 5
Available = 5
```

Then:

```python
connection = pool1.get_connection()
```

One connection moves:

```text
Available = 4
In Use = 1
```

Then:

```python
pool1.release_connection(connection)
```

moves it back:

```text
Available = 5
In Use = 0
```

Then:

```python
pool2 = ConnectionPoolImpl.get_instance(5)
```

returns the same pool:

```python
pool1 is pool2
```

is:

```text
True
```

After:

```python
ConnectionPoolImpl.reset_instance()
```

the next call creates a new object.

Therefore:

```text
pool1 is pool3
```

is:

```text
False
```

---

# 25. Final Mental Model

The three tasks now build on each other.

## Task 1

```text
Singleton
    ↓
One shared Configuration Manager
```

## Task 2

```text
Singleton
    ↓
One shared Logger
    ↓
One shared file resource
    ↓
Thread-safe logging
```

## Task 3

```text
Singleton
    ↓
One shared Connection Pool
    ↓
Fixed number of reusable connections
    ↓
Available / In Use
    ↓
Acquire / Release
    ↓
Thread-safe pool state
```

The key new idea in Task 3 is:

> **We are not just sharing an object anymore. We are sharing and managing a collection of reusable resources.**

---

# 26. The Core Invariant

The most important relationship to remember is:

```text
Total Connections
        =
Available Connections
        +
Connections In Use
```

For example:

```text
Total = 5

Available = 3
In Use = 2

3 + 2 = 5
```

If your implementation ever violates this relationship, there is a bug in your pool management.
