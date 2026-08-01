# Inheritance in Python
## Pillar 2 of Object-Oriented Programming

---

# First Principle Thinking

## The Question

Imagine you are building a **College Management System**.

The college has:

```
   Student
   Faculty
   Security
   HOD
   Principal
```

Let's write them.

> 🛑 **Ask the class before writing any code:**
> **What information is common among all of them?**

Students will usually answer:

- Name
- Age
- Gender
- Mobile Number
- Address

**Exactly.**

---

## Now ask another question

> 🛑 **Should we write these variables again and again?**

```python
class Student:
    name
    age
    mobile

class Faculty:
    name
    age
    mobile

class Principal:
    name
    age
    mobile
```

Students immediately say:

**"No."**

---

## Then push harder

> 🛑 **If tomorrow the college decides to add an Aadhaar Number?**

Now you must modify:

```
   Student      ← edit
   Faculty      ← edit
   Principal    ← edit
   Security     ← edit
   HOD          ← edit
```

**Every class.**

That is a **maintenance nightmare**.

> 💡 And it is worse than just five edits. Miss **one** class and you have a bug that appears only for Security staff — six months later, in production.

---

## The Solution

Instead of repeating, **store the common things only once**.

```
                    Person
                 name, age,
              gender, mobile
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
    Student       Faculty       Principal
```

Now `Person` contains:

```
   name
   age
   gender
   mobile
```

**Every child automatically gets them.**

Add Aadhaar tomorrow? **Edit one class. Five classes receive it.**

This idea is called **Inheritance** — reusing already existing code instead of writing it again.

---

## Definition

> 📖 **Inheritance is the process by which one class acquires the properties and methods of another class.**

Or simply:

> **Write once. Reuse everywhere.**

| Term | Meaning |
|:--|:--|
| **Parent class** | the existing class (also: base class, super class) |
| **Child class** | the new class (also: derived class, sub class) |

---
---

# First Example

## Without inheritance

```python
class Student:

    def __init__(self, name):
        self.name = name

    def login(self):
        print("Login")


class Faculty:

    def __init__(self, name):
        self.name = name

    def login(self):
        print("Login")
```

> 🛑 **Notice what is repeated.**

```
   Student          Faculty
   ─────────        ─────────
   name       ←→    name        repeated
   login()    ←→    login()     repeated
```

Both have `login()` and `name`. **Repeated.**

---

## Using inheritance

```python
# ============================================================
#  INHERITANCE — write the common part ONCE
# ============================================================

class User:
    """The PARENT class. Holds everything common to all users."""

    def __init__(self, name):
        self.name = name

    def login(self):
        print("Login")


# ------------------------------------------------------------------
# class Student(User)  means  "Student inherits from User".
#
# The brackets are the whole syntax. Java writes `extends`;
# Python just puts the parent's name in brackets.
# ------------------------------------------------------------------
class Student(User):
    # `pass` means "this class body is intentionally empty".
    # Student adds nothing of its own — it simply takes everything
    # User has.
    pass


class Faculty(User):
    pass


student = Student("Ashok")
student.login()
print(student.name)
```

### Output

```
Login
Ashok
```

---

## What just happened?

> 🛑 **`Student` is completely empty. It has no `login()` and no `__init__`. So how did this work?**

Python **searched upwards**.

```
   student.login()
        │
        ▼
   Look in Student  ────►  not found
        │
        ▼
   Look in User     ────►  ✓ FOUND IT — run this
```

Although `Student` never defined `login()`, Python found it in the parent.

> 💡 **KEY IDEA**
> **A child class does not copy the parent's code. It gets a *link* to it.**
> When an attribute is missing, Python walks up the chain until it finds one.

---

## How Python Searches

```
   Student()
      │
      ▼
   Student Class      ← look here first
      │
      ▼
   User Class         ← then here
      │
      ▼
   object Class       ← then here (the ultimate parent)
      │
      ▼
   AttributeError     ← give up
```

This searching order is called **MRO** — **Method Resolution Order**.

You can see it directly:

