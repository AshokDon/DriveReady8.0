# Task 3 — Singleton Connection Pool

## Story: The Application Is Getting More Traffic

You are a Software Engineer working on the same large application from the previous tasks.

The application has several services:

```text
                    E-Commerce Application
                            │
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
     User Service      Order Service      Payment Service
```

The services need to communicate with a database.

A simple approach is to create a new database connection every time a service needs to perform a database operation.

For example:

```text
Order Service
     │
     ├── Request 1 → Create Connection
     ├── Request 2 → Create Connection
     ├── Request 3 → Create Connection
     └── Request 4 → Create Connection
```

As the application becomes busy, this becomes expensive.

Creating database connections repeatedly can involve:

- Creating network connections
- Authentication
- Resource allocation
- Connection setup and cleanup

We need a better approach.

---

# The Idea: Connection Pool

Instead of creating a new connection every time, we can create a fixed number of connections once and keep them ready.

This collection of reusable connections is called a **Connection Pool**.

For example, suppose the application creates a pool containing 5 connections:

```text
Connection Pool

┌────┬────┬────┬────┬────┐
│ C1 │ C2 │ C3 │ C4 │ C5 │
└────┴────┴────┴────┴────┘
```

When a service needs a connection, it takes one from the pool.

```text
Order Service
      │
      │ request connection
      ↓
 Connection Pool
      │
      └── C1
```

When the service finishes its work, it returns the connection.

```text
Order Service
      │
      │ release C1
      ↓
 Connection Pool
      │
      └── C1 becomes available again
```

The connection is **reused** instead of creating a completely new connection.

---

# The Next Problem

Now imagine different services create their own connection pool:

```text
User Service
     │
     ↓
Connection Pool #1
C1 C2 C3 C4 C5


Order Service
     │
     ↓
Connection Pool #2
C1 C2 C3 C4 C5
```

We now have two pools.

That means the application may have created:

```text
5 connections + 5 connections = 10 connections
```

when it actually wanted a single shared pool of 5 connections.

Instead, we want:

```text
                    Connection Pool
                          │
             ┌────────────┼────────────┐
             ↓            ↓            ↓
        User Service  Order Service  Payment Service
             │            │            │
             └────────────┼────────────┘
                          ↓
                    SAME POOL
```

There should be **one Connection Pool Manager** shared by the application.

---

# Your Responsibility

Design a **Singleton Connection Pool** that manages a fixed number of reusable database connections.

The most important requirements are:

1. There should be only one Connection Pool instance at a time.
2. The pool should contain a fixed number of database connections.
3. Services should be able to acquire an available connection.
4. Services should be able to release a connection back to the pool.
5. The pool should track available connections.
6. The pool should track total connections.
7. Access to the shared pool should be thread-safe.

You will use the **Singleton Design Pattern**.

---

# Understanding the Pool

Suppose the maximum number of connections is:

```text
5
```

After initialization:

```text
Pool

┌────┬────┬────┬────┬────┐
│ C1 │ C2 │ C3 │ C4 │ C5 │
└────┴────┴────┴────┴────┘
  A    A    A    A    A

A = Available
```

Therefore:

```text
Total Connections     = 5
Available Connections = 5
```

---

# Getting a Connection

Suppose a service requests a connection:

```python
connection = pool.get_connection()
```

The pool should provide one available connection and mark it as unavailable.

For example:

```text
Before:

┌────┬────┬────┬────┬────┐
│ C1 │ C2 │ C3 │ C4 │ C5 │
└────┴────┴────┴────┴────┘
  A    A    A    A    A


After:

┌────┬────┬────┬────┬────┐
│ C1 │ C2 │ C3 │ C4 │ C5 │
└────┴────┴────┴────┴────┘
  U    A    A    A    A

U = In Use
```

Now:

```text
Total Connections     = 5
Available Connections = 4
```

---

# Releasing a Connection

When the service finishes its database operation:

```python
pool.release_connection(connection)
```

The connection should become available again.

```text
Before:

┌────┬────┬────┬────┬────┐
│ C1 │ C2 │ C3 │ C4 │ C5 │
└────┴────┴────┴────┴────┘
  U    A    A    A    A


After:

┌────┬────┬────┬────┬────┐
│ C1 │ C2 │ C3 │ C4 │ C5 │
└────┴────┴────┴────┴────┘
  A    A    A    A    A
```

The connection is now available for another service.

---

# Connection Pool Operations

## 1. Initialize Pool

The pool should create a fixed number of dummy database connections.

Example:

```python
pool.initialize_pool()
```

If the pool was created with:

```text
max_connections = 5
```

it should create 5 `DatabaseConnection` objects.

---

## 2. Get Connection

```python
connection = pool.get_connection()
```

This should:

- Find an available connection.
- Mark it as unavailable.
- Return the connection.

