# Python Functions — Assignment Sheet
### DriveReady 8.0 · Practice Set for `python_functions.md`

---

## 📌 Rules (read this first)

1. **Type every line yourself.** No copy-paste. Coding is a muscle, not a lecture.
2. **Predict the output before you run it.** Write your guess in a comment. Then run. If you were wrong, that gap is your real lesson.
3. **One file per problem.** Name it like `set03_p02.py`. Keep them in a folder.
4. **Break it on purpose.** After it works, delete a line, change a value, see what error you get. Read the error message fully.
5. **Stuck for 20 minutes?** Then look at the notes. Not before.

> Coding is not about listening. It is about your fingers hitting the keyboard.

**How to submit:** one folder, zipped, named `<yourname>_functions_assignment.zip`

---

## 🎯 Difficulty Legend

| Symbol | Meaning |
|--------|---------|
| ⭐ | Warm-up — you should finish in 5 minutes |
| ⭐⭐ | Core — this is the real practice |
| ⭐⭐⭐ | Challenge — think before you type |
| 🔥 | Interview favourite |

---
---

# SET 1 — Array Functions

### 1.1 Cricket Over Analyser ⭐

You are given runs scored in each over of a T20 innings.

Build an integer `array` and print the stats.

```
Input:  [6, 12, 4, 0, 15, 8, 3, 20]

Output:
Total runs      : 68
Highest over    : 20
Lowest over     : 0
Average per over: 8.5
Maiden overs    : 1
Bytes used      : 32
```

> Hint: "maiden over" = an over with 0 runs. Use `count()`. Bytes = `itemsize * len()`.

---

### 1.2 Array Surgery ⭐⭐

Start with `array('i', [10, 20, 30, 40, 50])` and apply these operations **in order**. Print the array after each step.

```
Operations:
  1. append 60
  2. insert 15 at index 1
  3. remove the value 30
  4. pop the element at index 0
  5. reverse

Output:
After append  : array('i', [10, 20, 30, 40, 50, 60])
After insert  : array('i', [10, 15, 20, 30, 40, 50, 60])
After remove  : array('i', [10, 15, 20, 40, 50, 60])
After pop     : array('i', [15, 20, 40, 50, 60])  (popped 10)
After reverse : array('i', [60, 50, 40, 20, 15])
```

---

### 1.3 Second Highest Scorer ⭐⭐ 🔥

Find the **second largest** element **without using `sort()` or `sorted()`**.

```
Input:  [45, 88, 12, 88, 67, 90]
Output: Second largest = 88

Input:  [5, 5, 5]
Output: No second largest
```

> Careful: `[45, 88, 12, 88, 67, 90]` — the largest is 90, so the second largest is 88, even though 88 appears twice.

---

### 1.4 Left Rotate by K ⭐⭐

Rotate an array to the **left** by `k` positions.

```
Input:  arr = [1, 2, 3, 4, 5, 6, 7],  k = 3
Output: [4, 5, 6, 7, 1, 2, 3]

Input:  arr = [1, 2, 3],  k = 5
Output: [3, 1, 2]
```

> `k` can be bigger than the array length. Handle it.

---

### 1.5 Merge Two Sorted Arrays ⭐⭐⭐

Merge two already-sorted arrays into one sorted array — **without using `sorted()`**.

```
Input:  a = [1, 4, 7, 9],  b = [2, 3, 8, 10, 15]
Output: [1, 2, 3, 4, 7, 8, 9, 10, 15]
```

---
---

# SET 2 — Arguments in Functions

### 2.1 Swiggy Order Bill ⭐⭐

Write `place_order(customer, *items, **charges)`.

```python
place_order("Ravi", "Biryani", "Coke", "Gulab Jamun",
            delivery=40, gst=25, discount=50)
```

```
Output:
Customer : Ravi
Items ordered (3):
  1. Biryani
  2. Coke
  3. Gulab Jamun
Charges:
  delivery : 40
  gst      : 25
  discount : 50
```

---

### 2.2 Flexible Calculator ⭐

`calculator(a, b, op="+")` supporting `+ - * /`.

```
calculator(10, 5)         ->  15
calculator(10, 5, "-")    ->  5
calculator(10, 5, "*")    ->  50
calculator(10, 0, "/")    ->  Error: cannot divide by zero
calculator(10, 5, "%")    ->  Error: unknown operator '%'
```

---

### 2.3 URL Query Builder ⭐⭐