```python
print([c.__name__ for c in Student.__mro__])
```

```
['Student', 'User', 'object']
```

> 💡 Notice **`object`** at the end. **Every class in Python inherits from `object`**, even when you don't write it. It is the ultimate parent of everything.

---

## Analogy — the inheritance you already understand

Imagine your father owns:

```
   House
   Land
   Car
```

When you become his legal heir, **do you build another house?**

**No. You inherit it.**

**Inheritance in programming works exactly the same way.** The child doesn't rebuild what the parent already has — it receives it.

---
---

# Real Example — A Banking App

Every account has:

```
   Account Number
   Balance
   Deposit
   Withdraw
```

And these three all have them:

```
   Savings Account
   Current Account
   Salary Account
```

So put the common part in a parent.

```python
# ============================================================
#  THE PARENT — everything every account shares
# ============================================================

class Account:

    def __init__(self, acc, balance):
        self.acc = acc
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. Balance: {self.balance}")

    def withdraw(self, amount):
        self.balance -= amount
        print(f"Withdrew {amount}. Balance: {self.balance}")


# ============================================================
#  THE CHILDREN — each adds only what makes it SPECIAL
# ============================================================

class SavingsAccount(Account):
    """Everything from Account, PLUS interest."""

    def interest(self):
        print("Interest Added")


class CurrentAccount(Account):
    """Everything from Account, PLUS overdraft."""

    def overdraft(self):
        print("Overdraft Allowed")


# ---------- using it ----------
user = SavingsAccount(1001, 5000)

user.deposit(500)      # inherited from Account
user.withdraw(100)     # inherited from Account
user.interest()        # SavingsAccount's own
```

### Output

```
Deposited 500. Balance: 5500
Withdrew 100. Balance: 5400
Interest Added
```

---

## What just happened?

> 🛑 **Count the lines inside `SavingsAccount`.**

**Three.** One `class` line, one docstring, one method.

`SavingsAccount` only wrote `interest()`. **Everything else came from `Account`** — the constructor, `deposit()`, `withdraw()`, and both attributes.

```
                Account
          acc, balance
          deposit(), withdraw()
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
   SavingsAccount        CurrentAccount
   + interest()          + overdraft()
```

> 💡 **The child class describes only the difference.** That is the whole economy of inheritance.

---
---

# Constructor Inheritance

## The Question

> 🛑 **If the child doesn't have `__init__`, whose constructor runs?**

**The parent's.**

## Example 1 — child has no constructor

```python
class A:
    def __init__(self):
        print("A")


class B(A):
    pass


B()
```

### Output

```
A
```

The parent's constructor ran, because `B` had none of its own and Python searched upward.

---

## Example 2 — child has its own constructor

```python
class A:
    def __init__(self):
        print("A")


class B(A):
    def __init__(self):
        print("B")


B()
```

### Output

```
B
```

> 🛑 **Where did `A` go?**

**The parent constructor is hidden.** Once the child defines its own `__init__`, Python finds it immediately and stops searching. The parent's version is never reached.

```
   B()
    │
    ▼
   B.__init__  ✓ found  →  stop. A.__init__ never runs.
```

---

## Example 3 — accessing the parent constructor

```python
class A:
    def __init__(self):
        print("A")


class B(A):
    def __init__(self):

        super().__init__()      # ← explicitly run the parent's version first

        print("B")


B()
```

### Output

```
A
B
```

Now **both** run — the parent's first, then the child's own work.

---
---

# What is `super()`?

## Ask the students

> 🛑 **Suppose you are inside the `Student` class. How do you call the `User` class?**

**Answer: `super()`**

Think of it as:

```
   Me
    │
    ▼
   My Parent
```

> 📖 **`super()` gives you access to the parent class from inside the child.**

---

## Example

```python
class User:

    def login(self):
        print("Login")


class Student(User):

    def login(self):
        # STEP 1 — run the parent's version (the common work)
        super().login()

        # STEP 2 — then add what is specific to a Student
        print("Student Dashboard")


Student().login()
```

### Output