If there are no available connections, your implementation should decide how to handle that situation based on your design.

---

## 3. Release Connection

```python
pool.release_connection(connection)
```

This should:

- Return the connection to the pool.
- Mark it as available again.

---

## 4. Get Available Connections Count

```python
pool.get_available_connections_count()
```

This should return the number of connections that are currently available.

Example:

```text
Total = 5
In Use = 2
Available = 3
```

The method should return:

```text
3
```

---

## 5. Get Total Connections Count

```python
pool.get_total_connections_count()
```

This should return the total number of connections created by the pool.

Example:

```text
Total = 5
In Use = 2
Available = 3
```

The method should return:

```text
5
```

---

# Singleton Requirement

The pool should be obtained through:

```python
pool1 = ConnectionPoolImpl.get_instance(5)
pool2 = ConnectionPoolImpl.get_instance(5)
```

Both references should point to the same object.

Therefore:

```python
print(pool1 is pool2)
```

should produce:

```text
True
```

The Singleton instance should be shared even when different services request the pool.

---

# Maximum Connections

The first call provides the maximum number of connections:

```python
ConnectionPoolImpl.get_instance(5)
```

This means the pool should manage at most:

```text
5 connections
```

The value is used when creating the Singleton/pool.

Think carefully about what should happen if `get_instance()` is called again with a different value:

```python
pool1 = ConnectionPoolImpl.get_instance(5)
pool2 = ConnectionPoolImpl.get_instance(10)
```

Since both calls return the same Singleton, you should not accidentally create a second pool.

---

# Reset Requirement

The pool should also provide:

```python
ConnectionPoolImpl.reset_instance()
```

After resetting, the next call to `get_instance()` should create a new pool.

Example:

```python
pool1 = ConnectionPoolImpl.get_instance(5)

ConnectionPoolImpl.reset_instance()

pool2 = ConnectionPoolImpl.get_instance(5)

print(pool1 is pool2)
```

Expected:

```text
False
```

---

# Thread-Safety Requirement

The application can have multiple threads requesting and releasing connections at the same time.

For example:

```text
Thread 1 → get_connection()
Thread 2 → get_connection()
Thread 3 → release_connection()
Thread 4 → get_connection()
```

The pool is shared by all of them.

Therefore, two threads should not accidentally acquire the same connection.

Your implementation should protect operations that modify the pool.

You may use Python's:

```python
threading
```

module.

---

# Required Files

Create the following three files:

```text
connection_pool.py
singleton_connection_pool.py
client.py
```

## `connection_pool.py`

Create:

```text
ConnectionPool
DatabaseConnection
```

`ConnectionPool` should define:

```text
initialize_pool()
get_connection()
release_connection()
get_available_connections_count()
get_total_connections_count()
```

`DatabaseConnection` represents a dummy database connection.

---

## `singleton_connection_pool.py`

Create:

```text
ConnectionPoolImpl
```

This class is responsible for:

- Singleton behaviour
- Creating the connection pool
- Initializing connections
- Providing connections
- Releasing connections
- Counting available connections
- Counting total connections
- Thread-safe pool access
- Resetting the Singleton

---

## `client.py`

Create a client that demonstrates:

1. Creating/getting a pool with a maximum number of connections.
2. Initializing the pool.
3. Checking total connections.
4. Checking available connections.
5. Getting a connection.
6. Checking the available count again.
7. Releasing the connection.
8. Checking the available count again.
9. Getting the Singleton again.
10. Verifying both pool references are the same.
11. Resetting the Singleton.
12. Getting a new pool.
13. Verifying that the new pool is a different object.

---

# Expected Behaviour

For a pool containing 5 connections, the client should demonstrate behaviour similar to:

```text
Total connections: 5
Available connections: 5

Available connections after get: 4

Available connections after release: 5

Same instance: True

New instance after reset: False
```

The exact order may depend on your implementation.

---

# Think Before You Code

### Question 1

What problem does a connection pool solve?

### Question 2

Why shouldn't every service create its own connection pool?

### Question 3

How do we represent connections that are available?

### Question 4

How do we represent connections that are currently being used?

### Question 5

What should happen when `get_connection()` is called?

### Question 6

What should happen when `release_connection()` is called?

### Question 7

How can we make sure the same connection is not given to two threads?

### Question 8

Where should the Singleton instance be stored?

### Question 9

What should happen if two threads request a connection at exactly the same time?

### Question 10

What should happen if there are no available connections?

---

# Goal

This task combines everything learned so far.

```text
Task 1
Singleton
   +
Shared Configuration
        ↓
Task 2
Singleton
   +
Shared Logger
   +
File Management
   +
Thread Safety
        ↓
Task 3
Singleton
   +
Shared Resource Pool
   +
Connection Management
   +
Thread Safety
```

The focus of this task is:

> **Singleton + Resource Pooling + Connection Management + Thread Safety**
