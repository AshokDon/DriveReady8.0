# Python Functions Masterclass
### From Arrays to Decorators — A Trainer's Complete Notebook

---

## How to use this book

I am going to teach you the way I teach in a classroom. Every chapter follows the same rhythm:

1. **Why does this exist?** — the problem the feature solves
2. **The mental model** — a picture in your head, not just syntax
3. **Syntax + runnable code** — every snippet is complete and tested
4. **Trace / dry run** — what the machine actually does, line by line
5. **Mistakes I see every batch** — the errors you *will* make
6. **Practice** — do these before moving on

Do not read this like a novel. Open a `.py` file, type every example **by hand** (no copy-paste), break it deliberately, and read the error message. Errors are the syllabus.

---

## Table of Contents

| # | Topic |
|---|-------|
| 1 | Array Functions |
| 2 | Arguments in Functions |
| 3 | Global vs Local Variables |
| 4 | Factorial in Python (Iterative) |
| 5 | Recursion |
| 6 | Factorial using Recursion |
| 7 | Higher Order Functions |
| 8 | Anonymous Functions using Lambda |
| 9 | The `filter()` Function |
| 10 | `map()` and `reduce()` |
| 11 | Inner Functions and Closures |
| 12 | Decorators |
| 13 | Modules and Packages |
| 14 | The Special Variable `__name__` |
| 15 | Capstone Project |
| — | Cheat Sheet + Interview Questions |

---
---

# Chapter 1 — Array Functions

## 1.1 Why does an array exist when we already have lists?

In C or Java, an array is a block of memory holding elements of **one type**, packed tightly, one after another. Python's `list` is different — it is a container of *references* to objects, and those objects can be of any type:

```python
mixed = [1, "hello", 3.14, True, [9, 8]]   # perfectly legal
```

That flexibility costs memory and speed. When you have 10 lakh integers and nothing else, you don't want 10 lakh full-blown Python objects. That is where the `array` module comes in.

**Rule of thumb:**

| Use | When |
|-----|------|
| `list` | 95% of the time — mixed data, small collections, general programming |
| `array` module | Large homogeneous numeric data, memory matters, binary file I/O |
| `numpy.ndarray` | Any real numerical/scientific work — maths on whole arrays at once |

## 1.2 Creating an array

```python
import array as arr

a = arr.array('i', [10, 20, 30, 40, 50])
print(a)
print(type(a))
```

**Output:**
```
array('i', [10, 20, 30, 40, 50])
<class 'array.array'>
```

Syntax: `array.array(typecode, initializer)`

The **typecode** is a single character telling Python what kind of number this array holds.

| Typecode | C Type | Python type | Min bytes |
|----------|--------|-------------|-----------|
| `'b'` | signed char | int | 1 |
| `'B'` | unsigned char | int | 1 |
| `'u'` | wchar_t | Unicode char | 2 |
| `'h'` | signed short | int | 2 |
| `'H'` | unsigned short | int | 2 |
| `'i'` | signed int | int | 2 (usually 4) |
| `'I'` | unsigned int | int | 2 (usually 4) |
| `'l'` | signed long | int | 4 |
| `'L'` | unsigned long | int | 4 |
| `'q'` | signed long long | int | 8 |
| `'Q'` | unsigned long long | int | 8 |
| `'f'` | float | float | 4 |
| `'d'` | double | float | 8 |

The big restriction: **every element must match the typecode.**

```python
a = arr.array('i', [10, 20, 30])
a.append(3.5)      # TypeError: 'float' object cannot be interpreted as an integer
a.append("hi")     # TypeError
```

This is a *feature*, not a limitation. The type error catches bugs early.

## 1.3 Accessing and slicing

```python
import array as arr
a = arr.array('i', [10, 20, 30, 40, 50])

print(a[0])      # 10   -> first element
print(a[3])      # 40
print(a[-1])     # 50   -> last element
print(a[1:4])    # array('i', [20, 30, 40])
print(a[::-1])   # array('i', [50, 40, 30, 20, 10])  reversed copy
print(len(a))    # 5
```

Note that slicing an array gives you back an **array**, not a list.

## 1.4 The array functions (methods) — one by one

I'll show them all against a single running example.

### `append(x)` — add one item at the end

```python
a = arr.array('i', [10, 20, 30])
a.append(40)
print(a)        # array('i', [10, 20, 30, 40])
```

### `insert(i, x)` — add at position `i`

```python
a.insert(1, 15)
print(a)        # array('i', [10, 15, 20, 30, 40])
```

### `extend(iterable)` — add many items at once

```python
a = arr.array('i', [1, 2])
a.extend([3, 4, 5])
print(a)        # array('i', [1, 2, 3, 4, 5])
```

> **Trainer note:** `append([3,4,5])` fails, `extend([3,4,5])` works. `append` adds *one* element; `extend` merges a whole sequence.

### `fromlist(list)` — append items from a Python list

```python
a = arr.array('i', [1, 2])
a.fromlist([7, 8, 9])
print(a)        # array('i', [1, 2, 7, 8, 9])
```

### `tolist()` — convert array back to a normal list

```python
print(a.tolist())    # [1, 2, 7, 8, 9]
print(type(a.tolist()))  # <class 'list'>
```

### `remove(x)` — delete the **first occurrence** of value `x`

```python
a = arr.array('i', [10, 20, 30, 20])
a.remove(20)
print(a)        # array('i', [10, 30, 20])   only the FIRST 20 went
```

If the value isn't present → `ValueError: array.remove(x): x not in array`

### `pop([i])` — remove **by index** and return the value

```python
a = arr.array('i', [10, 20, 30, 40])
last = a.pop()       # no argument -> removes last
print(last, a)       # 40 array('i', [10, 20, 30])

first = a.pop(0)     # removes index 0
print(first, a)      # 10 array('i', [20, 30])
```

> **`remove` vs `pop` — the classic exam question:**
> `remove(20)` means "delete the value 20". `pop(20)` means "delete whatever is sitting at index 20". One takes a *value*, the other takes a *position*. `pop` also *returns* the deleted item; `remove` returns `None`.

### `index(x)` — position of the first occurrence

```python
a = arr.array('i', [10, 20, 30, 20])
print(a.index(20))   # 1
```

### `count(x)` — how many times `x` appears

```python
print(a.count(20))   # 2
print(a.count(99))   # 0
```

### `reverse()` — reverse **in place**

```python
a = arr.array('i', [1, 2, 3])
a.reverse()
print(a)        # array('i', [3, 2, 1])
```

Note: `a.reverse()` modifies `a` and returns `None`. `a[::-1]` returns a new reversed array and leaves `a` alone. Never write `a = a.reverse()` — you'll get `None`.

### `buffer_info()` — memory address and element count

```python
a = arr.array('i', [1, 2, 3])
print(a.buffer_info())   # (140234..., 3)  -> (memory_address, number_of_items)
```

### `typecode` and `itemsize` — attributes, not methods (no parentheses)

```python
a = arr.array('i', [1, 2, 3])
print(a.typecode)   # i
print(a.itemsize)   # 4    -> bytes per element on most machines
print(a.itemsize * len(a), "bytes of data")   # 12 bytes of data
```

### `tobytes()` / `frombytes()` — binary conversion

```python
a = arr.array('i', [1, 2, 3])
raw = a.tobytes()
print(raw)          # b'\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00'

b = arr.array('i')
b.frombytes(raw)
print(b)            # array('i', [1, 2, 3])
```

This is how you write arrays into binary files efficiently.

### `tofile()` / `fromfile()` — save and load

```python
a = arr.array('i', [1, 2, 3, 4, 5])

with open("data.bin", "wb") as f:
    a.tofile(f)

b = arr.array('i')
with open("data.bin", "rb") as f:
    b.fromfile(f, 5)      # must say HOW MANY items to read

print(b)    # array('i', [1, 2, 3, 4, 5])
```

## 1.5 Complete worked program

```python
import array as arr

def array_demo():
    marks = arr.array('i', [85, 92, 78, 90, 66])

    print("Array         :", marks)
    print("As list       :", marks.tolist())
    print("Length        :", len(marks))
    print("Highest       :", max(marks))
    print("Lowest        :", min(marks))
    print("Total         :", sum(marks))
    print("Average       :", sum(marks) / len(marks))
    print("Index of 90   :", marks.index(90))
    print("Bytes/element :", marks.itemsize)

    marks.append(75)
    marks.insert(0, 100)
    marks.remove(66)
    dropped = marks.pop()

    print("After edits   :", marks)
    print("Popped        :", dropped)

    marks.reverse()
    print("Reversed      :", marks)

    print("Sorted (list) :", sorted(marks))

array_demo()
```

**Output:**
```
Array         : array('i', [85, 92, 78, 90, 66])
As list       : [85, 92, 78, 90, 66]
Length        : 5
Highest       : 92
Lowest        : 66
Total         : 411
Average       : 82.2
Index of 90   : 3
Bytes/element : 4
After edits   : array('i', [100, 85, 92, 78, 90])
Popped        : 75
Reversed      : array('i', [90, 78, 92, 85, 100])
Sorted (list) : [78, 85, 90, 92, 100]
```

> **Watch out:** arrays have no `.sort()` method. Use the built-in `sorted()` — but it returns a *list*. To get an array back: `arr.array('i', sorted(marks))`.

## 1.6 List functions (because 90% of "array" questions are really list questions)

```python
nums = [10, 20, 30]

nums.append(40)        # [10, 20, 30, 40]
nums.insert(1, 15)     # [10, 15, 20, 30, 40]
nums.extend([50, 60])  # [10, 15, 20, 30, 40, 50, 60]
nums.remove(15)        # deletes value 15
x = nums.pop()         # removes & returns last
nums.index(30)         # position of 30
nums.count(30)         # how many 30s
nums.sort()            # sorts in place
nums.sort(reverse=True)# descending
nums.reverse()         # reverse in place
copy = nums.copy()     # shallow copy
nums.clear()           # empties the list
```

Built-ins that work on both lists and arrays: `len()`, `sum()`, `max()`, `min()`, `sorted()`, `any()`, `all()`, `enumerate()`, `zip()`.

## 1.7 A one-minute look at NumPy

Once you go beyond a classroom, this is what people actually mean by "array":

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])

print(a * 2)          # [ 2  4  6  8 10]   -- whole array at once!
print(a + 10)         # [11 12 13 14 15]
print(a.mean())       # 3.0
print(a.sum())        # 15
print(a[a > 2])       # [3 4 5]  -- boolean filtering
```

With a plain list, `[1,2,3] * 2` gives `[1,2,3,1,2,3]` — repetition, not multiplication. That difference is the whole reason NumPy exists.

## 1.8 Mistakes I see every batch

1. `a.append([1,2,3])` when you meant `extend`.
2. `a = a.reverse()` → `a` becomes `None`. In-place methods return `None`.
3. Mixing `remove` (value) and `pop` (index).
4. Removing items while looping over the array — the indices shift under you.
5. Forgetting arrays are typed: `arr.array('i', [1.5])` fails.

## 1.9 Practice

1. Create an integer array of 10 numbers. Print only the elements at even indices.
2. Find the second largest element of an array without using `sort()`.
3. Merge two sorted arrays into a single sorted array.
4. Count how many even and odd numbers an array contains.
5. Rotate an array left by `k` positions.

---
---

# Chapter 2 — Arguments in Functions

## 2.1 The vocabulary that trips everyone up

```python
def greet(name):      # 'name' is a PARAMETER (the placeholder in the definition)
    print("Hello", name)

greet("Ravi")         # "Ravi" is an ARGUMENT (the actual value you pass)
```

Parameter = variable in the definition. Argument = value at the call. Most people use them interchangeably; in an exam, don't.

Python supports **five** ways to pass arguments. Learn them in this order.

## 2.2 Positional arguments

Matched by **order**. Nothing else.

```python
def student(name, course, city):
    print(f"{name} is learning {course} in {city}")

student("Anita", "Python", "Hyderabad")
```
**Output:** `Anita is learning Python in Hyderabad`

Change the order and the meaning breaks silently:

```python
student("Python", "Anita", "Hyderabad")
# Python is learning Anita in Hyderabad     <- no error, just wrong
```

Wrong *count* is a hard error:

```python
student("Anita", "Python")
# TypeError: student() missing 1 required positional argument: 'city'
```

## 2.3 Keyword arguments

Matched by **name**, so order stops mattering.

```python
student(course="Python", city="Hyderabad", name="Anita")
# Anita is learning Python in Hyderabad
```

You can mix them, but **positional must come first**:

```python
student("Anita", city="Hyderabad", course="Python")   # valid
student(name="Anita", "Python", "Hyderabad")          # SyntaxError
```

**Why use keyword arguments?** Readability. Compare:

```python
create_user("Ravi", 25, True, False, True)                       # what are these?
create_user("Ravi", age=25, active=True, admin=False, sms=True)  # obvious
```

## 2.4 Default arguments

Give a parameter a fallback value; the caller may skip it.

```python
def student(name, course="Python", city="Hyderabad"):
    print(f"{name} is learning {course} in {city}")

student("Anita")                        # Anita is learning Python in Hyderabad
student("Ravi", "Java")                 # Ravi is learning Java in Hyderabad
student("Kiran", city="Chennai")        # Kiran is learning Python in Chennai
```

**Hard rule:** non-default parameters cannot follow default ones.

```python
def f(a=10, b):     # SyntaxError: non-default argument follows default argument
    pass
```

Because otherwise `f(5)` would be ambiguous — is 5 for `a` or `b`?

### The mutable default trap (a genuine interview favourite)

```python
def add_item(item, cart=[]):        # DANGER
    cart.append(item)
    return cart

print(add_item("pen"))      # ['pen']
print(add_item("book"))     # ['pen', 'book']   <- WHY?!
print(add_item("bag"))      # ['pen', 'book', 'bag']
```

The default value `[]` is created **once**, when the `def` line executes — not on every call. All calls share that one list.

**The fix:**

```python
def add_item(item, cart=None):
    if cart is None:
        cart = []
    cart.append(item)
    return cart

print(add_item("pen"))      # ['pen']
print(add_item("book"))     # ['book']   correct
```

Never use a mutable default (`[]`, `{}`, `set()`). Always use `None` as the sentinel.

## 2.5 Variable-length arguments: `*args`

What if you don't know how many values will come? `*args` collects the extra positional arguments into a **tuple**.

```python
def total(*args):
    print(type(args), args)
    return sum(args)

print(total(1, 2, 3))            # <class 'tuple'> (1, 2, 3)  -> 6
print(total(1, 2, 3, 4, 5, 6))   # -> 21
print(total())                   # -> 0
```

Mixing with normal parameters:

```python
def bill(customer, *items):
    print("Customer:", customer)
    for i, item in enumerate(items, start=1):
        print(f"  {i}. {item}")
    print("Total items:", len(items))

bill("Anita", "Rice", "Dal", "Oil")
```
**Output:**
```
Customer: Anita
  1. Rice
  2. Dal
  3. Oil
Total items: 3
```

> The name `args` is only a convention. `*items`, `*nums`, `*values` all work. **The `*` is what matters.**

## 2.6 Variable-length keyword arguments: `**kwargs`

Collects extra *keyword* arguments into a **dictionary**.

```python
def profile(**kwargs):
    print(type(kwargs))
    for key, value in kwargs.items():
        print(f"{key:10} : {value}")

