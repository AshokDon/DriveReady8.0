# Java OOP & Advanced Concepts

## Tutorial 07 --- Concurrency-2: Executors, Thread Pools, Callable & Future

------------------------------------------------------------------------

# 1. Why Thread Pools?

Creating a new thread for every task is expensive.

Instead:

``` text
Tasks
 | | | | | | |
 v v v v v v v
+----------------+
| Thread Pool    |
| T1 T2 T3 T4    |
+----------------+
        |
        v
     CPU cores
```

Workers are reused.

Tasks wait in a queue until a worker becomes available.

------------------------------------------------------------------------

# 2. Executor Framework

The key types are:

``` text
Executor
ExecutorService
Executors
Callable
Future
```

`Executors` provides factory methods for creating common executor
configurations.

Example:

``` java
ExecutorService pool =
        Executors.newFixedThreadPool(5);
```

Submit work:

``` java
pool.execute(() -> {
    System.out.println("Task running");
});
```

------------------------------------------------------------------------

# 3. Fixed Thread Pool

``` java
ExecutorService pool =
        Executors.newFixedThreadPool(3);

for (int i = 1; i <= 10; i++) {
    int taskId = i;

    pool.execute(() -> {
        System.out.println(
            "Task " + taskId +
            " executed by " +
            Thread.currentThread().getName()
        );
    });
}
```

Only three worker threads are available.

The remaining tasks wait.

------------------------------------------------------------------------

# 4. Cached Thread Pool

A cached pool can create threads as needed and reuse idle ones.

``` java
ExecutorService pool =
        Executors.newCachedThreadPool();
```

It can be useful for workloads with many short-lived asynchronous tasks,
but the choice should be based on workload characteristics.

------------------------------------------------------------------------

# 5. Executor Lifecycle

An executor should be shut down.

``` java
ExecutorService pool =
        Executors.newFixedThreadPool(3);

pool.execute(() -> doWork());

pool.shutdown();
```

Useful lifecycle operations include:

``` java
shutdown()
shutdownNow()
isShutdown()
isTerminated()
```

Do not casually create executors and leave them running.

------------------------------------------------------------------------

# 6. `execute()` vs `submit()`

### `execute()`

``` java
pool.execute(runnable);
```

Used when no result is required.

### `submit()`

``` java
Future<Integer> future =
        pool.submit(() -> 42);
```

Used when you need a result or task status.

------------------------------------------------------------------------

# 7. Callable

`Runnable`:

``` java
void run()
```

`Callable<T>`:

``` java
T call() throws Exception
```

Example:

``` java
Callable<Integer> task = () -> {
    return 10 + 20;
};
```

Submit:

``` java
Future<Integer> future =
        pool.submit(task);
```

Retrieve:

``` java
Integer result = future.get();
```

`get()` waits if the computation has not completed.

------------------------------------------------------------------------

# 8. Future

A `Future<T>` represents a result that may become available later.

Think:

``` text
submit(task)
     |
     v
 Future<T>
     |
     +--> isDone()
     |
     +--> get()
     |
     +--> cancel()
```

The useful mental model is:

> "I do not have the result yet, but I have a handle through which I can
> obtain it."

------------------------------------------------------------------------

# 9. Parallel Merge Sort

Merge sort is a good concurrency example because independent halves can
be processed independently.

``` text
              Array
             /     \
          Left     Right
          /  \      /  \
         ... ...   ... ...
```

The left and right halves can be processed by different tasks.

A simplified structure:

``` java
Callable<int[]> leftTask = () -> mergeSort(left);
Callable<int[]> rightTask = () -> mergeSort(right);

Future<int[]> leftFuture = pool.submit(leftTask);
Future<int[]> rightFuture = pool.submit(rightTask);

int[] leftSorted = leftFuture.get();
int[] rightSorted = rightFuture.get();

return merge(leftSorted, rightSorted);
```

The important design principle is:

``` text
Independent work -> execute concurrently
Dependent work   -> wait for required result
```

------------------------------------------------------------------------

# 10. Thread Pool vs Threads

Prefer:

``` text
many tasks
+
controlled number of workers
+
task queue
```

instead of:

``` text
many tasks
+
one new thread per task
```

------------------------------------------------------------------------

## Key Takeaways

-   Thread pools reuse workers.
-   `ExecutorService` manages task execution.
-   `execute()` is suitable for fire-and-forget `Runnable` work.
-   `submit()` returns a `Future`.
-   `Callable` can return a value.
-   `Future.get()` may block.
-   Executors need lifecycle management.
-   Parallelism is useful when work is independent.

## Practice

Implement:

``` text
parallelSum()
```

that divides an integer array into chunks, submits each chunk to an
executor, obtains partial sums through `Future<Integer>`, and combines
them.
