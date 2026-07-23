# Low Level Design (LLD) — Introduction

*Class notes, turned into a tutorial.*

---

## Agenda

Here is what we will cover in this session:

1. Intro to LLD
2. What is LLD
3. Why LLD is so important
4. Module overview
5. Intro to OOP
6. Procedural programming
7. OOP

**How this course works:**

```
Attend the class  ──►  Complete the assignment  ──►  Clear the contest
```

> Whatever I know, I teach everything. Nothing is held back. Your job is to show up, do the assignments, and clear the contests.

---

# 1. What is LLD?

**LLD = Low Level Design.**

Before we define it, let me tell you a story, because that is the easiest way to understand it.

## The startup story

Almost everyone, at some point in their life, dreams of starting a **startup**.

Now, as a **software engineer**, if you start a startup, your primary product is **software**. You write some code, and that code will be used by many people.

So the picture looks like this:

```
   [ Client 1 ] ─┐
                 │            ┌────────────────────────┐
   [ Client 2 ] ─┼─────────► │        SERVER          │
                 │            │  A very powerful       │
   [ Client 3 ] ─┘            │  computing machine     │
                              │  with a lot of RAM     │
      clients                 └────────────────────────┘
```

Many **clients** (users on phones, laptops, browsers) send requests to your **server**. The server is just a powerful machine with a lot of RAM and CPU that runs your code and sends back answers.

If your product is good, it becomes **famous**. And when it becomes famous:

```
   Product becomes famous  ──►  Lots of business / customers coming in 🎉
```

Sounds great, right? But now a real problem appears.

## The problem: can one machine serve everyone?

Ask yourself one simple question:

> Can a **single laptop**, with a certain amount of RAM and CPU, handle an **infinite** number of requests?
>
> Can it serve **infinite** requests?

**Answer: NO.** ❌

### A simple example everyone has felt

Open **too many apps** on your phone at the same time. Does it stay smooth?

No — it **hangs**. It slows down and becomes unresponsive.

This slowing-down under heavy load has a name:

```
   ┌─────────────┐
   │  Throttling │
   └─────────────┘
```

The **same thing** happens to your server. When a *lot* of requests come at once, the server also gets throttled — it slows down or stops responding.

## So what do we do? Increase the capacity

When the server can't handle the load, you **increase the capacity**. There are two ways.

**Option 1 — Buy a bigger machine.**
**Option 2 — Add more resources (RAM + SSD) to the same machine.**

Both of these mean: *make one single machine stronger.*

```
   ┌──────┐                    ┌────────────────────┐
   │      │      ───►          │                    │
   │      │                    │                    │
   └──────┘                    │                    │
   Single                      │   Bigger Machine   │
   Machine                     │                    │
                               └────────────────────┘
   └──────────────── Vertical Scaling ──────────────┘
```

Making **one machine bigger and stronger** is called **Vertical Scaling**.

### Two big problems with vertical scaling

1. **There is a limit.** You cannot keep making one machine bigger forever. At some point, no bigger machine exists.

2. **Single Point of Failure.** If that one machine goes down, your **entire business becomes zero**. Everything depended on that one box.

```
   ⚠️  Single Point of Failure
       One machine dies  →  whole business is down
```

## The better way: buy more machines

Instead of one giant machine, use **many normal machines** working together.

```
   Buy more machines  ──►  Horizontal Scaling
```

Adding **more machines** is called **Horizontal Scaling**.

But now a new question: if there are many machines, *who decides which machine handles which request?* That job goes to a **Load Balancer**.

```
 [ Client ] ─┐         ┌───────┐       ┌────────┐
             │         │   L   │ ────► │   M1   │ ──┐
             │         │   O   │       └────────┘   │
 [ Client ] ─┼───────► │   A   │ ────► ┌────────┐   │      ┌──────┐
             │         │   D   │       │   M2   │ ──┼────► │  DB  │
             │         │   B   │       └────────┘   │      └──────┘
 [ Client ] ─┘         │   ⋮   │ ────► ┌────────┐   │
                       │   R   │       │   M3   │ ──┘
                       └───────┘       └────────┘
   clients          Load Balancer      servers        database
```

The **Load Balancer** takes all incoming requests and spreads them evenly across machines M1, M2, M3. All machines read and write to a shared **database (DB)**.

## HLD vs LLD — the key distinction

Now stop and notice something.

> Up to now, did I talk about **any code**? Did I say *how* to code the server?

**No.** I only talked about the **components** of the system — clients, server, load balancer, machines, database — and how they connect.

This type of design, where you talk about the **big components of a system** and **not** the actual code, is called:

```
   HLD  =  High Level Design
```

Once you decide **what components** will be in your system, the next step is:

> You have to **build** it. → **[ Implement ]** → **Code**

And *that* part — turning components into actual, well-structured code — is:

```
   LLD  =  Low Level Design
```

**In one line:**

| Design type | Talks about | Example |
|-------------|-------------|---------|
| **HLD** (High Level Design) | The components of the system and how they connect | Clients, load balancer, servers, DB |
| **LLD** (Low Level Design) | How to actually write the code for those components | Classes, objects, functions, relationships |

