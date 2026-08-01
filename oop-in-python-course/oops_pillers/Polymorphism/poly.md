# Polymorphism in Python
## Pillar 3 of Object-Oriented Programming

---

## The word itself

```
   POLY     =   Many
   MORPH    =   Forms
   ─────────────────────────────
   POLYMORPHISM = Many Forms
```

> 📖 **Definition**
> **Polymorphism means "one interface, many implementations."**
> A single operation behaves differently depending on the object it is working with.

You write **one** name. Python decides **at run time** which actual code to execute, based on what it is given.

---

## The three types

```
                    POLYMORPHISM
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
   1. DUCK TYPING   2. OPERATOR      3. METHOD
                       OVERLOADING      OVERRIDING

   same method       same operator     child changes
   name in           behaves           the parent's
   unrelated         differently       method
   classes

   work()            +  >  ==  len()   sound()
   no inheritance    magic methods     needs inheritance
```

We take them one at a time.

---
---

# 1. Duck Typing
### *Behaviour-based polymorphism*

## First Principle

Suppose you hire people to teach coding.

Do you care whether the person is a…

- Student
- Employee
- Freelancer
- Professor

> 🛑 **Think about it before reading on.**

**No.**

You only care whether **they can teach**.

**Python thinks exactly like this.** It doesn't ask:

> *"Who are you?"*

Instead it asks:

> *"Can you do the work?"*

**That is Duck Typing.**

> The name comes from the old saying:
> *"If it walks like a duck and quacks like a duck, then it is a duck."*
> Python never checks the type. It checks whether the **method exists**.

---

## Example

```python
# ============================================================
#  DUCK TYPING — three unrelated classes
# ============================================================

class Student:
    def work(self):
        print("Student is coding")


class Employee:
    def work(self):
        print("Employee is coding")


class Robot:
    def work(self):
        print("Robot is coding")


# ------------------------------------------------------------------
# This function does NOT say what type `person` must be.
# It only assumes ONE thing: that the object has a .work() method.
#
# Python does not check the type before calling. It simply looks up
# `work` on whatever object arrives and calls it.
# ------------------------------------------------------------------
def coding(person):
    person.work()


coding(Student())
coding(Employee())
coding(Robot())
```

### Output

```
Student is coding
Employee is coding
Robot is coding
```

---

## What just happened?

> 🛑 **Look carefully at the three classes. What do they have in common?**

```
   class Student:      class Employee:      class Robot:
       def work()          def work()           def work()

   ✗ no common parent
   ✗ no inheritance
   ✗ no interface
   ✓ they all have work()
```

**None of these classes are related.** There is no parent class, no inheritance, nothing connecting them.

**Python only checks whether the object has a `work()` method.** That is the entire requirement.

> 💡 **KEY IDEA**
> **Duck typing cares about behaviour, not identity.**
> The question is never *"what type is this?"* — it is *"can it do what I need?"*

---

## Analogy — the charging cable

Imagine a **Type-C charging cable**.

If a phone has a Type-C port, **it can charge**.

You don't care whether it is:

- Samsung
- OnePlus
- Google Pixel

You only care that it **accepts Type-C**.

```
   ┌──────────┐   ┌──────────┐   ┌──────────┐
   │ Samsung  │   │ OnePlus  │   │  Pixel   │
   │  [ C ]   │   │  [ C ]   │   │  [ C ]   │
   └────┬─────┘   └────┬─────┘   └────┬─────┘
        └──────────────┼──────────────┘
                       │
                  ─────┴─────
                  Type-C cable        one cable, many phones
```

**That is Duck Typing.**

---

## ⚠️ What if it *can't* do the work?

```python
class Chair:
    def sit(self):
        print("sitting")


coding(Chair())        # a Chair has no work() method
```

### Output

```
AttributeError: 'Chair' object has no attribute 'work'
```

> 💡 Python does not check in advance. It **tries**, and fails at the moment of the call.
>
> This is the trade-off: **flexibility now, error later.** Java would refuse to compile; Python runs happily until the exact line where the missing method is needed.

---

## ✓ Summary — Duck Typing

| | |
|:--|:--|
| **Based on** | behaviour — does the method exist? |
| **Inheritance needed?** | ❌ No |
| **Checked when?** | at run time, at the moment of the call |
| **Failure looks like** | `AttributeError` |
| **Our example** | `work()` |