`build_query(**filters)` turns keyword arguments into a URL query string.

```
build_query(city="hyderabad", rating=4, veg=True)
->  city=hyderabad&rating=4&veg=True

build_query()
->  (empty string)
```

---

### 2.4 The Shopping Cart Bug 🔥 ⭐⭐

This code is **broken**. Run it, observe the bug, explain **why** in a comment, then fix it.

```python
def add_to_cart(item, cart=[]):
    cart.append(item)
    return cart

print(add_to_cart("pen"))
print(add_to_cart("book"))
print(add_to_cart("bag"))
```

```
Buggy output:
['pen']
['pen', 'book']
['pen', 'book', 'bag']

Expected output after your fix:
['pen']
['book']
['bag']
```

---

### 2.5 Student Report Card ⭐⭐

Accept a name, any number of marks, and optional details.

```python
report("Priya", 85, 92, 78, 90, section="A", year=2)
```

```
Output:
Student : Priya
Section : A
Year    : 2
Marks   : 85, 92, 78, 90
Total   : 345
Average : 86.25
Result  : PASS
```

> Pass mark = average >= 40.

---

### 2.6 Predict, Then Run 🔥 ⭐⭐⭐

Write your prediction as a comment **before** running.

```python
def mystery(a, b=[], *c, **d):
    b.append(a)
    return a, b, c, d

print(mystery(1))
print(mystery(2, [9]))
print(mystery(3))
print(mystery(4, [7], 8, 9, x=10))
```

---
---

# SET 3 — Global vs Local Variables

### 3.1 Scope Puzzle Pack ⭐⭐ 🔥

For **each** snippet: write your predicted output as a comment, run it, then write one line explaining what happened.

**Puzzle A**
```python
x = 10
def f():
    print(x)
    x = 20
f()
```

**Puzzle B**
```python
x = 5
def f(x):
    x = 10
f(x)
print(x)
```

**Puzzle C**
```python
x = "global"
def outer():
    x = "enclosing"
    def inner():
        print(x)
    inner()
outer()
```

**Puzzle D**
```python
if True:
    z = 99
print(z)
```

---

### 3.2 Movie Ticket Counter ⭐⭐

Use a **global** variable to track seats.

```
Total seats: 100

book(3)   ->  Booked 3 seats. Remaining: 97
book(10)  ->  Booked 10 seats. Remaining: 87
book(200) ->  Only 87 seats left. Booking failed.
cancel(5) ->  Cancelled 5 seats. Remaining: 92
status()  ->  92 seats available out of 100
```

---

### 3.3 Same Counter, Two Ways ⭐⭐⭐

Build a counter twice:
1. Version A using `global`
2. Version B using a nested function and `nonlocal`

Then write 2-3 lines: **which one is safer, and why?**

```
Version A: 1 2 3
Version B: 1 2 3
```

---

### 3.4 LEGB in One File ⭐⭐

Write a single program that demonstrates **all four** LEGB layers printing four different values.

```
Expected output:
Local     : I am local
Enclosing : I am enclosing
Global    : I am global
Built-in  : 5
```

> The built-in layer: use something like `len("hello")`.

---
---

# SET 4 — Factorial (Iterative)

### 4.1 Factorial Table ⭐

```
Output:
  n |                        n! | digits
----+---------------------------+-------
  0 |                         1 |      1
  1 |                         1 |      1
  2 |                         2 |      1
  3 |                         6 |      1
  4 |                        24 |      2
  5 |                       120 |      3
 ...
 15 |         1,307,674,368,000 |     13
```

> Print 0 to 15. Use `{:,}` for comma formatting.

---

### 4.2 Trailing Zeros 🔥 ⭐⭐⭐

Find the number of trailing zeros in `n!` **without computing the factorial**.

```
Input: 10   ->  Output: 2      (10! = 3628800)
Input: 25   ->  Output: 6
Input: 100  ->  Output: 24
Input: 1000 ->  Output: 249
```

> Hint: a trailing zero comes from a factor of 10 = 2 × 5. There are always more 2s than 5s, so just count the 5s: `n//5 + n//25 + n//125 + ...`

---

### 4.3 Permutations and Combinations ⭐⭐

Write `nPr(n, r)` and `nCr(n, r)`.

```
nPr(5, 2)   ->  20
nCr(5, 2)   ->  10
nCr(15, 11) ->  1365
nCr(52, 5)  ->  2598960     (poker hands!)
nCr(5, 7)   ->  Error: r cannot be greater than n
```

