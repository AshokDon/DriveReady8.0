# Java OOP & Advanced Concepts

## Tutorial 09 --- Concurrency-4: Semaphores, Permits & Bounded Buffers

> Source: HackMD Concurrency-4\
> https://hackmd.io/@7ZhgEFzKSUeDhAQFDVj8mw/BkeBgqj7fg

------------------------------------------------------------------------

# 1. What Is a Semaphore?

A semaphore maintains a count of available permits.

``` java
Semaphore semaphore = new Semaphore(3);
```

There are three permits.

Acquire:

``` java
semaphore.acquire();
```

Release:

``` java
semaphore.release();
```

If no permit is available, `acquire()` waits.

------------------------------------------------------------------------

# 2. Mental Model

Imagine a room with three seats.

``` text
Capacity = 3

Thread A -> seat
Thread B -> seat
Thread C -> seat
Thread D -> waits
```

When A leaves:

``` text
Thread A -> release()
Thread D -> gets the available permit
```

This is different from a normal mutual-exclusion lock because multiple
threads can proceed simultaneously when multiple permits exist.

------------------------------------------------------------------------

# 3. Binary vs Counting Semaphore

### Binary

``` java
new Semaphore(1);
```

Only one permit exists.

Conceptually:

``` text
one-at-a-time access
```

### Counting

``` java
new Semaphore(5);
```

Up to five threads may hold permits concurrently.

------------------------------------------------------------------------

# 4. Producer-Consumer With Semaphores

A bounded buffer has a fixed capacity.

For a buffer of size `N`, maintain:

``` text
emptySlots = N
filledSlots = 0
```

Use two semaphores:

``` java
Semaphore emptySlots =
        new Semaphore(N);

Semaphore filledSlots =
        new Semaphore(0);
```

Producer:

``` text
acquire empty slot
insert item
release filled slot
```

Consumer:

``` text
acquire filled slot
remove item
release empty slot
```

------------------------------------------------------------------------

# 5. Producer Skeleton

``` java
emptySlots.acquire();

try {
    synchronized (buffer) {
        buffer.add(item);
    }
} finally {
    filledSlots.release();
}
```

The semaphore controls capacity.

The lock protects the mutation of the buffer.

This distinction is important:

``` text
Semaphore -> controls HOW MANY may proceed
Mutex     -> controls WHO may mutate shared state at once
```

------------------------------------------------------------------------

# 6. Consumer Skeleton

``` java
filledSlots.acquire();

try {
    synchronized (buffer) {
        item = buffer.remove();
    }
} finally {
    emptySlots.release();
}
```

Now the system guarantees:

``` text
buffer cannot exceed capacity
buffer cannot be consumed while empty
buffer mutation is protected
```

------------------------------------------------------------------------

# 7. Semaphore Has No Ownership

A semaphore tracks permits, not ownership.

For example:

``` java
semaphore.acquire();
```

and later:

``` java
semaphore.release();
```

The semaphore does not require the same thread to perform the release.

This differs from ownership-oriented lock semantics.

------------------------------------------------------------------------

# 8. Common Semaphore Mistakes

### Forgetting `release()`

``` text
permits leak
   |
   v
eventually no permits remain
   |
   v
waiting threads block forever
```

### Releasing too many times

An extra release can create permits that were never acquired.

### Reversing producer/consumer signals

Producer:

``` text
acquire(empty)
release(filled)
```

Consumer:

``` text
acquire(filled)
release(empty)
```

Reversing these breaks the protocol.

------------------------------------------------------------------------

# 9. Always Consider `try/finally`

When an operation must release a resource:

``` java
semaphore.acquire();

try {
    // protected work
} finally {
    semaphore.release();
}
```

The structure makes cleanup explicit.

------------------------------------------------------------------------

# 10. Semaphore Patterns

Semaphores commonly appear as:

``` text
Counter
Baton / signalling mechanism
Grouping mechanism
Capacity limiter
```

Examples:

-   database connection limits
-   API concurrency limits
-   parking capacity
-   bounded buffers
-   resource pools

------------------------------------------------------------------------

## Key Takeaways

-   A semaphore controls permits.
-   `acquire()` consumes a permit.
-   `release()` returns a permit.
-   Binary semaphore = one permit.
-   Counting semaphore = multiple permits.
-   Semaphores do not inherently track ownership.
-   Producer-consumer often needs both semaphores and a mutex.

## Practice

Build a parking-lot simulation:

``` text
capacity = 3

10 cars try to enter.
Only 3 can occupy slots at once.
A car leaving releases a permit.
```

Print entry and exit events with thread names.
