# Prototype and Registry Design Patterns — Java Tutorial

> **Teaching style:** Problem → first attempt → problems → next question → pattern → improvement → real use case.

This tutorial teaches **Prototype** and **Registry** together using a cloud/Virtual Machine (VM) example. They are different design patterns, but they naturally work together.

---

## 1. Real-World Story: Why Are We Talking About VMs?

Imagine we are building a cloud platform.

A customer can request a **Virtual Machine (VM)**. A VM is a software-created computer. It can have an operating system, runtime, monitoring software, networking, storage, and other configuration.

For our LLD example, a VM has:

```text
VM
├── OS                → Ubuntu 22.04
├── Runtime           → Docker 1.2
├── Monitoring Agent  → Datadog
├── Hostname          → backend-01
└── IP Address        → 123.41.23.12
```

Suppose the infrastructure team has already configured a VM correctly.

A customer now says:

> "Give me another VM with the same configuration. I only want a different hostname and IP address."

Creating another VM from scratch means repeating configuration. This is where our problem starts.

---

## 2. The First Attempt: Copy Field by Field

We could create an empty object and copy every field:

```java
VMInstance copy = new VMInstance();

copy.setOs(instance1.getOs());
copy.setRuntime(instance1.getRuntime());
copy.setMonitoringAgent(instance1.getMonitoringAgent());
copy.setHostname(instance1.getHostname());
copy.setIpAddress(instance1.getIpAddress());
```

This works, but your notes identify four important problems: too many lines, the client must know object details, private attributes may be impossible to copy, and child types can lead to an if-else ladder that violates OCP. 

### Problem 1 — Too many lines

If a VM has 5 fields, this is manageable.

What if it has 50 or 100 configuration fields?

```text
5 fields     → manageable
50 fields    → painful
100 fields   → hard to maintain
```

### Problem 2 — Client knows too much

The client needs to know what fields exist and how they should be copied.

That creates **tight coupling**.

> Tight coupling means one class depends heavily on another class's details.

### Problem 3 — Private data

Suppose the VM has:

```java
private String encryptionKey;
```

and there is no getter.

The client cannot copy it.

But the VM itself can access its own private state.

### Problem 4 — Child classes

Suppose:

```text
VMInstance
    └── GpuVMInstance
```

The GPU VM has:

```java
private String gpuType;
```

The client may start doing:

```java
if (vmInstance instanceof GpuVMInstance) {
    copy = new GpuVMInstance((GpuVMInstance) vmInstance);
}
else if (vmInstance instanceof VMInstance) {
    copy = new VMInstance(vmInstance);
}
```

Add more VM types and the client keeps growing.

That is the OCP problem highlighted in the source notes.

---

## 3. Ask the Next Question

At this point, ask:

> **Who should know how to copy an object?**

The client?

No. The object itself already knows its state.

So we want:

```java
instance1.clone();
```

instead of asking the client to understand every field.

This is the core idea of the **Prototype Design Pattern**.

---

# 4. Prototype Pattern — Core Idea

### Simple definition

> **Prototype creates a new object by copying an existing object that acts as a template or sample.**

Think about a physical template.

If you have one correctly prepared form, you don't redesign the form every time. You use the existing form as a template.

In software:

```text
Correctly configured object
          ↓
       Prototype
          ↓
        clone()
          ↓
     New similar object
```

Your notes describe Prototype as a template/sample used when we want to create a copy of an object easily. 

---

## 5. Copy Constructor — First Improvement

A copy constructor can reduce the field-by-field copying:

```java
public VMInstance(VMInstance other) {
    this.hostname = other.hostname;
    this.monitoringAgent = other.monitoringAgent;
    this.runtime = other.runtime;
    this.ipAddress = other.ipAddress;
    this.os = other.os;
}
```

Now:

```java
VMInstance copy = new VMInstance(instance1);
```

This is much cleaner.

But there is still a problem: the client needs to know which concrete copy constructor to use for every child type.

---

# 6. Introduce the Prototype Interface

We give copyable objects a common contract:

```java
public interface Prototype<T> {
    T clone();
}
```

### What does `<T>` mean?