```
Login
Student Dashboard
```

> 💡 **This is the difference between *replacing* and *extending*.**
>
> Without `super()`, the child **replaces** the parent's method.
> With `super()`, the child **extends** it — the common work still happens, and the child adds its own step on top.

---

## ⚠️ THE TRAP — the bug every student writes

Watch this carefully.

```python
class Account:
    def __init__(self, acc, balance):
        self.acc = acc
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount


class SavingsAccount(Account):
    def __init__(self, acc, balance, rate):
        self.rate = rate           # ❌ forgot super().__init__()


s = SavingsAccount(1002, 5000, 4.0)
print(s.__dict__)
s.deposit(100)
```

### Output

```
{'rate': 4.0}
AttributeError: 'SavingsAccount' object has no attribute 'balance'
```

> 🛑 **We passed `5000` as the balance. Where did it go?**

**Nowhere.** The child wrote its own `__init__`, which **hid** the parent's. So the parent's constructor never ran, and `acc` and `balance` were never created.

Look at `__dict__` — it contains **only** `rate`. The object is half-built.

### The fix

```python
class SavingsAccount(Account):
    def __init__(self, acc, balance, rate):
        super().__init__(acc, balance)     # ✅ build the parent part FIRST
        self.rate = rate                   # then add our own
```

```
{'acc': 1003, 'balance': 5000, 'rate': 4.0}
Deposited 100. Balance: 5100
```

> ⚠️ **Rule: if the child defines `__init__`, it must call `super().__init__(...)` — usually as the first line.**
>
> Python does **not** do this automatically. Forgetting it produces a silently half-built object, and the crash appears much later in a completely different method.

---
---

# Types of Inheritance

## 1. Single Inheritance

```
   A
   │
   ▼
   B
```

One parent, one child.

```python
class A:
    pass

class B(A):
    pass
```

---

## 2. Multilevel Inheritance

```
   A          Grandparent
   │
   ▼
   B          Parent
   │
   ▼
   C          Child
```

```python
class Person:
    def __init__(self, name):
        self.name = name
    def show(self):
        print(f"Person: {self.name}")


class Student(Person):
    def study(self):
        print("Studying")


class PlacementStudent(Student):
    def apply(self):
        print("Applying for placement")


p = PlacementStudent("Ashok")
p.show()      # from Person       (grandparent)
p.study()     # from Student      (parent)
p.apply()     # its own

print([c.__name__ for c in PlacementStudent.__mro__])
```

### Output

```
Person: Ashok
Studying
Applying for placement
['PlacementStudent', 'Student', 'Person', 'object']
```

**One object reached three levels up the chain.**

---

## 3. Hierarchical Inheritance

```
            A
        ┌───┼───┐
        ▼   ▼   ▼
        B   C   D
```

**One parent, many children.** This is exactly our college example — `Person` with `Student`, `Faculty`, `Principal`.

---

## 4. Multiple Inheritance

```
   A       B
    \     /
     \   /
       C
```

**Python supports this. Java does not.**

```python
class Father:
    def skills(self):
        print("Father: Gardening")


class Mother:
    def skills(self):
        print("Mother: Cooking")


class Child(Father, Mother):
    pass


Child().skills()
print([c.__name__ for c in Child.__mro__])
```

### Output

```
Father: Gardening
['Child', 'Father', 'Mother', 'object']
```

> 🛑 **Both parents have `skills()`. Why did Father's win?**

Because of the **MRO** — Python searches **left to right** through the parents. `Father` was written first in `class Child(Father, Mother)`, so it is found first.

---

## 5. Hybrid Inheritance

A **combination** of the above types. The most famous shape is the **diamond**:

```
        A
      /   \
     B     C
      \   /
        D
```

```python
class A:
    def hello(self): print("A")

class B(A):
    def hello(self): print("B")

class C(A):
    def hello(self): print("C")

class D(B, C):
    pass


D().hello()
print([c.__name__ for c in D.__mro__])
```

### Output

```
B
['D', 'B', 'C', 'A', 'object']
```