---

### 4.4 Compute `e` ⭐⭐⭐

Use the series `e = 1/0! + 1/1! + 1/2! + 1/3! + ...` for 20 terms.

```
Output:
Terms used : 20
Computed e : 2.718281828459045
math.e     : 2.718281828459045
Difference : 0.00e+00
```

> Try it with only 5 terms and then 10 terms. Watch how fast it converges.

---

### 4.5 Input Validator ⭐⭐

Write a factorial function that rejects bad input properly.

```
factorial(5)      ->  120
factorial(0)      ->  1
factorial(-3)     ->  ValueError: Factorial is not defined for negative numbers
factorial(2.5)    ->  TypeError: Expected an integer, got float
factorial("five") ->  TypeError: Expected an integer, got str
```

---
---

# SET 5 — Recursion

### 5.1 Digit Sum ⭐

```
Input: 12345   ->  Output: 15
Input: 9       ->  Output: 9
Input: 100     ->  Output: 1
```

---

### 5.2 Reverse a String ⭐

```
Input: "DriveReady"  ->  Output: "ydaeRevirD"
Input: "a"           ->  Output: "a"
```

> No slicing shortcut `s[::-1]`. Use recursion.

---

### 5.3 Palindrome Checker ⭐⭐

Ignore spaces and case.

```
Input: "madam"              ->  True
Input: "Never odd or even"  ->  True
Input: "python"             ->  False
Input: "Was it a car or a cat I saw"  ->  True
```

---

### 5.4 Tower of Hanoi ⭐⭐⭐ 🔥

Print every move and the total count.

```
Input: 3 disks (A -> C using B)

Output:
Move disk 1: A -> C
Move disk 2: A -> B
Move disk 1: C -> B
Move disk 3: A -> C
Move disk 1: B -> A
Move disk 2: B -> C
Move disk 1: A -> C
Total moves: 7
```

> For n disks the count should be `2^n - 1`. Verify with n = 4 (should be 15).

---

### 5.5 Staircase Problem ⭐⭐⭐ 🔥

You can climb 1 or 2 steps at a time. How many ways to reach step `n`?

```
Input: 1  ->  1
Input: 2  ->  2
Input: 3  ->  3
Input: 4  ->  5
Input: 5  ->  8
Input: 10 ->  89
```

> Notice the pattern. Then add `@lru_cache` and try `n = 100`.

---

### 5.6 Flatten a Messy List ⭐⭐⭐

```
Input:  [1, [2, 3, [4, [5, 6]], 7], 8]
Output: [1, 2, 3, 4, 5, 6, 7, 8]

Input:  [[[[1]]], 2, [[3, [4]]]]
Output: [1, 2, 3, 4]
```

---

### 5.7 Recursive Binary Search ⭐⭐

```
Input: [2, 5, 8, 12, 16, 23, 38, 56, 72, 91], target = 23
Output: Found at index 5

Input: same list, target = 100
Output: Not found (-1)
```

---
---

# SET 6 — Factorial using Recursion

### 6.1 The Classic ⭐

```
factorial(5)  ->  120
factorial(0)  ->  1
factorial(10) ->  3628800
```

---

### 6.2 Visual Trace Printer ⭐⭐ 🔥

Print what happens at every level. **This one problem will teach you recursion permanently.**

```
Input: 4

Output:
factorial(4) called
needs 4 * factorial(3) ... waiting
|  factorial(3) called
|  needs 3 * factorial(2) ... waiting
|  |  factorial(2) called
|  |  needs 2 * factorial(1) ... waiting
|  |  |  factorial(1) called
|  |  |  BASE CASE -> returning 1
|  |  got 1, so 2 * 1 = 2
|  got 2, so 3 * 2 = 6
got 6, so 4 * 6 = 24

Final answer: 24
```

> Pass a `depth` parameter and use `"|  " * depth` as padding.

---

### 6.3 The Negative Trap ⭐⭐

Run `factorial(-5)` on the naive version (no validation). Note down the exact error. Then explain in a comment: **why doesn't it stop?**

Then fix it.

```
Before fix: RecursionError: maximum recursion depth exceeded
After fix : ValueError: Factorial is not defined for negative numbers
```

---

### 6.4 Recursive Power ⭐⭐

```
power(2, 10)  ->  1024
power(5, 0)   ->  1
power(3, 4)   ->  81
```