`T` represents the type returned by `clone()`.

Conceptually:

```text
Prototype<VMInstance>
        ↓
clone() returns VMInstance
```

and a more specific prototype can return its own type.

The important idea is not the generic syntax. The important idea is:

> **Every prototype provides a common cloning operation.**

---

# 7. VMInstance Implements Prototype

```java
public class VMInstance implements Prototype<VMInstance> {

    private String os;
    private String runtime;
    private String monitoringAgent;
    private String hostname;
    private String ipAddress;

    public VMInstance(
            String os,
            String runtime,
            String monitoringAgent,
            String hostname,
            String ipAddress) {

        this.os = os;
        this.runtime = runtime;
        this.monitoringAgent = monitoringAgent;
        this.hostname = hostname;
        this.ipAddress = ipAddress;
    }

    public VMInstance(VMInstance other) {
        this.hostname = other.hostname;
        this.monitoringAgent = other.monitoringAgent;
        this.runtime = other.runtime;
        this.ipAddress = other.ipAddress;
        this.os = other.os;
    }

    @Override
    public VMInstance clone() {
        return new VMInstance(this);
    }

    // getters and setters
}
```

Now the client writes:

```java
VMInstance copy = instance1.clone();
```

The client no longer knows the copying details.

---

# 8. GPU VM and Polymorphic Cloning

```java
public class GpuVMInstance extends VMInstance {

    private String gpuType;

    public GpuVMInstance(
            String os,
            String runtime,
            String monitoringAgent,
            String hostname,
            String ipAddress,
            String gpuType) {

        super(os, runtime, monitoringAgent, hostname, ipAddress);
        this.gpuType = gpuType;
    }

    public GpuVMInstance(GpuVMInstance other) {
        this(
            other.getOs(),
            other.getRuntime(),
            other.getMonitoringAgent(),
            other.getHostname(),
            other.getIpAddress(),
            other.getGpuType()
        );
    }

    @Override
    public GpuVMInstance clone() {
        return new GpuVMInstance(this);
    }
}
```

Why does the GPU class need its own `clone()`?

Because it has extra state:

```text
Parent state
    + 
GPU-specific state
```

The child knows how to create its complete copy.

---

# 9. The Client Becomes Simple

```java
VMInstance instance1 =
    new VMInstance(
        "Ubuntu 22.4",
        "Docker 1.2",
        "Datadog",
        "Adity.com",
        "123.41.23.12"
    );

VMInstance copyInstance =
    instance1.clone();
```

For a GPU VM:

```java
GpuVMInstance gpuVMInstance =
    new GpuVMInstance(
        "Ubuntu 22.4",
        "Docker 1.2",
        "Datadog",
        "Adity.com",
        "123.41.23.12",
        "Nvidia"
    );

VMInstance copy =
    gpuVMInstance.clone();
```

No client-side:

```java
if (type == ...)
```

The actual object decides which `clone()` implementation runs.

---

# 10. Why Prototype Improves OCP

Before:

```text
Client
  ↓
if VM
  ↓
if GPU VM
  ↓
if Database VM
  ↓
if AI VM
  ↓
...
```

After:

```text
Client
   ↓
clone()
   ↓
Actual object decides how to copy itself
```

If we add:

```text
DatabaseVMInstance
```

it implements its own cloning logic.

The existing client does not need a new `if-else` branch.

---

# 11. New Question: Our Templates Are Ready. Where Do We Store Them?

Now imagine the cloud platform has standard templates:

```text
backend-server-v1
gpu-instance-v2
java-backend-v1
python-backend-v1
database-v1
high-memory-v1
```

We have solved:

> "How do I copy a VM?"

Prototype answered that.

Now ask:

> **"Where do we store all these ready-made prototypes?"**

We need a central place to register and retrieve them.

This leads to the **Registry Pattern**.

---

# 12. Registry Pattern — Simple Analogy

Think about a hotel reception desk.

The hotel has many rooms.

You don't walk through the hotel looking for a room. You tell reception:

> "Give me room 205."

The reception maintains a mapping:

```text
Room Number → Room
```

Our VM Registry does something similar:

```text
Template Name → VM Prototype
```

For example:

```text
"backend-server-v1" → Ubuntu VM Prototype
"gpu-instance-v2"   → GPU VM Prototype
```

> **Registry = a central place for storing and retrieving objects using a key.**

---

# 13. Why Use a Map?

A Java `Map` is a natural fit:

```java
Map<String, VMInstance>
```

because we want:

```text
Key                  Object
-----------------------------------------
backend-server-v1 →  VMInstance
gpu-instance-v2   →  GpuVMInstance
```

The key makes lookup simple.

---

# 14. First Registry Implementation

```java
import java.util.HashMap;
import java.util.Map;

public class VMInstanceRegistry {

    private Map<String, VMInstance> vmInstanceRegistry;

    public VMInstanceRegistry() {
        this.vmInstanceRegistry = new HashMap<>();
    }

    public void addVmInstance(
            String key,
            VMInstance vmInstance) {

        vmInstanceRegistry.put(key, vmInstance);
    }

    public VMInstance getVmInstance(String key) {
        return vmInstanceRegistry.get(key);
    }
}
```

At this point, the Registry stores and returns the registered object.

---

# 15. But There Is Another Problem

The client currently needs to do:

```java
VMInstance vm =
    registry
        .getVmInstance("backend-server-v1")
        .clone();
```

Ask:

> **"Why should the client remember to clone?"**

The Registry internally knows that these stored objects are prototypes.

The client should simply ask:

```java
VMInstance vm =
    registry.getVmInstance("backend-server-v1");
```

The Registry should handle cloning.

---

# 16. Improved Registry

Change:

```java
public VMInstance getVmInstance(String key) {
    return vmInstanceRegistry.get(key);
}
```

to:

```java
public VMInstance getVmInstance(String key) {

    VMInstance prototype =
        vmInstanceRegistry.get(key);

    return prototype.clone();
}
```

Now the Registry does two jobs related to prototypes:

```text
1. Find the prototype
2. Return a clone of the prototype
```

The prototype itself remains hidden from the client.

---

# 17. Final Registry

```java
import java.util.HashMap;
import java.util.Map;

public class VMInstanceRegistry {

    private Map<String, VMInstance> vmInstanceRegistry;

    public VMInstanceRegistry() {
        this.vmInstanceRegistry = new HashMap<>();
    }

    public void addVmInstance(
            String key,
            VMInstance vmInstance) {

        vmInstanceRegistry.put(key, vmInstance);
    }

    public VMInstance getVmInstance(String key) {

        VMInstance prototype =
            vmInstanceRegistry.get(key);

        return prototype.clone();
    }
}
```

The key line is:

```java
return prototype.clone();
```

---

# 18. Filling the Registry

We can prepare standard templates:

```java
public static void fillRegistry(
        VMInstanceRegistry registry) {

    VMInstance ubuntuInstance =
        new VMInstance(
            "Ubuntu 22.4",
            "Docker 1.2",
            "Datadog",
            null,
            null
        );

    registry.addVmInstance(
        "backend-server-v1",
        ubuntuInstance
    );

    GpuVMInstance gpuInstance =
        new GpuVMInstance(
            "Ubuntu 22.4",
            "Docker 1.2",
            "Datadog",
            "Adity.com",
            "123.41.23.12",
            "Nvidia"
        );

    registry.addVmInstance(
        "gpu-instance-v2",
        gpuInstance
    );
}
```

Now:

```text
VMInstanceRegistry
│
├── backend-server-v1 → Ubuntu VM Prototype
│
└── gpu-instance-v2   → GPU VM Prototype
```

---

# 19. Final Client

```java
public static void main(String[] args) {

    VMInstanceRegistry registry =
        new VMInstanceRegistry();

    fillRegistry(registry);

    VMInstance ashokInstance =
        registry.getVmInstance(
            "backend-server-v1"
        );

    VMInstance gpuMachine =
        registry.getVmInstance(
            "gpu-instance-v2"
        );
}
```

Notice:

```java
registry.getVmInstance("gpu-instance-v2");
```

The client does **not** need to know:

- which class to instantiate
- which constructor to call
- how many fields the class has
- how the prototype is copied
- whether the object is a normal VM or GPU VM
- that the Registry internally stores a prototype
- that cloning happens internally

This is a clean client API.

---

# 20. Complete Architecture

```text
                         VM REGISTRY
                  ┌────────────────────────┐
                  │                        │
                  │ backend-server-v1      │
                  │       ↓                │
                  │ VM Prototype           │
                  │                        │
                  │ gpu-instance-v2        │
                  │       ↓                │
                  │ GPU VM Prototype       │
                  │                        │
                  └───────────┬────────────┘
                              │
                       getVmInstance()
                              │
                              ↓
                         clone()
                              │
                              ↓
                         New VM Object
                              │
                              ↓
                            Client
```

---

# 21. Prototype vs Registry

These are **different design patterns**.

## Prototype

Answers:

> **How do I create a copy?**

```java
clone();
```

Responsibility:

```text
Object → knows how to copy itself
```

## Registry

Answers:

> **Where can I find the prototype?**

```java
registry.getVmInstance("gpu-instance-v2");
```

Responsibility:

```text
Registry → stores and retrieves prototypes
```

Together:

```text
Client
   ↓
Registry
   ↓
Find prototype
   ↓
Prototype.clone()
   ↓
New object
```

---

# 22. Why Should Registry Return a Clone?

Suppose:

```java
VMInstance template =
    registry.getVmInstance("backend-server-v1");
```

If Registry returned the original object, the client could modify the template itself.

We want:

```text
Stored Template
      │
      │ clone()
      ↓
  New VM Object
```

So:

```java
VMInstance vm1 =
    registry.getVmInstance("backend-server-v1");

VMInstance vm2 =
    registry.getVmInstance("backend-server-v1");
```

should conceptually produce:

```text
             Prototype
              /      \
          clone      clone
            ↓          ↓
           VM1        VM2
```

`vm1` and `vm2` are different objects, even though they start with the same configuration.

---

# 23. Shallow Copy vs Deep Copy

Prototype becomes important when an object contains mutable objects.

Suppose:

```java
class VMInstance {
    private List<String> packages;
}
```

If a clone simply does:

```java
this.packages = other.packages;
```

both objects refer to the same list:

```text
Original VM ─────┐
                 ├──→ Same List
Copied VM ───────┘
```

A defensive copy can create a separate list:

```java
this.packages =
    new ArrayList<>(other.packages);
```

Now:

```text
Original VM → List A
Copied VM   → List B
```

The values can initially be the same while the lists are independent.

### Important

Prototype does not automatically mean "deep copy everything."

You must decide how each field should be copied.

For immutable values such as `String`, sharing the reference is normally fine because the value cannot be modified.

For mutable collections or mutable child objects, the copy strategy needs careful thought.

---

# 24. Real-World Use Case 1 — Cloud VM Templates

This is our main example.

A cloud platform may maintain:

```text
ubuntu-backend
java-backend
python-backend
gpu-training
database
high-memory
```

Each is a ready-made template.

When a request arrives:

```text
Customer
   ↓
"gpu-training"
   ↓
Registry
   ↓
GPU Prototype
   ↓
clone()
   ↓
New GPU VM
   ↓
Customize hostname/IP
```

This avoids rebuilding the entire configuration every time.

---

# 25. Real-World Use Case 2 — Game Objects

A game may have complex enemy objects:

```text
Enemy
├── health
├── speed
├── weapon
├── armor
└── AI configuration
```

A prototype can represent a configured enemy.

```text
Enemy Prototype
      ↓
    clone()
      ↓
Enemy 1
Enemy 2
Enemy 3
...
```

A Registry can store:

```text
"zombie" → Zombie Prototype
"robot"  → Robot Prototype
"boss"   → Boss Prototype
```

The game asks for a type and receives a new copy.

---

# 26. Real-World Use Case 3 — Document Templates

A reporting system may have:

```text
Invoice
Resume
Monthly Report
Performance Report
```

Each template may contain lots of predefined configuration.

A Registry can keep:

