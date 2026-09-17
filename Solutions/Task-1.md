# Task 1 Solution — File-Based Configuration Manager

## 1. Understand the Story

We have an application with multiple services:

```text
                    E-Commerce Application
                            │
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
     User Service      Order Service      Payment Service
```

All services need common settings such as:

```text
app.name
database.url
timeout
max.connections
debug
```

The first thought is simple:

```python
config1 = FileBasedConfigurationManager()
config2 = FileBasedConfigurationManager()
```

But now we have two different objects.

The requirement says:

> There should be only one Configuration Manager instance.

That is exactly the problem Singleton solves.

---

# 2. Start With the Normal Class

Before thinking about Singleton, understand the normal object creation process:

```python
config1 = FileBasedConfigurationManager()
config2 = FileBasedConfigurationManager()
```

Conceptually:

```text
config1 ───────→ Object #1
config2 ───────→ Object #2
```

Therefore:

```python
config1 is config2
```

is:

```text
False
```

---

# 3. What Do We Need?

We need:

```text
config1 ─────┐
             ├──→ ONE Configuration Manager Object
config2 ─────┘
```

So we need a place to remember the single object.

A natural idea is a **class variable**:

```python
class FileBasedConfigurationManager:

    _instance = None
```

Think of it as:

```text
Class
 │
 └── _instance ──→ the one shared object
```

---

# 4. How Do We Stop Multiple Objects?

This is the important Python question.

When we write:

```python
FileBasedConfigurationManager()
```

Python performs object creation before initialization.

The method that controls object creation is:

```python
__new__()
```

The simplified flow is:

```text
Class(...)
   ↓
__new__()
   ↓
Object created
   ↓
__init__()
```

So Singleton logic belongs in `__new__()`.

---

# 5. Implement `__new__()`

We check whether the object already exists.

```python
def __new__(cls):

    if cls._instance is None:
        cls._instance = super().__new__(cls)

    return cls._instance
```

Let's understand it.

### First call

```python
config1 = FileBasedConfigurationManager()
```

Initially:

```text
_instance = None
```

Therefore:

```python
cls._instance = super().__new__(cls)
```

creates the object.

Now:

```text
_instance ──→ Object #1
```

---

### Second call

```python
config2 = FileBasedConfigurationManager()
```

Now:

```text
_instance ──→ Object #1
```

So the condition:

```python
cls._instance is None
```

is false.

We simply return the existing object.

Therefore:

```text
config1 ─────┐
             ├──→ Object #1
config2 ─────┘
```

---

# 6. Why `__init__()` Needs Care

There is an important Python detail.

Even if `__new__()` returns the same object, `__init__()` can still be called again.

So this is dangerous:

```python
def __init__(self):
    self.properties = {}
```

Suppose:

```python
config1 = FileBasedConfigurationManager()
config1.set_configuration("app.name", "MyApplication")

config2 = FileBasedConfigurationManager()
```

If `__init__()` resets the dictionary, the previous configuration can disappear.

We therefore initialize only once.

```python
def __init__(self):

    if hasattr(self, "_initialized"):
        return

    super().__init__()
    self._initialized = True
```

---

# 7. Why Do We Have a Base Class?

The assignment separates the configuration operations from the concrete Singleton implementation.

```text
ConfigManager
     ↑
     │
FileBasedConfigurationManager
```

The base class contains the shared configuration storage:

```python
class ConfigManager(ABC):

    def __init__(self):
        self.properties = {}
```

The concrete class implements the operations.

This keeps the design organized.

---

# 8. Implement `get_instance()`

The client should not need to know how the Singleton is created.

Instead of:

```python
FileBasedConfigurationManager()
```

we want:

```python
FileBasedConfigurationManager.get_instance()
```

Implementation:

```python
@classmethod
def get_instance(cls):
    return cls()
```

Why does this work?

Because `cls()` eventually calls our Singleton-controlled `__new__()`.

Flow:

```text
get_instance()
     ↓
cls()
     ↓
__new__()
     ↓
Existing object OR create one
     ↓
return Singleton
```

---

# 9. Implement `reset_instance()`

The assignment requires:

```python
FileBasedConfigurationManager.reset_instance()
```

The purpose is to remove the current Singleton reference:

```python
@classmethod
def reset_instance(cls):
    cls._instance = None
```

After this:

```text
_instance ──→ None
```

The next `get_instance()` creates a new object.

---

# 10. Implement `set_configuration()`

We store configuration values in a dictionary.

```python
def set_configuration(self, key, value):
    self.properties[key] = str(value)
```

Why convert to `str`?

The task represents configuration values as file-style values. Configuration files commonly store values as text.

For example:

```text
max.connections = "100"
timeout = "30.5"
```

---

# 11. Implement `get_configuration()`

Without a requested type:

```python
config.get_configuration("app.name")
```

we simply return the stored value.

```python
def get_configuration(self, key, value_type=None):

    value = self.properties.get(key)

    if value is None:
        return None

    if value_type is None:
        return value
```

---

# 12. Type Conversion

The task also allows:

```python
config.get_configuration("max.connections", int)
```

The stored value may be:

```text
"100"
```

but the caller wants:

```text
100
```

So:

```python
if value_type is str:
    return str(value)

if value_type is int:
    return int(value)

if value_type is float:
    return float(value)
```

---

# 13. Implement Remove

The requirement is:

```python
config.remove_configuration("timeout")
```

Implementation:

```python
def remove_configuration(self, key):
    self.properties.pop(key, None)
```

The `None` means that trying to remove a missing key does not cause an error.

---

# 14. Implement Clear

```python
def clear(self):
    self.properties.clear()
```

This removes every configuration value.

---

# 15. Final Implementation

## `config_manager.py`

```python
from abc import ABC, abstractmethod


class ConfigManager(ABC):

    def __init__(self):
        self.properties = {}

    @abstractmethod
    def get_configuration(self, key, value_type=None):
        pass

    @abstractmethod
    def set_configuration(self, key, value):
        pass

    @abstractmethod
    def remove_configuration(self, key):
        pass

    @abstractmethod
    def clear(self):
        pass
```

## `singleton_config_manager.py`

```python
from config_manager import ConfigManager


class FileBasedConfigurationManager(ConfigManager):

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if hasattr(self, "_initialized"):
            return

        super().__init__()
        self._initialized = True

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def reset_instance(cls):
        cls._instance = None

    def get_configuration(self, key, value_type=None):

        value = self.properties.get(key)

        if value is None:
            return None

        if value_type is None:
            return value

        if value_type is str:
            return str(value)

        if value_type is int:
            return int(value)

        if value_type is float:
            return float(value)

        raise TypeError(f"Unsupported type: {value_type}")

    def set_configuration(self, key, value):
        self.properties[key] = str(value)

    def remove_configuration(self, key):
        self.properties.pop(key, None)

    def clear(self):
        self.properties.clear()
```

---

# 16. Client

```python
from singleton_config_manager import FileBasedConfigurationManager


def main():

    config1 = FileBasedConfigurationManager.get_instance()

    config1.set_configuration("app.name", "MyApplication")
    config1.set_configuration("max.connections", 100)
    config1.set_configuration("timeout", 30.5)

    print("App Name:", config1.get_configuration("app.name"))

    print(
        "Max Connections:",
        config1.get_configuration("max.connections", int)
    )

    print(
        "Timeout:",
        config1.get_configuration("timeout", float)
    )

    config2 = FileBasedConfigurationManager.get_instance()

    print("Same instance:", config1 is config2)

    config1.remove_configuration("timeout")

    print(
        "Timeout after removal:",
        config2.get_configuration("timeout")
    )

    config1.clear()

    print(
        "App Name after clear:",
        config2.get_configuration("app.name")
    )

    FileBasedConfigurationManager.reset_instance()

    config3 = FileBasedConfigurationManager.get_instance()

    print("New instance after reset:", config1 is config3)


if __name__ == "__main__":
    main()
```

---

# 17. Final Mental Model

```text
                 FileBasedConfigurationManager
                              │
                     _instance variable
                              │
                              ↓
                       ONE OBJECT ONLY
                              │
          ┌───────────────────┼───────────────────┐
          ↓                   ↓                   ↓
       Service A           Service B           Service C
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ↓
                    Shared configuration
```

The key idea is:

> **Singleton controls how many objects can exist; the Configuration Manager controls what those objects do.**