Then write `fast_power(x, n)` using divide-and-conquer and compare the number of calls.

```
fast_power(2, 30)  ->  1073741824
```

---

### 6.5 Double Factorial ⭐⭐⭐

`n!! = n × (n-2) × (n-4) × ...` down to 1 or 2.

```
Input: 8   ->  384      (8 × 6 × 4 × 2)
Input: 7   ->  105      (7 × 5 × 3 × 1)
Input: 1   ->  1
Input: 0   ->  1
```

---
---

# SET 7 — Higher Order Functions

### 7.1 Apply Twice ⭐

```python
apply_twice(lambda x: x + 3, 10)   ->  16
apply_twice(lambda x: x * 2, 5)    ->  20
apply_twice(str.upper, "hi")       ->  "HI"
```

---

### 7.2 Function Composer ⭐⭐ 🔥

`compose(f, g)` returns a new function that computes `f(g(x))`.

```python
add_one    = lambda x: x + 1
double     = lambda x: x * 2

f = compose(add_one, double)    # add_one(double(x))
print(f(5))                     # 11

g = compose(double, add_one)    # double(add_one(x))
print(g(5))                     # 12
```

---

### 7.3 Menu Dispatch Table ⭐⭐

Replace a long `if/elif` chain with a dictionary of functions.

```
Input: 10 + 3   ->  13
Input: 10 - 3   ->  7
Input: 10 * 3   ->  30
Input: 10 / 3   ->  3.3333333333333335
Input: 10 % 3   ->  Unknown operator: %
```

---

### 7.4 IPL Player Sorter ⭐⭐⭐ 🔥

```python
players = [
    {"name": "Kohli",   "runs": 741, "team": "RCB"},
    {"name": "Gill",    "runs": 890, "team": "GT"},
    {"name": "Rahul",   "runs": 616, "team": "LSG"},
    {"name": "Jaiswal", "runs": 625, "team": "RR"},
    {"name": "Samson",  "runs": 616, "team": "RR"},
]
```

Print three different sorted lists:

```
By runs (high to low):
  Gill      890
  Kohli     741
  Jaiswal   625
  Rahul     616
  Samson    616

By team, then runs (high to low):
  GT   Gill      890
  LSG  Rahul     616
  RCB  Kohli     741
  RR   Jaiswal   625
  RR   Samson    616

By name length:
  Gill, Kohli, Rahul, Samson, Jaiswal
```

> For the two-key sort, use a tuple: `key=lambda p: (p["team"], -p["runs"])`

---

### 7.5 Text Cleaning Pipeline ⭐⭐⭐

Write `pipeline(text, *operations)` that applies each function in order and shows every step.

```
Input: "   Ravi Kumar Sharma   "
Operations: strip -> lowercase -> replace spaces with _ -> add "user_" prefix

Output:
Starting with: '   Ravi Kumar Sharma   '
  after clean          : 'Ravi Kumar Sharma'
  after to_lower       : 'ravi kumar sharma'
  after remove_spaces  : 'ravi_kumar_sharma'
  after add_prefix     : 'user_ravi_kumar_sharma'
Final: user_ravi_kumar_sharma
```

---
---

# SET 8 — Lambda / Anonymous Functions

### 8.1 One-Liner Pack ⭐

Write each as a **single lambda**:

```
is_even(10)        ->  True
is_leap(2024)      ->  True
is_leap(1900)      ->  False
reverse("python")  ->  "nohtyp"
bigger(10, 20)     ->  20
area_circle(7)     ->  153.93804002589985
```

---

### 8.2 Grade Machine ⭐⭐

One lambda using chained ternaries.

```
grade(95) ->  A
grade(82) ->  B
grade(65) ->  C
grade(45) ->  D
grade(20) ->  F
```

> Cutoffs: 90+ A, 75+ B, 60+ C, 40+ D, else F.

---

### 8.3 Case-Insensitive Sort ⭐⭐

```
Input:  ["banana", "Apple", "cherry", "Date"]
Output: ['Apple', 'banana', 'cherry', 'Date']
```

---

### 8.4 The Lambda Loop Trap 🔥 ⭐⭐⭐

Run this. Explain the output in a comment. Then fix it.

```python
funcs = []
for i in range(3):
    funcs.append(lambda: i * 10)

print([f() for f in funcs])
```

```
Buggy output   : [20, 20, 20]
Expected output: [0, 10, 20]
```