profile(name="Anita", age=22, city="Hyderabad", course="Python")
```
**Output:**
```
<class 'dict'>
name       : Anita
age        : 22
city       : Hyderabad
course     : Python
```

## 2.7 Everything together — the order rule

The full legal signature order is:

```
def f(positional, /, standard, default=val, *args, keyword_only, **kwargs):
```

A practical example:

```python
def register(name, age, course="Python", *hobbies, **details):
    print("Name    :", name)
    print("Age     :", age)
    print("Course  :", course)
    print("Hobbies :", hobbies)
    print("Details :", details)

register("Anita", 22, "Java", "chess", "music", city="Pune", fee=5000)
```
**Output:**
```
Name    : Anita
Age     : 22
Course  : Java
Hobbies : ('chess', 'music')
Details : {'city': 'Pune', 'fee': 5000}
```

**Memorise this order:** *positional → default → `*args` → `**kwargs`*.

## 2.8 Unpacking at the call site (`*` and `**` again, in reverse)

The same symbols do the opposite job when calling:

```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add(*nums))              # 6    -> unpacks list into a, b, c

data = {'a': 10, 'b': 20, 'c': 30}
print(add(**data))             # 60   -> unpacks dict by key name
```

**In a definition, `*` packs. In a call, `*` unpacks.** That one sentence clears most of the confusion.

## 2.9 Keyword-only and positional-only parameters

```python
def transfer(amount, *, to_account):    # anything after * is keyword-only
    print(f"Sent {amount} to {to_account}")

transfer(500, to_account="ACC123")      # OK
transfer(500, "ACC123")                 # TypeError
```

This forces the caller to be explicit — a good safety habit for dangerous operations.

```python
def power(base, exp, /):                # anything before / is positional-only
    return base ** exp

print(power(2, 3))            # 8
print(power(base=2, exp=3))   # TypeError
```

`/` is available from Python 3.8. You'll rarely write it, but you'll see it in the docs.

## 2.10 Is Python "pass by value" or "pass by reference"?

Neither. It is **pass by object reference**. What happens depends on whether the object is mutable.

```python
def change_number(n):
    n = n + 10
    print("inside :", n)

x = 5
change_number(x)
print("outside:", x)
```
**Output:**
```
inside : 15
outside: 5
```
Integers are immutable — reassignment inside makes a brand-new object.

```python
def change_list(lst):
    lst.append(99)
    print("inside :", lst)

items = [1, 2, 3]
change_list(items)
print("outside:", items)
```
**Output:**
```
inside : [1, 2, 3, 99]
outside: [1, 2, 3, 99]
```
Lists are mutable — you modified the very same object the caller holds.

But watch this:

```python
def rebind(lst):
    lst = [100, 200]     # rebinding the LOCAL name, not the caller's object
    print("inside :", lst)

items = [1, 2, 3]
rebind(items)
print("outside:", items)     # [1, 2, 3]  -- unchanged!
```

**The rule:** *mutating* an object is visible outside; *reassigning* the name is not.

## 2.11 Return values

```python
def divide(a, b):
    if b == 0:
        return None, "Cannot divide by zero"
    return a / b, "Success"

result, message = divide(10, 2)     # tuple unpacking
print(result, message)              # 5.0 Success
```

A function with no `return` returns `None`:

```python
def show():
    print("hi")

x = show()
print(x)      # hi  then  None
```

## 2.12 Mistakes I see every batch

1. Putting a positional argument after a keyword argument.
2. Mutable default arguments.
3. `def f(a=1, b)` — default before non-default.
4. Expecting `*args` to be a list — it's a **tuple** (immutable).
5. Assuming reassigning a list parameter changes the caller's list.

## 2.13 Practice

1. Write `calculator(a, b, op="+")` supporting `+ - * /` with zero-division handling.
2. Write `max_of_all(*nums)` returning the largest of any number of arguments.
3. Write `build_query(**filters)` that turns `name="x", age=2` into `"name=x&age=2"`.
4. Write a function accepting a student's name plus any number of subject=marks pairs, and print the average.
5. Predict the output before running:
   ```python
   def f(a, b=[], *c, **d):
       b.append(a)
       return a, b, c, d
   print(f(1))
   print(f(2, [9]))
   print(f(3))
   ```

---
---

# Chapter 3 — Global vs Local Variables

## 3.1 The core idea: scope

**Scope** = the region of code where a name is visible.

Every time a function is called, Python creates a fresh **namespace** — a private dictionary of names — and destroys it when the function returns. That is why:

```python
def show():
    x = 10          # local to show()
    print(x)

show()              # 10
print(x)            # NameError: name 'x' is not defined
```

`x` was born and died inside `show()`.

## 3.2 Local variables

```python
def calculate():
    a = 5           # local
    b = 10          # local
    print("Inside :", a + b)

calculate()         # Inside : 15
# print(a)          # NameError
```

Two functions can use the same local name with zero interference:

```python
def first():
    msg = "I am from first"
    print(msg)

def second():
    msg = "I am from second"
    print(msg)

first()     # I am from first
second()    # I am from second
```

## 3.3 Global variables

Defined at module level, readable from anywhere in the file.

```python
counter = 0                 # global

def show():
    print("Reading global:", counter)   # reading is fine

show()          # Reading global: 0
print(counter)  # 0
```

**Reading** a global inside a function works. **Writing** does not — and this is where beginners get stuck.

## 3.4 The `UnboundLocalError` that confuses everyone

```python
count = 10

def increment():
    count = count + 1       # BOOM
    print(count)

increment()
```
**Output:**
```
UnboundLocalError: cannot access local variable 'count' where it is not associated with a value
```

**Why?** Python scans the whole function body *before* running it. It sees `count = ...` — an assignment — and decides "`count` is a local variable of this function." Then at runtime, the right-hand side `count + 1` tries to read the *local* `count`, which has no value yet. Crash.

The global `count = 10` was never involved.

## 3.5 The `global` keyword

Tell Python explicitly: "this name refers to the module-level variable."

```python
count = 10

def increment():
    global count
    count = count + 1
    print("Inside :", count)

increment()             # Inside : 11
print("Outside:", count)  # Outside: 11
```

You can also *create* a global from inside a function:

```python
def setup():
    global config
    config = {"debug": True}

setup()
print(config)      # {'debug': True}
```

Works, but it's poor style — the variable appears out of nowhere.

## 3.6 The LEGB rule

When Python sees a name, it searches four scopes **in this exact order**:

```
L  Local       — inside the current function
E  Enclosing   — inside any outer function (for nested functions)
G  Global      — at module level
B  Built-in    — Python's own names: print, len, sum, list, ...
```

First match wins. If none match → `NameError`.

```python
x = "global"                 # G

def outer():
    x = "enclosing"          # E
    def inner():
        x = "local"          # L
        print(x)
    inner()

outer()      # local
```

Remove the local:

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        print(x)       # no local x -> look in Enclosing
    inner()

outer()      # enclosing
```

Remove the enclosing one too:

```python
x = "global"

def outer():
    def inner():
        print(x)       # no L, no E -> Global
    inner()

outer()      # global
```

And the built-in layer:

```python
print(len("hello"))     # 5   -> 'len' found in Built-in scope

len = 100               # shadowing a built-in (BAD practice)
# print(len("hello"))   # TypeError: 'int' object is not callable
```

Never name your variables `list`, `str`, `sum`, `type`, `id`, `input`, `max`, `min`, `dict`. Use `lst`, `s`, `total`, `data_type`, `user_id`.

## 3.7 The `nonlocal` keyword

`global` jumps all the way to module level. `nonlocal` targets the **enclosing function's** scope. This matters for nested functions and closures (Chapter 11).

```python
def outer():
    count = 0

    def inner():
        nonlocal count       # bind to outer's 'count'
        count += 1
        print("inner :", count)

    inner()
    inner()
    inner()
    print("outer :", count)

outer()
```
**Output:**
```
inner : 1
inner : 2
inner : 3
outer : 3
```

Remove `nonlocal` and you get `UnboundLocalError` again — the same lesson in a nested costume.

### `global` vs `nonlocal`

| | `global` | `nonlocal` |
|---|---|---|
| Targets | Module-level variable | Nearest enclosing function's variable |
| Can create a new variable? | Yes | No — the variable must already exist |
| Works at top level? | Yes | No — `SyntaxError` |
| Typical use | Counters, config flags | Closures, decorators |

## 3.8 Full comparison example

```python
name = "Global Anita"

def show_scope():
    name = "Local Ravi"
    print("Inside function :", name)

def modify_global():
    global name
    name = "Modified Kiran"
    print("Inside modifier :", name)

print("Before        :", name)
show_scope()
print("After show    :", name)
modify_global()
print("After modify  :", name)
```
**Output:**
```
Before        : Global Anita
Inside function : Local Ravi
After show    : Global Anita
Inside modifier : Modified Kiran
After modify  : Modified Kiran
```

## 3.9 Inspecting scope: `globals()` and `locals()`

```python
x = 100

def demo():
    y = 200
    print("locals :", locals())          # {'y': 200}
    print("x from globals:", globals()['x'])

demo()
```

Useful for debugging and understanding; rarely used in production code.

## 3.10 Why globals are discouraged

```python
# BAD
total = 0

def add(x):
    global total
    total += x

def reset():
    global total
    total = 0
```

Any function anywhere can change `total`. When a bug appears, you must read the *entire* program to find the culprit. Multiply this across a 5,000-line project and it becomes unmaintainable.

```python
# GOOD — pass in, return out
def add(total, x):
    return total + x

total = 0
total = add(total, 5)
total = add(total, 10)
print(total)      # 15
```

**Acceptable uses of globals:** constants (`PI = 3.14159`, `MAX_RETRIES = 3` — write these in `UPPER_CASE`), and module-level configuration set once at startup.

## 3.11 Mistakes I see every batch

1. Assigning to a global without declaring `global` → `UnboundLocalError`.
2. Thinking `global x` inside a nested function reaches the *enclosing* function. It doesn't — it goes to module level.
3. Shadowing built-ins (`list = [1,2,3]`, then `list(...)` fails).
4. Believing `if`/`for`/`while` blocks create scope. **They do not.** Only functions, classes, comprehensions, and modules do.
   ```python
   if True:
       z = 5
   print(z)      # 5 — perfectly fine
   ```
5. Overusing `global` as a shortcut instead of returning values.

## 3.12 Practice

1. Predict the output, then run:
   ```python
   x = 10
   def f():
       print(x)
       x = 20
   f()
   ```
2. Write a counter function using `global`, then rewrite it using `nonlocal` inside a nested function.
3. Explain why this prints `5` and not `10`:
   ```python
   x = 5
   def f(x):
       x = 10
   f(x)
   print(x)
   ```
4. Write a nested function three levels deep and demonstrate all four LEGB layers.

---
---

# Chapter 4 — Factorial in Python (Iterative)

## 4.1 The mathematics first

The factorial of a non-negative integer *n*, written **n!**, is the product of all positive integers from 1 to *n*.

```
5! = 5 × 4 × 3 × 2 × 1 = 120
4! = 4 × 3 × 2 × 1      = 24
3! = 3 × 2 × 1          = 6
1! = 1
0! = 1                  <- by definition, not an accident
```

**Why is 0! = 1?** Because n! counts the number of ways to arrange n objects. There is exactly **one** way to arrange nothing — do nothing. It also keeps the identity `n! = n × (n-1)!` valid at n = 1: `1! = 1 × 0!` only works if `0! = 1`.

Factorial is **not defined for negative numbers**. Your program must reject them.

## 4.2 Version 1 — `for` loop

```python
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result = result * i
    return result

print(factorial(5))     # 120
print(factorial(0))     # 1
print(factorial(1))     # 1
print(factorial(10))    # 3628800
```

**Dry run for n = 5:**

| Iteration | i | result before | operation | result after |
|-----------|---|---------------|-----------|--------------|
| start | — | 1 | — | 1 |
| 1 | 1 | 1 | 1 × 1 | 1 |
| 2 | 2 | 1 | 1 × 2 | 2 |
| 3 | 3 | 2 | 2 × 3 | 6 |
| 4 | 4 | 6 | 6 × 4 | 24 |
| 5 | 5 | 24 | 24 × 5 | **120** |

Two things people get wrong here:

- Starting `result = 0`. Then everything is 0. The multiplicative identity is **1**, not 0.
- Writing `range(1, n)`. That stops at n−1. You need `range(1, n+1)`.

## 4.3 Version 2 — counting downwards

```python
def factorial(n):
    result = 1
    for i in range(n, 0, -1):     # n, n-1, ..., 1
        result *= i
    return result

print(factorial(5))    # 120
```

Same answer. Multiplication is commutative, so direction doesn't matter.

## 4.4 Version 3 — `while` loop

```python
def factorial(n):
    result = 1
    i = 1
    while i <= n:
        result *= i
        i += 1
    return result

print(factorial(6))    # 720
```

Forget `i += 1` and you get an infinite loop. That is the whole risk of `while`.

## 4.5 Version 4 — production-quality, with validation

```python
def factorial(n):
    """Return n! for a non-negative integer n."""
    if not isinstance(n, int):
        raise TypeError(f"Expected an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")

    result = 1
    for i in range(2, n + 1):     # skip 1; multiplying by 1 is pointless
        result *= i
    return result


# Testing it
for value in [0, 1, 5, 10, 20]:
    print(f"{value:>3}! = {factorial(value)}")

for bad in [-3, 2.5, "five"]:
    try:
        factorial(bad)
    except (TypeError, ValueError) as e:
        print(f"{str(bad):>6} -> {type(e).__name__}: {e}")
```

**Output:**
```
  0! = 1
  1! = 1
  5! = 120
 10! = 3628800
 20! = 2432902008176640000
    -3 -> ValueError: Factorial is not defined for negative numbers
   2.5 -> TypeError: Expected an integer, got float
  five -> TypeError: Expected an integer, got str
```

## 4.6 Version 5 — the built-in (use this in real code)

```python
import math

print(math.factorial(5))     # 120
print(math.factorial(20))    # 2432902008176640000
print(math.factorial(0))     # 1
# math.factorial(-1)         # ValueError
# math.factorial(2.5)        # TypeError
```

It is written in C, so it's much faster, and it already validates its input. **Write your own only for learning or in an exam.**

## 4.7 Version 6 — one-liner with `reduce` (preview of Chapter 10)

```python
from functools import reduce

def factorial(n):
    return reduce(lambda x, y: x * y, range(1, n + 1), 1)

print(factorial(5))     # 120
print(factorial(0))     # 1  (the initial value 1 saves us on the empty range)
```

## 4.8 Interactive program

```python
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def main():
    while True:
        raw = input("Enter a non-negative integer (or 'q' to quit): ")
        if raw.lower() == 'q':
            print("Bye!")
            break
        try:
            n = int(raw)
            if n < 0:
                print("  Negative numbers have no factorial. Try again.")
                continue
            print(f"  {n}! = {factorial(n)}")
        except ValueError:
            print("  That's not a whole number. Try again.")

main()
```

## 4.9 Python's superpower: unlimited integer size

```python
print(len(str(math.factorial(100))))   # 158
print(math.factorial(100))
```
Prints a 158-digit number, exactly. In C or Java, `100!` overflows a 64-bit integer long before this. Python integers grow to whatever size is needed, limited only by memory.

## 4.10 Factorial table generator

```python
import math

print(f"{'n':>3} | {'n!':>25} | {'digits':>6}")
print("-" * 40)
for n in range(0, 21):
    f = math.factorial(n)
    print(f"{n:>3} | {f:>25,} | {len(str(f)):>6}")
```

## 4.11 Where factorial is actually used

- **Permutations:** number of ways to arrange n items = `n!`
- **Combinations:** `nCr = n! / (r! × (n-r)!)` — probability, lottery odds
- **Taylor series:** `e^x = 1 + x/1! + x²/2! + x³/3! + ...`
- **Probability:** birthday problem, card shuffles