---
---

# 2. Operator Overloading
### *Same operator, different behaviour*

## Ask the class first

> 🛑 **What does `+` actually mean?**

```python
5 + 7                 # → 12
```

means **addition**.

But…

```python
"Hello" + "World"     # → HelloWorld
```

means **concatenation**.

And…

```python
[1, 2] + [3, 4]       # → [1, 2, 3, 4]
```

means **merge lists**.

```
   ┌─────────────────────────────────────────────────┐
   │   SAME OPERATOR  +                              │
   ├─────────────────────────────────────────────────┤
   │   5 + 7            →  12          addition      │
   │   "Hi" + "There"   →  HiThere     concatenation │
   │   [1,2] + [3,4]    →  [1,2,3,4]   merging       │
   └─────────────────────────────────────────────────┘
```

**Same operator. Different behaviour.**

> 💡 **That is Polymorphism** — and you have been using it since your very first Python program.

---

## First Principle

> **Every operator is actually a method.**

```
   a + b
     │
     ▼
   a.__add__(b)
```

The operator is just **friendlier syntax** for a method call. Python translates it for you.

---

## Example — proving it

```python
# ============================================================
#  EVERY OPERATOR IS A METHOD
# ============================================================

a = 5
b = 7

print(a + b)                # the normal way
print(a.__add__(b))         # what Python actually calls
print(int.__add__(a, b))    # unrolled completely — the class, then both operands
```

### Output

```
12
12
12
```

**All three produce `12`**, because all three are the same thing written at different levels of detail.

---

## Another example

```python
print(str(100))
```

is actually:

```python
x = 100
print(x.__str__())
```

> ⚠️ **A syntax trap worth showing your class.** This looks like it should work but does not:
>
> ```python
> print(100.__str__())      # SyntaxError: invalid decimal literal
> ```
>
> **Why?** Python reads `100.` as the beginning of a **float** (like `100.5`), then hits `__str__` and gives up.
>
> Two ways to fix it — add brackets, or use a variable:
>
> ```python
> print((100).__str__())    # ✅ 100
>
> x = 100
> print(x.__str__())        # ✅ 100
> ```

---

## The Account example

Now let's make **our own** class respond to an operator.

```python
# ============================================================
#  OPERATOR OVERLOADING — teaching `>` to work on Accounts
# ============================================================

class Account:

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    # ------------------------------------------------------------------
    # __str__ is called by print() and str().
    # Without it, print(user1) would show <__main__.Account object at 0x...>
    # ------------------------------------------------------------------
    def __str__(self):
        return f"{self.name} : {self.balance}"

    # ------------------------------------------------------------------
    # __gt__  =  "greater than"  =  the  >  operator
    #
    # self  -> the object on the LEFT of >
    # other -> the object on the RIGHT of >
    #
    # We decide what "greater" MEANS for an Account:
    # here, the one with the bigger balance.
    # ------------------------------------------------------------------
    def __gt__(self, other):
        return self.balance > other.balance


user1 = Account("Ashok", 500)
user2 = Account("Ram", 300)

print(user1)

if user1 > user2:
    print(user1.name, "will pay")
else:
    print(user2.name, "will pay")
```

### Output

```
Ashok : 500
Ashok will pay
```

---

## What just happened?

> 🛑 **`>` normally only works on numbers. So why did it work on two Account objects?**

Because `>` is not built into the numbers — it is a **method lookup**.

When Python sees `user1 > user2`, it calls `user1.__gt__(user2)`. You defined that method, so it runs your code.

### Internal working

```
   user1 > user2
        │
        ▼
   user1.__gt__(user2)
        │
        ▼
   500 > 300
        │
        ▼
   True
```

> 💡 **KEY IDEA**
> **You are not changing what `>` means for numbers.**
> **You are teaching your own class how to respond when `>` is used on it.**

---

## 🎁 A bonus that surprises everyone

You only wrote `__gt__`. Try the opposite operator:

```python
print(user1 < user2)      # False  — and it works!
```

> 🛑 **We never defined `__lt__`. Why does `<` work?**

Because Python **reflects** the comparison. When it sees `user1 < user2`:

