# Task 2 — Singleton Logger

## Story: The Application Needs a Central Logger

You are a Software Engineer working on the same large application from Task 1.

The application has several services:

```text
                    E-Commerce Application
                            │
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
     User Service      Order Service      Payment Service
```

While the services are running, developers need to know what is happening inside the application.

For example:

```text
User Service     → User login successful
Order Service    → Order created
Payment Service  → Payment completed
```

These messages are useful for:

- Debugging problems
- Monitoring the application
- Understanding what happened during execution
- Finding errors

So the team decides to introduce a **central Logger**.

---

# The First Approach

A developer might create a logger whenever a service needs one:

```python
logger1 = Logger()
```

Another service might do:

```python
logger2 = Logger()
```

Now we have:

```text
User Service
     │
     ↓
Logger #1 → application.log


Order Service
     │
     ↓
Logger #2 → application.log
```

There can now be multiple logger objects trying to manage the same log file.

This can cause problems such as:

- Multiple objects managing the same file
- File access conflicts
- Different parts of the application using different logger state
- Unnecessary resource usage

The application needs **one central logger**.

---

# What Do We Actually Want?

All services should use the same Logger:

```text
                       Logger
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
     User Service    Order Service   Payment Service
          │              │              │
          └──────────────┼──────────────┘
                         ↓
                    SAME LOGGER
                         │
                         ↓
                  application.log
```

For example:

```text
User Service
     │
     └── log(INFO, "User logged in")
                  │
                  ↓
                Logger
                  │
                  ↓
           application.log
```

Then:

```text
Order Service
     │
     └── log(INFO, "Order created")
                  │
                  ↓
                Logger
                  │
                  ↓
           application.log
```

All services write through the **same Logger object**.

---

# Your Responsibility

Design a **Singleton Logger** that manages logging for the application.

The most important requirement is:

> There should be only **one Logger instance at a time**.

You will use the **Singleton Design Pattern**.

The Logger must also manage a **single log file** throughout the application's execution.

---

# Log Levels

A log message should have a level that describes the importance or type of the message.

Use these levels:

```text
TRACE
DEBUG
INFO
WARN
ERROR
FATAL
```

For example:

```python
logger.log(LogLevel.INFO, "User logged in")
```

or:

```python
logger.log(LogLevel.ERROR, "Payment failed")
```

The exact representation of `LogLevel` in Python is part of your implementation.

---

# Logging Format

Every log entry should contain:

1. A timestamp
2. The log level
3. The message

For example:

```text
2026-09-17 10:30:15 [INFO] User logged in
2026-09-17 10:30:20 [ERROR] Payment failed
```

The exact timestamp formatting is up to your implementation.

---

# Logger Operations

## 1. Set Log File

The Logger should allow the application to choose the file where logs are written.

Example:

```python
logger.set_log_file("application.log")
```

After this, log messages should be written to:

```text
application.log
```

---

## 2. Log

Write a message to the configured log file.

Example:

```python
logger.log(
    LogLevel.INFO,
    "User logged in successfully"
)
```

Another example:

```python
logger.log(
    LogLevel.ERROR,
    "Payment failed"
)
```

If `log()` is called before `set_log_file()`, the logger should raise an exception because it has not been initialized with a log file.

---

## 3. Get Log File

Return the current log file path.

Example:

```python
logger.get_log_file()
```

Expected:

```text
application.log
```

---

## 4. Flush

The Logger may buffer data before writing it completely to the file.

Provide:

```python
logger.flush()
```

This should flush pending log entries to the file.

---

## 5. Close

The Logger should release the file resource when it is no longer needed.

Provide:

```python
logger.close()
```

After closing, the logger should not continue writing through the closed file resource.

---

# Singleton Requirement

Consider:

```python
logger1 = LoggerImpl.get_instance()
logger2 = LoggerImpl.get_instance()
```

Both references should point to the same Logger object.

Therefore:

```python
print(logger1 is logger2)
```

should produce:

```text
True
```

---

# Reset Requirement

The Logger should also provide:

```python
LoggerImpl.reset_instance()
```

Example:

```python
logger1 = LoggerImpl.get_instance()

LoggerImpl.reset_instance()

logger2 = LoggerImpl.get_instance()
```

Now:

```python
print(logger1 is logger2)
```

should produce:

```text
False
```

The old Singleton has been reset and a new one has been created.

---

# Thread-Safety Requirement

The application may have multiple services or threads trying to write logs at the same time.

For example:

```text
Thread 1 → Logger → "User logged in"
Thread 2 → Logger → "Order created"
Thread 3 → Logger → "Payment completed"
```

The Logger should protect its shared file resource when performing logging operations.

Your implementation should therefore consider **thread-safe access** to the logger/file.

You may use Python's `threading` module.

---

# Required Files

Create the following three files:

```text
logger.py
singleton_logger.py
client.py
```

## `logger.py`

Create the base Logger interface/abstract class.

It should define:

```text
log()
set_log_file()
get_log_file()
flush()
close()
```

---

## `singleton_logger.py`

Create the concrete `LoggerImpl`.

It is responsible for:

- Singleton behaviour
- `get_instance()`
- `reset_instance()`
- Log file management
- Logging messages
- Flushing
- Closing
- Thread-safe access

---

## `client.py`

Create a client program that demonstrates the complete behaviour.

The client should:

1. Get the first Logger instance.
2. Configure a log file.
3. Write messages with different log levels.
4. Get the log file path.
5. Flush the logger.
6. Get the Logger instance again.
7. Verify that both references point to the same object.
8. Close the logger.
9. Reset the Singleton.
10. Get the Logger instance again.
11. Verify that a new object was created after reset.

---

# Expected Behaviour

Your client should demonstrate behaviour similar to:

```text
Log file: application.log
Same instance: True
New instance after reset: False
```

And `application.log` should contain entries similar to:

```text
2026-09-17 10:30:15 [INFO] Application started
2026-09-17 10:30:16 [DEBUG] User service initialized
2026-09-17 10:30:17 [WARN] Payment service is slow
2026-09-17 10:30:18 [ERROR] Payment failed
```

The exact timestamps will depend on when your program runs.

---

# Think Before You Code

### Question 1

What happens if every service creates its own Logger?

```python
logger1 = LoggerImpl()
logger2 = LoggerImpl()
```

Are they the same object?

---

### Question 2

If multiple logger objects use the same file, what could go wrong?

---

### Question 3

How can we make sure that every service receives the same Logger?

---

### Question 4

Where should we store the Singleton instance?

---

### Question 5

How can we control object creation in Python?

---

### Question 6

What happens if two threads try to create the Singleton at the same time?

---

### Question 7

What happens if two threads try to write to the log file at the same time?

---

### Question 8

Why do we need `flush()`?

---

### Question 9

Why do we need `close()`?

---

# Goal

Extend your understanding from Task 1:

```text
Task 1
Singleton
   ↓
Shared Configuration Manager
```

to:

```text
Task 2
Singleton
   ↓
Shared Logger
   ↓
One Log File
   ↓
Log Levels
   ↓
File Resource Management
   ↓
Thread-Safe Access
```

The focus of this task is:

> **Singleton + Logging + File Management + Thread Safety**