```python
import math

def nCr(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

print("Ways to pick 11 players from 15:", nCr(15, 11))   # 1365
print(math.comb(15, 11))    # 1365 — Python 3.8+ built-in, and far faster
```

## 4.12 Practice

1. Print factorials from 1 to 10 in a formatted table.
2. Find the number of trailing zeros in `100!` **without** computing `100!`. (Hint: count factors of 5.)
3. Write `nPr(n, r)` for permutations.
4. Compute `e` using the series `1 + 1/1! + 1/2! + ... ` up to 20 terms and compare with `math.e`.
5. Given a digit-sum function, find the digit sum of `50!`.

---
---

# Chapter 5 — Recursion

## 5.1 The idea

**Recursion** is a function calling itself to solve a smaller version of the same problem.

Real-life picture: you're in a cinema queue and want to know which row you're in. You can't see the screen. So you tap the person in front and ask, "Which row are you in?" They ask the person in front of them. This continues until it reaches the person in row 1, who says "I'm in row 1" — no asking needed. That answer travels back: 2, 3, 4… until it reaches you.

Two pieces make it work:

- **Base case** — the person in row 1 who answers *without* asking anyone. This stops the chain.
- **Recursive case** — everyone else, who asks a *smaller* question and adds 1 to the answer.

```python
def recursive_function(problem):
    if problem is small enough:        # BASE CASE — mandatory
        return direct_answer
    else:                              # RECURSIVE CASE
        return recursive_function(smaller_problem)
```

**Miss the base case and your program dies.** That is not a stylistic issue — it is the single rule of recursion.

## 5.2 Your first recursion — countdown

```python
def countdown(n):
    if n == 0:               # base case
        print("Blast off!")
        return
    print(n)
    countdown(n - 1)         # recursive case, moving TOWARD the base

countdown(5)
```
**Output:**
```
5
4
3
2
1
Blast off!
```

## 5.3 What actually happens — the call stack

Every function call gets a **stack frame**: a box holding its parameters and local variables. Calls stack up; when one returns, its box is destroyed.

```python
def add_upto(n):
    if n == 1:
        return 1
    return n + add_upto(n - 1)

print(add_upto(4))     # 10
```

**Winding phase** (calls going deeper — nothing has been computed yet):

```
add_upto(4)  ->  4 + add_upto(3)
                     add_upto(3)  ->  3 + add_upto(2)
                                          add_upto(2)  ->  2 + add_upto(1)
                                                               add_upto(1)  ->  1   [BASE CASE HIT]
```

**Unwinding phase** (answers travel back up):

```
add_upto(1) returns 1
add_upto(2) returns 2 + 1  = 3
add_upto(3) returns 3 + 3  = 6
add_upto(4) returns 4 + 6  = 10
```

**Key insight:** the deepest call finishes *first*. Nothing is actually added until the base case is reached.

You can see this with prints:

```python
def add_upto(n):
    print(f"{'  ' * (5-n)}-> entering add_upto({n})")
    if n == 1:
        print(f"{'  ' * (5-n)}<- base case, returning 1")
        return 1
    result = n + add_upto(n - 1)
    print(f"{'  ' * (5-n)}<- add_upto({n}) returning {result}")
    return result

add_upto(4)
```
**Output:**
```
  -> entering add_upto(4)
    -> entering add_upto(3)
      -> entering add_upto(2)
        -> entering add_upto(1)
        <- base case, returning 1
      <- add_upto(2) returning 3
    <- add_upto(3) returning 6
  <- add_upto(4) returning 10
```

Type this program out. Run it. Watching the indentation grow and shrink teaches recursion better than any paragraph I can write.

## 5.4 What happens with no base case

```python
def broken(n):
    return n + broken(n - 1)     # never stops

broken(5)
# RecursionError: maximum recursion depth exceeded
```

Python protects you with a depth limit (default 1000):

```python
import sys
print(sys.getrecursionlimit())     # 1000
sys.setrecursionlimit(3000)        # can raise it — but usually a design smell
```

If you *need* 10,000 levels of recursion, use a loop instead.

## 5.5 Classic recursion problems

### Sum of digits

```python
def digit_sum(n):
    if n == 0:
        return 0
    return n % 10 + digit_sum(n // 10)

print(digit_sum(12345))     # 15
```
Trace: `5 + (4 + (3 + (2 + (1 + 0))))`

### Reverse a string

```python
def reverse(s):
    if len(s) <= 1:
        return s
    return reverse(s[1:]) + s[0]

print(reverse("PYTHON"))     # NOHTYP
```
`reverse("PYTHON")` = `reverse("YTHON") + "P"` = … = `"NOHTY" + "P"`

### Palindrome check

```python
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])

print(is_palindrome("madam"))          # True
print(is_palindrome("Never odd or even"))  # True
print(is_palindrome("python"))         # False
```

### Power (x^n)

```python
def power(x, n):
    if n == 0:
        return 1
    return x * power(x, n - 1)

print(power(2, 10))     # 1024
```

A smarter version — **divide and conquer**, O(log n) instead of O(n):

```python
def fast_power(x, n):
    if n == 0:
        return 1
    half = fast_power(x, n // 2)
    if n % 2 == 0:
        return half * half
    return x * half * half

print(fast_power(2, 30))     # 1073741824
```

### GCD (Euclid's algorithm)

```python
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

print(gcd(48, 18))     # 6
print(gcd(100, 75))    # 25
```

Beautifully short. `gcd(48,18) → gcd(18,12) → gcd(12,6) → gcd(6,0) → 6`

### Fibonacci

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

**But this is a terrible implementation.** It has *two* recursive calls, so the work doubles at each level — O(2ⁿ). `fib(40)` takes seconds; `fib(50)` takes minutes.

Look at the wasted work for `fib(5)`:

```
                      fib(5)
              /                    \
          fib(4)                  fib(3)
         /      \                /      \
     fib(3)    fib(2)        fib(2)    fib(1)
     /    \     /   \         /   \
 fib(2) fib(1) fib(1) fib(0) fib(1) fib(0)
```

`fib(3)` is computed twice, `fib(2)` three times. The fix is **memoization** — remember what you've already computed:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(100))     # 354224848179261915075  — instant
```

That `@lru_cache` line is a **decorator** (Chapter 12). One line turned an exponential algorithm into a linear one.

Manual memoization, if you want to see the machinery:

```python
def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]

print(fib(50))     # 12586269025
```

### Tower of Hanoi

```python
def hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f"Move disk 1: {source} -> {target}")
        return
    hanoi(n - 1, source, auxiliary, target)
    print(f"Move disk {n}: {source} -> {target}")
    hanoi(n - 1, auxiliary, target, source)

hanoi(3, 'A', 'C', 'B')
```
**Output:**
```
Move disk 1: A -> C
Move disk 2: A -> B
Move disk 1: C -> B
Move disk 3: A -> C
Move disk 1: B -> A
Move disk 2: B -> C
Move disk 1: A -> C
```
Seven moves for 3 disks: `2ⁿ − 1`. Try writing this with loops and you'll appreciate recursion.

### Binary search

```python
def binary_search(arr, target, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low > high:
        return -1                     # not found
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search(arr, target, low, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, high)

nums = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(binary_search(nums, 23))     # 5
print(binary_search(nums, 100))    # -1
```

### Flatten a nested list

```python
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))    # recurse into sub-list
        else:
            result.append(item)
    return result

print(flatten([1, [2, 3, [4, [5, 6]], 7], 8]))
# [1, 2, 3, 4, 5, 6, 7, 8]
```

This is where recursion genuinely beats loops — you don't know the nesting depth in advance.

## 5.6 Recursion vs Iteration

| | Recursion | Iteration |
|---|---|---|
| Readability | Elegant for tree/nested problems | Clearer for simple repetition |
| Memory | O(n) stack frames | O(1) |
| Speed | Slower (function-call overhead) | Faster |
| Risk | `RecursionError` | Infinite loop |
| Best for | Trees, graphs, divide & conquer, backtracking, nested structures | Counting, accumulating, scanning |

Python has **no tail-call optimisation**, so deep recursion always costs stack space. In Python, when in doubt, loop.

## 5.7 Mistakes I see every batch

1. **No base case** → `RecursionError`.
2. **Base case unreachable:** `factorial(n-2)` from an odd `n` skips past 0 into negatives forever.
3. **Not returning the recursive call:**
   ```python
   def f(n):
       if n == 0: return 0
       f(n-1)          # missing 'return' -> function returns None
   ```
4. **Not moving toward the base case:** `countdown(n)` instead of `countdown(n-1)`.
5. **Using recursion where a loop is obviously right** — summing a list of a million numbers.

## 5.8 Practice

1. Count the number of digits in a number recursively.
2. Print a list in reverse using recursion.
3. Find the maximum element of a list recursively.
4. Generate all permutations of a string.
5. Solve: given `n` stairs and steps of 1 or 2, how many ways to climb? (Hint: it's Fibonacci.)
6. Write a recursive function to compute the sum of a nested list like `[1,[2,[3,4]],5]`.

---
---

# Chapter 6 — Factorial using Recursion

This chapter deserves its own space because it's the standard teaching example and the standard exam question.

## 6.1 The recursive definition

Look at the pattern:

```
5! = 5 × 4 × 3 × 2 × 1
4! =     4 × 3 × 2 × 1
```

So `5! = 5 × 4!`. In general:

```
n! = n × (n-1)!          for n > 0        <- recursive case
0! = 1                                     <- base case
```

The mathematical definition *is already recursive*. The code is a direct translation.

## 6.2 The code

```python
def factorial(n):
    if n == 0 or n == 1:        # BASE CASE
        return 1
    return n * factorial(n - 1)  # RECURSIVE CASE

print(factorial(5))     # 120
print(factorial(0))     # 1
print(factorial(1))     # 1
print(factorial(10))    # 3628800
```

Three lines. Compare that to the loop version — this is why recursion is beautiful when the problem is naturally recursive.

## 6.3 Full trace for `factorial(5)`

**Winding — going down:**

| Call | Base case? | Returns |
|------|-----------|---------|
| `factorial(5)` | No | `5 * factorial(4)` — *waits* |
| `factorial(4)` | No | `4 * factorial(3)` — *waits* |
| `factorial(3)` | No | `3 * factorial(2)` — *waits* |
| `factorial(2)` | No | `2 * factorial(1)` — *waits* |
| `factorial(1)` | **Yes** | `1` ✔ |

**Unwinding — coming back up:**

| Call | Computation | Result |
|------|-------------|--------|
| `factorial(1)` | — | 1 |
| `factorial(2)` | 2 × 1 | 2 |
| `factorial(3)` | 3 × 2 | 6 |
| `factorial(4)` | 4 × 6 | 24 |
| `factorial(5)` | 5 × 24 | **120** |

The stack at maximum depth:

```
| factorial(1) |  <- top, resolves first
| factorial(2) |
| factorial(3) |
| factorial(4) |
| factorial(5) |  <- bottom, resolves last
+--------------+
```

## 6.4 Watch it happen

```python
def factorial(n, depth=0):
    pad = "|  " * depth
    print(f"{pad}factorial({n}) called")

    if n == 0 or n == 1:
        print(f"{pad}BASE CASE -> returning 1")
        return 1

    print(f"{pad}needs {n} * factorial({n-1}) ... waiting")
    sub = factorial(n - 1, depth + 1)
    result = n * sub
    print(f"{pad}got {sub}, so {n} * {sub} = {result}")
    return result

print("\nFinal answer:", factorial(4))
```

**Output:**
```
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

Run this once and recursion stops being mysterious.

## 6.5 Handling negatives

The naive version is dangerous:

```python
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

factorial(-5)
# -5 -> -6 -> -7 -> ... never hits 0 or 1
# RecursionError: maximum recursion depth exceeded
```

The base case is **unreachable** from a negative start. Always guard:

```python
def factorial(n):
    if not isinstance(n, int):
        raise TypeError("Factorial requires an integer")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


for v in [5, 0, 1]:
    print(f"{v}! = {factorial(v)}")

try:
    factorial(-5)
except ValueError as e:
    print("Error:", e)
```
**Output:**
```
5! = 120
0! = 1
1! = 1
Error: Factorial is not defined for negative numbers
```

> Using `if n <= 1: return 1` instead of `if n == 0 or n == 1` is slightly safer and shorter — but only *after* you've validated the input.

## 6.6 Recursive vs iterative factorial — head to head

```python
import sys, time, math

def fact_recursive(n):
    if n <= 1:
        return 1
    return n * fact_recursive(n - 1)

def fact_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(fact_recursive(500) == fact_iterative(500) == math.factorial(500))  # True

# Now push it
try:
    fact_recursive(5000)
except RecursionError:
    print("Recursive version: RecursionError at n=5000")

print("Iterative version : works fine,", len(str(fact_iterative(5000))), "digits")

# Speed comparison
n = 900
t0 = time.perf_counter(); fact_recursive(n);  t1 = time.perf_counter()
t2 = time.perf_counter(); fact_iterative(n);  t3 = time.perf_counter()
t4 = time.perf_counter(); math.factorial(n);  t5 = time.perf_counter()

print(f"recursive : {(t1-t0)*1e6:8.1f} microseconds")
print(f"iterative : {(t3-t2)*1e6:8.1f} microseconds")
print(f"math      : {(t5-t4)*1e6:8.1f} microseconds")
```

Typical result: recursion is the slowest, `math.factorial` is dramatically the fastest.

| | Recursive | Iterative |
|---|---|---|
| Lines of code | 3 | 5 |
| Readability | Matches the maths exactly | Needs a trace to follow |
| Memory | O(n) stack frames | O(1) |
| Max n | ~995 (default limit) | Millions |
| Speed | Slowest | Fast |

**Verdict for interviews:** know both, explain the trade-off, and mention `math.factorial` as the real-world answer.

## 6.7 Practice

1. Write a recursive `power(base, exp)` and trace `power(2, 4)` on paper.
2. Write a recursive function for `nCr` using recursive factorial.
3. Add `@lru_cache` to the recursive factorial. Does it help? Why or why not?
4. Write a recursive `double_factorial(n)` where `n!! = n × (n-2) × (n-4) × ...`
5. Trace by hand what happens on `factorial(3.5)` with the naive version, and explain the error.

---
---

# Chapter 7 — Higher Order Functions

## 7.1 Functions are objects

This is the concept that unlocks the rest of this book. In Python, a function is a **first-class object** — the same as an int, a string, or a list. You can:

```python
def greet(name):
    return f"Hello, {name}!"

# 1. Assign it to a variable
hello = greet
print(hello("Anita"))          # Hello, Anita!
print(greet is hello)          # True — same object, two names

# 2. Store it in a list or dict
funcs = [greet, str.upper, len]
print(funcs[0]("Ravi"))        # Hello, Ravi!

# 3. Inspect it
print(type(greet))             # <class 'function'>
print(greet.__name__)          # greet

# 4. Pass it to another function
# 5. Return it from another function
```

Notice `hello = greet` has **no parentheses**. `greet` is the function object; `greet()` is the act of *calling* it. Mixing these up is the #1 error in this chapter.

```python
x = greet          # x is the function
y = greet("Ram")   # y is the result string
print(x)           # <function greet at 0x7f...>
print(y)           # Hello, Ram!
```

## 7.2 Definition

A **higher order function (HOF)** is a function that does at least one of:

1. Takes one or more functions as arguments, **or**
2. Returns a function as its result

That's it. Nothing more exotic.

## 7.3 Type 1 — a function as an argument