---

# 2. Why is LLD so important?

Here is a truth that surprises many beginners:

```
   Coding          ──►   Easy
   Design & Thinking ─►   Hard
```

Writing *some* code that works is easy. **Designing** good code — thinking about how to structure it — is the hard part. And that thinking is exactly what LLD trains.

## The Google insight

There was a famous idea shared around *Software Engineering at Google*:

> To solve a **single problem**, there are **multiple ways** to write the code.

So when you sit down to code, your **goal** can be one of two things:

```
            ┌─►  Just write some code that works (only for now)
   goal ────┤
            └─►  Write code that is useful in the future also  =  GOOD CODE
```

Good code is:

- **Maintainable** — easy to fix and update later.
- **Reusable** — you can use the same code in other places.
- **Extensible** — you can add new features without breaking old ones.

## The 12% that decides everything

Here is a number worth remembering:

```
   A Software Engineer spends only ~12% of their time actually writing code.
```

What about the other **88%**?

```
                  ┌──►  Planning
                  │
        88%  ─────┼──►  Debugging
                  │
                  ├──►  KT (Knowledge Transfer)
                  │
                  └──►  Solving problems
```

Now here is the important part:

> That small **12%** (how you write the code) **decides** the other **88%**.

If you write messy code in that 12%, you will spend the 88% suffering — debugging, explaining, and fixing. If you write **good, well-designed code**, the other 88% becomes much easier.

**So the whole question of this course is:** *How do we make the best use of that 12%?*

That is what LLD teaches you.

## LLD in interviews

Competition has increased a lot nowadays. So **even for a fresher**, LLD is now asked in interviews.

There are **3 types of LLD rounds** you may face:

```
   ┌─────────────────┐
   │  Theoretical    │  ──►  Normal service-based companies
   └─────────────────┘

   ┌─────────────────┐
   │  LLD round      │  ──►  Top / mid product-based companies
   └─────────────────┘        (you implement it)

   ┌─────────────────┐
   │  Machine Coding │  ──►  Design  +  end-to-end working code
   └─────────────────┘
```

- **Theoretical** — they ask you to explain concepts. Common in normal/service companies.
- **LLD round** — you actually design and implement. Common in top and mid product-based companies.
- **Machine Coding** — the hardest: full design **plus** a complete working program.

---

# 3. Module Overview

Here is how the LLD course is broken down:

```
   LLD 1  ──►  Learning advanced language concepts

   LLD 2  ──►  SOLID principles  &  Design Patterns  [about 9 to 10 of them]
              +  UML Diagrams

   LLD 3  ──►  Machine Coding
```

For **LLD 3 (Machine Coding)**, we will build real projects:

| Project | Built with |
|---------|-----------|
| Parking Lot | Normal Python |
| Splitwise App | FastAPI |
| Book My Show | FastAPI |
| Tic Tac Toe | Normal Python |

So by the end, you will not just *know* the theory — you will have **built real systems**.

---

# 4. Introduction to OOP

**OOP = Object Oriented Programming.**

To understand OOP, first understand the word **paradigm**.

```
   Programming Paradigm  =  a way of doing something
                         =  a way of writing code
```

There are several programming paradigms:

```
   ⇒  Procedural
   ⇒  OOP
   ⇒  Reactive
   ⇒  Functional
```

In this course we focus on the first two: **Procedural** and **OOP**. To understand *why* OOP exists, we must first see how procedural programming works — and where it breaks.

---

# 5. Procedural Programming

```
   Procedural Programming  ──►  Example language: C
```

The core idea of procedural programming:

> **Write everything in terms of functions.**

Functions are the center of the whole program. Everything is a function.

## Example: a Student Management system

Imagine we are building a system to manage students. In procedural style, we write a bunch of functions:

```c
getName();
getStudent();
solveAssignments();
updateBatch();
```

Notice something about these — they are all **actions**. They describe *how to do something*.

There are two kinds of things in any system:

```
   Active   →  How to DO something   →  (functions / procedures)
   Passive  →  Data / Entity          →  (the actual information)
```

In procedural programming, the **functions (active part)** are the boss. The data just sits there.

## A little history

When software engineering started, people used to code in **procedural** style.

Think about it — when computers were first invented, what was the very first thing a computer was used to do?

```
   Computer's first job  ──►  Calculation
```

Calculation is naturally a *function-style* task: take input, do steps, give output. So procedural made perfect sense back then.

But as systems grew bigger:

```
   As the system grows  ──►  the number of functions also keeps growing
```

Soon you have hundreds of functions floating around. And that is where the trouble begins.

## The major problem with procedural code

> What is the major issue if your **entire code is in terms of functions**?

**Problem #1: Data gets mixed up.** 🔴

Look at these functions that all touch a `student`:

```c
updateBatch(student, batch);
giveGraceMarks(student);
increasePsp(student);
```

Any function, anywhere in the program, can grab the `student` data and change it. In C, when you use a `struct`:

```c
struct Student {
    char name[50];
    int   batch;
    float psp;      // psp = problem solving percentage
};
```

