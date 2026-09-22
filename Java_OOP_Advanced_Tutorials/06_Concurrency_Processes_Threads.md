# Java OOP & Advanced Concepts

## Tutorial 06 --- Concurrency-1: Processes, Threads, Scheduling & Runnable
------------------------------------------------------------------------

# 1. Program vs Process

These are not the same.

``` text
Program  = application stored on disk
Process  = program currently executing
```

A simplified lifecycle:

``` text
Source Code
    |
    v
Compile
    |
    v
Executable / Bytecode
    |
    v
Load into memory
    |
    v
Process
```

A process needs resources such as:

-   memory
-   program counter
-   registers
-   operating-system bookkeeping

------------------------------------------------------------------------

# 2. Process Control Block (PCB)

The operating system maintains information about a process in a
structure commonly called a Process Control Block.

It can contain:

``` text
Process ID
Process state
Program counter
CPU register information
Scheduling information
Memory information
Open resource information
```

This information lets the OS pause and resume processes.

------------------------------------------------------------------------

# 3. Thread

A process can contain multiple threads.

``` text
Process
 |
 +-- Thread 1
 +-- Thread 2
 +-- Thread 3
```

A thread is an execution path within a process.

Threads in the same process can share process-level resources, including
memory.

This makes communication efficient, but shared memory also creates
synchronization problems.

------------------------------------------------------------------------

# 4. Concurrency vs Parallelism

### Concurrency

Multiple tasks make progress during overlapping periods.

### Parallelism

Multiple tasks literally execute at the same time on different CPU
cores.

Example:

``` text
4 cores

Core 1 -> Thread A
Core 2 -> Thread B
Core 3 -> Thread C
Core 4 -> Thread D
```

On one core, the OS can still provide concurrency by switching between
threads.

------------------------------------------------------------------------

# 5. Context Switching

The scheduler may stop one thread and run another.

``` text
Thread A
   |
   | save state
   v
Scheduler
   |
   | restore state
   v
Thread B
```

This is context switching.

Switching has overhead, so creating huge numbers of threads is not
automatically faster.

------------------------------------------------------------------------

# 6. Creating a Thread

One common approach is `Runnable`.

``` java
class PrintTask implements Runnable {

    @Override
    public void run() {
        for (int i = 1; i <= 5; i++) {
            System.out.println(i);
        }
    }
}
```

Start it:

``` java
Thread thread = new Thread(new PrintTask());
thread.start();
```

Important:

``` java
thread.start();
```

creates a new execution path.

Calling:

``` java
thread.run();
```

is just a normal method call and does not start a new thread.

------------------------------------------------------------------------

# 7. Lambda Form

Because `Runnable` is a functional interface:

``` java
Runnable task = () -> {
    System.out.println("Running in another thread");
};

Thread thread = new Thread(task);
thread.start();
```

This removes boilerplate.

------------------------------------------------------------------------

# 8. Why One Thread Per Task Does Not Scale

Suppose you have 100 tasks.

``` java
for (int i = 0; i < 100; i++) {
    new Thread(() -> doWork()).start();
}
```

Problems:

-   thread creation costs resources
-   too many threads cause scheduling overhead
-   many threads spend time waiting
-   memory consumption increases

A better solution is a thread pool.

That is the subject of the next tutorial.

------------------------------------------------------------------------

## Key Takeaways

-   Program is inactive code; process is executing code.
-   A process can contain multiple threads.
-   Concurrency is not the same as parallelism.
-   Context switching has overhead.
-   `start()` starts a new thread.
-   `run()` alone does not.
-   `Runnable` represents a unit of work.
-   Creating one thread per task is not scalable.

## Practice

Create three `Runnable` tasks:

``` text
Print even numbers
Print odd numbers
Print squares
```

Run them using three threads and observe that the output order is not
guaranteed.