---

### 8.5 When NOT to Use Lambda ⭐⭐

Take this unreadable lambda and rewrite it as a proper `def` with a docstring. Both must give the same output.

```python
process = lambda d: {k: (v * 2 if isinstance(v, int) else v.upper() if isinstance(v, str) else v) for k, v in d.items()}

print(process({"a": 5, "b": "hi", "c": 3.5}))
```

```
Output: {'a': 10, 'b': 'HI', 'c': 3.5}
```

---
---

# SET 9 — filter()

### 9.1 Filter Warm-Ups ⭐

```
Numbers divisible by 7 from 1 to 50
->  [7, 14, 21, 28, 35, 42, 49]

Words longer than 4 letters from ["hi", "python", "is", "great", "ok"]
->  ['python', 'great']

Palindromes from ["madam", "python", "level", "code", "radar"]
->  ['madam', 'level', 'radar']
```

---

### 9.2 Clean the Junk ⭐⭐

Use `filter(None, ...)`.

```
Input:  [0, 1, "", "hello", None, [], [1,2], False, True, 0.0, "0"]
Output: [1, 'hello', [1, 2], True, '0']
```

> Explain in a comment: **why did `"0"` survive but `0` did not?**

---

### 9.3 Above Average Students ⭐⭐⭐ 🔥

Filter students who scored **above the class average**.

```python
students = [
    {"name": "Ravi",   "marks": 78},
    {"name": "Priya",  "marks": 92},
    {"name": "Kiran",  "marks": 45},
    {"name": "Divya",  "marks": 88},
    {"name": "Suresh", "marks": 61},
]
```

```
Output:
Class average: 72.8
Above average:
  Priya  92
  Divya  88
  Ravi   78
```

> You need two passes — compute the average first, then filter.

---

### 9.4 Prime Filter ⭐⭐

```
Input:  range(1, 51)
Output: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

> Write `is_prime` as a proper `def`, not a lambda. Explain why in a comment.

---

### 9.5 The Exhaustion Trap 🔥 ⭐⭐

Run this and explain the second output.

```python
result = filter(lambda x: x > 3, [1, 2, 3, 4, 5])
print(list(result))
print(list(result))
```

```
Output:
[4, 5]
[]
```

Then fix it so both prints show `[4, 5]`.

---
---

# SET 10 — map() and reduce()

### 10.1 Map Warm-Ups ⭐

```
Squares of [1,2,3,4,5]                  ->  [1, 4, 9, 16, 25]
["1","2","3","42"] to integers          ->  [1, 2, 3, 42]
["ravi","priya"] to uppercase           ->  ['RAVI', 'PRIYA']
Lengths of ["hi","python","is"]         ->  [2, 6, 2]
```

---

### 10.2 Temperature Converter ⭐

```
Input:  [0, 25, 37, 100, -40]  (Celsius)
Output: [32.0, 77.0, 98.6, 212.0, -40.0]  (Fahrenheit)
```

> Formula: `F = C * 9/5 + 32`. Notice `-40` is the same in both scales.

---

### 10.3 Two Lists at Once ⭐⭐

Use `map` with **two** iterables.

```
names  = ["Ravi", "Priya", "Kiran"]
marks  = [78, 92, 45]

Output: ['Ravi: 78', 'Priya: 92', 'Kiran: 45']
```

Then try it where the lists have **different lengths** and note what happens.

---

### 10.4 Reduce Warm-Ups ⭐⭐

```
Sum of [1,2,3,4,5]                 ->  15
Product of [1,2,3,4,5]             ->  120
Maximum of [3,7,2,9,4]             ->  9
Join ["Python","is","powerful"]    ->  "Python is powerful"
Longest word in ["hi","python","is"] -> "python"
```

> For each one, also write the built-in equivalent (`sum`, `max`, ...) in a comment.

---

### 10.5 Word Frequency Counter ⭐⭐⭐ 🔥

Use `reduce` with a dictionary accumulator.

```
Input:  ["apple", "banana", "apple", "cherry", "banana", "apple"]
Output: {'apple': 3, 'banana': 2, 'cherry': 1}
```

---

### 10.6 The Full Pipeline ⭐⭐⭐ 🔥

Use **filter → map → reduce** together.

```python
sales = [
    {"product": "Laptop",   "price": 55000, "qty": 3,  "region": "South"},
    {"product": "Mouse",    "price": 500,   "qty": 20, "region": "North"},
    {"product": "Monitor",  "price": 12000, "qty": 5,  "region": "South"},
    {"product": "Keyboard", "price": 1500,  "qty": 12, "region": "South"},
    {"product": "Printer",  "price": 8000,  "qty": 2,  "region": "North"},
]
```

```
Output:
Total South revenue: Rs 243,000
Total North revenue: Rs 26,000
```

Then rewrite the whole thing as **one line** using a generator expression and `sum()`. Which is more readable?

---

### 10.7 Sum of Squares of Evens ⭐⭐⭐

Using **only** `map`, `filter`, and `reduce` — no loops, no comprehensions.

```
Input:  1 to 10
Output: 220        (4 + 16 + 36 + 64 + 100)