```python
def apply(func, value):
    return func(value)

def square(x):
    return x * x

def cube(x):
    return x ** 3

print(apply(square, 5))     # 25
print(apply(cube, 3))       # 27
print(apply(len, "Python")) # 6
print(apply(str.upper, "hi"))  # HI
```

`apply` doesn't know or care what `func` does. It just calls it. That is the power — **behaviour becomes a parameter.**

A more useful example:

```python
def process_all(items, operation):
    return [operation(item) for item in items]

nums = [1, 2, 3, 4, 5]

print(process_all(nums, square))            # [1, 4, 9, 16, 25]
print(process_all(nums, cube))              # [1, 8, 27, 64, 125]
print(process_all(nums, lambda x: x + 100)) # [101, 102, 103, 104, 105]
print(process_all(["a","b"], str.upper))    # ['A', 'B']
```

### Why does this matter? A before-and-after

**Without HOFs** — one function per operation:

```python
def double_all(nums):
    out = []
    for n in nums: out.append(n * 2)
    return out

def square_all(nums):
    out = []
    for n in nums: out.append(n ** 2)
    return out

def negate_all(nums):
    out = []
    for n in nums: out.append(-n)
    return out
```

Three functions. The loop is copy-pasted three times. Add a fourth operation and you copy it again.

**With a HOF** — the loop is written once:

```python
def transform(nums, func):
    return [func(n) for n in nums]

print(transform([1,2,3], lambda n: n * 2))    # [2, 4, 6]
print(transform([1,2,3], lambda n: n ** 2))   # [1, 4, 9]
print(transform([1,2,3], lambda n: -n))       # [-1, -2, -3]
```

This is the whole point: **separate the repetitive part (looping) from the varying part (the operation).**

## 7.4 Type 2 — returning a function

```python
def multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply          # returning the function itself

double = multiplier(2)
triple = multiplier(3)
ten_x  = multiplier(10)

print(double(5))     # 10
print(triple(5))     # 15
print(ten_x(5))      # 50
print(multiplier(4)(5))   # 20 — call it immediately
```

`multiplier` is a **function factory**. Each call manufactures a new, customised function. The inner function *remembers* `factor` even after `multiplier` has finished — that's a **closure**, which we'll dissect in Chapter 11.

Another practical factory:

```python
def make_tag(tag):
    def wrap(text):
        return f"<{tag}>{text}</{tag}>"
    return wrap

h1 = make_tag("h1")
bold = make_tag("b")

print(h1("Welcome"))     # <h1>Welcome</h1>
print(bold("Important")) # <b>Important</b>
```

## 7.5 Built-in higher order functions you already use

### `sorted(iterable, key=...)`

`key` takes a **function** that extracts the value to sort by.

```python
words = ["banana", "kiwi", "apple", "cherry"]

print(sorted(words))                    # ['apple', 'banana', 'cherry', 'kiwi']
print(sorted(words, key=len))           # ['kiwi', 'apple', 'banana', 'cherry']
print(sorted(words, key=len, reverse=True))
print(sorted(words, key=lambda w: w[-1]))   # sort by last letter
```

Sorting a list of dictionaries — this is the version you'll actually use at work:

```python
students = [
    {"name": "Anita",  "marks": 85, "age": 20},
    {"name": "Ravi",   "marks": 92, "age": 22},
    {"name": "Kiran",  "marks": 78, "age": 21},
    {"name": "Divya",  "marks": 92, "age": 19},
]

by_marks = sorted(students, key=lambda s: s["marks"], reverse=True)
for s in by_marks:
    print(s["name"], s["marks"])
```
**Output:**
```
Ravi 92
Divya 92
Anita 85
Kiran 78
```

Ravi and Divya both scored 92, and Ravi stays first because Python's sort is **stable** — equal elements keep their original relative order.

Sort by two keys at once — marks descending, then name alphabetically:

```python
result = sorted(students, key=lambda s: (-s["marks"], s["name"]))
print([s["name"] for s in result])
# ['Divya', 'Ravi', 'Anita', 'Kiran']
```

The `key` function returns a **tuple**; Python compares tuples element by element. The minus sign flips the numeric sort to descending.

### `max()` and `min()` with `key`

```python
print(max(students, key=lambda s: s["marks"])["name"])   # Ravi
print(min(students, key=lambda s: s["age"])["name"])     # Divya
print(max(words, key=len))                               # banana
```

### `map`, `filter`, `reduce`

The three canonical HOFs — Chapters 9 and 10.

### `functools.partial` — freeze some arguments

```python
from functools import partial

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube   = partial(power, exp=3)

print(square(5))    # 25
print(cube(2))      # 8
```

### `any()` / `all()` with generator expressions

```python
nums = [2, 4, 6, 8]
print(all(n % 2 == 0 for n in nums))    # True
print(any(n > 7 for n in nums))         # True
```

## 7.6 A realistic example — a pluggable pipeline

```python
def clean(text):
    return text.strip()

def to_lower(text):
    return text.lower()

def remove_spaces(text):
    return text.replace(" ", "_")

def add_prefix(text):
    return "user_" + text

def pipeline(text, *operations):
    """Apply each operation in sequence."""
    for op in operations:
        text = op(text)
        print(f"  after {op.__name__:15}: {text!r}")
    return text

raw = "   Anita Sharma   "
print(f"Starting with: {raw!r}")
final = pipeline(raw, clean, to_lower, remove_spaces, add_prefix)
print("Final:", final)
```
**Output:**
```
Starting with: '   Anita Sharma   '
  after clean          : 'Anita Sharma'
  after to_lower       : 'anita sharma'
  after remove_spaces  : 'anita_sharma'
  after add_prefix     : 'user_anita_sharma'
Final: user_anita_sharma
```

Want a different pipeline? Pass different functions. No changes to `pipeline` itself.

## 7.7 Dispatch tables — replacing long if/elif chains

```python
def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b): return a / b if b != 0 else "Error: divide by zero"

operations = {'+': add, '-': sub, '*': mul, '/': div}

def calculate(a, op, b):
    func = operations.get(op)
    if func is None:
        return f"Unknown operator: {op}"
    return func(a, b)

for op in ['+', '-', '*', '/', '%']:
    print(f"10 {op} 3 =", calculate(10, op, 3))
```
**Output:**
```
10 + 3 = 13
10 - 3 = 7
10 * 3 = 30
10 / 3 = 3.3333333333333335
10 % 3 = Unknown operator: %
```

Adding a new operator = adding one dictionary entry. Compare that to editing a 20-branch `if/elif` chain.

## 7.8 Mistakes I see every batch

1. `apply(square(), 5)` — calling the function when you meant to pass it.
2. `sorted(students, key=lambda s: s["marks"]())` — extra parentheses.
3. Forgetting `key=` expects a function taking **exactly one** argument.
4. Passing a function object into `print()` and being surprised by `<function ... at 0x...>`.

## 7.9 Practice

1. Write `apply_twice(func, value)` that applies `func` two times. `apply_twice(lambda x: x+3, 10)` → 16.
2. Write a `compose(f, g)` that returns a function computing `f(g(x))`.
3. Sort a list of `(name, age, city)` tuples by city, then by age.
4. Build a dispatch table for a text-menu program.
5. Write a HOF `repeat(func, n)` that calls `func` `n` times.

---
---

# Chapter 8 — Anonymous Functions using Lambda

## 8.1 What is a lambda?

A **lambda** is a small function with no name, written in a single expression.

```python
# Normal function
def square(x):
    return x * x

# Same thing as a lambda
square = lambda x: x * x

print(square(5))     # 25
```

**Syntax:**

```
lambda parameters : expression
```

- `lambda` — the keyword
- `parameters` — zero or more, comma-separated
- `:` — separator
- `expression` — a **single expression**, whose value is returned automatically

There is **no `return` keyword** — the expression's value is returned implicitly.

## 8.2 Variations

```python
# No arguments
greet = lambda: "Hello!"
print(greet())                    # Hello!

# One argument
double = lambda x: x * 2
print(double(7))                  # 14

# Multiple arguments
add = lambda a, b: a + b
print(add(3, 4))                  # 7

# Default arguments work
power = lambda base, exp=2: base ** exp
print(power(5))                   # 25
print(power(2, 10))               # 1024

# *args works too
total = lambda *nums: sum(nums)
print(total(1, 2, 3, 4))          # 10

# Conditional expression (ternary)
bigger = lambda a, b: a if a > b else b
print(bigger(10, 20))             # 20

grade = lambda m: "A" if m >= 90 else "B" if m >= 75 else "C" if m >= 60 else "F"
print(grade(95), grade(80), grade(65), grade(40))   # A B C F

# Calling immediately (IIFE)
print((lambda x, y: x * y)(6, 7))     # 42
```

## 8.3 What lambda **cannot** do

```python
# NO statements
f = lambda x: print(x); return x      # SyntaxError

# NO assignments
f = lambda x: y = x + 1               # SyntaxError

# NO multi-line blocks / loops / try-except
f = lambda x:
        for i in range(x):            # SyntaxError
            print(i)

# NO type hints, NO docstrings
```

**One expression. That is the entire restriction.** If you need more, write a `def`.

## 8.4 `lambda` vs `def`

| | `lambda` | `def` |
|---|---|---|
| Has a name | No (unless assigned) | Yes |
| Body | Single expression | Any number of statements |
| `return` | Implicit | Explicit |
| Docstring | No | Yes |
| Debugging | Shows as `<lambda>` in tracebacks | Shows the real name |
| Reusability | Throwaway | Reusable |
| Typical use | Inline argument to a HOF | Everything else |

## 8.5 The golden rule for lambdas

> **Use a lambda only where a function is needed *briefly*, in one place, as an argument to another function. Anywhere else, use `def`.**

This is bad style even though it works:

```python
# Don't do this — PEP 8 explicitly advises against it
square = lambda x: x * x
```

Why? Because it's identical to `def square(x): return x * x`, except the traceback will say `<lambda>` instead of `square`, and you can't add a docstring. You gained nothing and lost debuggability.

This, on the other hand, is exactly right:

```python
students.sort(key=lambda s: s["marks"])
```

The function is needed for a split second, so naming it would be noise.

## 8.6 Where lambdas shine

### With `sorted`

```python
people = [("Anita", 22), ("Ravi", 19), ("Kiran", 25)]

print(sorted(people, key=lambda p: p[1]))
# [('Ravi', 19), ('Anita', 22), ('Kiran', 25)]

print(sorted(people, key=lambda p: p[0]))
# [('Anita', 22), ('Kiran', 25), ('Ravi', 19)]
```

### With `map` / `filter` / `reduce`

```python
nums = [1, 2, 3, 4, 5, 6]
print(list(map(lambda x: x ** 2, nums)))          # [1, 4, 9, 16, 25, 36]
print(list(filter(lambda x: x % 2 == 0, nums)))   # [2, 4, 6]

from functools import reduce
print(reduce(lambda a, b: a * b, nums))           # 720
```

### With `max` / `min`

```python
words = ["python", "is", "wonderful"]
print(max(words, key=lambda w: len(w)))      # wonderful
```

### As dictionary values (a mini calculator)

```python
ops = {
    'add': lambda a, b: a + b,
    'sub': lambda a, b: a - b,
    'mul': lambda a, b: a * b,
    'div': lambda a, b: a / b if b else 'undefined',
}

for name, fn in ops.items():
    print(f"{name}(12, 4) = {fn(12, 4)}")
```
**Output:**
```
add(12, 4) = 16
sub(12, 4) = 8
mul(12, 4) = 48
div(12, 4) = 3.0
```

### As a default in `dict.get` fallbacks or in GUI callbacks

```python
# tkinter example (conceptual)
# button = Button(root, command=lambda: save_file("data.txt"))
```

Lambdas let you attach a *call with arguments* to a callback slot that expects a zero-argument function.

## 8.7 The classic lambda-in-a-loop trap

```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)

print([f() for f in funcs])     # [2, 2, 2]  -- not [0, 1, 2]!
```

**Why?** The lambda doesn't capture the *value* of `i` — it captures the *variable* `i`. By the time you call the lambdas, the loop has finished and `i` is 2.

**Fix — bind the value using a default argument:**

```python
funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)     # i=i evaluates NOW

print([f() for f in funcs])     # [0, 1, 2]
```

This shows up in real code constantly — GUI buttons in a loop, event handlers, callbacks.

## 8.8 When a lambda is the wrong tool

```python
# Unreadable — a lambda doing too much
process = lambda d: {k: (v * 2 if isinstance(v, int) else v.upper() if isinstance(v, str) else v) for k, v in d.items()}

# Readable — the same logic as a def
def process(d):
    """Double numbers, uppercase strings, leave everything else."""
    result = {}
    for key, value in d.items():
        if isinstance(value, int):
            result[key] = value * 2
        elif isinstance(value, str):
            result[key] = value.upper()
        else:
            result[key] = value
    return result
```

If your lambda needs a horizontal scrollbar, it should be a `def`.

Also — often you don't need a lambda at all:

```python
list(map(lambda x: x.upper(), words))   # works
list(map(str.upper, words))             # cleaner
sorted(words, key=lambda w: len(w))     # works
sorted(words, key=len)                  # cleaner
```

## 8.9 Mistakes I see every batch

1. Writing `lambda x: return x*2` — no `return` allowed.
2. Assigning lambdas to names instead of using `def`.
3. Trying to put a loop or `if` **statement** inside a lambda (the ternary `if` *expression* is fine).
4. The loop-variable capture trap above.
5. Cramming three operations into one lambda and making it unreadable.

## 8.10 Practice

1. Write a lambda that returns `True` for leap years.
2. Sort `["apple", "Banana", "cherry"]` case-insensitively using a lambda.
3. Use a lambda with `sorted` to sort a list of dicts by two keys.
4. Write a lambda that reverses a string.
5. Fix this so it prints `[0, 10, 20]`:
   ```python
   fs = [lambda: i * 10 for i in range(3)]
   print([f() for f in fs])
   ```

---
---

# Chapter 9 — The `filter()` Function

## 9.1 The idea

`filter()` picks out the elements of an iterable that **pass a test**. Nothing more.

```
filter(function, iterable)
```

- `function` returns `True` or `False` for each item (called a **predicate**)
- Items where the function returns `True` are **kept**
- Items where it returns `False` are **dropped**
- Returns a lazy **filter object** — wrap in `list()` to see it

## 9.2 First example

```python
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def is_even(n):
    return n % 2 == 0

evens = filter(is_even, nums)
print(evens)              # <filter object at 0x7f...>
print(list(evens))        # [2, 4, 6, 8, 10]
```

With a lambda — how you'll normally write it:

```python
evens = list(filter(lambda n: n % 2 == 0, nums))
print(evens)              # [2, 4, 6, 8, 10]
```

## 9.3 The lazy-evaluation gotcha

A `filter` object is an **iterator**. It can only be consumed **once**.

```python
result = filter(lambda x: x > 3, [1, 2, 3, 4, 5])

print(list(result))      # [4, 5]
print(list(result))      # []   <- exhausted!
```

The first `list()` drained it. If you need the data more than once, store the list:

```python
result = list(filter(lambda x: x > 3, [1, 2, 3, 4, 5]))
print(result)     # [4, 5]
print(result)     # [4, 5]   fine now
```

Laziness is a *feature* — with a 10-million-row file, `filter` doesn't build a 10-million-item list in memory. It hands over one item at a time.

## 9.4 More examples