1. It tries `user1.__lt__(user2)` → not defined
2. So it flips the question and tries `user2.__gt__(user1)` → **that exists!**
3. `300 > 500` → `False`

```
   user1 < user2
        │
        ├── try  user1.__lt__(user2)   ✗ not defined
        │
        └── flip: user2.__gt__(user1)  ✓ 300 > 500 → False
```

> 💡 One method, two operators. Python fills in the mirror image for free.

But note this **does not** happen for `==`:

```python
print(user1 == user2)     # False
```

That `False` is not comparing balances — it is Python's **default `__eq__`**, which compares *identity* (are these the same object?). If you want `==` to compare balances, you must define `__eq__` yourself.

---

## Common magic methods

| Operator | Magic method |
|:--|:--|
| `+` | `__add__` |
| `-` | `__sub__` |
| `*` | `__mul__` |
| `/` | `__truediv__` |
| `>` | `__gt__` |
| `<` | `__lt__` |
| `==` | `__eq__` |
| `>=` | `__ge__` |
| `<=` | `__le__` |
| `str()` | `__str__` |
| `len()` | `__len__` |

> These are called **magic methods** or **dunder methods** (double underscore). You have already met two of them: **`__init__`** (called when you create an object) and **`__str__`** (called when you print one).

---

## Putting several together

```python
# ============================================================
#  A shopping cart that responds to len(), + and ==
# ============================================================

class Cart:

    def __init__(self, items):
        self.items = items

    # len(cart)  →  __len__
    def __len__(self):
        return len(self.items)

    # cart1 + cart2  →  __add__   (returns a NEW Cart)
    def __add__(self, other):
        return Cart(self.items + other.items)

    # cart1 == cart2  →  __eq__   (compares contents, not identity)
    def __eq__(self, other):
        return self.items == other.items


c1 = Cart(["pen", "book"])
c2 = Cart(["bag"])

print(len(c1))                       # 2
print((c1 + c2).items)               # ['pen', 'book', 'bag']
print(c1 == Cart(["pen", "book"]))   # True
```

### Output

```
2
['pen', 'book', 'bag']
True
```

Three built-in operations — `len()`, `+`, `==` — now work on a class **you** wrote.

---

## ✓ Summary — Operator Overloading

| | |
|:--|:--|
| **Based on** | magic (dunder) methods |
| **Inheritance needed?** | ❌ No |
| **Core idea** | every operator is a method call in disguise |
| **`a + b` becomes** | `a.__add__(b)` |
| **Our example** | `+`, `>`, `==`, `len()` |

---
---

# 3. Method Overriding
### *Child changes the parent's method*

## First Principle

Suppose a **parent class** already has a method.

The **child** wants a different implementation.

> **That is Method Overriding.**

```
        ┌──────────────────┐
        │     Animal       │       parent defines sound()
        │   sound()        │
        └────────┬─────────┘
                 │  inherits
        ┌────────┴────────┐
        ▼                 ▼
   ┌─────────┐       ┌─────────┐
   │   Dog   │       │   Cat   │     each REPLACES it
   │ sound() │       │ sound() │
   └─────────┘       └─────────┘
```

---

## Example

```python
# ============================================================
#  METHOD OVERRIDING
# ============================================================

class Animal:
    def sound(self):
        print("Animal Sound")


# ------------------------------------------------------------------
# class Dog(Animal)  means "Dog inherits from Animal".
# Dog gets everything Animal has — but here we REDEFINE sound(),
# so Dog's version REPLACES the parent's version.
#
# Note: Python needs no @Override annotation. Just redefine it.
# ------------------------------------------------------------------
class Dog(Animal):
    def sound(self):
        print("Bark")


class Cat(Animal):
    def sound(self):
        print("Meow")


Dog().sound()
Cat().sound()
```

### Output

```
Bark
Meow
```

**The parent method is replaced.**

---

## Another example — payments

```python
# ============================================================
#  THE REAL-WORLD VERSION
# ============================================================

class Payment:
    def pay(self):
        print("Generic Payment")


class PhonePe(Payment):
    def pay(self):
        print("Paid using PhonePe")


class GooglePay(Payment):
    def pay(self):
        print("Paid using Google Pay")


# ------------------------------------------------------------------
# THIS LOOP IS THE WHOLE POINT OF POLYMORPHISM.
#
# We call payment.pay() without ever checking what type it is.
# Python decides at RUN TIME which pay() to execute, based on the
# actual object in the list.
# ------------------------------------------------------------------
payments = [
    PhonePe(),
    GooglePay()
]

for payment in payments:
    payment.pay()
```