Input:  1 to 100
Output: 171700
```

---
---

# SET 11 — Inner Functions and Closures

### 11.1 Power Factory ⭐⭐

```python
square = make_power(2)
cube   = make_power(3)

print(square(5))   # 25
print(cube(3))     # 27
print(make_power(4)(2))  # 16
```

---

### 11.2 Independent Counters ⭐⭐ 🔥

```python
c1 = make_counter()
c2 = make_counter()

print(c1(), c1(), c1())   # 1 2 3
print(c2(), c2())         # 1 2
print(c1())               # 4
```

> The two counters must **not** interfere. Use `nonlocal`.

---

### 11.3 Running Average ⭐⭐⭐

```python
avg = make_averager()

print(avg(10))    # 10.0
print(avg(20))    # 15.0
print(avg(30))    # 20.0
print(avg(40))    # 25.0
```

---

### 11.4 Closure Stack ⭐⭐⭐

Return `push`, `pop`, and `size` functions sharing one hidden list.

```
push(10)  ->  Pushed 10. Size: 1
push(20)  ->  Pushed 20. Size: 2
push(30)  ->  Pushed 30. Size: 3
pop()     ->  Popped 30. Size: 2
pop()     ->  Popped 20. Size: 1
size()    ->  1
pop()     ->  Popped 10. Size: 0
pop()     ->  Stack is empty
```

---

### 11.5 Call Me Once ⭐⭐⭐ 🔥

`once(func)` lets a function actually run only the **first** time. After that it returns the cached result without re-running.

```python
@... (or) setup = once(expensive_setup)

print(setup())   # Running setup...  ->  "DONE"
print(setup())   # DONE   (no "Running setup..." printed)
print(setup())   # DONE
```

---

### 11.6 UPI Wallet ⭐⭐⭐

Closure-based wallet. The balance must be **impossible** to access from outside.

```
create_wallet("Ravi", 1000)

statement()   ->  Ravi's balance: 1000
deposit(500)  ->  Deposited 500. Balance: 1500
withdraw(2000)->  Insufficient funds. Balance: 1500
withdraw(300) ->  Withdrew 300. Balance: 1200
deposit(-100) ->  Deposit must be positive
statement()   ->  Ravi's balance: 1200
```

Then try to change the balance directly from outside. Write in a comment: **can you?**

---
---

# SET 12 — Decorators

### 12.1 Shout Decorator ⭐

`@uppercase` converts the returned string to uppercase.

```python
@uppercase
def greet(name):
    return f"hello, {name}"

print(greet("ravi"))   # HELLO, RAVI
```

---

### 12.2 Call Counter ⭐⭐

```python
@count_calls
def say_hi():
    print("Hi!")

say_hi()
say_hi()
say_hi()
print(say_hi.count)
```

```
Output:
Call #1
Hi!
Call #2
Hi!
Call #3
Hi!
3
```

---

### 12.3 The Timer ⭐⭐ 🔥

```python
@timer
def slow_sum(n):
    return sum(range(n))

print(slow_sum(1_000_000))
```

```
Output:
[TIMER] slow_sum took 0.0201s
499999500000
```

---

### 12.4 The Three Rules 🔥 ⭐⭐⭐

Write a decorator that **deliberately breaks** all three rules, then fix them one at a time and record what changed:

| Rule broken | What goes wrong |
|-------------|-----------------|
| No `*args, **kwargs` | ? |
| No `return result` | ? |
| No `@wraps(func)` | ? |

```python
@my_decorator
def add(a, b):
    """Adds two numbers."""
    return a + b