```python
# Positive numbers
nums = [-5, 3, -2, 8, 0, -7, 12]
print(list(filter(lambda n: n > 0, nums)))          # [3, 8, 12]

# Long words
words = ["hi", "python", "is", "wonderful", "ok"]
print(list(filter(lambda w: len(w) > 2, words)))    # ['python', 'wonderful']

# Words starting with a letter
names = ["Anita", "Ravi", "Amit", "Kiran", "Arjun"]
print(list(filter(lambda n: n.startswith("A"), names)))
# ['Anita', 'Amit', 'Arjun']

# Palindromes
words = ["madam", "python", "level", "code", "radar"]
print(list(filter(lambda w: w == w[::-1], words)))
# ['madam', 'level', 'radar']

# Divisible by 3 AND 5
nums = range(1, 101)
print(list(filter(lambda n: n % 15 == 0, nums)))
# [15, 30, 45, 60, 75, 90]
```

## 9.5 `filter(None, iterable)` — removing falsy values

Pass `None` as the function and Python keeps everything that is **truthy**.

```python
data = [0, 1, "", "hello", None, [], [1,2], False, True, 0.0, "0"]
print(list(filter(None, data)))
# [1, 'hello', [1, 2], True, '0']
```

Falsy values in Python: `0`, `0.0`, `""`, `[]`, `{}`, `()`, `set()`, `None`, `False`.

Note that the string `"0"` survives — it's a non-empty string, therefore truthy.

Practical use — cleaning up user input:

```python
raw = ["Anita", "", "Ravi", None, "Kiran", "  ", "Divya"]
clean = list(filter(None, (name.strip() if name else name for name in raw)))
print(clean)      # ['Anita', 'Ravi', 'Kiran', 'Divya']
```

## 9.6 Filtering dictionaries and objects

```python
students = [
    {"name": "Anita", "marks": 85, "city": "Pune"},
    {"name": "Ravi",  "marks": 45, "city": "Delhi"},
    {"name": "Kiran", "marks": 92, "city": "Pune"},
    {"name": "Divya", "marks": 38, "city": "Mumbai"},
]

passed = list(filter(lambda s: s["marks"] >= 50, students))
for s in passed:
    print(s["name"], s["marks"])
```
**Output:**
```
Anita 85
Kiran 92
```

Chaining filters:

```python
pune_toppers = filter(lambda s: s["marks"] >= 80,
                filter(lambda s: s["city"] == "Pune", students))
print([s["name"] for s in pune_toppers])    # ['Anita', 'Kiran']
```

Readable version — combine the conditions:

```python
result = list(filter(lambda s: s["city"] == "Pune" and s["marks"] >= 80, students))
```

## 9.7 A worked example: prime numbers

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

primes = list(filter(is_prime, range(1, 51)))
print(primes)
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

This is a case where a named `def` beats a lambda — the logic is too long for one expression.

## 9.8 `filter()` vs list comprehension

These are equivalent:

```python
nums = [1, 2, 3, 4, 5, 6]

a = list(filter(lambda n: n % 2 == 0, nums))
b = [n for n in nums if n % 2 == 0]

print(a == b)     # True
```

**Which should you use?**

| Situation | Preferred |
|-----------|-----------|
| Condition is a lambda | List comprehension — more readable |
| Condition is an existing named function | `filter(is_prime, nums)` reads beautifully |
| You also want to *transform* items | List comprehension (filter can't transform) |
| Huge/infinite data, memory matters | `filter` (lazy) or a generator expression |

Most experienced Python developers reach for comprehensions. Know `filter` anyway — it's in exams, in older codebases, and in functional-style code.

Comprehensions can filter *and* transform in one step, which `filter` alone cannot:

```python
nums = [1, 2, 3, 4, 5, 6]
print([n ** 2 for n in nums if n % 2 == 0])     # [4, 16, 36]

# The filter equivalent needs map too:
print(list(map(lambda n: n**2, filter(lambda n: n % 2 == 0, nums))))
```

The comprehension wins on readability there.

## 9.9 Mistakes I see every batch

1. Forgetting `list()` and printing `<filter object at 0x...>`.
2. Consuming the filter object twice and getting `[]` the second time.
3. Predicate returns a value instead of a boolean — `filter(lambda x: x*2, nums)` keeps everything except 0 (because non-zero is truthy). Probably not what you meant.
4. Expecting `filter` to modify the original list. It never does — it returns a new iterator.
5. Trying to transform inside `filter`. Filter selects; `map` transforms.

## 9.10 Practice

1. Filter all numbers divisible by 7 from 1 to 200.
2. From a list of emails, keep only those ending in `.com`.
3. Filter students who scored above the class average. (You'll need two passes.)
4. Remove all vowels from a string using `filter`.
5. From a list of mixed types, keep only the integers. (Hint: `isinstance`.)

---
---

# Chapter 10 — `map()` and `reduce()`

Together with `filter`, these three form the classic functional toolkit:

- **`map`** — transform every element (n items in → n items out)
- **`filter`** — select some elements (n items in → ≤ n items out)
- **`reduce`** — combine all elements into one value (n items in → 1 item out)

## 10.1 `map()` — transform everything

```
map(function, iterable, ...)
```

Applies `function` to every item and returns a lazy map object.

```python
nums = [1, 2, 3, 4, 5]

squares = list(map(lambda x: x ** 2, nums))
print(squares)      # [1, 4, 9, 16, 25]
```

The loop you replaced:

```python
squares = []
for x in nums:
    squares.append(x ** 2)
```

Four lines become one.

## 10.2 `map` with named and built-in functions

```python
nums = [1, 2, 3, 4]

def cube(x):
    return x ** 3

print(list(map(cube, nums)))              # [1, 8, 27, 64]

# Built-ins work directly — no lambda needed
strings = ["1", "2", "3", "42"]
print(list(map(int, strings)))            # [1, 2, 3, 42]
print(list(map(float, strings)))          # [1.0, 2.0, 3.0, 42.0]

names = ["anita", "ravi", "kiran"]
print(list(map(str.upper, names)))        # ['ANITA', 'RAVI', 'KIRAN']
print(list(map(str.capitalize, names)))   # ['Anita', 'Ravi', 'Kiran']
print(list(map(len, names)))              # [5, 4, 5]
```

The classic use — reading numbers from input:

```python
# user types: 10 20 30 40
numbers = list(map(int, input("Enter numbers: ").split()))
print(sum(numbers))
```

This one line is worth memorising. It's in half the competitive-programming solutions you'll ever read.

## 10.3 `map` with multiple iterables

`map` can take several iterables and feed one item from each into the function.

```python
a = [1, 2, 3, 4]
b = [10, 20, 30, 40]

print(list(map(lambda x, y: x + y, a, b)))     # [11, 22, 33, 44]
print(list(map(lambda x, y: x * y, a, b)))     # [10, 40, 90, 160]

# Three iterables
c = [100, 200, 300, 400]
print(list(map(lambda x, y, z: x + y + z, a, b, c)))
# [111, 222, 333, 444]
```

**If the lengths differ, `map` stops at the shortest:**

```python
print(list(map(lambda x, y: x + y, [1, 2, 3], [10, 20])))
# [11, 22]   -- the 3 is dropped
```

## 10.4 `map` on dictionaries and complex data

```python
students = [
    {"name": "Anita", "marks": 85},
    {"name": "Ravi",  "marks": 92},
    {"name": "Kiran", "marks": 78},
]

names = list(map(lambda s: s["name"], students))
print(names)      # ['Anita', 'Ravi', 'Kiran']

# Add a grade to each record
def add_grade(s):
    s = s.copy()
    s["grade"] = "A" if s["marks"] >= 85 else "B"
    return s

for s in map(add_grade, students):
    print(s)
```
**Output:**
```
{'name': 'Anita', 'marks': 85, 'grade': 'A'}
{'name': 'Ravi', 'marks': 92, 'grade': 'A'}
{'name': 'Kiran', 'marks': 78, 'grade': 'B'}
```

## 10.5 `map` is lazy too

```python
m = map(lambda x: x * 2, [1, 2, 3])
print(list(m))     # [2, 4, 6]
print(list(m))     # []   -- exhausted
```

Same rule as `filter`. Convert to a list if you need it twice.

## 10.6 `map` vs list comprehension

```python
nums = [1, 2, 3, 4, 5]

a = list(map(lambda x: x ** 2, nums))
b = [x ** 2 for x in nums]
```

Guidance:

- Existing function → `map(int, data)` is cleaner than `[int(x) for x in data]`
- Needs a lambda → the comprehension is usually clearer
- Filtering *and* transforming → comprehension, easily
- Multiple parallel iterables → `map` handles it naturally (comprehensions need `zip`)

## 10.7 `reduce()` — collapse a sequence to one value

`reduce` lives in `functools`, not in built-ins (Python 3 moved it there deliberately — Guido considered it hard to read).

```python
from functools import reduce

reduce(function, iterable[, initializer])
```

The function takes **two** arguments: the accumulated result so far, and the next item.

```python
from functools import reduce

nums = [1, 2, 3, 4, 5]

total = reduce(lambda a, b: a + b, nums)
print(total)     # 15
```

**How it works — step by step:**

| Step | a (accumulator) | b (next item) | Result |
|------|-----------------|---------------|--------|
| 1 | 1 | 2 | 3 |
| 2 | 3 | 3 | 6 |
| 3 | 6 | 4 | 10 |
| 4 | 10 | 5 | **15** |

It folds the list from the left, carrying the running result forward.

## 10.8 `reduce` examples

```python
from functools import reduce

nums = [1, 2, 3, 4, 5]

print(reduce(lambda a, b: a + b, nums))        # 15   sum
print(reduce(lambda a, b: a * b, nums))        # 120  product (= factorial of 5!)
print(reduce(lambda a, b: a if a > b else b, nums))   # 5   maximum
print(reduce(lambda a, b: a if a < b else b, nums))   # 1   minimum

words = ["Python", "is", "very", "powerful"]
print(reduce(lambda a, b: a + " " + b, words))
# Python is very powerful
```

### The `initializer` argument

```python
print(reduce(lambda a, b: a + b, [1, 2, 3], 100))     # 106  starts at 100
print(reduce(lambda a, b: a + b, [], 0))              # 0    safe on empty
print(reduce(lambda a, b: a + b, []))                 # TypeError!
```

**Always pass an initializer when the sequence might be empty.** Without it, `reduce` on an empty list raises `TypeError: reduce() of empty iterable with no initial value`.

### Flattening with reduce

```python
nested = [[1, 2], [3, 4], [5, 6]]
print(reduce(lambda a, b: a + b, nested))     # [1, 2, 3, 4, 5, 6]
```

### Counting with reduce

```python
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

def count(acc, word):
    acc[word] = acc.get(word, 0) + 1
    return acc

print(reduce(count, words, {}))
# {'apple': 3, 'banana': 2, 'cherry': 1}
```

## 10.9 When *not* to use reduce

For the common cases, Python already has better built-ins:

```python
from functools import reduce
nums = [1, 2, 3, 4, 5]

reduce(lambda a, b: a + b, nums)   # works, but...
sum(nums)                          # ...use this. Clearer and faster.

reduce(lambda a, b: a if a > b else b, nums)
max(nums)                          # use this

import math
math.prod(nums)                    # Python 3.8+ — for products
```

**Use `reduce` only when the combining operation is genuinely custom** and no built-in exists.

## 10.10 The three together — a complete pipeline

```python
from functools import reduce

sales = [
    {"product": "Laptop",   "price": 55000, "qty": 3, "region": "South"},
    {"product": "Mouse",    "price": 500,   "qty": 20, "region": "North"},
    {"product": "Monitor",  "price": 12000, "qty": 5, "region": "South"},
    {"product": "Keyboard", "price": 1500,  "qty": 12, "region": "South"},
    {"product": "Printer",  "price": 8000,  "qty": 2, "region": "North"},
]

# 1. FILTER: only South region
south = filter(lambda s: s["region"] == "South", sales)

# 2. MAP: compute revenue per item
revenues = map(lambda s: s["price"] * s["qty"], south)

# 3. REDUCE: total it up
total = reduce(lambda a, b: a + b, revenues, 0)

print(f"Total South revenue: Rs {total:,}")
# Total South revenue: Rs 243,000
```

The same thing, readably, in modern Python:

```python
total = sum(s["price"] * s["qty"] for s in sales if s["region"] == "South")
print(f"Total South revenue: Rs {total:,}")
```

I show you both deliberately. Know the functional version because exams and legacy code use it. Write the second version at work.

## 10.11 Summary table

| | `map` | `filter` | `reduce` |
|---|-------|----------|----------|
| Purpose | Transform | Select | Combine |
| Function returns | Any value | True/False | Combined value |
| Function takes | 1 arg (or n) | 1 arg | **2** args |
| Output size | Same as input | ≤ input | Single value |
| Returns | map object (lazy) | filter object (lazy) | The final value |
| Import needed | No | No | **Yes** — `from functools import reduce` |

## 10.12 Mistakes I see every batch

1. Forgetting to import `reduce`.
2. Writing a one-argument lambda for `reduce` — it needs **two**.
3. Forgetting `list()` around `map`/`filter`.
4. Calling `reduce` on a possibly-empty list without an initializer.
5. Using `reduce(lambda a,b: a+b, nums)` when `sum(nums)` exists.
6. Assuming `map` with unequal-length iterables pads — it truncates.

## 10.13 Practice

1. Convert `["3", "7", "11"]` to integers and find their sum using `map` and `reduce`.
2. Given a list of temperatures in Celsius, convert to Fahrenheit with `map`.
3. Find the longest word in a list using `reduce`.
4. Given `names` and `marks` as two parallel lists, use `map` to produce `["Anita: 85", ...]`.
5. Using only `map`, `filter`, and `reduce`, compute the sum of squares of all even numbers from 1 to 100.

---
---

# Chapter 11 — Inner Functions and Closures

## 11.1 What is an inner function?

A function defined **inside** another function. Also called a nested function.

```python
def outer():
    print("outer starts")

    def inner():                 # defined inside outer
        print("  inner running")

    inner()                      # called inside outer
    print("outer ends")

outer()
```
**Output:**
```
outer starts
  inner running
outer ends
```

The key fact: `inner` **does not exist** outside `outer`.

```python
inner()      # NameError: name 'inner' is not defined
```

Each time you call `outer()`, Python *re-creates* `inner` from scratch. The `def inner():` line is a statement that executes like any other.

## 11.2 Why bother?

Three good reasons.

### Reason 1 — Encapsulation (hiding a helper)

```python
def send_email(to, subject, body):

    def validate(address):
        return "@" in address and "." in address.split("@")[-1]

    def format_body(text):
        return text.strip().replace("\n\n", "\n")

    if not validate(to):
        return f"Invalid email: {to}"

    return f"To: {to}\nSubject: {subject}\n\n{format_body(body)}"

print(send_email("anita@example.com", "Hi", "  Hello there  "))
print(send_email("not-an-email", "Hi", "test"))
```
**Output:**
```
To: anita@example.com
Subject: Hi

Hello there
Invalid email: not-an-email
```

`validate` and `format_body` are implementation details of `send_email`. Nobody else needs them, so nobody else should see them. Your module's public surface stays small.

### Reason 2 — Access to the outer function's variables

The inner function can read the outer function's locals without them being passed in:

```python
def calculate_bill(items, tax_rate):

    def subtotal():
        return sum(price * qty for price, qty in items)    # sees 'items'

    def tax():
        return subtotal() * tax_rate                       # sees 'tax_rate'

    return subtotal() + tax()

cart = [(100, 2), (50, 3), (200, 1)]
print(calculate_bill(cart, 0.18))     # 649.0
```

### Reason 3 — Closures and decorators

Which is the rest of this chapter.

## 11.3 Closures — the important concept

A **closure** happens when an inner function is **returned** from the outer function, and it *remembers* the outer function's variables even after the outer function has finished executing.

```python
def multiplier(factor):
    def multiply(x):
        return x * factor        # 'factor' comes from the enclosing scope
    return multiply              # note: no parentheses — returning the function

double = multiplier(2)
triple = multiplier(3)

print(double(10))     # 20
print(triple(10))     # 30
```

Stop and appreciate what just happened.

`multiplier(2)` **finished running**. Its local variable `factor` should have been destroyed. But `double(10)` still knows `factor` is 2. The returned function carried its environment with it. That package — *function + captured environment* — is a **closure**.

`double` and `triple` are separate closures with separate captured values. They don't interfere.

### Three conditions for a closure

1. There is a nested function
2. The inner function refers to a variable from the enclosing scope
3. The outer function returns the inner function

## 11.4 Proving the closure exists

Python stores the captured values in a `__closure__` attribute:

```python
def multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = multiplier(2)

print(double.__closure__)                    # (<cell at 0x...: int object at 0x...>,)
print(double.__closure__[0].cell_contents)   # 2
print(double.__code__.co_freevars)           # ('factor',)
```

`co_freevars` lists the names the function captured from outside. A plain function has an empty tuple and `__closure__` is `None`:

```python
def plain(x):
    return x * 2

print(plain.__closure__)               # None
print(plain.__code__.co_freevars)      # ()
```

## 11.5 Closures with state — `nonlocal` in action

Closures can hold *mutable* state across calls:

```python
def make_counter():
    count = 0

    def counter():
        nonlocal count       # required to REASSIGN the enclosing variable
        count += 1
        return count

    return counter

c1 = make_counter()
c2 = make_counter()

print(c1(), c1(), c1())     # 1 2 3
print(c2(), c2())           # 1 2
print(c1())                 # 4  -- c1 kept its own count
```

`c1` and `c2` each have a private `count`. Neither can be touched from outside — there is no `c1.count`. This is data hiding without writing a class.

Remove `nonlocal` and you get `UnboundLocalError`, exactly as in Chapter 3.

> **Reading vs writing:** if you only *read* the enclosing variable, you don't need `nonlocal`. You need it only when you **reassign** it. This works without `nonlocal`:
> ```python
> def make_appender():
>     items = []
>     def append(x):
>         items.append(x)      # MUTATING, not reassigning
>         return items
>     return append
> ```

## 11.6 A practical closure — bank account

```python
def create_account(owner, balance=0):

    def deposit(amount):
        nonlocal balance
        if amount <= 0:
            return "Deposit must be positive"
        balance += amount
        return f"Deposited {amount}. Balance: {balance}"

    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return f"Insufficient funds. Balance: {balance}"
        balance -= amount
        return f"Withdrew {amount}. Balance: {balance}"

    def statement():
        return f"{owner}'s balance: {balance}"

    return deposit, withdraw, statement


dep, wit, stmt = create_account("Anita", 1000)

print(stmt())          # Anita's balance: 1000
print(dep(500))        # Deposited 500. Balance: 1500
print(wit(2000))       # Insufficient funds. Balance: 1500
print(wit(300))        # Withdrew 300. Balance: 1200
print(stmt())          # Anita's balance: 1200
```

`balance` cannot be reached or corrupted from outside. Only the three returned functions can touch it.

## 11.7 Closure vs Class

These two do the same job:

```python
# Closure version
def make_counter(start=0):
    count = start
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

# Class version
class Counter:
    def __init__(self, start=0):
        self.count = start
    def increment(self):
        self.count += 1
        return self.count
```

| | Closure | Class |
|---|---------|-------|
| Lines of code | Fewer | More |
| State access from outside | Impossible | `obj.count` |
| Number of behaviours | Best with 1–2 | Any number |
| Inheritance | No | Yes |
| Readability for beginners | Trickier | Familiar |

**Use a closure** for one small piece of behaviour with hidden state. **Use a class** when you have several related methods and shared data.

## 11.8 Common uses of closures

### Configurable validators

```python
def length_validator(min_len, max_len):
    def validate(text):
        if len(text) < min_len:
            return f"Too short (min {min_len})"
        if len(text) > max_len:
            return f"Too long (max {max_len})"
        return "Valid"
    return validate

username_check = length_validator(3, 15)
password_check = length_validator(8, 30)

print(username_check("ab"))              # Too short (min 3)
print(username_check("anita_sharma"))    # Valid
print(password_check("123"))             # Too short (min 8)
```

### Memoization by hand

```python
def memoize(func):
    cache = {}
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]
    return wrapper

def slow_square(n):
    print(f"  computing {n}^2...")
    return n * n

fast_square = memoize(slow_square)

print(fast_square(4))    # computing 4^2...  then 16
print(fast_square(4))    # 16   -- no computation, cache hit
print(fast_square(5))    # computing 5^2...  then 25
```

Look carefully at `memoize`. It takes a function and returns a function. **That is a decorator.** You've just written one without knowing it — which is exactly where the next chapter starts.

## 11.9 Mistakes I see every batch

1. `return inner()` instead of `return inner` — you return the *result*, not the function.
2. Forgetting `nonlocal` when reassigning an enclosing variable.
3. Using `global` when you meant `nonlocal`.
4. Calling the inner function from outside → `NameError`.
5. The late-binding loop trap:
   ```python
   funcs = [lambda: i for i in range(3)]
   print([f() for f in funcs])     # [2, 2, 2]
   funcs = [lambda i=i: i for i in range(3)]
   print([f() for f in funcs])     # [0, 1, 2]  -- fixed
   ```

## 11.10 Practice

1. Write `make_power(n)` returning a function that raises its argument to the power `n`.
2. Write a closure-based stack with `push`, `pop`, and `size` functions.
3. Write `make_averager()` that remembers all numbers given to it and returns the running average.
4. Write `once(func)` — a closure that lets `func` be called only once and returns the cached result afterwards.
5. Explain why this prints `[2, 2, 2]` and fix it:
   ```python
   handlers = []
   for i in range(3):
       handlers.append(lambda: print(i))
   for h in handlers: h()
   ```

---
---

# Chapter 12 — Decorators in Python

## 12.1 The problem decorators solve

Suppose you want to time three functions:

```python
import time

def fetch_data():
    start = time.time()
    time.sleep(0.1)
    result = "data"
    end = time.time()
    print(f"fetch_data took {end - start:.4f}s")
    return result

def process_data():
    start = time.time()
    time.sleep(0.2)
    result = "processed"
    end = time.time()
    print(f"process_data took {end - start:.4f}s")
    return result
```

The timing code is copy-pasted. Add ten more functions and you copy it ten more times. Change the format and you edit it in eleven places. The actual *work* of each function is buried in bookkeeping.

A **decorator** lets you write the timing logic once and attach it anywhere.

## 12.2 Definition

> A **decorator** is a function that takes another function as input, adds some behaviour around it, and returns a new function — **without modifying the original function's code**.

It is a higher order function (Ch. 7) built with an inner function and a closure (Ch. 11). If those chapters made sense, this one is easy.

## 12.3 Building one from scratch

### Step 1 — the raw idea, no syntax sugar

```python
def my_decorator(func):
    def wrapper():
        print("Before the function runs")
        func()
        print("After the function runs")
    return wrapper

def say_hello():
    print("Hello!")

say_hello = my_decorator(say_hello)     # wrap it manually
say_hello()
```
**Output:**
```
Before the function runs
Hello!
After the function runs
```

`say_hello` now points to `wrapper`. When you call it, `wrapper` runs the prints and calls the original `func` (which the closure remembered).

### Step 2 — the `@` syntax

```python
def my_decorator(func):
    def wrapper():
        print("Before the function runs")
        func()
        print("After the function runs")
    return wrapper

@my_decorator                # this line replaces  say_hello = my_decorator(say_hello)
def say_hello():
    print("Hello!")

say_hello()
```

Identical output. **`@my_decorator` is pure syntactic sugar** for `say_hello = my_decorator(say_hello)`. Nothing more. If you remember that one equation, decorators hold no mystery.

## 12.4 Handling arguments — `*args` and `**kwargs`

The version above breaks the moment the function takes arguments:

```python
@my_decorator
def greet(name):
    print(f"Hello, {name}!")

greet("Anita")
# TypeError: wrapper() takes 0 positional arguments but 1 was given
```

The fix: make `wrapper` accept anything and forward it.

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)     # forward everything
        print("After")
        return result                      # don't swallow the return value!
    return wrapper

@my_decorator
def add(a, b):
    print(f"  adding {a} + {b}")
    return a + b

print("Result:", add(3, 5))
```
**Output:**
```
Before
  adding 3 + 5
After
Result: 8
```

**Two rules for every decorator you write:**

1. `wrapper(*args, **kwargs)` — accept and forward all arguments
2. `return result` — pass the original return value back

Forget rule 2 and every decorated function silently returns `None`. This is the single most common decorator bug.

## 12.5 `functools.wraps` — preserving identity

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greets a person by name."""
    return f"Hello, {name}"

print(greet.__name__)     # wrapper       <- WRONG
print(greet.__doc__)      # None          <- WRONG
```

The original function's metadata is gone — because `greet` really *is* `wrapper` now. This breaks documentation tools, debuggers, and tracebacks.

**The fix:**

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)                          # copies __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greets a person by name."""
    return f"Hello, {name}"

