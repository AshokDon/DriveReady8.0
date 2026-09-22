# Java OOP & Advanced Concepts

## Tutorial 13 --- Streams in Practice, Exception Handling & Robust Java Code

> Source: HackMD Java Advanced Concepts-4\
> https://hackmd.io/@7ZhgEFzKSUeDhAQFDVj8mw/BygqpXDL4Gl

------------------------------------------------------------------------

# 1. `map()` With Objects

Streams are especially useful with object hierarchies.

Suppose:

``` java
List<Item> items = new ArrayList<>();

items.add(new Electronics(...));
items.add(new Book(...));
items.add(new Clothing(...));
```

Because these classes extend `Item`, the list can contain all of them.

A mapping operation can extract a property:

``` java
List<String> names =
        items.stream()
             .map(Item::getName)
             .toList();
```

The stream remains polymorphic while processing the common `Item` API.

------------------------------------------------------------------------

# 2. Transforming Data

Example:

``` java
List<Double> prices =
        items.stream()
             .map(Item::getPrice)
             .toList();
```

Or:

``` java
List<String> labels =
        items.stream()
             .map(item ->
                 item.getName() + " : ₹" + item.getPrice())
             .toList();
```

Remember:

`textmap = transform every element`

------------------------------------------------------------------------

# 3. `filter()` and Matching

Filter:

``` java
List<Item> expensive =
        items.stream()
             .filter(item -> item.getPrice() > 1000)
             .toList();
```

Matching operations:

``` java
boolean hasExpensiveItem =
        items.stream()
             .anyMatch(item -> item.getPrice() > 10000);

boolean allAvailable =
        items.stream()
             .allMatch(item -> item.getQuantity() > 0);

long count =
        items.stream()
             .filter(item -> item.getQuantity() == 0)
             .count();
```

------------------------------------------------------------------------

# 4. Exception Handling

An exception represents an abnormal condition during program execution.

Example:

``` java
int result = 10 / 0;
```

This produces an `ArithmeticException`.

------------------------------------------------------------------------

# 5. `try` / `catch`

``` java
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Cannot divide by zero");
}
```

The risky operation is placed inside `try`.

The recovery/handling logic belongs in `catch`.

------------------------------------------------------------------------

# 6. `finally`

`finally` is commonly used for cleanup.

``` java
try {
    // resource operation
} catch (Exception e) {
    // handling
} finally {
    // cleanup
}
```

The cleanup block is intended to execute regardless of whether the
protected operation succeeds or fails.

------------------------------------------------------------------------

# 7. `throw`

Use `throw` when your code detects an invalid condition.

``` java
public void addItem(Item item) {
    if (item == null) {
        throw new IllegalArgumentException(
                "Item cannot be null"
        );
    }

    items.add(item);
}
```

This is different from catching an exception.

``` text
throw  -> create/report an exceptional condition
catch  -> handle an exception
```

------------------------------------------------------------------------

# 8. Custom Exceptions

Suppose duplicate item IDs are not allowed.

``` java
public class DuplicateItemException
        extends RuntimeException {

    public DuplicateItemException(String message) {
        super(message);
    }
}
```

Use:

``` java
if (itemsById.containsKey(item.getId())) {
    throw new DuplicateItemException(
        "Item already exists: " + item.getId()
    );
}
```

Because this extends `RuntimeException`, callers are not forced to
declare it with `throws`.

------------------------------------------------------------------------

# 9. Checked vs Unchecked Exceptions

### Checked

Subclass of `Exception` excluding `RuntimeException`.

The compiler requires handling or declaration.

``` java
void load() throws IOException {
}
```

### Unchecked

Subclass of `RuntimeException`.

``` java
throw new IllegalArgumentException("Invalid input");
```

The compiler does not force a `throws` declaration.

The important design question is:

> Is the caller realistically expected to recover from this condition?

Choose the exception model accordingly.

------------------------------------------------------------------------

# 10. Exception Ordering

Specific exceptions should generally be caught before broader ones.

Correct:

``` java
try {
    // ...
} catch (ArithmeticException e) {
    // specific
} catch (RuntimeException e) {
    // broader
} catch (Exception e) {
    // broadest
}
```

Incorrect ordering can make later catch blocks unreachable.

------------------------------------------------------------------------

# 11. Try-With-Resources

For resources implementing `AutoCloseable`, prefer try-with-resources.

``` java
try (BufferedReader reader =
         new BufferedReader(new FileReader("data.txt"))) {

    String line = reader.readLine();

} catch (IOException e) {
    System.out.println("Unable to read file");
}
```

The resource is automatically closed.

This is safer than manually remembering:

``` java
close();
```

on every execution path.

------------------------------------------------------------------------

# 12. Streams + Exceptions

Keep stream pipelines readable.

Good:

``` java
List<String> names =
        items.stream()
             .filter(item -> item.getQuantity() > 0)
             .map(Item::getName)
             .toList();
```

If complex exception-prone logic is required, consider extracting it
into a well-named method rather than creating an unreadable lambda.

------------------------------------------------------------------------

# 13. A Clean Inventory Service

A simplified service can combine the concepts:

``` java
class Inventory<T extends Item> {

    private final Map<String, T> items =
            new HashMap<>();

    public void add(T item) {
        if (item == null) {
            throw new IllegalArgumentException(
                    "Item cannot be null");
        }

        if (items.containsKey(item.getId())) {
            throw new DuplicateItemException(
                    "Duplicate ID: " + item.getId());
        }

        items.put(item.getId(), item);
    }

    public List<T> findExpensive(double limit) {
        return items.values()
                .stream()
                .filter(item -> item.getPrice() > limit)
                .toList();
    }
}
```

This combines:

``` text
Generics
Collections
Streams
Lambdas
Exceptions
Encapsulation
```

------------------------------------------------------------------------

# 14. Advanced Topics to Revisit

The original lesson also points toward several advanced Java topics:

``` text
Method references
Collectors.groupingBy()
flatMap()
parallelStream()
Thread / sleep / interrupt
```

Examples:

### Method reference

``` java
items.forEach(System.out::println);
```

### Grouping

``` java
Map<String, List<Item>> grouped =
        items.stream()
             .collect(
                 Collectors.groupingBy(
                     Item::getCategory
                 )
             );
```

### `flatMap`

Useful when each element contains another collection.

``` java
orders.stream()
      .flatMap(order -> order.getItems().stream())
      .forEach(System.out::println);
```

These should be introduced only after the basic stream pipeline is
comfortable.

------------------------------------------------------------------------

## Key Takeaways

-   `map()` transforms elements.
-   `filter()` selects elements.
-   `anyMatch`, `allMatch`, and `noneMatch` express common predicates.
-   `throw` reports an invalid condition.
-   `try`/`catch` handles exceptions.
-   `finally` is useful for cleanup.
-   Custom exceptions communicate domain-specific failures.
-   Prefer try-with-resources for `AutoCloseable` resources.
-   Keep stream pipelines readable.
-   Generics, collections, streams, and exceptions work together to
    create robust Java services.

## Practice

Build an `InventoryService<T extends Item>` that supports:

``` textadd()
remove()
findById()
findByPriceRange()
findOutOfStock()
groupByCategory()
sortByPrice()
```

Add:

``` textduplicateitemexception
ItemNotFoundException
InvalidPriceException
```

Use streams for the query operations.
