# Task 1 — File-Based Configuration Manager

## Story: Building a Growing Software System

Imagine you are a **Software Engineer** working on a large software application.

The application is not one single program. It is made up of several services.

For example:

```text
                    E-Commerce Application
                            │
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
     User Service      Order Service      Payment Service
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ↓
                  Application Settings
```

Each service needs some common settings to decide how it should behave.

For example:

```text
app.name
database.url
timeout
max.connections
debug
```

These settings may come from a configuration file.

---

# The Problem

At first, the application is small.

A developer might simply create a configuration manager whenever a service needs it:

```python
config1 = FileBasedConfigurationManager()
```

Later, another service does the same thing:

```python
config2 = FileBasedConfigurationManager()
```

Now we have:

```text
User Service
     │
     ↓
Configuration Manager #1


Order Service
     │
     ↓
Configuration Manager #2
```

But we don't want every service to maintain its own configuration manager.

We want **one central configuration manager** that is shared by all services.

```text
                    Configuration Manager
                            │
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
        User Service   Order Service   Payment Service
             │              │              │
             └──────────────┼──────────────┘
                            ↓
                       SAME OBJECT
```

If one service changes a configuration value, other services should see the same configuration.

For example:

```text
User Service
    │
    └── set timeout = 30
              │
              ↓
      Configuration Manager
              │
              ├── Order Service sees 30
              └── Payment Service sees 30
```

---

# Your Responsibility

As the software engineer, design a **File-Based Configuration Manager** that can be shared by the entire application.

The most important requirement is:

> There should be only **one Configuration Manager instance at a time**.

This is the problem you need to solve using the **Singleton Design Pattern**.

---

# What Should the Configuration Manager Do?

Apart from being a Singleton, the configuration manager should provide basic configuration operations.

It should allow services to:

### 1. Set a configuration

Example:

```python
config.set_configuration("app.name", "MyApplication")
```

Another example:

```python
config.set_configuration("timeout", 30.5)
```

---

### 2. Get a configuration

Example:

```python
config.get_configuration("app.name")
```

Expected:

```text
MyApplication
```

If the key does not exist, return:

```text
None
```

---

### 3. Get a configuration with a type

Sometimes a configuration file stores values as text.

For example:

```text
max.connections = "100"
timeout = "30.5"
```

A service may want the value in a specific type.

Example:

```python
config.get_configuration("max.connections", int)
```

Expected:

```text
100
```

And:

```python
config.get_configuration("timeout", float)
```

Expected:

```text
30.5
```

Support at least:

```text
str
int
float
```

---

### 4. Remove a configuration

Example:

```python
config.remove_configuration("timeout")
```

After removal:

```python
config.get_configuration("timeout")
```

should return:

```text
None
```

---

### 5. Clear all configurations

Example:

```python
config.clear()
```

After clearing:

```python
config.get_configuration("app.name")
```

should return:

```text
None
```

---

# Singleton Requirement

The application should not allow different services to create independent Configuration Manager objects.

Consider:

```python
config1 = FileBasedConfigurationManager.get_instance()
config2 = FileBasedConfigurationManager.get_instance()
```

Both variables should refer to the same object.

Therefore:

```python
print(config1 is config2)
```

should produce:

```text
True
```

---

# Reset Requirement

For testing and application lifecycle management, the Singleton should also support resetting its current instance.

Provide:

```python
FileBasedConfigurationManager.reset_instance()
```

Example:

```python
config1 = FileBasedConfigurationManager.get_instance()

FileBasedConfigurationManager.reset_instance()

config2 = FileBasedConfigurationManager.get_instance()
```

After the reset, a new instance should be created.

Therefore:

```python
print(config1 is config2)
```

should produce:

```text
False
```

---

# Required Files

Create the following three files:

```text
client.py
config_manager.py
singleton_config_manager.py
```

## `config_manager.py`

Create the base/abstract configuration manager.

It should define the configuration operations:

```text
get_configuration()
set_configuration()
remove_configuration()
clear()
```

It should also contain the configuration storage.

---

## `singleton_config_manager.py`

Create the concrete `FileBasedConfigurationManager`.

This class is responsible for:

- Implementing Singleton behaviour
- Providing `get_instance()`
- Providing `reset_instance()`
- Implementing configuration operations

---

## `client.py`

Create a client program that demonstrates the complete behaviour.

The client should:

1. Obtain a configuration manager.
2. Store configuration values.
3. Read configuration values.
4. Read values using type conversion.
5. Obtain the configuration manager again.
6. Verify that both references point to the same object.
7. Remove a configuration.
8. Clear all configurations.
9. Reset the Singleton.
10. Obtain the configuration manager again.
11. Verify that a new object was created after reset.

---

# Example Configuration

You may use:

```text
app.name          = MyApplication
max.connections   = 100
timeout           = 30.5
database.url      = localhost:5432
debug             = true
```

---

# Expected Behaviour

Your client should demonstrate output similar to:

```text
App Name: MyApplication
Max Connections: 100
Timeout: 30.5

Same instance: True

Timeout after removal: None

App Name after clear: None

New instance after reset: False
```

---

# Important Constraints

- The client should not directly manage Singleton creation logic.
- Use `get_instance()` to obtain the Configuration Manager.
- There should be only one active Configuration Manager instance at a time.
- `reset_instance()` should allow the Singleton to be recreated.
- Keep configuration storage inside the Configuration Manager.
- Keep the client focused on using and testing the manager.
- Use clear class, method, and variable names.

---

# What You Are Expected to Think About

Before writing the final solution, think about these questions:

### Question 1

What happens if we simply write:

```python
config1 = FileBasedConfigurationManager()
config2 = FileBasedConfigurationManager()
```

Are they the same object?

---

### Question 2

If they are different, where can we store a reference to the one object that should be shared?

---

### Question 3

How can we prevent normal object creation from producing different objects?

---

### Question 4

In Python, which part of the object creation process can we control?

---

### Question 5

How should `get_instance()` behave?

---

### Question 6

What should happen when `reset_instance()` is called?

---

# Goal of the Assignment

By completing this assignment, you should understand how to move from a normal class to a **Singleton-based shared service**.

You should be able to explain:

```text
Normal Class
     ↓
Multiple Objects
     ↓
Problem: Different Configuration Managers
     ↓
Requirement: One Shared Object
     ↓
Singleton
     ↓
get_instance()
     ↓
reset_instance()
```

The focus of this task is **Singleton + Configuration Management**.
