# Java OOP & Advanced Concepts

## Tutorial 11 --- Collections Lab: Inventory Management System

> Source: HackMD Java Advanced Concepts-2\
> https://hackmd.io/@7ZhgEFzKSUeDhAQFDVj8mw/H1ZiYzG4Mg

------------------------------------------------------------------------

# 1. Item Hierarchy

Start with a shared base class:

``` java
public class Item implements Comparable<Item> {

    private String id;
    private String name;
    private double price;
    private int quantity;

    @Override
    public int compareTo(Item other) {
        return this.name.compareTo(other.name);
    }
}
```

Subclasses:

``` java
class Book extends Item {
    private String author;
}

class Clothing extends Item {
    private String size;
}

class Electronics extends Item {
    private int warranty;
}
```

The common state belongs in `Item`.

------------------------------------------------------------------------

# 2. Comparable

`Comparable<T>` defines the object's natural ordering.

``` java
@Override
public int compareTo(Item other) {
    return this.name.compareTo(other.name);
}
```

Then:

``` java
Collections.sort(items);
```

sorts according to the natural ordering.

Use `Comparable` when the class has one obvious default ordering.

------------------------------------------------------------------------

# 3. Comparator

When multiple orderings are useful, use `Comparator`.

``` java
Comparator<Item> byPrice =
        (a, b) -> Double.compare(a.getPrice(), b.getPrice());
```

Sort:

``` java
items.sort(byPrice);
```

Another:

``` java
Comparator<Item> byQuantity =
        Comparator.comparingInt(Item::getQuantity);
```

The important difference:

``` text
Comparable  -> natural/default order
Comparator  -> external/custom order
```

------------------------------------------------------------------------

# 4. Generic Inventory

``` java
class Inventory<T extends Item> {

    private final List<T> items = new ArrayList<>();

    public void add(T item) {
        items.add(item);
    }

    public List<T> getItems() {
        return items;
    }
}
```

The bound guarantees that every item has the `Item` API.

------------------------------------------------------------------------

# 5. Recently Viewed Items

A recently viewed list needs:

-   newest item at the front
-   fixed maximum size
-   duplicates removed
-   repeated views move the item to the front

`LinkedList` can help with front/back operations.

``` java
Deque<Item> recent = new LinkedList<>();
```

Typical logic:

``` java
recent.remove(item);
recent.addFirst(item);

if (recent.size() > capacity) {
    recent.removeLast();
}
```

This is a simplified version of the logic behind an LRU-style cache.

------------------------------------------------------------------------

# 6. HashSet and `equals()` / `hashCode()`

A `HashSet` stores unique elements.

Uniqueness depends on equality and hashing.

If `Item` identity is based on `id`:

``` java
@Override
public boolean equals(Object obj) {
    if (this == obj) return true;
    if (!(obj instanceof Item)) return false;

    Item other = (Item) obj;
    return id.equals(other.id);
}

@Override
public int hashCode() {
    return id.hashCode();
}
```

The contract is:

``` text
a.equals(b) == true
        =>
a.hashCode() == b.hashCode()
```

If you override `equals()`, override `hashCode()` consistently.

------------------------------------------------------------------------

# 7. Useful Collection Factory Methods

For an unmodifiable empty list:

``` java
List<Item> items = Collections.emptyList();
```

For a single element:

``` java
List<String> values =
        Collections.singletonList("Java");
```

Modern Java also provides convenient factory methods such as:

``` java
List.of("A", "B", "C");
Set.of(1, 2, 3);
Map.of("Java", 95);
```

These are useful when the collection should not be modified.

------------------------------------------------------------------------

# 8. Lambda Comparator

Modern Java makes custom ordering concise.

``` java
Comparator<Item> byPriceDescending =
        (a, b) -> Double.compare(
                b.getPrice(),
                a.getPrice()
        );
```

Or:

``` java
Comparator<Item> byPriceDescending =
        Comparator.comparingDouble(Item::getPrice)
                  .reversed();
```

------------------------------------------------------------------------

# 9. Design Lesson

Do not create:

``` textsortbyname()
sortByPrice()
sortByQuantity()
sortById()
```

inside `Inventory` just because the system currently needs four sorts.

Instead:

``` java
public void sortItems(Comparator<T> comparator) {
    items.sort(comparator);
}
```

The ordering strategy becomes a parameter.

This keeps the inventory class focused.

------------------------------------------------------------------------

## Key Takeaways

-   `Comparable` defines natural ordering.
-   `Comparator` defines custom ordering.
-   `HashSet` depends on correct `equals()` / `hashCode()`.
-   `Deque` is useful for front/back operations.
-   Generic bounds preserve type safety.
-   Pass behaviour such as sorting rules instead of hardcoding every
    variation.

## Practice

Extend the inventory with:

1.  `Grocery extends Item`
2.  `expiryDate`
3.  sort groceries by expiry date
4.  remove duplicate items by ID
5.  implement a recently-viewed list with capacity 5