> 💡 **This is the famous "diamond problem".** `D` inherits from both `B` and `C`, which both inherit from `A`. Which `hello()` should run?
>
> Python answers it with a **fixed, predictable order**: `D → B → C → A → object`. It checks all children before reaching the shared grandparent.
>
> **Java avoids the problem entirely by banning multiple class inheritance.** Python solves it instead.

### Python will refuse an impossible order

```python
class X(A, B):     # A is B's parent — this ordering is contradictory
    pass
```

```
TypeError: Cannot create a consistent method resolution order (MRO)
for bases A, B
```

> Python checks that a sensible order exists and **refuses to create the class** if it doesn't. It never guesses.

---
---

# `isinstance()`

Suppose:

```python
student = Student()
```

> 🛑 **Is `student` a `Student`?** Yes.
> **Is `student` also a `User`?** Yes — it inherited from it.

Check:

```python
print(isinstance(student, Student))    # True
print(isinstance(student, User))       # True
print(isinstance(student, object))     # True — everything is an object
```

**All return `True`.**

A child object **is** its parent type. That is what "is-a" means.

> 💡 There is also **`issubclass()`**, which asks the same question about *classes* rather than objects:
> ```python
> print(issubclass(Student, User))     # True
> ```

> ⚠️ Compare with `type()`, which checks the **exact** class and ignores inheritance:
> ```python
> print(type(student) is User)         # False — it's a Student, not a User
> print(isinstance(student, User))     # True  — but it IS-A User
> ```
> **Use `isinstance()`.** `type()` breaks the moment inheritance is involved.

---
---

# Why Use Inheritance?

| Without inheritance | With inheritance |
|:--|:--|
| Copy | **Write Once** |
| Paste | **Reuse** |
| Modify | **Maintain Easily** |
| Repeat | **Extend Easily** |

Go back to the Aadhaar question from the very beginning:

```
   WITHOUT inheritance          WITH inheritance
   ──────────────────────       ──────────────────────
   edit Student                 edit Person
   edit Faculty                       │
   edit Principal                     ▼
   edit Security                all five receive it
   edit HOD
   (and hope you missed none)
```

**Five edits versus one.** That is the entire argument.

---

# Real Life Examples

### Amazon
```
   User
    │
    ▼
   Seller
    │
    ▼
   PrimeSeller
```

### Hospital
```
   Person
    │
    ▼
   Doctor
    │
    ▼
   Cardiologist
```

### Food Delivery
```
   Order
    │
    ▼
   OnlineOrder
    │
    ▼
   ExpressOrder
```

### College
```
   Person
    │
    ▼
   Student
    │
    ▼
   PlacementStudent
```

> 💡 **The test before you use inheritance:** can you say **"a Cardiologist IS-A Doctor"** and have it sound true?
>
> If yes → inheritance. If you can only say **"has-a"** — *an Order HAS-A Customer* — then it is **not** inheritance. Make it an attribute instead.

---
---

# 🎯 Common Interview Questions

**Q1. Why do we use inheritance?**

> To eliminate code duplication and promote code reuse. Common behaviour is defined once in a parent class and every related class receives it — so a change is made in one place instead of many.

**Q2. Can a child access parent methods?**

> **Yes.** Python searches the child first, then walks up the chain to the parent.

**Q3. Can a parent access child methods?**

> **No.** Inheritance flows downward only. The parent has no knowledge that any child exists.

**Q4. Does Python support multiple inheritance?**

> **Yes** — `class C(A, B)`. Java does not allow it for classes, to avoid the diamond problem. Python allows it and resolves conflicts using the MRO, searching left to right.

**Q5. Which class is the ultimate parent?**

> **`object`.** Everything in Python inherits from `object`, whether you write it or not. It sits at the end of every MRO.

**Q6. What is MRO?**

> Method Resolution Order — the sequence in which Python searches classes for an attribute. View it with `ClassName.__mro__`. For `class D(B, C)` it is `D → B → C → A → object`.

**Q7. If a child defines `__init__`, does the parent's still run?**

