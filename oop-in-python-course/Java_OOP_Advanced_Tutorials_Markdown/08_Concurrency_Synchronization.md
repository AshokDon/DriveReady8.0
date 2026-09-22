# Java OOP & Advanced Concepts

## Tutorial 08 --- Concurrency-3: Race Conditions, Critical Sections & Synchronization

> Source: HackMD Concurrency-3\
> https://hackmd.io/@7ZhgEFzKSUeDhAQFDVj8mw/ByFK0-FQMl

------------------------------------------------------------------------

# 1. Shared Memory Is the Danger Zone

Suppose two threads share:

``` java
class Counter {
    private int value;

    public int getValue() {
        return value;
    }

    public void setValue(int value) {
        this.value = value;
    }
}
```

Adder:

``` java
counter.setValue(counter.getValue() + i);
```

Subtractor:

``` java
counter.setValue(counter.getValue() - i);
```

Mathematically the operations may cancel.

But concurrency can produce an unexpected result.

Why?

Because:

``` text
read
modify
write
```

is not one atomic operation.

------------------------------------------------------------------------

# 2. Race Condition

Suppose:

``` text
counter = 10
```

Thread A reads:

``` text
10
```

Thread B reads:

``` text
10
```

Thread A writes:

``` text
11
```

Thread B writes:

``` text
9
```

One update has effectively been lost.

The final state depends on timing.

That is a race condition.

------------------------------------------------------------------------

# 3. Critical Section

A critical section is code that accesses shared mutable state and must
be protected.

Example:

``` java
counter.setValue(counter.getValue() + i);
```

It contains:

``` text
READ
+
MODIFY
+
WRITE
```

Multiple threads must not execute the protected operation
simultaneously.

------------------------------------------------------------------------

# 4. Pre-emption

A scheduler can interrupt a thread between operations.

Conceptually:

``` text
Thread A:
READ
  |
  | <-- pre-empted
  v
Thread B:
READ
MODIFY
WRITE
  |
  v
Thread A:
MODIFY
WRITE
```

The race is about timing, not arithmetic.

------------------------------------------------------------------------

# 5. Mutex

Mutex means mutual exclusion:

``` text
Only one thread can enter the critical section at a time.
```

In Java, one approach is:

``` java
synchronized (counter) {
    counter.setValue(counter.getValue() + i);
}
```

Other threads attempting to enter the same monitor-protected region must
wait.

------------------------------------------------------------------------

# 6. Synchronized Method

You can synchronize an instance method:

``` java
public synchronized void increment() {
    value++;
}
```

This is conceptually similar to locking the current object.

``` text
synchronized method
        |
        v
lock on this object
```

------------------------------------------------------------------------

# 7. Lock on the Object

Consider:

``` java
synchronized (counter) {
    // critical section
}
```

The lock is associated with the `counter` object.

Two threads must synchronize on the same object to coordinate through
that monitor.

This is important:

``` java
synchronized (counter1) { ... }
synchronized (counter2) { ... }
```

does not provide mutual exclusion between the two blocks because they
use different lock objects.

------------------------------------------------------------------------

# 8. Explicit Lock

Java also provides lock classes such as `ReentrantLock`.

``` java
Lock lock = new ReentrantLock();

lock.lock();

try {
    counter.setValue(counter.getValue() + 1);
} finally {
    lock.unlock();
}
```

The `finally` block is important.

Even if the protected code throws an exception, the lock should be
released.

------------------------------------------------------------------------

# 9. Producer-Consumer

A classic concurrency problem has:

``` text
Producer -> creates items
Consumer -> consumes items
Buffer   -> shared storage
```

Example:

``` text
Producer ---> [ Buffer ] ---> Consumer
```

Problems:

-   producer must not exceed buffer capacity
-   consumer must not consume from an empty buffer
-   shared buffer mutation must be protected

------------------------------------------------------------------------

# 10. Concurrency Design Checklist

When reviewing concurrent code, ask:

``` text
1. What data is shared?
2. Is it mutable?
3. Which threads access it?
4. What is the critical section?
5. What lock protects it?
6. Is the same lock used consistently?
7. Can a lock remain held after an exception?
8. Can the design deadlock?
```

------------------------------------------------------------------------

## Key Takeaways

-   Shared mutable state is the main source of many concurrency bugs.
-   A race condition depends on execution timing.
-   Critical sections need protection.
-   `synchronized` provides mutual exclusion through object monitors.
-   `ReentrantLock` gives explicit lock management.
-   Always release explicit locks in `finally`.
-   Producer-consumer requires both coordination and safe shared-state
    mutation.

## Practice

Implement a thread-safe counter using:

1.  `synchronized` method
2.  `synchronized` block
3.  `ReentrantLock`

Compare the three designs.