print(add(3, 5))
print(add.__name__)
print(add.__doc__)
```

```
Expected after all fixes:
8
add
Adds two numbers.
```

---

### 12.5 Login Required ⭐⭐⭐

```python
admin = {"name": "Ravi", "logged_in": True}
guest = {"name": "Anon", "logged_in": False}

@require_login
def view_dashboard(user):
    return f"Welcome {user['name']}!"

print(view_dashboard(admin))   # Welcome Ravi!
print(view_dashboard(guest))   # Access denied. Please log in.
```

---

### 12.6 Repeat N Times ⭐⭐⭐ 🔥

A decorator that **takes an argument** — three layers.

```python
@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Priya")
```

```
Output:
Hello, Priya!
Hello, Priya!
Hello, Priya!
```

---

### 12.7 Stacking Order 🔥 ⭐⭐⭐

```python
@bold
@italic
def text():
    return "Hello"
print(text())        # ?

@italic
@bold
def text2():
    return "Hello"
print(text2())       # ?
```

```
Output:
<b><i>Hello</i></b>
<i><b>Hello</b></i>
```

Write one line explaining **why** the order flips.

---

### 12.8 Cache the Fibonacci ⭐⭐⭐

Write your own `@cache` decorator. Then compare:

```
Without cache: fib(35) took about 3 seconds
With cache   : fib(35) took about 0.0000 seconds
With cache   : fib(100) = 354224848179261915075
```

> Then replace yours with `@functools.lru_cache` and confirm the same result.

---
---

# SET 13 — Modules and Packages

### 13.1 Build a Calculator Package ⭐⭐

Create this exact structure:

```
calculator/
├── __init__.py
├── basic.py         (add, subtract, multiply, divide)
└── scientific.py    (power, square_root, log)

main.py
```

```python
# main.py
from calculator.basic import add, divide
from calculator.scientific import power, square_root

print(add(10, 5))        # 15
print(divide(10, 0))     # Error: cannot divide by zero
print(power(2, 10))      # 1024
print(square_root(144))  # 12.0
```

> In `__init__.py`, add `__version__ = "1.0.0"` and re-export `add` so that `from calculator import add` also works.

---

### 13.2 String Tools Module ⭐⭐

Create `stringtools.py` with at least 5 functions and an `__all__` list.

```python
import stringtools as st

print(st.reverse("python"))          # nohtyp
print(st.is_palindrome("madam"))     # True
print(st.count_vowels("education"))  # 5
print(st.title_case("ravi kumar"))   # Ravi Kumar
print(st.remove_spaces("a b c"))     # abc
```

Then test that `from stringtools import *` hides your private helper.

---

### 13.3 The Name Collision Disaster 🔥 ⭐⭐

Create a file called `random.py` in your folder with just this:

```python
print("This is MY random file")
```

Then in another file, try:

```python
import random
print(random.randint(1, 10))
```

Record the exact error. Explain **why** it happened and how to fix it. Then delete the file **and** the `__pycache__` folder.

---

### 13.4 Folder Report ⭐⭐⭐

Use `os` and `datetime` to list every `.py` file in a folder with its size and last-modified date.

```
Output:
File                     Size      Last Modified
------------------------------------------------
set01_p01.py             412 B     23-07-2026 10:15
set02_p03.py             856 B     23-07-2026 11:02
main.py                  1.2 KB    23-07-2026 14:30
------------------------------------------------
Total: 3 files
```

---
---

# SET 14 — The Special Variable `__name__`

### 14.1 The Two-File Experiment ⭐

**File `demo.py`:**
```python
print("The value of __name__ is:", __name__)
```

**File `runner.py`:**
```python
import demo
print("Runner finished")
```

Run **both** files. Record both outputs and explain the difference.

```
$ python demo.py
The value of __name__ is: __main__

$ python runner.py
The value of __name__ is: demo
Runner finished
```

---

### 14.2 The Leaking Module ⭐⭐ 🔥

**Step 1** — Create `mathutils.py` with a test print at the bottom (no guard):

```python
def add(a, b): return a + b
def subtract(a, b): return a - b

print("Testing add:", add(5, 3))
print("Testing subtract:", subtract(5, 3))
```

**Step 2** — Create `app.py` that imports it. Observe the leak:

```
$ python app.py
Testing add: 8            <- unwanted!
Testing subtract: 2       <- unwanted!
App started
300
```

**Step 3** — Add the main guard. Confirm the leak is gone:

```
$ python app.py
App started
300
```

---

### 14.3 Dual-Purpose Module ⭐⭐⭐

Write `temperature.py` that works **two ways**:

- Run directly → runs self-tests and prints a demo
- Imported → gives clean functions, no output

```
$ python temperature.py
All self-tests passed
0°C  = 32.0 °F
37°C = 98.6 °F