print(greet.__name__)     # greet
print(greet.__doc__)      # Greets a person by name.
```

**Always use `@wraps(func)`.** Treat it as part of the decorator template, not an optional extra.

## 12.6 The decorator template — memorise this

```python
from functools import wraps

def decorator_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # code BEFORE the function runs
        result = func(*args, **kwargs)
        # code AFTER the function runs
        return result
    return wrapper
```

Every decorator you ever write is a variation of these eight lines.

## 12.7 Real-world decorators

### Timer

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMER] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

print(slow_sum(1_000_000))
```
**Output:**
```
[TIMER] slow_sum took 0.0201s
1783293664
```

Now compare this with the copy-pasted version at the start of the chapter. That is the payoff.

### Logger

```python
from functools import wraps

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_list = [repr(a) for a in args]
        arg_list += [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(arg_list)
        print(f"[LOG] Calling {func.__name__}({signature})")
        try:
            result = func(*args, **kwargs)
            print(f"[LOG] {func.__name__} returned {result!r}")
            return result
        except Exception as e:
            print(f"[LOG] {func.__name__} raised {type(e).__name__}: {e}")
            raise
    return wrapper

@logger
def divide(a, b):
    return a / b

divide(10, 2)
try:
    divide(10, 0)
except ZeroDivisionError:
    pass
```
**Output:**
```
[LOG] Calling divide(10, 2)
[LOG] divide returned 5.0
[LOG] Calling divide(10, 0)
[LOG] divide raised ZeroDivisionError: division by zero
```

### Caching / memoization

```python
from functools import wraps

def cache(func):
    stored = {}
    @wraps(func)
    def wrapper(*args):
        if args in stored:
            print(f"  (cache hit for {args})")
            return stored[args]
        result = func(*args)
        stored[args] = result
        return result
    wrapper.cache = stored          # expose the cache for inspection
    return wrapper

@cache
def fib(n):
    return n if n <= 1 else fib(n-1) + fib(n-2)

print(fib(30))          # instant instead of ~1 second
print(len(fib.cache), "values cached")
```

Python ships with a better version:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fib(n):
    return n if n <= 1 else fib(n-1) + fib(n-2)

print(fib(100))          # 354224848179261915075
print(fib.cache_info())  # CacheInfo(hits=98, misses=101, maxsize=128, currsize=101)
```

### Input validation

```python
from functools import wraps

def validate_positive(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for a in args:
            if isinstance(a, (int, float)) and a < 0:
                raise ValueError(f"{func.__name__} does not accept negative values: {a}")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def area(length, width):
    return length * width

print(area(5, 3))       # 15
try:
    area(-5, 3)
except ValueError as e:
    print("Error:", e)  # Error: area does not accept negative values: -5
```

### Retry on failure

```python
import time, random
from functools import wraps

def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for attempt in range(1, 4):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"  attempt {attempt} failed: {e}")
                if attempt == 3:
                    raise
                time.sleep(0.1)
    return wrapper

@retry
def unstable_api():
    if random.random() < 0.7:
        raise ConnectionError("network glitch")
    return "success!"
```

## 12.8 Decorators with arguments

What if you want `@repeat(3)`? You need **one more layer**: a function that returns a decorator.

```python
from functools import wraps

def repeat(times):                    # Layer 1: takes the ARGUMENT
    def decorator(func):              # Layer 2: takes the FUNCTION
        @wraps(func)
        def wrapper(*args, **kwargs): # Layer 3: takes the CALL arguments
            for i in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Anita")
```
**Output:**
```
Hello, Anita!
Hello, Anita!
Hello, Anita!
```

**What `@repeat(3)` really does:**

```python
greet = repeat(3)(greet)
#        ^^^^^^^^^  this call returns 'decorator'
#                  ^^^^^^^ then decorator(greet) returns 'wrapper'
```

Three layers, three jobs:

| Layer | Receives | Returns |
|-------|----------|---------|
| `repeat(times)` | the decorator's arguments | `decorator` |
| `decorator(func)` | the function being decorated | `wrapper` |
| `wrapper(*args)` | the runtime call arguments | the result |

Another example — a configurable logger:

```python
from functools import wraps

def log(level="INFO"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{level}] Entering {func.__name__}")
            result = func(*args, **kwargs)
            print(f"[{level}] Exiting {func.__name__}")
            return result
        return wrapper
    return decorator

@log("DEBUG")
def compute():
    return 42

@log()                      # note the parentheses — still required
def other():
    return 1

compute()
```
**Output:**
```
[DEBUG] Entering compute
[DEBUG] Exiting compute
```

> **Gotcha:** with a parameterised decorator you must write `@log()` even when using all defaults. `@log` without parentheses would pass the *function* as the `level` argument.

## 12.9 Stacking multiple decorators

```python
from functools import wraps

def bold(func):
    @wraps(func)
    def wrapper(*a, **k):
        return f"<b>{func(*a, **k)}</b>"
    return wrapper

def italic(func):
    @wraps(func)
    def wrapper(*a, **k):
        return f"<i>{func(*a, **k)}</i>"
    return wrapper

@bold
@italic
def text():
    return "Hello"

print(text())     # <b><i>Hello</i></b>
```

**Order matters.** Decorators apply **bottom-up**:

```python
text = bold(italic(text))
```

`italic` wraps first (inner), `bold` wraps second (outer). Swap the two lines:

```python
@italic
@bold
def text():
    return "Hello"

print(text())     # <i><b>Hello</b></i>
```

**Memory aid:** the decorator closest to the `def` is applied first and sits innermost.

## 12.10 Class-based decorators

A decorator only needs to be *callable*, so a class with `__call__` works too:

```python
from functools import wraps

class CountCalls:
    def __init__(self, func):
        wraps(func)(self)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call #{self.count} to {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hi():
    print("Hi!")

say_hi()
say_hi()
print("Total calls:", say_hi.count)
```
**Output:**
```
Call #1 to say_hi
Hi!
Call #2 to say_hi
Hi!
Total calls: 2
```

## 12.11 Built-in decorators you'll meet

```python
class Circle:
    PI = 3.14159

    def __init__(self, radius):
        self._radius = radius

    @property                     # access a method like an attribute
    def area(self):
        return Circle.PI * self._radius ** 2

    @staticmethod                 # no self, no cls — just a namespaced function
    def describe():
        return "A circle is a round shape."

    @classmethod                  # receives the class, not the instance
    def from_diameter(cls, d):
        return cls(d / 2)