```text
"invoice" → Invoice Prototype
"resume"  → Resume Prototype
```

A new document can be created from the appropriate prototype.

---

# 27. Real-World Use Case 4 — Request Templates

An application may repeatedly create similar requests containing:

```text
headers
authentication
timeout
retry policy
serialization settings
```

A configured request object can act as a prototype.

A Registry can keep common templates:

```text
"payment-request"
"notification-request"
"analytics-request"
```

The application gets a copy and changes only what is different.

---

# 28. When Should We Think About Prototype?

Think about Prototype when:

### Object creation is complicated

The object requires many configuration steps.

### Objects are mostly similar

Only a few properties change between instances.

### Creating the object is expensive or repetitive

A correctly configured object already exists and can be reused as a starting point.

### There are many concrete types

Polymorphic `clone()` can avoid client-side type-checking logic.

---

# 29. When Should We Think About Registry?

Think about Registry when:

- There are many reusable templates/objects.
- Objects need meaningful names or keys.
- Clients repeatedly need to find those templates.
- You want a central place to manage them.

A Registry is essentially:

```text
Name / Key
     ↓
Registered Object / Prototype
```

---

# 30. Final Mental Model

Remember these three words:

```text
PROTOTYPE = TEMPLATE
REGISTRY  = LOOKUP
CLONE     = COPY
```

So:

```text
                 TEMPLATE
                    ↓
                Prototype
                    ↓
             stored in Registry
                    ↓
              get("gpu")
                    ↓
                 clone()
                    ↓
                New Object
```

### Prototype says:

> "I know how to copy myself."

### Registry says:

> "I know where the templates are."

### Client says:

> "Give me the type I need."

---

# 31. Complete Learning Journey

```text
Real-world VM problem
        ↓
Need another similar VM
        ↓
Create from scratch
        ↓
Manual field-by-field copying
        ↓
Too many lines
        ↓
Client knows too much
        ↓
Private fields become difficult
        ↓
Child classes require if-else
        ↓
OCP problem
        ↓
Who should know how to copy?
        ↓
The object itself
        ↓
Prototype Pattern
        ↓
Prototype<T>
        ↓
clone()
        ↓
Each class knows its own copy logic
        ↓
Templates are ready
        ↓
Where do we store them?
        ↓
Registry Pattern
        ↓
Map<String, VMInstance>
        ↓
add/register
        ↓
get
        ↓
Registry internally calls clone()
        ↓
Client gets a NEW object
```

---

# 32. Responsibilities

| Component | Responsibility |
|---|---|
| `Prototype<T>` | Defines the cloning contract |
| `VMInstance` | Knows how to copy a normal VM |
| `GpuVMInstance` | Knows how to copy a GPU VM |
| `VMInstanceRegistry` | Stores and retrieves prototypes |
| `Client` | Requests the VM it needs |

---

# 33. Practice Task — Notification Template Registry

Design:

```text
Notification
    ├── EmailNotification
    ├── SMSNotification
    └── PushNotification
```

Each notification should support:

```java
clone()
```

Create:

```java
Prototype<T>
```

Then create:

```java
NotificationRegistry
```

using:

```java
Map<String, Notification>
```

Register:

```java
registry.add(
    "welcome-email",
    welcomeEmailTemplate
);

registry.add(
    "otp-sms",
    otpSmsTemplate
);
```

The client should be able to write:

```java
Notification notification =
    registry.get("welcome-email");
```

and receive a **new copy**, not the registered template.

### Challenge

Add:

```text
WhatsAppNotification
```

without modifying the Registry.

If the Registry needs an `if-else` for WhatsApp, revisit your Prototype design.

---

# 34. Final Takeaway

When you hear:

> "We already have a correctly configured object and need many similar objects."

Think:

**Prototype.**

When you hear:

> "We have many ready-made templates and need a central place to find them."

Think:

**Registry.**

When they work together:

```text
Registry
   ↓
Find template
   ↓
Prototype
   ↓
clone()
   ↓
New Object
```

**Prototype solves copying.**

**Registry solves storing and finding reusable prototypes.**

They are different patterns, but they can form a clean object-creation workflow.