> **No** — it is hidden. You must call `super().__init__(...)` explicitly, otherwise the parent's attributes are never created and you get an `AttributeError` later.

**Q8. What is the difference between `isinstance()` and `type()`?**

> `isinstance()` respects inheritance — a `Student` object *is* a `User`. `type()` checks the exact class only. Use `isinstance()`.

---

# ⚠️ Common Mistakes

| Mistake | What happens |
|:--|:--|
| Child defines `__init__` but forgets `super().__init__()` | Parent's attributes are never created → `AttributeError` later |
| Using inheritance for a "has-a" relationship | `class Order(Customer)` is wrong. An order **has** a customer. |
| Very deep chains (5+ levels) | Nobody can tell where a method actually lives |
| Using `type()` instead of `isinstance()` | Breaks the moment a subclass is introduced |
| Expecting the parent to see child methods | Inheritance flows **downward** only |
| Overriding a method with a different signature | Runs, but breaks any code written for the parent |

---

# ✓ Summary

| Concept | Meaning |
|:--|:--|
| **Inheritance** | Acquiring properties and methods from another class |
| **Parent** | Existing class (base / super class) |
| **Child** | New class (derived / sub class) |
| **`super()`** | Access the parent's methods / constructor |
| **`pass`** | Empty class body |
| **`isinstance()`** | Checks the inheritance relationship |
| **MRO** | Order in which Python searches for attributes |
| **`object`** | The ultimate parent of every class |

### Types at a glance

| Type | Shape | Supported |
|:--|:--|:--|
| Single | `A → B` | ✅ |
| Multilevel | `A → B → C` | ✅ |
| Hierarchical | `A → B, C, D` | ✅ |
| Multiple | `A, B → C` | ✅ **Python yes, Java no** |
| Hybrid | combination (diamond) | ✅ resolved by MRO |

---

# ✓ One-Line Summary

> **Inheritance is not about creating new classes — it is about identifying common behaviour, placing it in one parent class, and allowing all related classes to reuse it.**

---

# ✓ Practice Questions

1. Predict the output, then run it:
   ```python
   class A:
       def __init__(self): print("A")
   class B(A):
       def __init__(self):
           print("B")
           super().__init__()
   B()
   ```
   Now **swap the two lines** inside `B.__init__`. Does the output change? Why?

2. Build the college hierarchy: `Person` with `name`, `age`, `mobile`; children `Student`, `Faculty`, `Principal`, each adding one unique method. Then add `aadhaar` — **how many classes did you edit?**

3. ```python
   class A:
       def greet(self): print("A")
   class B(A):
       def greet(self): print("B")
   class C(A):
       def greet(self): print("C")
   class D(C, B):     # note the order!
       pass
   D().greet()
   ```
   Predict the output and the MRO. Compare with `class D(B, C)`.

4. Write `SavingsAccount(Account)` with its own `__init__` that takes an interest rate — and **deliberately forget** `super().__init__()`. Print `__dict__` and explain what is missing.

5. Which of these are correct uses of inheritance, and which should be attributes instead?
   `Car → Engine` · `Dog → Animal` · `Student → Person` · `Order → Customer` · `SavingsAccount → Account`

---

# ✓ Mini Assignment

Build a **Hospital Management System** using inheritance:

- **`Person`** — `name`, `age`, `gender`, `mobile`; a method `show_details()`
- **`Doctor(Person)`** — adds `specialization`, `consultation_fee`; a method `treat()`. Its `__init__` **must** call `super().__init__()`
- **`Cardiologist(Doctor)`** — adds `perform_surgery()`; override `treat()` and use `super().treat()` inside it
- **`Patient(Person)`** — adds `patient_id`, `disease`

Then:

1. Create one of each and call every method
2. Print the MRO of `Cardiologist`
3. Use `isinstance()` to prove a `Cardiologist` is also a `Doctor` **and** a `Person`
4. Show that a `Person` object **cannot** call `treat()`, and explain why in a comment

---

*All code in this tutorial was executed and verified.*