c = Circle(5)
print(c.area)                     # 78.53975  -- no parentheses!
print(Circle.describe())          # A circle is a round shape.
c2 = Circle.from_diameter(10)
print(c2.area)                    # 78.53975
```

Others worth knowing: `@functools.lru_cache`, `@functools.cache` (3.9+), `@dataclasses.dataclass`, `@abc.abstractmethod`, `@functools.wraps`.

If you use Flask or FastAPI, `@app.route("/")` and `@app.get("/items")` are decorators too. Now you know exactly what they're doing.

## 12.12 Mistakes I see every batch

1. **Forgetting `return result`** in the wrapper → everything returns `None`. The #1 bug.
2. Forgetting `*args, **kwargs` → `TypeError` as soon as the function takes arguments.
3. Forgetting `@wraps(func)` → broken `__name__`, `__doc__`, and confusing tracebacks.
4. Writing `@log` instead of `@log()` for a parameterised decorator.
5. Getting the stacking order backwards.
6. `return func(...)` inside the decorator instead of `return wrapper` — you call the function immediately at decoration time instead of returning a wrapper.

## 12.13 Practice

1. Write `@uppercase` that converts a function's string return value to uppercase.
2. Write `@count_calls` (function-based, not class-based) that tracks how many times a function ran.
3. Write `@timeout_warning(seconds)` that prints a warning if a function takes longer than `seconds`.
4. Write `@require_login(user)` that only runs the function if `user["logged_in"]` is True.
5. Stack `@timer` and `@logger` on the same function. Does the order change the output? Explain why.

---
---

# Chapter 13 — Modules and Packages

## 13.1 Why modules exist

A single 5,000-line `.py` file is unnavigable. Modules let you split code into files organised by purpose — and reuse those files across projects.

- **Module** = one `.py` file
- **Package** = a folder containing modules (and possibly sub-packages)
- **Library / Framework** = a collection of packages, usually distributed via PyPI

## 13.2 Creating your own module

**File: `mathutils.py`**

```python
"""A small collection of maths helpers."""

PI = 3.14159
E  = 2.71828

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def factorial(n):
    if n < 0:
        raise ValueError("No factorial for negatives")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def circle_area(radius):
    return PI * radius ** 2

print("mathutils module loaded!")     # we'll use this to prove a point later
```

**File: `main.py`** (in the same folder)

```python
import mathutils

print(mathutils.add(5, 3))            # 8
print(mathutils.PI)                   # 3.14159
print(mathutils.circle_area(10))      # 314.159
print(mathutils.factorial(5))         # 120
```
**Output:**
```
mathutils module loaded!
8
3.14159
314.159
120
```

Note that `mathutils module loaded!` printed even though we didn't ask for it. **Importing a module executes every top-level statement in it.** Remember that — Chapter 14 is entirely about the consequences.

## 13.3 The six ways to import

```python
# 1. Import the whole module
import mathutils
print(mathutils.add(2, 3))

# 2. Import with an alias
import mathutils as mu
print(mu.add(2, 3))

# 3. Import specific names
from mathutils import add, PI
print(add(2, 3))          # no prefix needed
print(PI)

# 4. Import a name with an alias
from mathutils import factorial as fact
print(fact(5))

# 5. Import everything  (AVOID)
from mathutils import *
print(add(2, 3))

# 6. Conditional / delayed import
def heavy_task():
    import numpy as np      # imported only when this function runs
    return np.array([1,2,3])
```

**Why avoid `from module import *`?**

```python
from math import *
from mathutils import *

print(pi)    # which pi? math's 3.141592653589793 or ours?
```

Names collide silently, and a reader can't tell where any name came from. The only common exception is an interactive session or a module explicitly designed for it (like `tkinter`).

## 13.4 Where does Python look for modules?

```python
import sys
for path in sys.path:
    print(path)
```

Search order:

1. The directory of the script being run (or the current directory)
2. Directories in the `PYTHONPATH` environment variable
3. Installation-dependent defaults (the standard library)
4. `site-packages` (where `pip` installs things)

First match wins — which causes a classic beginner disaster:

> **Never name your file `random.py`, `math.py`, `string.py`, `json.py`, `email.py`, or `test.py`.** Your file will shadow the standard library module and things will break in bewildering ways. If you've done it, delete the file *and* the `__pycache__` folder.

## 13.5 Inspecting a module

```python
import mathutils

print(dir(mathutils))          # every name defined in it
print(mathutils.__name__)      # 'mathutils'
print(mathutils.__doc__)       # its docstring
print(mathutils.__file__)      # full path on disk

help(mathutils)                # formatted documentation
help(mathutils.factorial)      # documentation for one function
```

## 13.6 Controlling `import *` with `__all__`

```python
# inside mathutils.py
__all__ = ['add', 'subtract', 'PI']       # only these are exported by *

def add(a, b): return a + b
def subtract(a, b): return a - b
def _internal_helper(): pass              # leading _ = private by convention
PI = 3.14159
E = 2.71828
```

```python
from mathutils import *
print(add(1,2))     # works
print(E)            # NameError — not in __all__
```

Even without `__all__`, names starting with `_` are skipped by `import *`. That underscore is Python's convention for "internal, don't touch."

## 13.7 Packages

A **package** is a directory with an `__init__.py` file.

```
myproject/
│
├── main.py
│
└── mypackage/
    ├── __init__.py
    ├── mathutils.py
    ├── stringutils.py
    │
    └── advanced/
        ├── __init__.py
        └── statistics.py
```

**`mypackage/__init__.py`**
```python
"""My utility package."""
print("mypackage initialised")

__version__ = "1.0.0"

# Re-export for convenience so users can write: from mypackage import add
from .mathutils import add, subtract
```

**`mypackage/stringutils.py`**
```python
def reverse(s):
    return s[::-1]

def is_palindrome(s):
    clean = s.lower().replace(" ", "")
    return clean == clean[::-1]
```

**`mypackage/advanced/statistics.py`**
```python
def mean(nums):
    return sum(nums) / len(nums) if nums else 0

def median(nums):
    s = sorted(nums)
    n = len(s)
    mid = n // 2
    return s[mid] if n % 2 else (s[mid-1] + s[mid]) / 2
```

**`main.py`**
```python
import mypackage
from mypackage import stringutils
from mypackage.advanced.statistics import mean, median

print(mypackage.__version__)              # 1.0.0
print(mypackage.add(2, 3))                # 5  -- thanks to __init__.py
print(stringutils.is_palindrome("madam")) # True
print(mean([10, 20, 30, 40]))             # 25.0
print(median([10, 20, 30, 40]))           # 25.0
```

### What does `__init__.py` do?

1. Marks the directory as a package
2. Runs automatically when the package is first imported
3. Is the right place for package-level setup, `__version__`, and convenience re-exports

Since Python 3.3, a folder without `__init__.py` can still be imported (a "namespace package"), but **include it anyway** — it's explicit, it's expected, and it gives you a place for package initialisation.

### Absolute vs relative imports

```python
# Absolute — full path from the project root. PREFERRED.
from mypackage.mathutils import add
from mypackage.advanced.statistics import mean

# Relative — relative to the current module. Only inside packages.
from .mathutils import add           # same package
from ..mathutils import add          # parent package
from .advanced.statistics import mean
```

PEP 8 recommends absolute imports — they're unambiguous and don't break when files move. Relative imports are fine *inside* a package where the internal structure is stable.

## 13.8 Useful standard library modules

Python's "batteries included" philosophy means most things you need are already there.

```python
import math
print(math.sqrt(16), math.ceil(4.2), math.floor(4.8), math.pi)
print(math.gcd(48, 18), math.factorial(5), math.log(100, 10))

import random
print(random.randint(1, 100))
print(random.choice(["a", "b", "c"]))
print(random.sample(range(1, 50), 6))       # lottery numbers
nums = [1,2,3,4,5]; random.shuffle(nums); print(nums)

import datetime
now = datetime.datetime.now()
print(now.strftime("%d-%m-%Y %H:%M:%S"))
print(datetime.date.today() + datetime.timedelta(days=30))

import os
print(os.getcwd())
print(os.listdir("."))
print(os.path.exists("data.txt"))
print(os.path.join("folder", "sub", "file.txt"))

import sys
print(sys.version)
print(sys.platform)
print(sys.argv)                             # command-line arguments

import json
data = {"name": "Anita", "marks": [85, 92]}
text = json.dumps(data, indent=2)
print(text)
print(json.loads(text))

import re
print(re.findall(r'\d+', "Order 123 costs 456 rupees"))    # ['123', '456']
print(re.sub(r'\s+', ' ', "too    many     spaces"))

from collections import Counter, defaultdict
print(Counter("mississippi"))
print(Counter("mississippi").most_common(2))

import statistics
print(statistics.mean([1,2,3,4]), statistics.median([1,2,3,4]))
```

Others worth knowing: `itertools`, `functools`, `pathlib`, `csv`, `time`, `sqlite3`, `urllib`, `unittest`, `logging`, `argparse`.

## 13.9 Third-party packages and `pip`

```bash
pip install requests            # install
pip install pandas==2.0.3       # a specific version
pip install --upgrade requests  # upgrade
pip uninstall requests          # remove
pip list                        # what's installed
pip show requests               # details about one package
pip freeze > requirements.txt   # snapshot the environment
pip install -r requirements.txt # recreate it elsewhere
```

**Always use a virtual environment** so projects don't fight over versions:

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install requests
deactivate
```

Without this, every project shares one global site-packages, and sooner or later Project A needs `pandas 1.5` while Project B needs `pandas 2.1`. Virtual environments make that a non-issue.

## 13.10 `__pycache__` and `.pyc` files

The first time a module is imported, Python compiles it to bytecode and caches it in a `__pycache__` folder as a `.pyc` file. Later imports skip the compile step.

- It's automatic. Don't create or edit these files.
- Add `__pycache__/` to your `.gitignore`.
- If a module behaves strangely after edits, deleting `__pycache__` is a valid troubleshooting step.

## 13.11 Mistakes I see every batch

1. Naming a file the same as a standard library module (`random.py`, `math.py`).
2. `from module import *` causing invisible name collisions.
3. **Circular imports:** `a.py` imports `b.py`, which imports `a.py`. Fix by restructuring, or by moving the import inside the function that needs it.
4. Forgetting `__init__.py` and wondering why the package won't import.
5. Running a script from the wrong directory so Python can't find the module.
6. Installing packages globally instead of into a virtual environment.

## 13.12 Practice

1. Create a `calculator` package with `basic.py` (add, subtract, multiply, divide) and `scientific.py` (power, sqrt, log). Import and use both.
2. Write a `stringtools` module with at least five functions and a `__all__` list.
3. Use `os` and `datetime` to write a script that lists every `.py` file in a folder with its last-modified date.
4. Create a package with a sub-package two levels deep and import from the deepest module.
5. Set up a virtual environment, install `requests`, and freeze a `requirements.txt`.

---
---

# Chapter 14 — The Special Variable `__name__`

## 14.1 The one-line answer

`__name__` is a built-in variable that Python sets automatically in every module:

- If the file is **run directly**, `__name__` is set to the string `"__main__"`
- If the file is **imported** by another file, `__name__` is set to the **module's name**

That's the entire mechanism. Everything else follows from it.

## 14.2 See it yourself

**File: `demo.py`**
```python
print("The value of __name__ is:", __name__)
```

Run it directly:
```bash
$ python demo.py
The value of __name__ is: __main__
```

Import it from another file:
```python
# other.py
import demo
```
```bash
$ python other.py
The value of __name__ is: demo
```

Same file, two different values, depending on *how it was loaded*.

## 14.3 Why do we need this? The problem it solves

Remember from Chapter 13: **importing a module runs all of its top-level code.**

**File: `mathutils.py`**
```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# My quick tests while developing
print("Testing add:", add(5, 3))
print("Testing subtract:", subtract(5, 3))
```

Running it directly is fine:
```bash
$ python mathutils.py
Testing add: 8
Testing subtract: 2
```

But now someone imports it:

**File: `app.py`**
```python
import mathutils
print("App started")
print(mathutils.add(100, 200))
```
```bash
$ python app.py
Testing add: 8            <- unwanted noise from mathutils!
Testing subtract: 2       <- unwanted noise!
App started
300
```

The test output leaks into every program that imports the module. If the module contained `input()` or a database connection or a 30-second training loop, it would run every single time — during import.

## 14.4 The solution — the main guard

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

if __name__ == "__main__":
    print("Testing add:", add(5, 3))
    print("Testing subtract:", subtract(5, 3))
```

Now:

```bash
$ python mathutils.py
Testing add: 8
Testing subtract: 2

$ python app.py
App started
300                       <- clean!
```

Read the guard in plain English: **"Only run this block if this file is the one being executed directly, not when it's imported."**

## 14.5 The standard project layout

```python
"""
myscript.py — a well-structured Python script.
"""

# 1. Imports
import sys
import math

# 2. Constants
MAX_ATTEMPTS = 3
PI = math.pi

# 3. Class definitions
class Calculator:
    def add(self, a, b):
        return a + b

# 4. Function definitions
def process(data):
    return [x * 2 for x in data]

def main():
    """Entry point — all the 'doing' lives here."""
    print("Program starting...")
    calc = Calculator()
    print(calc.add(10, 5))
    print(process([1, 2, 3]))
    print("Program finished.")

# 5. The main guard, at the very bottom
if __name__ == "__main__":
    main()
```

Why wrap everything in a `main()` function rather than putting it directly in the guard?

- Everything inside `main()` is **local scope** — no accidental globals
- `main()` is testable: `from myscript import main`
- The structure is obvious to any reader
- Easy to add argument parsing or a return code later

Some people write `sys.exit(main())` so `main` can return an exit code. Both styles are common.

## 14.6 A complete two-file example

**File: `calculator.py`**
```python
"""Calculator module — usable as a library or standalone."""

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: division by zero"
    return a / b


def run_interactive():
    """Only used when this file is run directly."""
    print("=== Calculator ===")
    ops = {'1': ('Add', add), '2': ('Subtract', subtract),
           '3': ('Multiply', multiply), '4': ('Divide', divide)}
    for key, (name, _) in ops.items():
        print(f"{key}. {name}")

    choice = input("Choose (1-4): ")
    if choice not in ops:
        print("Invalid choice")
        return
    a = float(input("First number: "))
    b = float(input("Second number: "))
    name, func = ops[choice]
    print(f"{name} result: {func(a, b)}")


if __name__ == "__main__":
    run_interactive()
```

**File: `report.py`**
```python
"""Uses calculator as a library — no interactive prompts appear."""
from calculator import add, multiply

items = [(100, 3), (250, 2), (75, 4)]

total = 0
for price, qty in items:
    line = multiply(price, qty)
    total = add(total, line)
    print(f"{qty} x {price} = {line}")

print("Grand total:", total)
```

```bash
$ python calculator.py       # menu appears, waits for input
$ python report.py           # no menu — just the report
```

**One file, two roles.** This is the single most valuable habit in this chapter.

## 14.7 `__name__` in packages

```python
# mypackage/mathutils.py
print(__name__)
```
```python
import mypackage.mathutils
# prints: mypackage.mathutils     <- full dotted path
```

Running a module inside a package:
```bash
$ python -m mypackage.mathutils
__main__
```
The `-m` flag runs a module as a script — and `__name__` becomes `"__main__"` again.

## 14.8 Other dunder variables you'll see

`__name__` is one of several "dunder" (double-underscore) attributes Python maintains:

```python
import math

print(math.__name__)      # math
print(math.__doc__)       # module docstring
print(math.__file__)      # path to the .so / .py  (built-ins may lack this)
print(math.__package__)   # ''

