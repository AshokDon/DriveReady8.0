# Java OOP & Advanced Concepts

## Tutorial 12 --- Streams, Lambdas, Functional Interfaces & Optional

> Source: HackMD Java Advanced Concepts-3\
> https://hackmd.io/@7ZhgEFzKSUeDhAQFDVj8mw/SJXV0p4EGe

------------------------------------------------------------------------

# 1. Functional Interfaces

A functional interface has exactly one abstract method.

Examples:

``` text
Runnable      -> run()
Callable      -> call()
Comparable    -> compareTo()
Comparator    -> compare()
Predicate<T>  -> test()
Function<T,R> -> apply()
Consumer<T>   -> accept()
```

You can mark your own interface:

``` java
@FunctionalInterface
interface Calculator {
    int calculate(int a, int b);
}
```

------------------------------------------------------------------------

# 2. Lambda Expressions

Without a lambda:

``` java
Runnable task = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello");
    }
};
```

With a lambda:

``` java
Runnable task =
        () -> System.out.println("Hello");
```

The lambda expresses the behaviour directly.

------------------------------------------------------------------------

# 3. Lambda Syntax

General form:

``` text
(parameters) -> expression
```

Example:

``` java
(a, b) -> a + b
```

Block form:

``` java
(a, b) -> {
    int result = a + b;
    return result;
}
```

------------------------------------------------------------------------

# 4. Predicate

A `Predicate<T>` returns `boolean`.

``` java
Predicate<Integer> isEven =
        n -> n % 2 == 0;
```

Use:

``` java
System.out.println(isEven.test(10));
// true
```

------------------------------------------------------------------------

# 5. Function

A `Function<T, R>` converts one value to another.

``` java
Function<String, Integer> length =
        s -> s.length();
```

------------------------------------------------------------------------

# 6. Consumer

A `Consumer<T>` accepts a value and returns nothing.

``` java
Consumer<String> printer =
        s -> System.out.println(s);
```

------------------------------------------------------------------------

# 7. Streams

A stream represents a pipeline of operations over data.

Example:

``` java
List<Integer> numbers =
        List.of(1, 2, 3, 4, 5, 6);

numbers.stream()
       .filter(n -> n % 2 == 0)
       .map(n -> n * n)
       .forEach(System.out::println);
```

Pipeline:

``` text
source
  |
filter
  |
map
  |
forEach
```

------------------------------------------------------------------------

# 8. `filter()`

`filter()` keeps elements that satisfy a condition.

``` java
List<Integer> result =
        numbers.stream()
               .filter(n -> n > 3)
               .toList();
```

Important:

``` text
filter can reduce element count
```

------------------------------------------------------------------------

# 9. `map()`

`map()` transforms each element.

``` java
List<String> names =
        List.of("Ashok", "Ravi", "Maya");

List<Integer> lengths =
        names.stream()
             .map(String::length)
             .toList();
```

Important:

``` text
map is one-to-one
```

The number of output elements normally matches the number entering the
operation.

------------------------------------------------------------------------

# 10. `distinct()`

Removes duplicate values.

``` java
numbers.stream()
       .distinct()
       .forEach(System.out::println);
```

------------------------------------------------------------------------

# 11. `sorted()`

Natural ordering:

``` java
numbers.stream()
       .sorted()
       .forEach(System.out::println);
```

Custom ordering:

``` java
numbers.stream()
       .sorted((a, b) -> b - a)
       .forEach(System.out::println);
```

For general numeric code, prefer safe comparator methods when overflow
is possible:

``` java
.sorted(Integer::compare)
```

------------------------------------------------------------------------

# 12. Intermediate vs Terminal Operations

Intermediate operations:

``` textfilter
map
distinct
sorted
```

Terminal operations:

``` textforeach
collect
toList
count
findFirst
findAny
anyMatch
allMatch
noneMatch
```

A stream pipeline generally does not execute its intermediate stages
until a terminal operation is requested.

------------------------------------------------------------------------

# 13. Optional

Suppose:

``` java
Optional<Integer> result =
        numbers.stream()
               .filter(n -> n > 100)
               .findAny();
```

There may be no matching element.

Instead of returning `null`, `Optional` explicitly represents:

`textvalue exists OR value is absent`

Use:

``` java
result.ifPresent(System.out::println);
```

Or:

``` java
int value = result.orElse(0);
```

------------------------------------------------------------------------

# 14. Matching Operations

``` java
boolean any =
        numbers.stream()
               .anyMatch(n -> n > 100);

boolean all =
        numbers.stream()
               .allMatch(n -> n > 0);

boolean none =
        numbers.stream()
               .noneMatch(n -> n < 0);
```

These are terminal operations.

------------------------------------------------------------------------

# 15. Common Stream Mistakes

### Reusing a closed stream

``` java
Stream<Integer> stream = numbers.stream();

stream.count();
stream.forEach(System.out::println); // invalid
```

A stream is not a collection.

Create a new stream when another pipeline is needed.

### Confusing `filter` and `map`

``` text
filter -> decide whether an element survives
map    -> change the element
```

------------------------------------------------------------------------

## Key Takeaways

-   Functional interfaces have one abstract method.
-   Lambdas provide concise implementations.
-   Streams express data-processing pipelines.
-   `filter()` selects.
-   `map()` transforms.
-   `distinct()` removes duplicates.
-   `sorted()` orders.
-   Intermediate operations are lazy.
-   Terminal operations trigger the pipeline.
-   `Optional` represents presence or absence of a value.

## Practice

Given:

``` java
List<Integer> numbers =
        List.of(4, 8, 1, 9, 8, 2, 10, 3);
```

Write streams to:

1.  find even numbers
2.  square them
3.  remove duplicates
4.  sort descending
5.  find the first value greater than 50
6.  check whether all values are positive
