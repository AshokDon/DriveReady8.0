# Java OOP & Advanced Concepts

## Tutorial 10 --- Generics & Collections

> Source: HackMD Java Advanced Concepts-1\
> https://hackmd.io/@7ZhgEFzKSUeDhAQFDVj8mw/BJmMLbRXzl

------------------------------------------------------------------------

# 1. Why Collections?

A collection is a group of objects.

Java provides the Collections Framework with common abstractions such
as:

``` text
List
Set
Queue
Deque
Map
```

Examples:

``` java
List<String> names = new ArrayList<>();
Set<Integer> uniqueIds = new HashSet<>();
Queue<String> queue = new LinkedList<>();
Map<String, Integer> marks = new HashMap<>();
```

------------------------------------------------------------------------

# 2. The Problem Before Generics

Before generics, a container could use `Object`.

``` java
class Stack {
    private Object[] arr;

    public void push(Object value) {
        // ...
    }

    public Object pop() {
        return null;
    }
}
```

Anything could be inserted:

``` java
stack.push(10);
stack.push("Hello");
```

The compiler cannot enforce a single element type.

A later cast can fail:

``` java
Integer x = (Integer) stack.pop();
```

The problem appears at runtime.

------------------------------------------------------------------------

# 3. Generics

Generics move type checking to compile time.

``` java
class Stack<T> {

    private Object[] arr;

    public void push(T value) {
        // ...
    }

    public T pop() {
        return null;
    }
}
```

Use:

``` java
Stack<Integer> numbers = new Stack<>();
Stack<String> words = new Stack<>();
```

Now:

``` java
numbers.push(10);
numbers.push(20);

// numbers.push("Hello"); // compile error
```

This is the main value of generics:

`texttype safety + reuse`

------------------------------------------------------------------------

# 4. Generic Methods

A method can declare its own type parameter.

``` java
public static <T> void print(T value) {
    System.out.println(value);
}
```

Usage:

``` java
print(10);
print("Hello");
print(3.14);
```

The method works with many types while remaining type-safe.

------------------------------------------------------------------------

# 5. Generic Pair

A pair can hold two independent types.

``` java
class Pair<T, V> {
    private T first;
    private V second;

    public Pair(T first, V second) {
        this.first = first;
        this.second = second;
    }

    public T getFirst() {
        return first;
    }

    public V getSecond() {
        return second;
    }
}
```

Examples:

``` java
Pair<String, Integer> marks =
        new Pair<>("Java", 95);

Pair<String, Double> attendance =
        new Pair<>("DSA", 92.5);
```

------------------------------------------------------------------------

# 6. Bounded Type Parameters

Suppose:

``` java
class Item {
    public String getId() {
        return "";
    }
}
```

An unbounded generic type:

``` java
class Inventory<T> {
    void printId(T item) {
        // item.getId(); // compiler cannot guarantee this
    }
}
```

Use a bound:

``` java
class Inventory<T extends Item> {

    public void printId(T item) {
        System.out.println(item.getId());
    }
}
```

Now Java knows that `T` is an `Item` or subclass.

------------------------------------------------------------------------

# 7. Wildcards

This is invalid:

``` java
List<Cat> cats = new ArrayList<>();

List<Animal> animals = cats; // compile error
```

Why?

Because if it were allowed:

``` java
animals.add(new Dog());
```

the `List<Cat>` would contain a Dog.

Generics are intentionally invariant.

------------------------------------------------------------------------

# 8. `? extends`

Use when you mainly want to read from a producer.

``` java
static double total(List<? extends Number> numbers) {
    double sum = 0;

    for (Number n : numbers) {
        sum += n.doubleValue();
    }

    return sum;
}
```

A useful memory aid:

``` text
? extends T -> producer
? super T   -> consumer
```

------------------------------------------------------------------------

# 9. Collections Overview

### List

Ordered, duplicates allowed.

``` java
List<Integer> list = new ArrayList<>();
```

### Set

Unique elements.

``` java
Set<Integer> set = new HashSet<>();
```

### Queue

Processing order.

``` java
Queue<Integer> queue = new LinkedList<>();
```

### Map

Key-value relationship.

``` java
Map<String, Integer> marks = new HashMap<>();
```

------------------------------------------------------------------------

## Key Takeaways

-   Generics provide compile-time type safety.
-   Generic classes eliminate repetitive type-specific implementations.
-   Generic methods can declare their own type parameters.
-   Bounds restrict what types a generic can accept.
-   `List<Cat>` is not a subtype of `List<Animal>`.
-   Wildcards express flexible generic relationships.
-   Prefer parameterized collections over raw types.

## Practice

Implement:

``` java
class Stack<T>
class Pair<T, V>
class Inventory<T extends Item>
```

Then create examples using:

``` textinteger
String
Double
custom Item subclasses
```