$ python -c "from temperature import c_to_f; print(c_to_f(100))"
212.0
```

---

### 14.4 Restructure Your Own Code ⭐⭐

Take **any** program you wrote in Sets 1-12 and restructure it properly:

```python
# 1. Imports
# 2. Constants
# 3. Functions
# 4. def main():
# 5. if __name__ == "__main__": main()
```

Write 2 lines on why `main()` is better than putting the code directly inside the guard.

---
---

# 🔥 FINAL BOSS — Movie Ticket Booking System

**This one project uses every single concept from the course.**

Build `booking_system.py` that produces this output:

```
============================================================
              PVR CINEMAS - BOOKING REPORT
============================================================

Show timings array : array('i', [9, 12, 15, 18, 21])
Bytes used         : 20

Name       Movie          Seats  Price   Total   Category
---------------------------------------------------------
Ravi       RRR                3    250     750   GOLD
Priya      Kalki              2    300     600   GOLD
Kiran      Salaar             5    200    1000   PLATINUM
Divya      RRR                1    250     250   SILVER
Suresh     Kalki              4    300    1200   PLATINUM

Metrics:
  Total bookings    : 5
  Total seats sold  : 15
  Total revenue     : Rs 3,800
  Average per ticket: Rs 253.33
  Highest booking   : Suresh (Rs 1200)

Bookings by movie:
  Kalki  : Priya, Suresh
  RRR    : Ravi, Divya
  Salaar : Kiran

Seat arrangement combinations:
  Ways to choose 3 seats from 10: 120
  5! = 120

[TIMER] generate_report ran in 0.42 ms
Total operations logged: 4
============================================================
```

**Requirements checklist:**

| # | Must use | Where |
|---|----------|-------|
| 1 | `array` module | show timings |
| 2 | `*args` / `**kwargs` | the `summarise()` function |
| 3 | Global variable | operation counter |
| 4 | Factorial (iterative or recursive) | seat combinations |
| 5 | Recursion | `nCr` or flatten |
| 6 | Higher order function | `summarise(data, *metrics)` |
| 7 | Lambda | sorting bookings |
| 8 | `filter()` | bookings above a price |
| 9 | `map()` | calculating totals |
| 10 | `reduce()` | grouping by movie |
| 11 | Closure | booking counter with `nonlocal` |
| 12 | Decorator | `@timer` and `@count_operations` |
| 13 | Module structure | split into 2+ files if you can |
| 14 | `__name__` guard | at the bottom |

**Category rules:** PLATINUM if total >= 1000, GOLD if >= 500, else SILVER.

---

## 🧠 Bonus: Rapid-Fire "Predict the Output"

Do these **on paper first**. No running. Then check.

```python
# 1
print(list(map(lambda x, y: x + y, [1,2,3], [10,20])))

# 2
def f(a, b=[]):
    b.append(a)
    return b
print(f(1), f(2), f(3))

# 3
x = 10
def g():
    global x
    x += 5
g(); g()
print(x)

# 4
fs = [lambda: i for i in range(3)]
print([f() for f in fs])

# 5
r = filter(lambda x: x % 2 == 0, [1,2,3,4])
print(sum(r), sum(r))

# 6
from functools import reduce
print(reduce(lambda a, b: a + b, [], 0))

# 7
def outer():
    x = 1
    def inner():
        x = 2
    inner()
    return x
print(outer())

# 8
print((lambda *a: len(a))(1, 2, 3))

# 9
def h(n):
    if n == 0: return 0
    h(n - 1)
print(h(3))

# 10
print(list(filter(None, [0, "0", "", [], [0], False])))
```

---

## ✅ Submission Checklist

- [ ] Every problem in its own file, correctly named
- [ ] Every file has your **predicted output** written as a comment at the top
- [ ] Sets 1-14 attempted (⭐⭐⭐ ones can be partial — show your attempt)
- [ ] Final Boss attempted
- [ ] Rapid-fire answers written **on paper** and photographed
- [ ] Zipped as `<yourname>_functions_assignment.zip`

---

*You will not remember this by reading. You will remember it by typing it, breaking it, and fixing it. Start now.*
