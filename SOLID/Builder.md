# Design Patterns 02 — Builder

**DriveReady 8.0 · AI Applied Engineer · Post-read**

Last class was Singleton, which controls **how many** objects exist (exactly one). This one
solves a completely different problem: how do you safely construct **one correctly validated
object** when it has a lot of fields, some of which may be missing, and all of which need
checking before the object is allowed to exist?

Both are creational patterns. They have almost nothing else in common.

We build it from one running example — a `Student` class — improving it step by step until it
becomes Builder. Every sample is in Java and Python, and here that difference matters more than
usual: **several of the problems that force Java to reach for Builder don't exist in Python at
all.** Section 9 is about which ones, and what's left over.

---

## Contents

1. [Why we need a different way to build objects](#1-why-we-need-a-different-way-to-build-objects)
2. [Telescoping constructors](#2-telescoping-constructors)
3. [From a dictionary to a real class](#3-from-a-dictionary-to-a-real-class)
4. [Builder, first working version](#4-builder-first-working-version)
5. [Making it production-ready](#5-making-it-production-ready)
6. [The bug AI leaves in](#6-the-bug-ai-leaves-in)
7. [Where Builder already runs](#7-where-builder-already-runs)
8. [Generated builders — Lombok and dataclasses](#8-generated-builders--lombok-and-dataclasses)
9. [Does Python even need Builder?](#9-does-python-even-need-builder)
10. [Pitfalls, collected](#10-pitfalls-collected)
11. [Java ↔ Python glossary](#11-java--python-glossary)
12. [Interview questions](#12-interview-questions)
13. [Check yourself](#13-check-yourself)
14. [Homework](#14-homework)

---

## 1. Why we need a different way to build objects

A `Student` for a college app realistically needs a lot of fields:

**Java**

```java
class Student {
    String name;
    int age;
    double psp;
    String batch;
    long id;
    String universityName;
    int gradYear;
    String phoneNumber;
}
```

**Python**

```python
class Student:
    name: str
    age: int
    psp: float
    batch: str
    id: int
    university_name: str
    grad_year: int
    phone_number: str
```

The familiar way to fill this in is an empty object plus setters:

**Java**

```java
Student st = new Student();
st.setName("Naman");
st.setAge(21);
st.setPsp(89.21);
st.setBatch("April 21");
```

**Python**

```python
st = Student()
st.name = "Naman"
st.age = 21
st.psp = 89.21
st.batch = "April 21"
```

Now add a real rule: graduation year cannot be later than 2022, and must be at least
`age + 2000`.

**Should that check run before the object exists, or after?** Before. An invalid `Student`
should never exist in the program, not even briefly.

That is exactly where setters fail. Nothing stops someone creating `st` and simply **forgetting**
to set `grad_year` at all. There is now an unvalidated object loose in the program and no way to
force the check.

### Move the check into the constructor

The constructor is the one piece of code guaranteed to run before the object can be used. So put
every field there and validate inside it.

**Java**

```java
Student(String name, int age, double psp, String batch,
        long id, String universityName, int gradYear, String phoneNumber) {
    // validation goes here
}
```

**Python**

```python
def __init__(self, name, age, psp, batch,
             id, university_name, grad_year, phone_number):
    # validation goes here
    ...
```

And now creating one looks like this:

**Java**

```java
Student st = new Student("Naman", 21, 89.21, "XYZ", 123, "ABC", 2021, "9999999999");
```

**Python**

```python
st = Student("Naman", 21, 89.21, "XYZ", 123, "ABC", 2021, "9999999999")
```

### Three new problems

**1. Unreadable.** What is `"XYZ"`? What is `"ABC"`? You have to open the class and count
parameter positions every single time you read this line.

**2. Silently wrong.** `name` and `universityName` are both strings. Swap them and Java compiles
it happily — a `String` is a `String`, the compiler has no idea one was meant to be a name. Same
in Python: nothing stops you at runtime either. The code runs, the data is wrong, nobody notices.

**3. Fragile.** Add one field and every `new Student(...)` in the codebase has to be found and
updated. In a real repo with hundreds of call sites this is a large, risky refactor. It's the
same brittleness OCP warned about in the SOLID module, arriving through a constructor instead of
a method.

### And the missing-value problem

The constructor demands all eight values. What about a caller who genuinely doesn't have the
email yet, because the student hasn't given one? They can't use it. They're forced to invent a
value.

The obvious next thought is "write a second constructor without email." Then a different caller
is missing the phone number and needs a third. That spiral is Section 2.

**Watch for:**

- Expecting the compiler to catch a same-type swap. It checks types and positions, never
  meanings.
- Underestimating the cost of adding one field later. Trivial in a class exercise, one of the
  most common large refactors in real code.

---

## 2. Telescoping constructors

The instinct is: write one constructor per combination of fields. In Java that hits a wall
immediately.

**Java**

```java
Student(String name, double psp);
Student(String universityName, double psp);   // identical to Java. Won't compile.
```

**Python**

```python
def __init__(self, name, psp): ...
def __init__(self, university_name, psp): ...   # the second silently replaces the first
```

Java tells constructors apart by the **type and order** of parameters only. It ignores their
names entirely, so those two look identical and it refuses to compile both.

Python's failure is different and quieter: there's no overloading at all. The second `__init__`
just overwrites the first in the class body, no error, no warning. You end up with one
constructor and no idea the other vanished.

### The combinatorial explosion

If a class has `n` fields, how many "which fields are filled in" combinations exist?

```
n fields  →  up to 2ⁿ combinations
Student has 8 fields  →  up to 256
```

Unmanageable, and in Java most of them couldn't even be written without clashing.

### Why "telescoping"

Picture a collapsible telescope: tubes of decreasing size, each sliding inside the next. Each
constructor calls a slightly smaller one and adds one value on top.

**Java**

```java
Student(String name) { this.name = name; }

Student(String name, double psp) {
    this(name);
    this.psp = psp;
}

Student(String name, double psp, int age) {
    this(name, psp);
    this.age = age;
}
// and it keeps growing
```

**Python**

```python
# Python can't overload __init__, so the telescoping shape has to be faked
# with classmethods — which makes the problem even more visible
class Student:
    def __init__(self, name):
        self.name = name

    @classmethod
    def with_psp(cls, name, psp):
        s = cls(name)
        s.psp = psp
        return s

    @classmethod
    def with_psp_and_age(cls, name, psp, age):
        s = cls.with_psp(name, psp)
        s.age = age
        return s
    # and it keeps growing
```

Does this fix unreadable, silently-wrong or fragile? No. It's arguably worse — the same problems
are now spread across many places instead of concentrated in one.

```
Rule of thumb: never use telescoping constructors.
```

**Watch for:**

- Assuming Java distinguishes constructors by parameter name. It doesn't.
- Assuming Python will warn you about a duplicate `__init__`. It won't. It silently keeps the
  last one.

---

## 3. From a dictionary to a real class

Different idea: what if the constructor took **one** parameter that could hold many labelled
values inside it? A `Map` in Java, a `dict` in Python.

**Java**

```java
class Student {
    Student(Map<String, Object> map) {
        ...
    }
}
```

**Python**

```python
class Student:
    def __init__(self, data: dict):
        ...
```

That does solve "too many constructors" — one is enough now. But look at reading the values back
out:

**Java**

```java
String name = (String) map.get("name");
Double psp  = (Double) map.get("psp");
```

**Python**

```python
name = data["name"]
psp = data["psp"]        # no type known, no check, no help
```

Java needs a manual **cast** back to the right type. Put the wrong type in — `map.put("psp",
"hello")` — and nothing complains until the program runs and throws `ClassCastException`.

> **Correction to the source material:** the original writes `(Integer) map.get("psp")`, but
> `psp` is declared `double`. Casting it to `Integer` throws at runtime regardless of what was
> stored. It should be `(Double)`. Worth flagging in class, because a student typing it as
> written will hit a confusing exception and blame the pattern.

Second problem, and it's the worse one: misspell a key.

**Java**

```java
map.put("nmae", "Naman");     // typo. No error. Nothing at all.
```

**Python**

```python
data["nmae"] = "Naman"        # typo. No error. Nothing at all.
```

The name simply never gets set. Later, something looks for `"name"`, doesn't find it, and there
is no clue why.

```
Map / dict as a field bundle:
  + solves "too many constructors"
  - destroys every compile-time check you had
  - a wrong key does nothing, silently
  - a wrong type fails later, while running, far from the mistake
```

### The fix: use a plain class

What we actually want is a map that the compiler checks for us. Both languages already have one:
a class.

Write `helper.name = "Naman"` and the field has to genuinely exist with the right type. A typo
won't compile in Java, and a type checker flags it in Python — either way the mistake is caught
where it was made, not three files away at runtime.

**Java**

```java
class Helper {
    String name;
    int age;
    double psp;
    String universityName;
    String batch;
    long id;
    int gradYear;
    String phoneNumber;
}
```

**Python**

```python
from dataclasses import dataclass


@dataclass
class Helper:
    name: str = ""
    age: int = 0
    psp: float = 0.0
    university_name: str = ""
    batch: str = ""
    id: int = 0
    grad_year: int = 0
    phone_number: str = ""
```

**Why doesn't `Helper` validate anything itself?** Because `Helper` isn't the object being
protected — `Student` is. `Helper` is a temporary place to collect values. The check belongs at
the point the real object gets built.

**Java**

```java
Helper helper = new Helper();
helper.name = "Naman";
helper.age = 21;
helper.psp = 89.21;

Student s = new Student(helper);      // validation happens HERE
```

**Python**

```python
helper = Helper()
helper.name = "Naman"
helper.age = 21
helper.psp = 89.21

s = Student(helper)                   # validation happens HERE
```

**Java**

```java
class Student {
    Student(Helper helper) {
        if (helper.gradYear > 2022) {
            throw new IllegalArgumentException("Grad year cannot be greater than 2022");
        }
        this.gradYear = helper.gradYear;
        this.name = helper.name;
        // ...
    }
}
```

**Python**

```python
class Student:
    def __init__(self, helper: Helper):
        if helper.grad_year > 2022:
            raise ValueError("Grad year cannot be greater than 2022")
        self.grad_year = helper.grad_year
        self.name = helper.name
        # ...
```

`Helper` collects values with the compiler watching. `Student`'s constructor becomes the single
checkpoint, and there is no way to get a `Student` without passing through it.

**That is the Builder pattern.** What we called `Helper`, everyone else calls a **Builder**.

**Watch for:**

- Treating a dict as a safe way to bundle optional fields. It removes every check you had.
- Putting validation inside the collector. Its job is to collect. Checking belongs at the one
  real entry point.

---

## 4. Builder, first working version

Following normal encapsulation habits, the builder's fields should be private with getters and
setters rather than touched directly.

**Java**

```java
public class Builder {
    private String name;
    private int age;
    private int gradYear;
    // ...remaining fields

    public String getName()               { return name; }
    public void   setName(String name)    { this.name = name; }

    public int  getAge()                  { return age; }
    public void setAge(int age)           { this.age = age; }

    public int  getGradYear()             { return gradYear; }
    public void setGradYear(int gradYear) { this.gradYear = gradYear; }
}
```

**Python**

```python
class Builder:
    def __init__(self):
        self._name = ""
        self._age = 0
        self._grad_year = 0
        # ...remaining fields

    def set_name(self, name: str) -> None:      self._name = name
    def set_age(self, age: int) -> None:        self._age = age
    def set_grad_year(self, year: int) -> None: self._grad_year = year

    @property
    def name(self) -> str: return self._name

    @property
    def age(self) -> int: return self._age

    @property
    def grad_year(self) -> int: return self._grad_year
```

Python has no `private`. A single leading underscore is a convention meaning "don't touch this
from outside," and `@property` gives read access without a `get_` prefix. It's honour-system
rather than enforced, but it's the same intent.

**Java**

```java
public class Student {
    String name;
    int age;
    int gradYear;

    Student(Builder builder) {
        if (builder.getGradYear() > 2022) {
            throw new IllegalArgumentException("Grad year cannot be greater than 2022");
        }
        this.gradYear = builder.getGradYear();
        this.age = builder.getAge();
        this.name = builder.getName();
    }
}
```

**Python**

```python
class Student:
    def __init__(self, builder: Builder):
        if builder.grad_year > 2022:
            raise ValueError("Grad year cannot be greater than 2022")
        self.grad_year = builder.grad_year
        self.age = builder.age
        self.name = builder.name
```

**Java**

```java
Builder builder = new Builder();
builder.setAge(21);
builder.setName("Naman");
builder.setGradYear(2023);      // will trigger the validation error

Student st = new Student(builder);
```

**Python**

```python
builder = Builder()
builder.set_age(21)
builder.set_name("Naman")
builder.set_grad_year(2023)     # will trigger the validation error

st = Student(builder)
```

Trace it: `grad_year` is 2023, the constructor sees 2023 > 2022, and throws. **No `Student` object
is created at all.** That is exactly the guarantee missing in Section 1 — an invalid object never
comes into existence, not even for a moment.

**Watch for:**

- Thinking this is the finished pattern. It's a working first draft. Section 5 fixes four real
  gaps still in it.

---

## 5. Making it production-ready

The Section 4 version works but is clunky. Four small fixes, each solving exactly one problem.

### Fix 1 — how would anyone know Builder exists?

Open `Student` for the first time and nothing hints that a separate `Builder` must be made first.
Put a method **on `Student`** that hands one back. It has to run before any `Student` exists, so
it's `static` in Java and a `@staticmethod` in Python.

**Java**

```java
public class Student {
    public static Builder getBuilder() {
        return new Builder();
    }
}
```

**Python**

```python
class Student:
    @staticmethod
    def get_builder() -> "Builder":
        return Builder()
```

### Fix 2 — who's doing the actual work?

In `new Student(builder)`, who validates and creates? `Student`'s constructor. `Builder` just
holds values. A class called Builder that doesn't build anything is backwards. Give it a
`build()`.

**Java**

```java
public Student build() {
    if (getGradYear() > 2022) {
        throw new IllegalArgumentException("Grad year cannot be greater than 2022");
    }
    return new Student(this);
}
```

**Python**

```python
def build(self) -> "Student":
    if self._grad_year > 2022:
        raise ValueError("Grad year cannot be greater than 2022")
    return Student(self)
```

`new Student(...)` is no longer written by the caller at all.

### Fix 3 — can this be one smooth line?

**Java**

```java
Student st = Student.getBuilder()
        .setAge(21)
        .setName("Naman")
        .setGradYear(2021)
        .build();
```

**Python**

```python
st = (Student.get_builder()
      .set_age(21)
      .set_name("Naman")
      .set_grad_year(2021)
      .build())
```

For `.setAge(21).setName(...)` to chain, what must `setAge` return? **The builder itself.** If it
returned nothing, there'd be nothing to call `.setName` on.

**Java**

```java
public Builder setAge(int age) {
    this.age = age;
    return this;
}
```

**Python**

```python
def set_age(self, age: int) -> "Builder":
    self._age = age
    return self
```

```
Rule for every setter on a Builder:
  1. set the value
  2. return the builder itself instead of nothing

That one habit is what makes .set_age(21).set_name("Naman") work.
The style has a name: fluent chaining.
```

There is only ever **one** builder object in that chain. Nothing new is created at each step —
it's the same object handed forward:

```
  Student.get_builder()  ──►  ┌──────────┐
                              │ Builder  │
  .set_age(21)  ──────────────┤ age=21   ├──► returns itself
                              │          │
  .set_name("Naman") ─────────┤ name=... ├──► returns itself
                              │          │
  .set_grad_year(2021) ───────┤ year=... ├──► returns itself
                              └────┬─────┘
  .build() ────────────────────────┴──────► validates, THEN creates Student
```

Compare that to `Student("Naman", 21, 89.21, "XYZ", 123, "ABC", 2021, "9999999999")` from
Section 1. The readability jump is the main reason anyone bothers with this pattern.

### Fix 4 — can someone still skip the Builder?

`Student(Builder)` is still public. Anyone can call it directly, skipping `build()` and skipping
validation with it.

**Java**

```java
public class Student {
    String name;
    int age;
    int gradYear;

    public static Builder getBuilder() { return new Builder(); }

    private Student(Builder builder) {          // now private
        this.gradYear = builder.getGradYear();
        this.age = builder.getAge();
        this.name = builder.getName();
    }

    static class Builder {                      // now nested INSIDE Student
        private String name;
        private int age;
        private int gradYear;

        public Builder setName(String n)     { this.name = n;     return this; }
        public Builder setAge(int a)         { this.age = a;      return this; }
        public Builder setGradYear(int y)    { this.gradYear = y; return this; }

        public String getName()    { return name; }
        public int    getAge()     { return age; }
        public int    getGradYear(){ return gradYear; }

        public Student build() {
            if (gradYear > 2022) {
                throw new IllegalArgumentException("Grad year cannot be greater than 2022");
            }
            return new Student(this);
        }
    }
}
```

**Python**

```python
class Student:
    _key = object()                             # only Builder has this

    def __init__(self, builder: "Student.Builder", _key=None):
        if _key is not Student._key:
            raise TypeError("Use Student.get_builder()...build()")
        self.grad_year = builder.grad_year
        self.age = builder.age
        self.name = builder.name

    @staticmethod
    def get_builder() -> "Student.Builder":
        return Student.Builder()

    class Builder:
        def __init__(self):
            self._name = ""
            self._age = 0
            self._grad_year = 0

        def set_name(self, n: str) -> "Student.Builder":  self._name = n;      return self
        def set_age(self, a: int) -> "Student.Builder":   self._age = a;       return self
        def set_grad_year(self, y: int) -> "Student.Builder": self._grad_year = y; return self

        @property
        def name(self) -> str: return self._name

        @property
        def age(self) -> int: return self._age

        @property
        def grad_year(self) -> int: return self._grad_year

        def build(self) -> "Student":
            if self._grad_year > 2022:
                raise ValueError("Grad year cannot be greater than 2022")
            return Student(self, Student._key)
```

**This is where the two languages stop matching, and it's worth saying plainly.**

Java's fix is airtight. A private constructor can only be called from inside the same class,
which is exactly why `Builder` has to move inside `Student`. After that, `Student.getBuilder()
...build()` is the only door in, and the compiler enforces it.

Python has no `private`, so there is no airtight version. The sentinel-key trick above works, but
any determined caller can read `Student._key` and bypass it. **In Python this is a convention
backed by a speed bump, not a guarantee.** Nesting `Builder` inside `Student` is still worth
doing for discoverability, but be honest with students that it isn't enforcement.

If you actually need "cannot be constructed invalid" in Python, the answer isn't a sentinel — it's
to validate in `__init__` or `__post_init__` so there's no unchecked path to begin with. Section 9
covers that.

```
The four fixes:
  1  Student.get_builder()          → "how do I start?"
  2  Builder.build()                → "who does the real work?"
  3  every setter returns self      → "can I chain?"
  4  private ctor + nested Builder  → "can someone skip validation?"
                                       (airtight in Java, convention in Python)
```

**Watch for:**

- Setters returning nothing. Chaining can't work without `return this` / `return self`.
- Leaving the constructor public in Java. Until it's private, the Builder is optional.
- Presenting the Python sentinel as real enforcement. It isn't.

---

## 6. The bug AI leaves in

AI tools write the *shape* of Builder correctly almost every time: private constructor, nested
builder, chainable setters, validating `build()`. There's one detail they routinely miss, and it
quietly destroys the reason the pattern exists.

### Ask for a Builder with a list field

```
Generate a Student class using the Builder pattern, with fields name, age,
gradYear, and a phoneNumbers list. Validate gradYear <= 2022.
```

The shape will come back right. Check one line: **how does the list get copied?**

**Java**

```java
this.phoneNumbers = builder.phoneNumbers;                  // shares the same list
this.phoneNumbers = new ArrayList<>(builder.phoneNumbers); // brand new list
```

**Python**

```python
self.phones = builder.phones          # shares the same list
self.phones = list(builder.phones)    # brand new list
```

AI usually writes the first one.

### Why one line breaks everything

If `Student`'s list *is* the builder's list, then after `build()` has finished and validated, you
can still reach back through the builder and change the "finished" object.

**Java**

```java
Builder b = Student.getBuilder().setName("Naman");
List<String> phones = new ArrayList<>();
phones.add("9999999999");
b.setPhoneNumbers(phones);
Student st = b.build();

phones.add("0000000000");     // silently changes st too, after it was built
```

**Python**

```python
phones = ["9999999999"]
st = Student.get_builder().set_name("Naman").set_phones(phones).build()

phones.append("0000000000")   # silently changes st too, after it was built
print(st.phones)              # ['9999999999', '0000000000']
```

Measured, in Python:

```
student's phones after external mutation: ['9999999999', '0000000000']
with list(phones) instead:                ['9999999999']
```

What's actually happening in memory:

```
BUGGY — one list, two names pointing at it

   builder.phones ──┐
                    ├──►  [ "9999999999", "0000000000" ]
   student.phones ──┘          ▲
                               └── a change through either name is seen by both


FIXED — build() makes a second list

   builder.phones ─────────►  [ "9999999999", "0000000000" ]

   student.phones ─────────►  [ "9999999999" ]
                                  ▲
                                  └── untouched, exactly as validated
```

The whole promise of Builder is that once `build()` returns, you hold a checked, stable object
that cannot silently change. Copying a reference instead of the values breaks that promise
without breaking the build.

### Python has a second version of this trap

This one is Python-only and catches more people than the first:

**Python**

```python
def add_phone(number, phones=[]):     # default evaluated ONCE, at def time
    phones.append(number)
    return phones


add_phone("111")     # ['111']
add_phone("222")     # ['111', '222']  <- leaked from the previous call
```

The default list is created once when the function is defined, not once per call, so every caller
shares it. In a builder's `__init__` this means every builder you create shares one list. The fix
is `None` plus a fresh list inside, or `field(default_factory=list)` on a dataclass.

**Python**

```python
def __init__(self, phones: list[str] | None = None):
    self._phones = list(phones) if phones else []
```

```
The habit:
  1. Let AI write the first draft. The shape is usually right.
  2. Then ask: "can anything here still be changed from outside,
     after the object is supposedly finished?"

Java's version of this lesson was the missing `volatile` in Singleton.
Python's is the shared list — plus the mutable default argument, which
is the same bug arriving one step earlier.
```

**Watch for:**

- Assuming a Builder that compiles is safe. A missing defensive copy compiles, looks fine, and
  only shows up when something external mutates the shared collection later.
- Checking only `int` and `String` fields. Those can't be mutated after copying. The risk is
  specific to lists, dicts, sets and other mutable references.

---

## 7. Where Builder already runs

You have been using this pattern for months without knowing its name.

```
Java
  StringBuilder                 sb.append("a").append("b") — fluent chaining,
                                probably from your first week of Java
  OkHttp Request.Builder        nearly every Android or backend HTTP call
  Firebase RequestConfiguration nested Builder, chainable setters, build()
  Lombok @Builder               generates the whole shape for you

Python
  SQLAlchemy query building     session.query(User).filter(...).order_by(...)
                                .limit(10).all()  — the same fluent chain, and
                                you use it in Week 5
  pathlib.Path                  Path("/tmp") / "data" / "out.json"
  matplotlib / plotly figures   assembled piece by piece, then rendered
  LLM API request objects       model, system prompt, temperature, max_tokens,
                                tools[] — the exact "many optional fields,
                                some needing validation" problem
```

Google didn't invent anything for Firebase. They used the shape we just derived from a simple
problem. That's the real win here: not learning something new, but being able to name something
you've been using all along.

The SQLAlchemy one is worth pointing at directly in class, because students will type it in
Week 5. `.filter(...).order_by(...).limit(10)` is Builder — each call returns the query object so
the next call can chain, and `.all()` is `build()`.

---

## 8. Generated builders — Lombok and dataclasses

Everything hand-written in Sections 4 and 5 can be generated.

### Java: Lombok `@Builder`

**Java**

```java
import lombok.Builder;

@Builder
public class Student {
    private String name;
    private int age;
    private double psp;
    private int gradYear;
    private List<String> phoneNumbers;
}
```

**Java**

```java
Student st = Student.builder()
        .name("Naman")
        .age(21)
        .gradYear(2021)
        .build();
```

Note it's `.builder()` rather than `.getBuilder()` — Lombok's naming convention, same idea
underneath.

**Two catches, both tying back to earlier sections.** Plain `@Builder` does **not** add your
`gradYear > 2022` rule; Lombok generates the shape, it has no idea what "valid" means for your
class. And for a `List` field it can carry the exact Section 6 shared-reference problem unless
you add `@Singular`, which builds a protected internal copy.

`@With` is the related annotation for immutable classes. Instead of a setter that changes the
object, it returns a **new copy** with one field changed:

**Java**

```java
import lombok.Value;
import lombok.With;

@Value      // all fields private final, getters generated, no setters
@With
public class Student {
    String name;
    int age;
    int gradYear;
}
```

**Java**

```java
Student original = new Student("Naman", 21, 2021);
Student updated  = original.withAge(22);   // brand-new Student

// original.getAge() is still 21
```

```
@Builder  →  constructing an object safely the first time
@With     →  getting a modified copy of one that already exists
```

### Python: `@dataclass` does both, in the standard library

**Python**

```python
from dataclasses import dataclass, field, replace


@dataclass
class Student:
    name: str
    age: int
    grad_year: int
    phones: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.grad_year > 2022:
            raise ValueError("Grad year cannot be greater than 2022")
        self.phones = list(self.phones)          # defensive copy
```

`__post_init__` runs immediately after the generated `__init__`, which makes it the exact
equivalent of `build()`'s validation step — except there is no way around it, because it *is* the
constructor. Measured:

```
>>> Student(name="Naman", age=21, grad_year=2023)
ValueError: Grad year cannot be greater than 2022
```

Note that Python's answer solves in two lines what Lombok leaves to you in both cases: the
validation and the defensive copy sit right there in `__post_init__`.

For `@With`, Python has `frozen=True` plus `dataclasses.replace`:

**Python**

```python
@dataclass(frozen=True)
class Student:
    name: str
    age: int
    grad_year: int


original = Student("Naman", 21, 2021)
updated = replace(original, age=22)     # brand-new Student

original.age = 30                       # FrozenInstanceError
```

Measured:

```
original: Student(name='Naman', age=21) | updated: Student(name='Naman', age=22)
mutation blocked -> FrozenInstanceError: cannot assign to field 'age'
```

Unlike the Section 5 sentinel trick, **this one is real enforcement.** A frozen dataclass genuinely
cannot be mutated.

**Watch for:**

- Assuming `@Builder` validates. It generates structure only.
- Assuming `@Builder` defensive-copies collections. Use `@Singular`.
- Confusing `@Builder` with `@With`. Construct versus modified copy.

---

## 9. Does Python even need Builder?

This is the section the source material's own header admits was planned and never written. It's
the most useful part of the class for a Python-first course, so here it is.

Go back to Section 1 and count the problems that motivated Builder:

| Problem from Section 1 | Java | Python |
|---|---|---|
| Unreadable positional call | needs Builder | keyword arguments |
| Same-type parameters swapped silently | needs Builder | `kw_only=True` makes it impossible |
| Adding a field breaks every caller | needs Builder | default values keep callers working |
| Missing values force more constructors | needs Builder | default values |
| 2ⁿ constructor combinations | needs Builder | one constructor with defaults |
| Validation before the object exists | needs Builder | `__post_init__` or Pydantic |

**Four of the six vanish because Python has keyword arguments and default parameter values.**
Java doesn't have either, and a large part of why Builder is a big deal in Java is that it's
simulating them.

Here is the swap problem, made structurally impossible:

**Python**

```python
from dataclasses import dataclass


@dataclass(kw_only=True)
class Student:
    name: str
    university_name: str
    age: int


Student("Naman", "ABC University", 21)       # TypeError
Student(name="Naman", university_name="ABC University", age=21)   # the only way
```

Measured:

```
positional call rejected -> Student.__init__() takes 1 positional argument but 4 were given
```

You cannot swap two same-type parameters if you cannot pass them positionally at all. In Java
that entire class of bug requires the Builder pattern to prevent. In Python it requires one
keyword argument on a decorator.

### Pydantic: the version you'll actually use

Your Week 5 stack already ships the production answer. A Pydantic model validates **types and
values on construction**, which is `build()`'s job, done by the constructor.

**Python**

```python
from pydantic import BaseModel, Field, field_validator


class Student(BaseModel):
    name: str
    age: int
    psp: float
    grad_year: int
    phones: list[str] = Field(default_factory=list)

    @field_validator("grad_year")
    @classmethod
    def check_grad_year(cls, v: int) -> int:
        if v > 2022:
            raise ValueError("Grad year cannot be greater than 2022")
        return v
```

Measured, all three at once:

```
Student(name="Naman", age=21, psp=89.21, grad_year=2023)
  -> Value error, Grad year cannot be greater than 2022

Student(name="Naman", age="twenty one", psp=89.21, grad_year=2021)
  -> Input should be a valid integer, unable to parse string as an integer

shared = ["9999999999"]
s = Student(..., phones=shared)
shared.append("0000000000")
  -> s.phones is still ['9999999999']
```

Read that last one again. **Pydantic defensive-copies the list for you**, so the Section 6 bug —
the one AI keeps writing, the one that took a whole section to explain — cannot happen. It also
catches the wrong type, which neither the hand-written Builder nor Lombok does.

### So when does Builder still earn its place in Python?

Not never. Three cases:

- **Construction spread across time or code.** If one function sets some fields, another sets
  more, and a third finally builds, you need an object to carry the half-finished state. A
  constructor can't do that.
- **A fluent API is the product.** SQLAlchemy's query builder exists because
  `.filter().order_by().limit()` reads better than one enormous call. That's Builder, and it's
  the right choice.
- **One builder producing many variants.** Set the shared fields once, then call `.build()`
  repeatedly with small changes between.

```
Rule of thumb for Python:

  Fixed set of fields, all known at once   →  dataclass or Pydantic model
  Needs validation                         →  Pydantic (or __post_init__)
  Needs immutability                       →  frozen dataclass + replace()
  Built up in stages, or a fluent API      →  Builder, genuinely
```

**Learn the pattern anyway.** You will read it constantly in Java, in SDKs, and in Python
libraries like SQLAlchemy. Recognising it matters even where you wouldn't write it. But don't
hand-roll a Builder in Python for a class with eight fields and one rule — that's a Pydantic
model, and pretending otherwise is cargo-culting Java into a language that solved the problem
differently.

---

## 10. Pitfalls, collected

```
1.  Expecting the compiler to catch a same-type parameter swap
      Java checks type and position, never names. Python doesn't check at
      all unless a type checker runs.

2.  Solving "some fields are missing" by adding more constructors
      Spreads the same problems across more places. In Java many
      combinations can't even be written. In Python a second __init__
      silently replaces the first.

3.  Using a Map or dict to bundle fields
      Removes every compile-time check. Wrong key does nothing at all;
      wrong type fails later, far from the mistake.

4.  Validating inside the collector instead of at the real entry point
      The collector gathers. The checkpoint is where the object is built.

5.  Setters that return nothing
      Fluent chaining can't work without return this / return self.

6.  Leaving the constructor public in Java after adding build()
      Until it's private, the Builder is optional and so is validation.

7.  Presenting the Python sentinel-key trick as real enforcement
      It's a speed bump. Python has no private. If you need the guarantee,
      validate in __init__ or __post_init__ instead.

8.  Copying a mutable field by reference instead of defensive-copying
      The "finished, checked" object can still change from outside.
      Compiles fine, looks fine, breaks the entire promise.

9.  Python — a mutable default argument (phones=[])
      Evaluated once at def time, so every builder shares one list.
      Use None, or field(default_factory=list).

10. Assuming Lombok's @Builder validates or copies collections
      It generates structure only. Validation is yours; collections need
      @Singular.

11. Reaching for Builder on every class
      A Point with x and y doesn't need one. The boilerplate has to be
      earned by field count and validation weight.

12. Hand-rolling a Builder in Python out of habit
      Keyword args, defaults and Pydantic cover most of what Builder is
      for in Java. Use Builder when construction is genuinely staged.
```

---

## 11. Java ↔ Python glossary

| Concept | Java | Python |
|---|---|---|
| Bundle of named fields | a class, or `Map<String,Object>` | `@dataclass`, or a `dict` |
| Overloaded constructors | allowed, by type and order | not available; last `__init__` wins |
| Named arguments at the call site | not available | keyword arguments |
| Optional fields | more constructors, or Builder | default parameter values |
| Force keyword-only calls | not available | `@dataclass(kw_only=True)` |
| Validation checkpoint | `build()` | `__post_init__`, or a Pydantic validator |
| Private constructor | `private` — enforced | no equivalent; convention only |
| Nested builder class | `static class Builder` | `class Builder:` inside the class |
| Defensive copy | `new ArrayList<>(x)` | `list(x)` |
| Mutable default trap | doesn't exist | `def f(x=[])` — shared across calls |
| Generated boilerplate | Lombok `@Builder` | `@dataclass` (standard library) |
| Immutable + modified copy | Lombok `@Value` + `@With` | `@dataclass(frozen=True)` + `replace()` |
| Type validation on construction | not built in | Pydantic |

**Terms**

| Term | Plain meaning |
|---|---|
| Telescoping constructors | Each constructor calls a slightly smaller one, adding one field |
| Builder | A helper object that collects values, validates, then builds the real object |
| `build()` | The method that validates and returns the finished object |
| Fluent chaining | Each setter returns the same object, so calls link together |
| Nested class | A class inside another class, able to reach its private members |
| Defensive copy | A brand-new copy of a mutable field, so the original can't affect it later |
| Mutable | Contents can change after creation — a list, a dict |
| Immutable | Contents can never change after creation |
| Lombok | A Java library that generates boilerplate from annotations |
| `@dataclass` | Python's standard-library equivalent: generates `__init__` and more |
| `__post_init__` | Runs straight after a dataclass's generated `__init__` — the validation hook |
| Pydantic | Python library validating types and values at construction time |

---

## 12. Interview questions

**1. Why is one large constructor bad for a class with many fields?**
Unreadable, because the values carry no labels at the call site. Silently breakable, because
same-type parameters can be swapped with no warning. Fragile, because adding one field means
updating every caller.

**2. What are telescoping constructors and why avoid them?**
Each constructor calls a slightly smaller one, adding one field, to cover different combinations
of missing values. They spread the same readability and mistake-proneness problems across many
places instead of fixing them, and in Java overload rules mean not every combination can even be
written.

**3. Why is `Map<String, Object>` worse than it looks?**
It removes compile-time safety. A misspelled key fails completely silently — the field is simply
never set. A wrong type only fails at runtime, far from the mistake.

**4. What's the core idea of Builder?**
A helper object collects values using ordinary typed fields so the compiler can check them, and a
`build()` method validates and constructs the real object only once everything passes.

**5. Why must the real constructor be private in Java?**
So `build()` is the only route in, and validation can't be skipped. A public constructor makes
the Builder optional.

**6. Why must the Builder be nested inside the class it builds?**
Because the constructor is private, and only code inside the same class can call a private
constructor. An outside Builder has no way to reach it.

**7. What must a setter return for chaining to work?**
The builder itself — `this` in Java, `self` in Python. Returning nothing leaves nothing to call
the next setter on.

**8. What's a defensive copy and why does Builder need one?**
A brand-new copy of a mutable field's contents rather than a copy of the reference. Without it,
the builder's list and the finished object's list are the same list in memory, so changes made
through the builder after `build()` silently change the "finished" object.

**9. What does Lombok's `@Builder` generate, and what doesn't it?**
It generates the structure: nested builder, chainable setters, `build()`. It does not add your
validation rules, and it doesn't defensive-copy collections unless you add `@Singular`.

**10. Difference between `@Builder` and `@With`?**
`@Builder` constructs a new object safely the first time. `@With` produces a modified copy of an
existing immutable object without changing the original.

**11. Which of Builder's problems don't exist in Python, and why?**
Four of the six. Keyword arguments fix the unreadable call and, with `kw_only=True`, make a
same-type swap impossible to write. Default parameter values fix missing fields, the need for
extra constructors, and the 2ⁿ combination explosion. What remains is validation, which
`__post_init__` or Pydantic handles inside the constructor.

**12. When is Builder still the right call in Python?**
When construction is genuinely staged across different places or times, when a fluent API is the
point (SQLAlchemy's query builder), or when one builder produces many variants. For a fixed set
of fields known at once, a dataclass or Pydantic model is the better answer.

---

## 13. Check yourself

1. List the three problems from Section 1 that appear when all fields go into one constructor.
2. Explain why Java can't distinguish `Student(String name, double psp)` from
   `Student(String universityName, double psp)`, and what happens instead in Python when you
   define `__init__` twice.
3. Why does a dict miss a misspelled key while a class catches it?
4. Write out the four fixes from Section 5 and the problem each one solves.
5. Explain why a Builder setter must return the builder rather than nothing.
6. Explain why the Builder must be nested inside the class in Java — and why the Python
   equivalent isn't real enforcement.
7. Write a snippet showing a shared list letting a built object change after `build()`.
8. Give the fix for question 7 and say why it works.
9. Predict the output of `add_phone("111")` then `add_phone("222")` with a `phones=[]` default,
   then run it. Explain the result.
10. Name three places Builder already runs that you've used without knowing the name.
11. Take the Section 1 `Student` and write it three ways in Python: hand-rolled Builder, frozen
    dataclass, Pydantic model. Which is shortest? Which gives the strongest guarantee?
12. Name one situation where you'd still write a Builder in Python, and justify it.

---

## 14. Homework

```
1. Build the full Student + Builder in BOTH languages, with at least two
   validation rules of your own.

2. Now write the same class as a Pydantic model. Compare the line counts
   and write two sentences on what each version guarantees that the other
   doesn't.

3. Ask an AI assistant for a Builder with at least one list or dict field,
   in either language. Check whether the finished object can still be
   changed from outside after build(). Paste the buggy line and your fix
   into your README.

4. Run the mutable-default-argument example from Section 6 and paste the
   output. Explain in one sentence why the second call sees the first
   call's data.

5. Find one real Builder in a library you already use — StringBuilder,
   OkHttp, SQLAlchemy, an LLM client. Write down which part is the builder
   and which part is build().

6. Push to GitHub — branch: builder-lecture-complete
```

---

*Post-read · Design Patterns 02 of 10 · Previous: Singleton · Next: Factory*