> A `struct` makes **everything public**. So **every function can change everything.**

There is no protection. Fifty different functions can all reach in and modify the student's data. When something goes wrong, you have no idea *which* function corrupted the data. This is the "data got mixed up" problem.

In procedural programming:

```
   Function is the power.
```

The functions are in control, and the data is exposed to all of them. That freedom is exactly what causes the mess.

---

# 6. Object Oriented Programming (OOP)

Now let's flip our thinking.

In a **real system**, what do we actually think about **first**?

Not functions. We think about **Entities**.

## Example: Uber

Think about how Uber works. The first things that come to mind are the *things* involved:

```
   Uber
     ├──►  Car
     ├──►  Driver
     └──►  Customer
```

These are **entities** — real things in the system. Notice they are **nouns** (car, driver, customer), not actions.

So OOP flips the priority:

```
   Active   :  Entity  (objects)   →  Nouns   ←  now the BOSS
   Passive  :  Procedures                       ←  now secondary
```

In **procedural**, functions were active and data was passive.
In **OOP**, the **entities (objects)** are active, and the procedures serve them.

## The big idea: Data Ownership

This is the heart of OOP.

> **Each entity owns its own data.**

Let's take a course example — call it **CTT** — with these entities and their data:

```
   CTT
     ├──►  Student  →  10
     ├──►  Class    →  20
     ├──►  Mentor   →  15
     └──►  Batch    →  20
                       ────
                        65
```

Here, the `Student` entity owns its 10 pieces of data. The `Mentor` owns its 15. Nobody else reaches in and messes with them.

```
   Entity owns the entire data.   ←  Data Ownership
```

## Restaurant analogy for data ownership

Think of a **restaurant**. 🍽️

The kitchen owns the food. You (the customer) don't walk into the kitchen and start cooking or rearranging things. You place an order, and the kitchen decides how to handle its own food.

That is **data ownership** — the entity that owns the data is the only one allowed to change it. Outsiders must go through the entity, not around it.

## Procedural vs OOP — the same code, two ways

Let's make it concrete. Here is the Student example in both styles.

**Procedural style (data is exposed to everyone):**

```python
# The data is just a loose dictionary — anyone can change anything
student = {"name": "Anita", "batch": 1, "psp": 0}

def update_batch(student, batch):
    student["batch"] = batch          # any function can reach in

def increase_psp(student, amount):
    student["psp"] += amount

# Nothing stops some random code from doing this:
student["psp"] = 99999                 # 🔴 data got mixed up!
```

**OOP style (the entity owns and protects its data):**

```python
class Student:
    def __init__(self, name, batch):
        self.name  = name
        self.batch = batch
        self.psp   = 0                 # the Student owns this data

    def update_batch(self, batch):     # only Student's own methods
        self.batch = batch             # are meant to change it

    def increase_psp(self, amount):
        self.psp += amount


# Now you talk TO the entity, not around it:
s = Student("Anita", batch=1)
s.update_batch(2)
s.increase_psp(10)

print(s.name, s.batch, s.psp)          # Anita 2 10
```

See the difference? In the OOP version, the `Student` **owns** its `name`, `batch`, and `psp`. The proper way to change them is by asking the `Student` object through its own methods. The data and the behaviour live **together**, inside one entity.

## One honest trade-off

OOP is not magic — it has a cost:

```
   OOP is a bit slow compared to procedural.
```

Procedural code can be faster because it is simpler and closer to raw calculation. OOP adds a layer of structure (objects, ownership), which costs a little speed. But in return you get code that is **maintainable, reusable, and extensible** — and for large, growing systems, that trade is almost always worth it.

---

# Quick Recap

Here is everything from today in one glance:

| Concept | Key idea |
|---------|----------|
| **HLD** | Design the **components** of a system (no code yet) |
| **LLD** | **Implement** those components as good code |
| **Vertical Scaling** | Make one machine bigger → has a limit + single point of failure |
| **Horizontal Scaling** | Add more machines + a load balancer → no single point of failure |
| **Why LLD** | Good code = maintainable, reusable, extensible |
| **12% rule** | You code ~12% of the time, but it decides the other 88% |
| **Paradigm** | A way of writing code (Procedural, OOP, Reactive, Functional) |
| **Procedural** | Everything is a **function**; data is exposed → gets mixed up |
| **OOP** | Everything is an **entity (object)**; each entity **owns its data** |

**The one sentence to carry forward:**

> Procedural asks *"what functions do I need?"*
> OOP asks *"what entities exist, and what data does each one own?"*

---

# What's Next

In **LLD 1**, we start learning the **advanced language concepts** we need before we can design well. After that come **SOLID principles, design patterns, and UML** (LLD 2), and finally **machine coding** real projects like Parking Lot, Splitwise, Book My Show, and Tic Tac Toe (LLD 3).

For now, make sure you are solid on one thing: **the difference between thinking in functions (procedural) and thinking in entities that own their data (OOP).** Everything we build from here stands on that idea.

*Attend the class → complete the assignment → clear the contest. See you in the next one.* 🚀