### Output

```
Paid using PhonePe
Paid using Google Pay
```

**Same method. Different implementation.**

---

## What just happened?

> 🛑 **Notice what the loop does NOT contain.**

```python
for payment in payments:
    payment.pay()
```

There is no `if`. No type checking. No `isinstance()`. The loop does not know or care which payment app it is holding.

Compare with life **without** polymorphism:

```python
# ❌ the version you never want to write
for payment in payments:
    if isinstance(payment, PhonePe):
        print("Paid using PhonePe")
    elif isinstance(payment, GooglePay):
        print("Paid using Google Pay")
    elif isinstance(payment, Paytm):
        print("Paid using Paytm")
    # ... and you edit this every time a new payment app is added
```

> 💡 **KEY IDEA**
> **Polymorphism replaces a chain of `if / elif` with a single method call.**
>
> Add `Paytm(Payment)` tomorrow and the loop **does not change by one character**. That is the real prize.

---

## Runtime polymorphism — proving it

The decision is made **when the code runs**, not when it is written:

```python
payments = [PhonePe(), GooglePay(), Payment()]

for p in payments:
    print(type(p).__name__, "->", end=" ")
    p.pay()
```

### Output

```
PhonePe -> Paid using PhonePe
GooglePay -> Paid using Google Pay
Payment -> Generic Payment
```

The **same line** `p.pay()` executed **three different methods**. Python looked at the actual object each time.

> This is why method overriding is called **runtime polymorphism**.

---

## 🎁 Extending instead of replacing — `super()`

Sometimes the child does not want to *replace* the parent's work — it wants to **add to it**.

```python
class Payment:
    def pay(self, amount):
        print(f"Processing {amount}")           # common work: logging, validation


class PhonePe(Payment):
    def pay(self, amount):
        super().pay(amount)                     # 1. run the PARENT's version first
        print(f"Paid {amount} using PhonePe")   # 2. then add our own step


PhonePe().pay(500)
```

### Output

```
Processing 500
Paid 500 using PhonePe
```

> 💡 `super()` gives you the parent's version. Use it when every payment needs the same validation or logging before its own specific step — so that common code lives in **one place**.

---

## ✓ Summary — Method Overriding

| | |
|:--|:--|
| **Based on** | inheritance |
| **Inheritance needed?** | ✅ **Yes** |
| **Decided when?** | at run time, from the actual object |
| **Also called** | runtime polymorphism |
| **Extend the parent** | `super().method()` |
| **Our example** | `sound()`, `pay()` |

---
---

# Final Comparison

| | **Duck Typing** | **Operator Overloading** | **Method Overriding** |
|:--|:--|:--|:--|
| **Core idea** | Same method name in **unrelated** classes | Same operator behaves differently | Child changes the parent's method |
| **Inheritance** | ❌ Not required | ❌ Not required | ✅ **Required** |
| **Mechanism** | Behaviour matters, not type | Operators become methods | Runtime polymorphism |
| **Question asked** | *"Can you do the work?"* | *"What does `+` mean here?"* | *"Which version should run?"* |
| **Example** | `work()` | `+`, `>`, `==`, `len()` | `sound()`, `pay()` |
| **Fails with** | `AttributeError` | `TypeError` | *(no failure — parent runs)* |

---

## One picture for the whole topic

```
   POLYMORPHISM  =  one name, many behaviours

   ┌────────────────────────────────────────────────────────┐
   │                                                        │
   │   person.work()      same NAME, unrelated classes      │
   │        ↓                     DUCK TYPING               │
   │                                                        │
   │   a + b              same OPERATOR, different types    │
   │        ↓                  OPERATOR OVERLOADING         │
   │        a.__add__(b)                                    │
   │                                                        │
   │   payment.pay()      same METHOD, child's version      │
   │        ↓                   METHOD OVERRIDING           │
   │                                                        │
   └────────────────────────────────────────────────────────┘
```

---

# ✓ Key Takeaways