# In your own file:
print(__name__)           # __main__
print(__file__)           # /path/to/yourfile.py
print(__doc__)            # your module's docstring
```

Functions have them too:

```python
def greet(name):
    """Say hello."""
    return f"Hi {name}"

print(greet.__name__)         # greet
print(greet.__doc__)          # Say hello.
print(greet.__defaults__)     # None
print(greet.__module__)       # __main__
```

Recall from Chapter 12 that `@functools.wraps` exists precisely to copy these across when a decorator wraps a function.

## 14.9 Testing the module both ways

```python
# temperature.py

def c_to_f(c):
    """Celsius to Fahrenheit."""
    return c * 9/5 + 32

def f_to_c(f):
    """Fahrenheit to Celsius."""
    return (f - 32) * 5/9


def _self_test():
    assert c_to_f(0) == 32
    assert c_to_f(100) == 212
    assert round(f_to_c(98.6), 1) == 37.0
    print("All self-tests passed ✔")


if __name__ == "__main__":
    _self_test()
    print("0°C  =", c_to_f(0), "°F")
    print("37°C =", c_to_f(37), "°F")
```

Run directly → tests run and results print. Import it → you just get two clean functions. This is exactly how well-written modules in the standard library are organised.

## 14.10 Mistakes I see every batch

1. Writing `if __name__ == "main":` — it needs the **double underscores**: `"__main__"`.
2. Writing `if __name__ = "__main__":` — one equals sign. `SyntaxError`.
3. Putting the guard at the top of the file, before the functions are defined → `NameError`.
4. Not using a guard at all, so importing a module triggers menus, downloads, or tests.
5. Assuming the guard is *required*. It isn't — Python runs fine without it. It's a discipline, not a rule.
6. Confusing `__name__` (the module's name) with `__file__` (the module's path).

## 14.11 Practice

1. Create two files and print `__name__` from both. Run each and explain the outputs.
2. Take any script you've already written and restructure it with `main()` plus a guard.
3. Write a module with self-tests that run only on direct execution.
4. Explain to a classmate, in your own words, why importing a module runs its top-level code.
5. Predict: what does `python -m mymodule` print for `__name__`, and why does it differ from `import mymodule`?

---
---

# Chapter 15 — Capstone Project

Everything from this book, in one program. Read it, type it, then extend it.

**File: `student_analytics.py`**

```python
"""
Student Analytics — a capstone using every concept in this course.

Concepts used:
  arrays, function arguments, scope, factorial, recursion, higher order
  functions, lambda, filter, map, reduce, inner functions, closures,
  decorators, modules, and __name__.
"""

import array as arr
import math
import time
from functools import reduce, wraps


# ---------------------------------------------------------------- CONSTANTS
PASS_MARK = 40          # module-level constants (Ch. 3)
GRADE_CUTOFFS = ((90, 'A+'), (80, 'A'), (70, 'B'), (60, 'C'), (40, 'D'))

_operation_count = 0    # a deliberate global, to demonstrate Ch. 3


# --------------------------------------------------------------- DECORATORS
def timer(func):                                          # Ch. 12
    """Report how long the function took."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"    [{func.__name__} ran in {(time.perf_counter()-start)*1000:.2f} ms]")
        return result
    return wrapper


def count_operations(func):                               # Ch. 12 + Ch. 3
    """Increment a module-level counter on every call."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        global _operation_count
        _operation_count += 1
        return func(*args, **kwargs)
    return wrapper


def validate_marks(func):                                 # Ch. 12
    """Reject marks outside 0-100."""
    @wraps(func)
    def wrapper(students, *args, **kwargs):
        for s in students:
            if not 0 <= s['marks'] <= 100:
                raise ValueError(f"{s['name']}: marks {s['marks']} out of range")
        return func(students, *args, **kwargs)
    return wrapper


# --------------------------------------------------------- RECURSIVE HELPERS
def factorial(n):                                         # Ch. 6
    """n! computed recursively."""
    if n < 0:
        raise ValueError("Factorial undefined for negatives")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def nCr(n, r):                                            # Ch. 4
    """Combinations, built on recursive factorial."""
    return factorial(n) // (factorial(r) * factorial(n - r))


def flatten(nested):                                      # Ch. 5
    """Flatten an arbitrarily nested list, recursively."""
    out = []
    for item in nested:
        out.extend(flatten(item)) if isinstance(item, list) else out.append(item)
    return out


# -------------------------------------------------------------- CLOSURES
def make_grader(cutoffs):                                 # Ch. 11
    """Return a grading function configured with these cutoffs."""
    def grade(marks):
        for threshold, letter in cutoffs:
            if marks >= threshold:
                return letter
        return 'F'
    return grade


def make_tracker():                                       # Ch. 11 + nonlocal
    """Closure holding private, mutable state."""
    processed = 0

    def track(n=1):
        nonlocal processed
        processed += n
        return processed

    return track


# -------------------------------------------------- HIGHER ORDER FUNCTIONS
def summarise(students, *metrics, **options):             # Ch. 2, Ch. 7
    """
    Apply any number of metric functions to the student list.

    *metrics  : functions taking the student list and returning a value
    **options : e.g. precision=2
    """
    precision = options.get('precision', 2)
    results = {}
    for metric in metrics:
        value = metric(students)
        results[metric.__name__] = round(value, precision) if isinstance(value, float) else value
    return results


@timer                                                     # decorators stack
@count_operations
@validate_marks
def analyse(students):                                     # Ch. 9, 10
    """The main analysis pipeline."""
    grade_of = make_grader(GRADE_CUTOFFS)
    track = make_tracker()

    # MAP — attach a grade to every student
    graded = list(map(lambda s: {**s, 'grade': grade_of(s['marks'])}, students))

    # FILTER — split into passed and failed
    passed = list(filter(lambda s: s['marks'] >= PASS_MARK, graded))
    failed = list(filter(lambda s: s['marks'] < PASS_MARK, graded))

    # REDUCE — total marks in one fold
    total = reduce(lambda acc, s: acc + s['marks'], graded, 0)

    for _ in graded:
        track()

    return {
        'graded': graded,
        'passed': passed,
        'failed': failed,
        'total': total,
        'average': total / len(graded) if graded else 0,
        'tracked': track(0),
    }


# ------------------------------------------------------------------ METRICS
def highest(students):
    return max(students, key=lambda s: s['marks'])['marks']

def lowest(students):
    return min(students, key=lambda s: s['marks'])['marks']

def average(students):
    return sum(map(lambda s: s['marks'], students)) / len(students)

def pass_percentage(students):
    return len(list(filter(lambda s: s['marks'] >= PASS_MARK, students))) / len(students) * 100


# --------------------------------------------------------------------- MAIN
def main():                                                # Ch. 14
    students = [
        {'name': 'Anita',  'marks': 92, 'city': 'Pune'},
        {'name': 'Ravi',   'marks': 78, 'city': 'Delhi'},
        {'name': 'Kiran',  'marks': 35, 'city': 'Pune'},
        {'name': 'Divya',  'marks': 88, 'city': 'Mumbai'},
        {'name': 'Suresh', 'marks': 61, 'city': 'Delhi'},
        {'name': 'Meera',  'marks': 29, 'city': 'Pune'},
    ]

    print("=" * 56)
    print(" STUDENT ANALYTICS REPORT".center(56))
    print("=" * 56)

    report = analyse(students)

    # --- Array module (Ch. 1) -----------------------------------------
    marks_array = arr.array('i', [s['marks'] for s in students])
    print(f"\nMarks array   : {marks_array}")
    print(f"Type / size   : '{marks_array.typecode}', {marks_array.itemsize} bytes each")
    print(f"Memory used   : {marks_array.itemsize * len(marks_array)} bytes")

    # --- Graded roster -------------------------------------------------
    print(f"\n{'Name':<10}{'City':<10}{'Marks':>6}  Grade  Status")
    print("-" * 46)
    for s in sorted(report['graded'], key=lambda s: -s['marks']):    # Ch. 7, 8
        status = "PASS" if s['marks'] >= PASS_MARK else "FAIL"
        print(f"{s['name']:<10}{s['city']:<10}{s['marks']:>6}  {s['grade']:^5}  {status}")

    # --- Metrics via a higher order function ---------------------------
    stats = summarise(students, highest, lowest, average, pass_percentage, precision=1)
    print("\nMetrics:")
    for name, value in stats.items():
        print(f"  {name.replace('_',' ').title():<18}: {value}")

    print(f"\n  Total marks       : {report['total']}")
    print(f"  Class average     : {report['average']:.2f}")
    print(f"  Passed / Failed   : {len(report['passed'])} / {len(report['failed'])}")
    print(f"  Students tracked  : {report['tracked']}  (via closure)")

    # --- Recursion showcase --------------------------------------------
    n = len(students)
    print(f"\nRecursion:")
    print(f"  {n}! = {factorial(n)}")
    print(f"  Ways to pick a 3-member team from {n}: {nCr(n, 3)}")
    print(f"  math.comb cross-check: {math.comb(n, 3)}")
    print(f"  flatten([1,[2,[3,[4]]],5]) = {flatten([1,[2,[3,[4]]],5]])}")

    # --- City grouping with reduce -------------------------------------
    def group_by_city(acc, s):
        acc.setdefault(s['city'], []).append(s['name'])
        return acc

    by_city = reduce(group_by_city, students, {})
    print("\nBy city:")
    for city, names in sorted(by_city.items()):
        print(f"  {city:<8}: {', '.join(names)}")

    print(f"\nDecorated operations run: {_operation_count}")
    print("=" * 56)


if __name__ == "__main__":                                 # Ch. 14
    main()
```

> **One deliberate typo:** the `flatten` line above has an extra `]`. Find it, fix it, and run the program. Debugging someone else's code is the skill that actually pays.

### Extensions to try

1. Add a `@retry` decorator around a function that reads marks from a file.
2. Replace the closure-based grader with a class and compare the code.
3. Add `@lru_cache` to `factorial` and measure the difference for repeated calls.
4. Split the file into a package: `analytics/decorators.py`, `analytics/metrics.py`, `analytics/core.py`.
5. Add a `--csv` command-line flag using `sys.argv` that outputs the roster as CSV.

---
---

# Cheat Sheet

```python
# ---------- ARRAYS -------------------------------------------------------
import array as arr
a = arr.array('i', [1,2,3])
a.append(4); a.insert(0,0); a.extend([5,6])
a.remove(3)        # by VALUE
a.pop(1)           # by INDEX, returns it
a.index(2); a.count(2); a.reverse(); a.tolist(); a.buffer_info()
a.typecode; a.itemsize          # attributes, no ()

# ---------- ARGUMENTS ----------------------------------------------------
def f(pos, default=1, *args, kw_only, **kwargs): ...
f(*a_list, **a_dict)            # unpacking at the call site
# ORDER: positional -> default -> *args -> keyword-only -> **kwargs
# NEVER: def f(x=[])            # mutable default trap -> use x=None

# ---------- SCOPE --------------------------------------------------------
# LEGB: Local -> Enclosing -> Global -> Built-in
global x        # rebind a module-level variable
nonlocal x      # rebind an ENCLOSING FUNCTION's variable

# ---------- FACTORIAL ----------------------------------------------------
math.factorial(n)                                       # use this
def f(n): return 1 if n <= 1 else n * f(n-1)            # recursive
def f(n):                                               # iterative
    r = 1
    for i in range(2, n+1): r *= i
    return r

# ---------- RECURSION ----------------------------------------------------
def rec(n):
    if base_condition: return base_value    # MANDATORY
    return rec(smaller_n)                   # must APPROACH the base
sys.getrecursionlimit()   # 1000 by default

# ---------- HIGHER ORDER FUNCTIONS ---------------------------------------
def hof(func): return func(10)          # takes a function
def factory(n):                         # returns a function
    def inner(x): return x * n
    return inner
sorted(data, key=lambda d: d['k'])
max(data, key=len)
functools.partial(func, arg=value)

# ---------- LAMBDA -------------------------------------------------------
lambda x: x * 2                     # single EXPRESSION only, implicit return
lambda a, b=2, *args: a + b
lambda x: "big" if x > 10 else "small"
# Trap: [lambda: i for i in range(3)]  -> all give 2
#  Fix: [lambda i=i: i for i in range(3)]

# ---------- MAP / FILTER / REDUCE ----------------------------------------
list(map(func, it))                 # transform     n -> n
list(filter(pred, it))              # select        n -> <= n
reduce(func2, it, init)             # combine       n -> 1
from functools import reduce        # reduce needs an import!
list(filter(None, it))              # drop falsy values
# map/filter are LAZY -> consumable once

# ---------- CLOSURES -----------------------------------------------------
def outer(x):
    def inner(y): return x + y      # captures x
    return inner                    # no () !
f.__closure__[0].cell_contents

# ---------- DECORATORS ---------------------------------------------------
from functools import wraps
def deco(func):
    @wraps(func)                            # ALWAYS
    def wrapper(*args, **kwargs):           # ALWAYS
        result = func(*args, **kwargs)
        return result                       # ALWAYS
    return wrapper

@deco                     #  ==  f = deco(f)
def f(): ...

def deco_with_args(param):        # 3 layers for parameterised decorators
    def deco(func):
        @wraps(func)
        def wrapper(*a, **k): return func(*a, **k)
        return wrapper
    return deco
@deco_with_args(5)        #  ==  f = deco_with_args(5)(f)

# stacking: bottom-up. @a @b def f  ==  f = a(b(f))

# ---------- MODULES & PACKAGES -------------------------------------------
import module
import module as m
from module import name, other
from module import name as alias
from module import *          # avoid
__all__ = ['public_name']     # controls what * exports
# package = folder + __init__.py
from .sibling import thing    # relative
from pkg.sub.mod import thing # absolute (preferred)

# ---------- __name__ -----------------------------------------------------
if __name__ == "__main__":    # DOUBLE underscores, DOUBLE equals
    main()
# run directly  -> "__main__"
# imported      -> "modulename"
```

---

# Interview Questions

**Arrays**
1. Difference between a list, an `array.array`, and a NumPy array?
2. Why does `array` require a typecode?
3. Difference between `remove()` and `pop()`?

**Arguments**
4. Difference between `*args` and `**kwargs`?
5. Why is a mutable default argument dangerous? Show the fix.
6. Is Python pass-by-value or pass-by-reference? Justify with an example.
7. What's the legal order of parameters in a function definition?

**Scope**
8. Explain the LEGB rule.
9. `global` vs `nonlocal`?
10. Why does this raise `UnboundLocalError`?
    ```python
    x = 1
    def f():
        print(x)
        x = 2
    ```

**Recursion**
11. What are the two mandatory parts of a recursive function?
12. Why is naive recursive Fibonacci slow, and how do you fix it?
13. Recursion vs iteration — memory and speed trade-offs?
14. What is Python's default recursion limit and why does it exist?

**Functional**
15. What makes a function "higher order"?
16. When is a lambda appropriate and when is it bad style?
17. `map` vs list comprehension?
18. Why was `reduce` moved out of built-ins in Python 3?
19. Why can you only iterate a `filter` object once?

**Closures & Decorators**
20. Define a closure. What are its three requirements?
21. What does `@decorator` actually translate to?
22. Why is `functools.wraps` necessary?
23. Explain the three layers of a decorator that takes arguments.
24. With `@a` above `@b`, which wraps first?
25. Closure vs class — when would you pick each?

**Modules**
26. Module vs package vs library?
27. What is `__init__.py` for?
28. Absolute vs relative imports?
29. What happens if you name your file `random.py`?
30. Explain `__name__ == "__main__"` to someone who has never seen it.

---

*Type every example. Break every example. Fix every break. That's the course.*