- **Poly** = many, **morph** = forms → **one interface, many implementations**
- **Duck Typing** — Python asks *"can you do the work?"*, never *"who are you?"*. No inheritance needed.
- **Operator Overloading** — every operator is a method. `a + b` **is** `a.__add__(b)`.
- **Method Overriding** — the child redefines the parent's method; Python picks the right one at run time.
- Defining `__gt__` gives you `<` for free, because Python **reflects** comparisons.
- ⚠️ `100.__str__()` is a `SyntaxError` — write `(100).__str__()` or use a variable.
- Polymorphism's real value: **it removes `if / elif` chains** and makes new types drop in without editing old code.

---

# 🎯 Interview Questions

**Q1. What is polymorphism?**

> "One interface, many implementations." A single operation behaves differently depending on the object it acts on. Python has three forms: duck typing, operator overloading and method overriding.

**Q2. What is duck typing?**

> Python does not check an object's type before calling a method — it only checks whether the method exists. *"If it walks like a duck and quacks like a duck, it's a duck."* This allows unrelated classes to be used interchangeably with no shared parent.

**Q3. How does `a + b` work internally?**

> Python translates it to `a.__add__(b)`. Every operator is a magic method, which is why `+` adds numbers, concatenates strings and merges lists — three different `__add__` implementations.

**Q4. Does Python support method overloading (same method, different parameters)?**

> No. A second definition of a method **silently replaces** the first. Python uses default arguments and `*args` instead. It does support method **over*riding***, which is a different thing — a child redefining a parent's method.

**Q5. What's the difference between overloading and overriding?**

> **Overloading** = same name, different parameter lists, resolved at compile time (Python does not have it). **Overriding** = a child class replacing a parent's method, resolved at run time.

**Q6. Why is method overriding called runtime polymorphism?**

> Because the decision about which version to execute is made while the program is running, based on the actual object — not when the code is written.

---

# ⚠️ Common Mistakes

| Mistake | What happens |
|:--|:--|
| Expecting duck typing to catch errors early | It fails only at the moment of the call — `AttributeError` |
| Writing `100.__str__()` | `SyntaxError` — Python reads `100.` as a float |
| Defining `__eq__` and expecting `!=` to be wrong | Python derives `!=` from `__eq__` automatically |
| Defining `__eq__` without `__hash__` | The object becomes unhashable — can't go in a `set` or as a dict key |
| Thinking Python supports method overloading | It doesn't. The second definition wipes out the first. |
| Overriding a method with a different signature | It works, but callers written for the parent will break |
| Forgetting `super()` when the parent has shared setup | The parent's work silently never happens |

---

# ✓ Practice Questions

1. Write three unrelated classes — `Car`, `Bike`, `Truck` — each with a `start_engine()` method. Write one function that starts any of them. **Which type of polymorphism is this?**

2. Predict the output, then run it:
   ```python
   class Box:
       def __init__(self, n): self.n = n
       def __gt__(self, other): return self.n > other.n

   print(Box(5) > Box(3))
   print(Box(5) < Box(3))
   ```
   Explain the **second** line — you never wrote `__lt__`.

3. Create a `Time` class storing hours and minutes. Overload `+` so `Time(2, 30) + Time(1, 45)` gives `Time(4, 15)`. Handle the minute carry-over.

4. Build a `Shape` parent with an `area()` method, and `Circle`, `Square`, `Rectangle` children that override it. Put all three in a list and print every area in one loop — with **no `if` statements**.

5. Take the `Payment` example and add `Paytm`. **How many existing lines did you have to change?** Explain why that number is the whole point of polymorphism.

---

# ✓ Mini Assignment

Build a small **UPI payment system**:

- A `Payment` parent class with `pay(amount)` that validates the amount and prints "Processing..."
- Three children — `PhonePe`, `GooglePay`, `Paytm` — each overriding `pay()` and calling `super().pay(amount)` first
- Overload `__str__` on all four
- Overload `__gt__` on a `Transaction` class so transactions can be compared by amount
- A `process_all(payments, amount)` function using **duck typing** — it must work even for a class that does **not** inherit from `Payment`

Then answer in a comment: **which of the three types of polymorphism did each part use, and why was that the right choice?**

---

*All code in this tutorial was executed and verified.*
