# Object-Oriented Programming in Python
## Chapter 1 — Introduction to OOP

*A first-principles tutorial for students writing their first line of object-oriented code.*

---

## Before you begin

Hello.

I'm going to teach you Object-Oriented Programming. Not by giving you definitions to memorise — by letting you *discover* why every single feature exists.

Here's my promise to you:

> **You will never see a piece of syntax in this chapter before you understand the problem it was invented to solve.**

That's the deal. If I ever break it, you have my permission to stop reading.

### How this chapter works

Each topic follows the same journey:

```
   PROBLEM  ──►  you try it the obvious way
      │
      ▼
   IT BREAKS  ──►  and you see exactly why
      │
      ▼
   THINK  ──►  I ask, you answer, then we check
      │
      ▼
   PRINCIPLE  ──►  the underlying idea
      │
      ▼
   CODE  ──►  only now does syntax appear
```

Along the way you'll see these boxes:

> 🛑 **STOP AND THINK** — do not read past this until you've had a guess. Being wrong here is the point.

> 💡 **KEY IDEA** — the sentence worth remembering.

> ⚠️ **COMMON MISTAKE** — I've watched hundreds of students make this one.

> 🎯 **INTERVIEW** — this exact question gets asked.

> 🔁 **JAVA CORNER** — if you're also learning Java, here's how it differs.

### The chapter agenda

We follow this order, and we don't skip:

| # | Topic |
|:--|:--|
| 1 | Entities — what are we even modelling? |
| 2 | The Four Properties — 3 Pillars + 1 Principle |
| 3 | Abstraction — the Principle |
| 4 | Classes and Objects |
| 5 | Building your first class — fields, methods, members, state |
| 6 | Reference variables and the memory model |
| 7 | Constructor and `self` |
| 8 | The `static` idea — class-level members |
| 9 | Pass by value — simple values vs objects |
| 10 | `to_string()` → `__str__` |
| 11 | Encapsulation — Pillar 1 |

---

## Setting up your workspace

One minute of setup, then we start.

Make this folder structure:

```
uber_project/
└── uber/
    ├── __init__.py      ← empty file
    ├── driver.py        ← where we WRITE our class
    └── client.py        ← where we USE our class
```

```bash
mkdir -p uber_project/uber
cd uber_project
touch uber/__init__.py uber/driver.py uber/client.py
```

Why two files? Because they have two completely different jobs, and keeping them apart will teach you something important later:

| File | Job |
|:--|:--|
| `driver.py` | **Describes** what a driver is. Creates nothing. |
| `client.py` | **Uses** drivers. Creates them, calls them, prints them. |

To run your program, always do this from inside `uber_project`:

```bash
python3 -m uber.client
```

Note the **dot**, and no `.py` at the end. That's it — setup done.

---
---

# TOPIC 1
# Entities — What Are We Even Modelling?

---

## 1. The Problem

Imagine it's your first day as a software engineer at Uber.

Your manager walks over with a coffee and says:

> *"Hey. We're rebuilding the driver system from scratch. You're on it. Start today."*

She walks away.

You open your laptop. You create a brand new file. You put your fingers on the keyboard.

And then you stop.

Because you have absolutely no idea what to type on line 1.

You know Python. You know `print()`, `if`, `for`, lists, functions. But none of that helps you right now, because **"build Uber" is not a thing you can type.**

So let's figure out what you type first. Together.

---

## 2. Observation

Forget code for a minute. Just open the Uber app in your head and *look* at it.

What do you actually see on the screen?

```
   ┌─────────────────────────────┐
   │  📍 Your location            │
   │                             │
   │       🗺️  the map            │
   │                             │
   │  ┌───────────────────────┐  │
   │  │ 👤 Ashok      ⭐ 4.8  │  │
   │  │ 🚗 KA-01-AB-1234      │  │
   │  │ 💰 ₹247               │  │
   │  │ ⏱️  4 min away         │  │
   │  └───────────────────────┘  │
   └─────────────────────────────┘
```

Now notice something. That screen isn't showing you *code*. It's showing you **things**.

A person named Ashok. A car with a number plate. An amount of money. A journey that's about to happen.

Ashok is a *thing*. The car is a *thing*. The payment is a *thing*. The trip is a *thing*.

Hold that observation. We'll come back to it.

---

## 3. Wrong Assumptions

Before I tell you the answer, let me show you the two roads most beginners go down. Both are dead ends, and walking down them for a minute is genuinely useful.

### Wrong road #1: "I'll just make variables for everything."

This feels natural. You know variables. Let's use them.

```python
driver1_name = "Ashok"
driver1_rating = 4.8
driver1_is_online = True
driver1_car = "KA-01-AB-1234"

driver2_name = "Meera"
driver2_rating = 4.9
driver2_is_online = False
driver2_car = "KA-05-XY-9876"
```

Looks fine, right? It even runs.

Now let me ask you something.

> 🛑 **STOP AND THINK**
> Uber has around **5 million** drivers. How many lines is this file?

Four lines per driver × 5,000,000 drivers = **20 million lines of code.**

And that's before anyone takes a single ride.

But honestly? The line count isn't even the worst part. Look closer:

```python
driver1_name = "Ashok"
driver1_rating = 4.8
```

**What connects these two lines?**

Nothing. Absolutely nothing. To Python, these are two unrelated variables that happen to start with the same letters. The fact that they describe *the same human being* exists only inside your head.

Delete `driver1_rating` and Python won't complain. Set `driver1_rating = "hello"` and Python won't complain. Swap `driver1_name` with `driver2_name` and Python won't complain.

The relationship is invisible to the computer.

### Wrong road #2: "I'll start with the hardest part — the map."

Also tempting. The map looks impressive, so let's build it.

But stop and ask: **what goes on the map?**

Drivers. You need drivers before you can put drivers on a map.

And what does a driver need? A name, a rating, a car, a location.

So you can't start with the map. You have to start further back.

---

## 4. Think

Let me ask you a few questions. Actually answer them before reading on.

**Question 1:** When an architect designs a hospital, what does she draw first — the door handles, or the rooms?

**Question 2:** When you describe your college to a friend, do you list every brick? Or do you say "there are students, teachers, classrooms, and exams"?

**Question 3:** Look back at the Uber screen. If you had to describe that screen to someone over the phone using only **nouns**, which nouns would you use?

...

Take a second. I'll wait.

...

Here's what I'd say: **driver, customer, car, payment, trip.**

Five nouns. That's it. That's the whole screen.

---

## 5. First Principle

Now here's the idea underneath all of this. It's simple, and once you see it you can't unsee it:

> 💡 **KEY IDEA**
> **Software exists to model the real world.**
> **The real world is made of things.**
> **So find the things first.**

Your program isn't fundamentally made of loops and if-statements. Those are just the machinery. Your program is fundamentally about **drivers, customers, trips, and payments** — and the loops exist to move those things around.

So the very first thing you type isn't code at all.

It's a **list of things**.

---

## 6. Solution — The Entity

Those "things" have a name in software design.

> 📖 **Definition**
> **An Entity is any person, place, thing, or concept from the real world that you want to represent inside your program.**

Notice the definition arrived *after* you already understood it. That's how it should feel.

### Uber's entities

```
                          UBER
                            │
       ┌─────────┬──────────┼──────────┬─────────┐
       │         │          │          │         │
       ▼         ▼          ▼          ▼         ▼
    Driver   Customer    Vehicle    Payment    Trip
```

Five nouns. The same five you came up with yourself.

### Entities everywhere

Once you have this lens, you can point it at any app you've ever used:

| Company | Entities |
|:--|:--|
| **Swiggy** | Customer, Restaurant, Dish, Order, DeliveryPartner |
| **Amazon** | Product, Cart, Order, Seller, Payment, Review |
| **Netflix** | User, Video, Playlist, Subscription, Profile |
| **WhatsApp** | User, Message, Chat, Group, MediaFile |
| **Instagram** | Account, Post, Comment, Story, Follower |
| **Bank** | Account, Customer, Transaction, Loan, Branch |
| **Hospital** | Patient, Doctor, Appointment, Prescription, Bill |
| **College** | Student, Faculty, Course, Batch, Exam |
| **Airline** | Flight, Passenger, Ticket, Crew, Aircraft |

> 🛑 **STOP AND THINK**
> Pick any app on your phone right now. Open it. Write down five nouns you can see.
> Congratulations — you just did system design.

---

## 7. The Code (and why it isn't enough yet)

Here's the honest part: an entity is an *idea*, not syntax. There's no `entity` keyword.

But we can still write the "before" picture, so you feel the pain that the next topics will cure.

```python
# uber/client.py
# The "loose variables" approach — DO NOT write real code like this.

driver1_name = "Ashok"
driver1_rating = 4.8
driver1_is_online = True

driver2_name = "Meera"
driver2_rating = 4.9
driver2_is_online = False


def print_driver(name, rating, is_online):
    status = "online" if is_online else "offline"
    print(f"{name} | rating {rating} | {status}")


print_driver(driver1_name, driver1_rating, driver1_is_online)
print_driver(driver2_name, driver2_rating, driver2_is_online)
```

### Output

```
Ashok | rating 4.8 | online
Meera | rating 4.9 | offline
```

---

## 8. What Just Happened?

**What happened:** It worked. We printed two drivers.

**Why it's still bad:** Look at that function signature.

```python
def print_driver(name, rating, is_online):
```

Three parameters for a driver with three pieces of data. Now imagine a real driver — name, rating, online status, driver ID, phone number, car number, licence number, current latitude, current longitude, total trips, joining date, bank account.

```python
def print_driver(name, rating, is_online, driver_id, phone, car_number,
                 licence, lat, lng, total_trips, joined_on, bank_account):
```

Twelve parameters. And here's the killer:

> ⚠️ **The day you add a 13th field, every single function that takes a driver breaks.**

Every call site. Across the whole codebase. Because there is no such thing as "a driver" in your program — there are only twelve loose values that you have to keep passing around together and hope nobody drops one.

**How Python executes this:** it creates six independent variables in memory with no relationship between them, and a function that has no idea those six values belong together.

The computer doesn't know what a driver is. **Only you do.** And that's the problem we spend the rest of this chapter fixing.

---

## 9. Real-World Analogy

Imagine a hospital where patient information is stored like this:

- All the **names** in one drawer
- All the **blood groups** in a second drawer
- All the **allergies** in a third drawer

Every drawer is neatly sorted. Nothing is missing. The filing is perfect.

Now a patient arrives unconscious and the doctor needs to know: *does this person have a penicillin allergy?*

She has to open three drawers and hope the ordering matches.

**That's your loose-variables program.** The data is all there. The *connection* between the data is not.

What you actually want is **one file per patient**, with everything about that person inside it.

That file is what we're building towards.

---

## 10. The Big Question From Class

Here's a question that comes up every single time, and the answer is more interesting than you'd expect.

> **"Does the real Uber system only have these 5 entities?"**

Have a guess.

...

**No. Not even close.** Real Uber has hundreds — promotions, surge zones, support tickets, driver documents, wallets, referrals, ratings, cancellation policies.

But now here's the part that actually matters. Think about what happens when you tap **Book Ride**:

```
   You tap one button
        │
        ▼
   Find drivers near you        ← millions of GPS points to search
        │
        ▼
   But "near" by road, not by air   ← a river, a one-way street, a jam
        │
        ▼
   Compute the fastest route    ← a graph of the whole city's roads
        │
        ▼
   Predict arrival time         ← a machine-learning model
        │
        ▼
   Offer to a driver, wait, retry
        │
        ▼
   Take payment, check fraud
```

**Not one of those steps is on our five-entity diagram.** Not the map search, not the road graph, not the ETA prediction.

So did we get it wrong?

No. **We chose the entry points.** We picked the handful of things through which the entire system can be *discussed*.

And watch what that buys us. Once `Driver` and `Trip` exist as real things in code, all that horrifying complexity gets somewhere to hide:

```python
nearest = dispatch.find_nearest(customer.location)
trip = Trip(customer, nearest)
```

The map search lives inside `find_nearest`. The road graph lives inside it. The ML model lives inside it.

But *your* conversation stays at the level of drivers and trips.

> 💡 **KEY IDEA**
> **You identify the main five high-level entities so that you can start building step by step.**
> **Choosing the right five is exactly what makes the other hundred manageable.**

And notice what you just did there — you took something enormous and made it look small.

**That has a name.** We'll get to it in Topic 3.

---

## 11. 🎯 Interview Questions

**Q1. What is an entity in object-oriented design?**

> Any person, place, thing, or concept from the real world that the program needs to represent. Entities are identified before any code is written — they become the classes of the system.

**Q2. Uber has hundreds of concepts. Why do we start by listing only five?**

> Because the goal isn't completeness, it's *tractability*. The five high-level entities are entry points through which the whole system becomes discussable. Every remaining concept attaches to one of them as you go deeper.

**Q3. How would you identify entities for a system you've never seen?**

> Describe the main user journey out loud, using only nouns. The nouns that keep recurring — and that hold data *and* do things — are your entities.

---

## 12. ⚠️ Common Mistakes

| Mistake | Why it's wrong |
|:--|:--|
| Listing 30 entities on day one | You'll drown. Start with 5 and expand. |
| Choosing **actions** as entities (`Login`, `Search`) | Entities are nouns. `Login` is something a `User` *does*. |
| Choosing **screens** as entities (`HomePage`) | UI changes constantly. Entities model the business, not the display. |
| Skipping this step entirely | Then your classes get invented accidentally, one bug at a time. |

---

## 13. Summary

We started with "build Uber" and no idea what to type.

We tried loose variables and discovered that the computer has no concept of "a driver" — only unrelated values we hoped to keep in sync.

We realised software models reality, reality is made of things, so we should **find the things first**.

Those things are called **entities**, and they become the classes of our system.

---

## ✓ Key Takeaways

- **An entity** is any real-world person, place, thing, or concept your program must represent.
- Entities are found by describing the system **in nouns**, before writing code.
- Uber's core five: `Driver`, `Customer`, `Vehicle`, `Payment`, `Trip`.
- Real systems have hundreds of concepts. You pick the **high-level five** as entry points — that choice is what makes the rest manageable.
- Loose variables fail not because they're long, but because **the computer can't see the relationship** between them.

---

## ✓ Practice Questions

1. List five entities for **Swiggy**. Now list five more you deliberately left out — and justify the split.
2. A student says `PlaceOrder` should be an entity in Amazon. Explain, kindly, why it shouldn't — and what it should be instead.
3. For a **Hospital Management System**, write down the five entities. Then write, in one sentence each, what data each one holds.
4. Take the loose-variable code from Section 7 and add a `phone_number` for each driver. Count how many lines you had to touch. Now imagine 5 million drivers.

---

## ✓ Mini Assignment

Write a file `entities.md` containing:

- Your five entities for **Netflix**
- For each entity: three pieces of data it holds, and two things it can do
- One paragraph on why you rejected two other candidates

No code. This is a *thinking* assignment, and thinking is the part most people skip.

---

## ✓ Real-World Exercise

Open **any** app on your phone. Not a tutorial app — a real one you actually use.

1. Screenshot the main screen.
2. Circle every distinct "thing" you can see.
3. Name each circle with a single noun.
4. Now open a second screen in the app and see how many new nouns appear.

If your original five still cover most of what you see — **you chose well.** That's the same skill senior engineers use in design meetings, and you just practised it.

---
---

# TOPIC 2
# The Four Properties — 3 Pillars + 1 Principle

---

## 1. The Problem

You now have your five entities. You're ready to write code.

But before you do, there's a question you're going to be asked in every interview of your career, and most people get it slightly wrong:

> **"How many pillars does OOP have?"**

You've probably already heard the answer somewhere: *four*.

Encapsulation. Inheritance. Polymorphism. Abstraction.

Fine. Memorise it, move on?

**No.** Because if you memorise that list, you will spend the next two years slightly confused about what abstraction actually *is* — and you won't know why you're confused.

Let's fix that now, properly.

---

## 2. Observation

Here's something odd. Let me show you three of those four words as they appear in actual code:

```python
class Driver:
    def __init__(self, rating):
        self._rating = rating          # ← encapsulation. You can SEE it.


class PremiumDriver(Driver):           # ← inheritance. You can SEE it.
    def commission(self):              # ← polymorphism. You can SEE it.
        return 0.10
```

Three of them are **things you type**. `_rating`. The brackets in `class PremiumDriver(Driver)`. The redefined method.

Now write me the line of code that "does abstraction."

Go on. What's the keyword?

...

There isn't one.

> 🛑 **STOP AND THINK**
> Three of the four have syntax. One doesn't.
> Doesn't that seem like a strange thing to ignore?

---

## 3. Wrong Assumption

The wrong mental model — and it's extremely common — looks like this:

```
   OOP has 4 tools:

   [Encapsulation]  [Inheritance]  [Polymorphism]  [Abstraction]

   ← four equal things, sitting side by side →
```

Students carry this picture for years. And then in an interview someone asks *"how do you achieve abstraction?"* and they freeze, because in this picture abstraction isn't achieved — it just **is**, like the other three.

The picture is wrong.

---

## 4. Think

Let me ask it a different way.

**Question:** Is "winning a cricket match" a cricket skill?

Think about that. Batting is a skill. Bowling is a skill. Fielding is a skill.

Is *winning* a skill in the same sense?

...

No. **Winning is what happens when you apply the skills well.** It's the outcome, not a technique. You can't practise "winning" directly — you practise batting, bowling and fielding, and winning results.

Now:

**Question:** Is "being healthy" an exercise?

Running is an exercise. Sleeping well is a habit. Eating properly is a habit.

Is *health* one of those? No. **Health is the result.**

> 🛑 **STOP AND THINK**
> Which one is abstraction — is it a *skill*, or is it a *result*?

---

## 5. First Principle

> 💡 **KEY IDEA**
> **Three of them are mechanisms. One of them is the outcome.**

```
   ┌───────────────────┐
   │   Encapsulation   │──┐
   ├───────────────────┤  │
   │   Inheritance     │──┼───►  THE 3 PILLARS
   ├───────────────────┤  │      mechanisms · things you type · the HOW
   │   Polymorphism    │──┘
   └───────────────────┘
                                        │
                        you use them    │  in order to achieve
                                        ▼
   ┌───────────────────┐
   │   Abstraction     │──────────►  THE PRINCIPLE
   └───────────────────┘             the outcome · the goal · the WHY
```

Read it as one sentence, out loud:

> **We use encapsulation, inheritance and polymorphism *in order to achieve* abstraction.**

Abstraction is not a fourth tool standing beside the other three.

**It is the reason the other three exist.**

---

## 6. Solution — The Correct Mental Model

| | The 3 Pillars | Abstraction |
|:--|:--|:--|
| What is it? | Mechanisms, techniques | A goal, an outcome |
| Do you type it? | ✅ Yes | ❌ No keyword exists |
| Can you point at it in code? | Yes — this line, right here | Only at the *effect* |
| Relationship | The tools | What the tools are **for** |
| Cricket analogy | Batting, bowling, fielding | Winning |

### Where the "4 pillars" idea comes from

Textbooks — including *The Complete Reference: Java*, which you'll meet in your Java course — list four. They're not lying to you. It's a simplification, and it's fine for a first pass.

But the sharper version is more useful, and it will make you sound like someone who actually understands the subject rather than someone who memorised a list.

---

## 7. Real-World Analogy

Think about a **restaurant kitchen**.

| In the kitchen | In OOP |
|:--|:--|
| Knife skills | Encapsulation |
| Heat control | Inheritance |
| Seasoning | Polymorphism |
| **A delicious meal** | **Abstraction** |

Nobody walks into a kitchen and says "today I'll practise delicious-meal." You practise chopping, heat and seasoning — and the meal is what comes out.

Same here. Nobody types "abstraction." You write encapsulated classes, sensible hierarchies and swappable behaviours — and abstraction is what comes out.

---

## 8. 🎯 Interview Questions

**Q1. How many pillars does OOP have?**

> A strong answer:
> *"Four properties are usually listed. Three of them — encapsulation, inheritance and polymorphism — are mechanisms you actually write in code. Abstraction is the principle you achieve by applying those three; there's no keyword for it."*
>
> This is correct **and** it shows you understand the relationship rather than having memorised a list. Interviewers notice the difference immediately.

**Q2. How do you achieve abstraction?**

> By applying the three pillars. Encapsulation hides data behind methods. Inheritance lets you express "is-a" without repetition. Polymorphism lets one operation work across many types. The combined result is a system that can be used without being understood.

**Q3. Is abstraction the same as encapsulation?**

> No, and this is the classic follow-up.
> - **Encapsulation** is a mechanism: hide the data, expose controlled methods.
> - **Abstraction** is the outcome: the user works with a simple idea instead of the complex reality.
>
> One-liner: *encapsulation is how you hide it; abstraction is what the user sees instead.*

---

## 9. ⚠️ Common Mistakes

| Mistake | Correction |
|:--|:--|
| "Abstraction and encapsulation are the same thing" | One is a mechanism, one is the goal. |
| "There's an abstraction keyword" | There isn't. In Python there's `ABC`, but that's a *tool for enforcing interfaces* — not abstraction itself. |
| Listing the four pillars without understanding the relationship | Fine for a quiz. Fails the follow-up question. |
| Thinking abstraction is "advanced" | It's the most beginner-relevant idea in OOP. You use it every time you call a function you didn't write. |

---

## 10. Summary

Three of OOP's four famous properties are things you type. One isn't.

That one — **abstraction** — is the *result* of using the other three well. It's the win, not the skill; the meal, not the knife.

That's why the next topic is entirely about abstraction, before we write a single class.

---

## ✓ Key Takeaways

- **Pillars (mechanisms):** Encapsulation, Inheritance, Polymorphism.
- **Principle (outcome):** Abstraction.
- The relationship: *we use the pillars in order to achieve abstraction.*
- Abstraction has **no keyword** — that's the clue that it's different in kind.
- In an interview, explain the *relationship*, not the list.

---

## ✓ Practice Questions

1. Explain the pillars-versus-principle distinction using an analogy that is **not** cricket, kitchen, or health.
2. A friend says: "Abstraction is when you hide data using `private`." What two mistakes are in that sentence?
3. Which pillar is most responsible for abstraction, in your opinion? Defend your answer — there's no single right one.

---

## ✓ Mini Assignment

Write a **one-page explanation** of the four properties aimed at a student one year junior to you.

Constraint: you may not use the words *hide*, *reuse*, or *many forms*. Those are the memorised words. Find your own.

---

## ✓ Real-World Exercise

Ask three people who already know OOP: *"How many pillars does OOP have, and is abstraction one of them?"*

Note how many say four without hesitation. Then ask the follow-up: *"So how do you achieve abstraction?"*

Watch what happens. That pause is exactly the gap this topic just closed for you.

---
---

# TOPIC 3
# Abstraction — The Principle

---

## 1. The Problem

Let's go back to the Uber app.

You tap **Book Ride**. Fifteen seconds later, a car is coming.

Here's my question, and I want you to take it seriously:

> **How hard was that for you?**

Not hard at all. One tap. You didn't think about it.

Now here's the same question about the software:

> **How hard was that for Uber?**

Let's actually find out — because the gap between those two answers is the entire subject of this topic.

---

## 2. Observation — Peeling Back One Button

### Step 1: "Find drivers near me"

Sounds easy. Uber has millions of drivers with GPS positions. So just measure the distance to each one and pick the closest:

```python
for driver in all_five_million_drivers:
    distance = calculate_distance(my_location, driver.location)
# then sort
```

> 🛑 **STOP AND THINK**
> Five million distance calculations. Every time somebody taps the button. Thousands of taps per minute, in one city.
> Will this work?

It won't. It's hopelessly slow.

So Uber stopped treating the Earth as a flat sheet of coordinates. They divide the whole planet into **hexagonal cells**, each with a short ID. A driver's position isn't stored as latitude and longitude — it's stored as *which hexagon they're standing in*.

Now "find drivers near me" becomes: **look in my hexagon, and its 6 neighbours.** Seven lookups instead of five million comparisons.

```
        ⬡ ⬡ ⬡
       ⬡ ⬢ ⬡          ⬢ = you
        ⬡ ⬡ ⬡         ⬡ = the 6 neighbours you also check
```

> **Why hexagons and not squares?** In a square grid, the 4 squares touching your edges are closer than the 4 touching your corners — so "one cell away" secretly means two different distances. A hexagon has **6 neighbours, all the same distance away**. Searching outwards becomes even and predictable.

### Step 2: The nearest driver isn't the nearest driver

You now have 30 nearby drivers. Pick the closest one?

> 🛑 **STOP AND THINK**
> A driver is 200 metres away — but there's a river between you, and the nearest bridge is 6 km north.
> Is he the closest?

He's the closest in **distance**. He's nowhere near closest in **time**.

Straight-line distance is the wrong measure. What you want is *travel time*. And travel time depends on roads, which are one-way, which have traffic, which have turns that take longer than others.

So the whole city's road network gets modelled as a **graph** — junctions are dots, roads are lines between them, and every line carries a number: how long it takes to drive.

```
        A ────6──── B
        │           │
        4           3
        │           │
        C ────2──── D
```

Finding the fastest route is now a **shortest-path problem** — the kind you'll study in your algorithms course.

### Step 3: Even the perfect route is wrong

The routing engine gives a mathematically perfect answer.

Reality laughs at it. The pickup point is inside a mall, and there's a five-minute walk to the gate. That junction floods every Friday evening.

So Uber runs a **machine-learning model** on top — one that doesn't predict the arrival time, but predicts *how wrong the routing engine is going to be*, and corrects it.

### Step 4: And then

Offer the trip to the best driver. He has seconds to accept. If he doesn't, move to the next one. Meanwhile, also consider drivers who are busy now but will be free by the time they'd reach you.

Then: payment authorisation, fraud check, surge pricing, live tracking, receipt.

---

## 3. Now Count What You Saw

**One button.**

Behind it: a planet-wide hexagonal grid, a graph of every road in the city, a shortest-path algorithm, a neural network, a real-time auction, and a payments pipeline.

And your experience was: **tap.**

> 🛑 **STOP AND THINK**
> What word would you use for the thing that just happened — where something enormously complicated was presented to you as something tiny?

---

## 4. First Principle

> 💡 **KEY IDEA**
> **Software systems are enormously complex.**
> **But we want to see them as a few simple steps.**
> **That gap — complex underneath, simple on the surface — is abstraction.**

Now the definition, which should feel obvious rather than new:

> 📖 **Definition**
> **Abstraction is representing a complex system through a simple, high-level interface, hiding the internal complexity from whoever uses it.**

Or, in the compressed form worth memorising:

> **Abstraction = representing a complex system in a few working steps.**

---

## 5. More Examples, Because This Idea Is Everywhere

### A research paper's abstract

Why is it *called* an abstract?

A research paper is 40 pages of methodology, statistics and citations. The abstract is one paragraph: here's the problem, here's what we did, here's what we found.

You now know what the paper *does* without knowing how it works.

**That is exactly the relationship between an interface and its implementation.** The word was borrowed for a reason.

### Attending an online class

Your experience of joining a class:

```
   login  ──►  dashboard  ──►  join
```

Three steps. So is the backend three steps?

```
   login       →  check credentials, hash the password, issue a token,
                  create a session, verify 2FA
   dashboard   →  authorise every request, query the database,
                  check permissions, hit the cache, call five services
   join        →  open a websocket, allocate a media server,
                  negotiate video codecs, adapt to your bandwidth,
                  balance load across regions
```

**No. But for you, it is an abstraction of those three steps.**

### WhatsApp's send button

You type a message and press ➤.

Underneath: the message is encrypted end-to-end, split into packets, routed across continents, queued if the recipient is offline, retried on failure, acknowledged, and then a second tick appears.

Your interface: **one arrow.**

### An ATM

You want ₹2,000.

You do not open the vault. You do not update the ledger. You do not verify your own identity. You press buttons on a machine that offers you exactly four operations, and it does everything else.

> 🛑 **STOP AND THINK**
> Could you use an ATM if you had to understand double-entry bookkeeping first?
> Would anyone use banks at all?

---

## 6. Why We Need It — The Payoff Most Tutorials Miss

There are two payoffs, and the second one is the one that makes senior engineers care.

### Payoff 1: You can use things you don't understand

Obvious, but worth stating. You use `print()` every day. Do you know how it writes to a terminal buffer? No. Does it matter? No.

### Payoff 2: Things can change underneath you without breaking you

This is the big one.

Uber originally built its ETA feature on an off-the-shelf routing engine. Later, they replaced it with one they wrote themselves. Different algorithms, different data structures, different everything.

Now here's the question:

> 🛑 **STOP AND THINK**
> The entire routing engine was replaced. How much of the dispatch code had to be rewritten?

Think about what dispatch actually calls:

```python
eta = routing_service.get_eta(driver.location, rider.location)
```

Two points in. Minutes out.

If *that* stayed the same, then dispatch didn't care what happened behind it. **Almost nothing had to change.**

> 💡 **KEY IDEA**
> **Abstraction isn't only about making things easy to use.**
> **It's about making them safe to change.**
>
> A good interface is a wall. Complexity lives on one side. You can demolish and rebuild that side, and nobody on the other side notices.

---

## 7. How Do We Achieve It?

> **By using the three pillars.**

- **Encapsulation** hides *data* behind methods → the caller can't corrupt what they can't reach.
- **Inheritance** lets you say "this is a kind of that" → the caller can treat many things as one.
- **Polymorphism** lets one operation work across many types → the caller doesn't need to know which type they hold.

Each one removes something the caller would otherwise have to know. Remove enough, and what's left is a simple interface over a complex machine.

```
        The user sees:            Underneath:

        ┌─────────────┐          ┌────────────────────────┐
        │ Book Ride   │          │ hexagons, graphs,       │
        │             │  ◄─────  │ Dijkstra, ML models,    │
        └─────────────┘   wall   │ auctions, payments      │
                                 └────────────────────────┘
              ▲                              ▲
         abstraction              built with the 3 pillars
```

Today we build the raw materials, and finish with the first pillar.

---

## 8. Code — Abstraction You've Already Used

You don't need a class to see this. You've been on the good side of the wall since your first Python program.

```python
# uber/client.py

numbers = [42, 7, 91, 3, 15]

numbers.sort()          # ← how does this work?
print(numbers)

name = "ashok"
print(name.upper())     # ← how does THIS work?
```

### Output

```
[3, 7, 15, 42, 91]
ASHOK
```

### What just happened?

`sort()` used a genuinely sophisticated sorting algorithm — a hybrid one, tuned over years, with special handling for partially-sorted data.

`upper()` handled Unicode. Not just A–Z, but Greek, Cyrillic, and languages where uppercasing one character produces two.

**How much of that did you know before this page?** None. **Did your code work?** Perfectly.

> 💡 That is abstraction. You've been using it all along — you just didn't have the word.

And here's the part that should give you a small thrill:

**Everything you write from Topic 4 onwards is you moving from the user's side of that wall to the builder's side.**

---

## 9. Real-World Analogy

**Driving a car.**

To turn left: rotate the wheel left.

Underneath: a rack-and-pinion assembly, hydraulic pressure, tie rods, and steering geometry designed by engineers over a century.

Now the important bit. Car makers replaced hydraulic power steering with electric power steering. Completely different mechanism.

**Did you have to relearn how to drive?**

No. Because the interface — *rotate the wheel* — never changed.

**Interface stable. Implementation replaced. Nobody noticed.** That's Payoff 2, sitting in your driveway.

---

## 10. 🎯 Interview Questions

**Q1. What is abstraction?**

> Representing a complex system through a simple, high-level interface while hiding internal complexity. It's the *outcome* of applying encapsulation, inheritance and polymorphism — not a mechanism itself.

**Q2. Give a real example of abstraction from a system you've used.**

> Don't say "a car." Everyone says "a car." Say something like:
> *"When I call `list.sort()`, I get a sorted list. I never had to know which algorithm it uses. If Python replaced that algorithm tomorrow, my code wouldn't change by one character — that's the real value."*

**Q3. What's the difference between abstraction and encapsulation?**

> Encapsulation is the mechanism — restrict access to data, expose controlled methods. Abstraction is the result — the user works with a simple idea instead of the complex reality. *Encapsulation is how you hide; abstraction is what they see instead.*

**Q4. Why is abstraction valuable beyond convenience?**

> Because it decouples users from implementations. If the interface holds, the implementation can be rewritten, optimised, or replaced entirely without breaking a single caller.

---

## 11. ⚠️ Common Mistakes

| Mistake | Correction |
|:--|:--|
| "Abstraction means hiding data" | That's encapsulation. Abstraction is hiding *complexity*. |
| "Abstraction is only about abstract classes" | Abstract classes are one tool for it. Every well-named function is abstraction. |
| Building a "simple" interface that leaks | If the caller must still understand the internals to use it correctly, you haven't abstracted anything. |
| Over-abstracting on day one | Ten layers of indirection to hide two lines of code is not abstraction — it's decoration. Hide complexity that *exists*. |

---

## 12. Summary

We took one button and found a hexagonal planet-grid, a city-wide road graph, a shortest-path algorithm and a neural network underneath it.

Your experience was a tap.

That gap is **abstraction** — complex underneath, simple on the surface. It's achieved through the three pillars, and its real prize isn't convenience but **changeability**: a stable interface lets you rebuild everything behind it.

Now we start building. Topic 4 introduces the tool you'll use to make your own walls: the **class**.

---

## ✓ Key Takeaways

- **Abstraction = representing a complex system in a few working steps.**
- It's the **principle/outcome**, achieved *by using* the 3 pillars.
- The word comes from a research paper's *abstract* — same idea exactly.
- Two payoffs: **usability** (use without understanding) and **changeability** (rebuild without breaking callers).
- You've used abstraction since your first program — `print()`, `sort()`, `upper()`.

---

## ✓ Practice Questions

1. Take **Google Search**. The interface is one text box and one button. List five hard problems hiding behind it.
2. Explain abstraction to a non-programmer in under 30 seconds. Write the exact words.
3. Which is the better abstraction and why: `send_message(text, recipient)` or `send_message(text, recipient, retry_count, encryption_key, server_region, packet_size)`?
4. Name something in **Instagram** where the implementation could be completely replaced without users noticing.

---

## ✓ Mini Assignment

Pick one button in an app you use daily.

Write a document that peels it back in **four layers**, like we did with Book Ride. Layer 1 is what the user sees; layer 4 should be something genuinely hard.

Finish with one sentence: *"The user sees ____, and never needs to know ____."*

---

## ✓ Real-World Exercise

Find a Python function you've used but never looked inside — `sorted()`, `len()`, `open()`, anything.

1. Write down what you *think* it does internally.
2. Search for how it actually works.
3. Note how wrong you were.
4. Now note that **your code worked anyway.**

Step 4 is the lesson. Write it down somewhere you'll see again.

---
---

# TOPIC 4
# Classes and Objects

---

## 1. The Problem

You have your entities. You understand abstraction. Now you actually have to build something.

Let's switch examples so this doesn't become the Uber show. You're building a **College Management System** for your own college.

First entity: **Student**.

So... write it.

Go on. Open `driver.py` — no wait, that's for Uber. Open a fresh file and write "a student."

> 🛑 **STOP AND THINK**
> Seriously, try. What's line 1?

You're stuck again, but this time for a different reason.

Last time you didn't know *what* to build. Now you know what — a student — but you don't know **how to describe a thing to a computer.**

---

## 2. Observation — Nobody Builds Without a Plan

Let me ask you something completely unrelated.

You want to build a house.

Do you go to a shop, buy 4,000 bricks, and start stacking?

> 🛑 **STOP AND THINK**
> What's the very first thing that gets made when a house is built?

Not the foundation. Before that.

**A blueprint.**

A drawing on paper that says: three bedrooms here, two bathrooms there, kitchen on the north side, 1200 square feet.

Now two questions about that blueprint, and they matter more than they look:

**Question A:** Can anyone live in the blueprint?

No. It's a piece of paper. It has no address. It occupies no land. Nobody sleeps in it.

**Question B:** How many houses can you build from one blueprint?

As many as you want. Fifty houses, all following the same plan, each one real, each one with its own address, each one with different people inside.

> 🛑 **STOP AND THINK**
> One drawing. Fifty real houses. Hold that shape in your mind — it's about to become the most important idea in this chapter.

---

## 3. Think — Designing the Student "Blueprint"

Let's design the plan for a student. There are exactly two questions.

### Question 1: What do we need to *store* about every student?

Think about your own college. What do they actually keep on file?

```
                          Student
        ┌──────────┬──────────┬──────────┬─────────────┐
        │          │          │          │             │
        ▼          ▼          ▼          ▼             ▼
      name      email      phone     grad_year    roll_number
```

Now — an important question, and it's the one from your class notes:

> 🛑 **STOP AND THINK**
> At this exact moment, while we're drawing this diagram, has any student taken admission into the college?

**No.**

Nobody has enrolled. No name has been typed. No email exists. We are not storing information about anybody.

We are only deciding: *"IF I build a college system, THIS is what I will store for every student."*

That decision — that plan, made before anyone exists — is exactly what a blueprint is.

### Question 2: Apart from data, what will a student *do*?

Data alone is a dead thing. A student isn't just a row of facts; a student **acts**.

What does a student do in your college?

```
   join_class()
   solve_assignment()
   give_contest()
   give_mock_test()
```

That's **behaviour**.

> 💡 **KEY IDEA**
> **A blueprint = what it stores (data) + what it does (behaviour).**
>
> Both halves. Always. A thing with data but no behaviour is a spreadsheet row. A thing with behaviour but no data has nothing to work on.

---

## 4. First Principle

> 💡 **KEY IDEA**
> **You describe a kind of thing once. Then you create as many real ones as you like.**

Description ≠ the real thing. The recipe is not the cake. The blueprint is not the house. The form template is not your filled-in passport.

Programming languages give you both halves:

| The description | The real thing |
|:--|:--|
| **Class** | **Object** |

---

## 5. Solution — Class and Object

> 📖 **Definition**
> **A class is a blueprint that defines the structure (data) and behaviour (methods) that all objects of that type will have.**

> 📖 **Definition**
> **An object is an instance of a class — a real, concrete thing that exists in memory, with its own copy of the data.**

The same relationship, in five forms:

| Class (the plan) | Object (the real thing) |
|:--|:--|
| House blueprint | The house at Plot 42 |
| Cookie cutter | Each cookie |
| Blank passport form | Your actual passport |
| Recipe | The dish on your plate |
| `Student` class | Ashok, Meera, and 3,000 others |

```
                    ┌─────────────────┐
                    │  class Student  │   ← ONE description
                    │  (the plan)     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ "Ashok"  │  │ "Meera"  │  │  "Ravi"  │   ← MANY real students
        │ 2026     │  │ 2027     │  │  2026    │
        └──────────┘  └──────────┘  └──────────┘
         object 1       object 2       object 3
```

---

## 6. Now Let's Understand "Object" Properly

Your class notes say something that sounds strange the first time:

> *"A real-world entity in the system is called an object."*
> *"In computer science, what does 'real' mean? — **memory has been allocated**."*

Let's unpack that, because it's the sentence that makes objects click.

### What exists when you've only written the class?

You've typed `class Student:` into a file. What's in the computer right now?

> 🛑 **STOP AND THINK**
> Is there a name stored anywhere? An email? A phone number?

**No.**

There is some *text* in a file. Characters. The word "class", the word "Student", a colon. Python has read it and remembered the plan.

But **no student data has been allocated**, because there is no *particular* student yet. Just like a blueprint doesn't contain bricks.

### And when you create an object?

*Now* the computer sets aside actual memory. A real region of RAM that holds "Ashok", 2026, a phone number. Something with a location. Something you could point at.

That's what "real" means to a computer: **it has an address.**

> 💡 **KEY IDEA**
> **Class = a description. Costs no memory for data.**
> **Object = memory has been allocated. It genuinely exists.**

---

## 7. Python Code — Finally

Enough theory. Let's build it.

### The blueprint — `uber/driver.py`

We'll switch back to our Uber project now, since that's the system we're building.

```python
# uber/driver.py

class Driver:
    """A driver in the Uber system."""

    def __init__(self, driver_id, name, rating, is_online):
        # ---- DATA: what every driver stores ----
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online

    # ---- BEHAVIOUR: what every driver can do ----
    def accept_ride(self, ride_id):
        print(f"Ride has been accepted {ride_id}")

    def change_status(self):
        self.is_online = not self.is_online
        print(f"Driver is {self.is_online}")
```

Two things to notice right now, and then we move on:

1. **This file creates no drivers.** Not one. It only *describes* what a driver is. It's a pure blueprint file.
2. There's some unexplained syntax — `__init__` and `self`. **Ignore them completely for now.** They get two full topics of their own (Topic 7). Right now, just read them as "the setup part."

### Using the blueprint — `uber/client.py`

```python
# uber/client.py

from uber.driver import Driver


def main():
    # Creating OBJECTS from the class
    d1 = Driver(4021, "Ashok", 4.8, True)
    d2 = Driver(4088, "Meera", 4.9, True)

    print(d1.name)          # Ashok
    print(d2.name)          # Meera

    # Each object has its OWN data
    d1.is_online = False

    print(d1.is_online)     # False
    print(d2.is_online)     # True   ← untouched!


if __name__ == "__main__":
    main()
```

### Run it

```bash
cd uber_project
python3 -m uber.client
```

### Output

```
Ashok
Meera
False
True
```

---

## 8. What Just Happened?

Let's walk through it line by line, because this is the moment OOP becomes real.

### `d1 = Driver(4021, "Ashok", 4.8, True)`

> 🛑 **STOP AND THINK**
> `Driver` is a class — a description. Why are we calling it like a function, with brackets?

Because **in Python, calling the class name is how you create an object.** That's the syntax. `Driver(...)` means *"build me one real driver."*

Python does three things:

```
   1. Sets aside memory for one new Driver object
   2. Runs __init__, filling in the data
   3. Hands the finished object back to you
```

And `d1` now refers to it.

> 🔁 **JAVA CORNER**
> Java writes `Driver d1 = new Driver(...)`. Python has **no `new` keyword** — calling the class *is* the creation. One less word to type, same idea.

### `print(d1.name)` and `print(d2.name)`

Different values from the same class. Because `d1` and `d2` are **two separate objects**, each with its own memory, each holding its own data.

### The line that proves everything

```python
d1.is_online = False
print(d1.is_online)     # False
print(d2.is_online)     # True   ← Meera is unaffected
```

We changed Ashok. Meera didn't move.

> 💡 **KEY IDEA**
> **One class. Many objects. Each object has a completely independent copy of the data.**
>
> This is the whole point. You wrote `Driver` once, and it can now describe five million distinct people, each with their own name, rating and status.

### How Python executes this

```
   from uber.driver import Driver
        │
        ▼  Python reads driver.py, learns the plan.
           NO driver data exists yet.
        │
   d1 = Driver(4021, "Ashok", 4.8, True)
        │
        ▼  Memory allocated. __init__ runs. Object #1 exists.
        │
   d2 = Driver(4088, "Meera", 4.9, True)
        │
        ▼  Memory allocated AGAIN. Object #2 exists, separate from #1.
```

---

## 9. ⚠️ Wrong Assumption to Kill Right Now

Many students believe this:

> *"The class stores the data of all objects."*

**No.** The class stores the *plan*. Each object stores its own data.

```
   ✗ WRONG picture                    ✓ RIGHT picture

   ┌───────────────────┐              ┌───────────────┐
   │   class Driver    │              │ class Driver  │
   │  Ashok  4.8       │              │  (just a plan)│
   │  Meera  4.9       │              └───────────────┘
   │  Ravi   4.7       │
   └───────────────────┘              ┌────┐ ┌────┐ ┌────┐
                                      │Ashok││Meera││Ravi│
   the class does NOT                 │ 4.8 ││ 4.9 ││4.7 │
   hold everyone's data               └────┘ └────┘ └────┘
                                       each object holds its own
```

You can verify this yourself:

```python
d1 = Driver(4021, "Ashok", 4.8, True)
print(d1.__dict__)
# {'driver_id': 4021, 'name': 'Ashok', 'rating': 4.8, 'is_online': True}
```

`__dict__` shows you **everything that object personally owns**. Try it on `d2` — different values, same keys. Two separate boxes.

Remember `__dict__`. It's the single most useful debugging tool in this chapter, and we'll use it again in Topic 8 to catch a nasty bug.

---

## 10. Real-World Analogies

### Instagram

There is **one** `Account` class in Instagram's codebase. Written once, by one team.

There are **two billion** account objects. Yours is one of them. Your username, your followers, your posts — your own private copy of the data.

When Instagram adds a feature, they change **one class**. Two billion objects get the feature.

> 🛑 **STOP AND THINK**
> Imagine maintaining Instagram with the loose-variables approach from Topic 1.
> `user_1_username`, `user_2_username`, ... `user_2000000000_username`.

### The passport office

There's one blank passport **form** — the template. Printed millions of times.

You fill one in. It becomes **your** passport, with your photo, your number, your name.

Someone else fills in an identical blank and gets a completely different passport.

**One template. Millions of passports. Each independent.**

Class and object.

---

## 11. 🎯 Interview Questions

**Q1. What's the difference between a class and an object?**

> A class is a blueprint — a description of structure and behaviour, costing no memory for data. An object is an instance of that class: memory has actually been allocated, and it holds its own independent copy of the data. One class, many objects.

**Q2. How much memory does a class take?**

> The class itself holds the method definitions and the plan — that's it. **Object data memory is allocated per object.** Creating 1,000 objects means 1,000 sets of instance data, but still only one copy of the methods.

**Q3. Can you have a class with no objects?**

> Yes, and it's completely normal. The class simply describes something nobody has created yet — like a blueprint for a house nobody has built.

**Q4. What does "instance" mean?**

> The same thing as "object." You'll hear "an instance *of* a class," which is the more precise phrasing — it names the relationship, not just the thing.

---

## 12. ⚠️ Common Mistakes

| Mistake | Why it's wrong |
|:--|:--|
| Thinking the class holds all objects' data | Each object holds its own. Verify with `__dict__`. |
| Writing `Driver` when you meant `Driver()` | Without brackets you're referring to the *blueprint*, not creating a house. |
| Creating objects inside `driver.py` | The blueprint file describes; the client file uses. Keep them separate. |
| Naming the class `driver` (lowercase) | Classes are `PascalCase`: `Driver`, `BankAccount`, `DeliveryPartner`. |
| Expecting `d2` to change when you change `d1` | They're independent objects. (Unless… see Topic 6. There's a twist coming.) |

---

## 13. Summary

You couldn't describe "a student" to a computer, so we asked how humans describe things they haven't built yet — and found the **blueprint**.

A blueprint has two halves: **what it stores** and **what it does**. In code that's a **class**.

Build from the blueprint and you get an **object** — a real thing, with memory allocated, holding its own independent copy of the data.

One class. Unlimited objects. That's the leverage.

---

## ✓ Key Takeaways

- **Class** = blueprint. Describes data + behaviour. No data memory allocated.
- **Object** = an instance. Memory allocated. Owns its data.
- In CS, "real" means **memory has been allocated**.
- Creating an object in Python: `d1 = Driver(...)` — **no `new` keyword**.
- Every object's data is **independent**; changing one doesn't touch another.
- `obj.__dict__` shows exactly what one object owns.

---

## ✓ Practice Questions

1. Explain class vs object with an analogy that is **not** blueprint, cookie cutter, recipe, or passport.
2. What exists in memory after `class Driver:` is read, but before any object is created?
3. Predict the output, then run it:
   ```python
   a = Driver(1, "A", 5.0, True)
   b = Driver(1, "A", 5.0, True)
   a.name = "Changed"
   print(b.name)
   ```
4. Write a `Video` class for YouTube with four pieces of data and two behaviours. Create three video objects.

---

## ✓ Mini Assignment

Build `college/student.py` with a `Student` class:

- **Data:** `name`, `email`, `phone`, `grad_year`, `roll_number`
- **Behaviour:** `join_class()`, `solve_assignment()`, `give_contest()`, `give_mock_test()`

Then `college/client.py` that creates **three** students and calls every method on each.

Finish by printing `student1.__dict__` and writing one sentence explaining what you see.

---

## ✓ Real-World Exercise

Pick **Swiggy**. Choose one entity — say, `Order`.

On paper, without writing code:

1. List everything an order must **store**.
2. List everything an order can **do**.
3. Now circle anything in list 1 that shouldn't be there because it belongs to a *different* entity.

That last step is real design work. Most beginners put the restaurant's phone number inside `Order`. Ask yourself why that's a mistake.

---
---

# TOPIC 5
# Building Your First Class — Fields, Methods, Members and State

---

## 1. The Problem

You have a class. You have objects. But right now you're using words loosely — "data", "stuff", "the things inside".

Engineers don't talk like that. And more importantly, there's one word in this topic that will explain **almost every bug you write for the next two years**.

Let's earn all four words properly.

---

## 2. Observation — Look at WhatsApp

Open a chat. Send a message. Watch what happens to it.

```
   ➤  "Hey, are you free?"                    ⏱️   sending
   ➤  "Hey, are you free?"                    ✓    sent
   ➤  "Hey, are you free?"                    ✓✓   delivered
   ➤  "Hey, are you free?"                    ✓✓   read (blue)
```

> 🛑 **STOP AND THINK**
> Four screenshots. Is that four different messages, or one message?

**One message.** The text never changed. The sender never changed. The time it was written never changed.

What changed was its **status** — and it changed four times in about two seconds.

Hold that. It's the word we're building to.

---

## 3. Think

Let me ask about a driver instead.

Here is Ashok, right now, at 3am:

```
   driver_id  = 4021
   name       = "Ashok"
   rating     = 4.8
   is_online  = False        ← he's asleep
```

Two hours later he wakes up and opens the app:

```
   driver_id  = 4021
   name       = "Ashok"
   rating     = 4.8
   is_online  = True         ← changed
```

Three questions:

**Q1.** Is this the same driver, or a different one?

**Q2.** Did the object get destroyed and rebuilt?

**Q3.** So what exactly changed?

...

**A1.** Same driver. Same object. Same memory.
**A2.** No. Nothing was rebuilt.
**A3.** One value inside it.

> 🛑 **STOP AND THINK**
> If the object is the same object, but something about it is different… what do we call the "something"?

---

## 4. First Principle

> 💡 **KEY IDEA**
> **An object is not a fixed thing. An object is a thing that *changes over time*.**
> **The snapshot of what it looks like right now has a name: its state.**
> **And methods are what move it from one state to the next.**

That's the whole topic. Now the four vocabulary words.

---

## 5. Solution — The Four Words

> 📖 **Definitions**
>
> **Member variables** (also called *fields*, or *instance attributes*) — the variables that belong to a class.
>
> **Member methods** — the functions that belong to a class.
>
> **Members** — the collective word for both. Everything that is a *member of* the class.
>
> **State** — the value of an object's variables at a given point in time.

Mapped onto our class:

```python
class Driver:

    def __init__(self, driver_id, name, rating, is_online):
        self.driver_id = driver_id      # ┐
        self.name = name                # │  MEMBER VARIABLES
        self.rating = rating            # │  (the data)
        self.is_online = is_online      # ┘

    def accept_ride(self, ride_id):     # ┐
        ...                             # │  MEMBER METHODS
                                        # │  (the behaviour)
    def change_status(self):            # │
        ...                             # ┘
```

And **state** isn't in the code at all — state is what the *values* are at a moment in time. The code is the same for every driver; the state is different for each one, and different at each moment.

```
   THE CLASS               THE OBJECT'S STATE
   (written once)          (changes constantly)

   name                    "Ashok"    →   "Ashok"
   rating                   4.8       →    4.8
   is_online               False      →   True      ← state changed
                          ─────────      ─────────
                            3am            5am
```

---

## 6. Python Code

### `uber/driver.py`

```python
# uber/driver.py

class Driver:
    """A driver in the Uber system."""

    def __init__(self, driver_id, name, rating):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = False          # every driver starts offline
        self.trips_today = 0

    def go_online(self):
        self.is_online = True
        print(f"{self.name} is now ONLINE")

    def go_offline(self):
        self.is_online = False
        print(f"{self.name} is now OFFLINE")

    def complete_trip(self):
        self.trips_today = self.trips_today + 1
        print(f"{self.name} completed a trip. Today's count: {self.trips_today}")
```

### `uber/client.py`

```python
# uber/client.py

from uber.driver import Driver


def show_state(driver):
    print(f"    STATE → {driver.__dict__}")


def main():
    ashok = Driver(4021, "Ashok", 4.8)

    print("Just created:")
    show_state(ashok)

    print("\nHe starts his shift:")
    ashok.go_online()
    show_state(ashok)

    print("\nHe drives three people:")
    ashok.complete_trip()
    ashok.complete_trip()
    ashok.complete_trip()
    show_state(ashok)

    print("\nEnd of shift:")
    ashok.go_offline()
    show_state(ashok)


if __name__ == "__main__":
    main()
```

### Output

```
Just created:
    STATE → {'driver_id': 4021, 'name': 'Ashok', 'rating': 4.8, 'is_online': False, 'trips_today': 0}

He starts his shift:
Ashok is now ONLINE
    STATE → {'driver_id': 4021, 'name': 'Ashok', 'rating': 4.8, 'is_online': True, 'trips_today': 0}

He drives three people:
Ashok completed a trip. Today's count: 1
Ashok completed a trip. Today's count: 2
Ashok completed a trip. Today's count: 3
    STATE → {'driver_id': 4021, 'name': 'Ashok', 'rating': 4.8, 'is_online': True, 'trips_today': 3}

End of shift:
Ashok is now OFFLINE
    STATE → {'driver_id': 4021, 'name': 'Ashok', 'rating': 4.8, 'is_online': False, 'trips_today': 0 → 3}
```

*(That last line reads `'trips_today': 3` — I've marked the change for you.)*

---

## 7. What Just Happened?

**What happened:** We printed the same object's `__dict__` at four different moments and got four different pictures.

**Why:** Because we never created a second driver. There was one `Driver` object from start to finish. What changed was its **state**.

**How Python executes this:**

```
   ashok = Driver(4021, "Ashok", 4.8)
        │
        ▼   memory allocated. State #1 written.
        │
   ashok.go_online()
        │
        ▼   finds the SAME object, changes ONE value → State #2
        │
   ashok.complete_trip()  × 3
        │
        ▼   same object, one value incremented each time → State #3
```

> 💡 **KEY IDEA**
> **The object's identity stayed the same. Its state moved.**
>
> That's what it means to say an object *lives* — it has a history.

### The state machine

Draw a driver's life and you get this:

```
                  go_online()
    ┌─────────┐  ───────────►  ┌─────────┐
    │ OFFLINE │                │ ONLINE  │
    └─────────┘  ◄───────────  └─────────┘
                  go_offline()       │
                                     │ gets a trip
                                     ▼
                               ┌──────────┐
                               │ ON_TRIP  │
                               └──────────┘
                                     │ complete_trip()
                                     └──► back to ONLINE
```

Every method is an **arrow**. Every box is a **state**.

---

## 8. Why This Word Matters So Much

Here's the payoff, and it's worth reading twice.

> 💡 **KEY IDEA**
> **Almost every serious bug in object-oriented software is a state bug.**

Not a syntax error. Not a typo. A state bug — where an object ended up in a combination of values that should have been *impossible*.

Real examples:

| The impossible state | What the user sees |
|:--|:--|
| A driver with `is_online = False` but an active trip | Passenger waits forever for a car that isn't coming |
| A driver assigned to **two trips at once** | Two people, one car, both furious |
| A bank account with `balance = -5000` | Money created from nothing |
| A Swiggy order marked `delivered` with no delivery partner | Nobody can find your food |
| A rating of `-50` | Dispatch's sorting goes haywire |

Look at the last one carefully:

```python
ashok.rating = -50        # nothing stops you
```

The `Driver` class *knows* a rating must be between 0 and 5. But it has no power to enforce that, because the value is sitting wide open for any line of code anywhere to overwrite.

> 🛑 **STOP AND THINK**
> Whose job should it be to make sure a driver's rating is always valid?
> The thousand files that use drivers? Or the `Driver` class itself?

Write down your answer. Topic 11 is entirely about it — and now you'll know why that topic exists.

---

## 9. Real-World Analogies

### A traffic light

Three states: red, amber, green. One object — the light on the corner. Its behaviour is a set of arrows between those states.

Now imagine a **state bug**: red and green on at the same time. The object is technically fine — two booleans, both `True`. The consequences are not fine.

### Your Swiggy order

```
   PLACED → ACCEPTED → COOKING → PICKED_UP → DELIVERED
```

One order. Five states. The little tracker in the app is literally showing you the object's state.

And you already know what a state bug feels like here: the app says *delivered*, your hands say otherwise.

---

## 10. 🎯 Interview Questions

**Q1. What is the state of an object?**

> The values of its member variables at a given point in time. Same object, different moments, different state.

**Q2. What's the difference between a member variable and a local variable?**

> A member variable belongs to the object and lives as long as the object does (`self.name`). A local variable exists only inside a method and disappears when the method returns.

**Q3. Two objects of the same class — do they share state?**

> No. Each object has its own independent copy of the member variables. (There's an exception coming in Topic 8 — class-level attributes — and knowing that exception is what separates a good answer from a great one.)

**Q4. Why do people say "state management" is the hard part of software?**

> Because behaviour is easy to test in isolation, but state accumulates. Bugs appear from a *sequence* of valid-looking operations leaving the object in an invalid combination — which is much harder to reproduce than a single bad function.

---

## 11. ⚠️ Common Mistakes

| Mistake | Why it's wrong |
|:--|:--|
| Forgetting `self.` — writing `name = name` inside a method | Creates a local variable that vanishes. The member variable never changes. **No error is shown.** (Full explanation in Topic 7.) |
| Setting some attributes outside `__init__` | Then the attribute exists on *some* objects and not others → `AttributeError` at 2am. |
| Letting any file modify state directly | This is the door every state bug walks through. Topic 11 closes it. |
| Confusing state with identity | Ashok going offline doesn't make him a different driver. |

---

## 12. Summary

An object isn't a frozen box of values — it's a thing with a **history**.

- **Member variables** = the data it holds
- **Member methods** = the things it can do
- **Members** = both together
- **State** = what the values are *right now*

Methods are the arrows that move an object from one state to the next. And the day you can't guarantee your object's state is valid is the day the bugs start.

---

## ✓ Key Takeaways

- **Member variables** (fields) — variables of the class.
- **Member methods** — functions of the class.
- **State** — the value of an object's variables at a given point in time.
- Same object + different moment = **different state, same identity**.
- `obj.__dict__` prints an object's current state. Use it constantly.
- **Most real bugs are state bugs** — impossible combinations of values.

---

## ✓ Practice Questions

1. Draw the state machine for a **Swiggy order**. Boxes = states, arrows = methods.
2. In the `Driver` class, which member variable should *never* change after creation? Why?
3. Write a method `reset_day()` that sets `trips_today` back to 0. Print `__dict__` before and after.
4. Give three examples of an "impossible state" for an **Instagram account** object.

---

## ✓ Mini Assignment

Build a `BankAccount` class:

- **Member variables:** `account_number`, `holder_name`, `balance`
- **Member methods:** `deposit(amount)`, `withdraw(amount)`, `show_balance()`

Then, in the client, deliberately create an impossible state — withdraw more money than exists — and watch the balance go negative.

Write one paragraph on why your class allowed that, and what you'd need to prevent it.

*(Keep this file. We come back to it in Topic 11.)*

---

## ✓ Real-World Exercise

Order something on Swiggy or Zomato. Screenshot the tracker at **every** stage.

Then write out:

1. The list of states you observed.
2. What event caused each transition.
3. One state the app is probably tracking that it *doesn't* show you.

You've just reverse-engineered a state machine from the outside — which is exactly what engineers do when they join a new team.

---
---

# TOPIC 6
# Reference Variables and the Memory Model

---

## 1. The Problem

At the end of Topic 4 I told you something, and you believed me:

> *"Each object has a completely independent copy of the data. Changing one doesn't touch another."*

That's true. But I hid something from you.

Let's find it. Here's a tiny program. **Predict the output before you read on.**

```python
d1 = Driver(4021, "Ashok", 4.8)
d2 = d1                          # ← look at this line

d2.name = "CHANGED"

print(d1.name)
print(d2.name)
```

> 🛑 **STOP AND THINK**
> We changed `d2`. What does `d1.name` print?
>
> Write your answer down. Actually write it. This matters.

Most students say:

```
Ashok
CHANGED
```

The real output is:

```
CHANGED
CHANGED
```

**Both changed.**

If that surprised you — good. You've just found the single most misunderstood thing in Python, and we're going to fix it permanently in the next ten minutes.

---

## 2. Observation — What Did That Line Actually Do?

```python
d2 = d1
```

Read it out loud. What do you *think* it means?

Most people read it as: *"make a copy of d1 and call it d2."*

But the output proves that's not what happened. If a copy had been made, there'd be two drivers, and changing one wouldn't touch the other.

So `=` did **not** make a copy.

> 🛑 **STOP AND THINK**
> If it didn't copy the driver… what did it copy?

---

## 3. Wrong Assumption — The Box Picture

Here's the mental model almost everyone starts with. It comes from school algebra, and it's wrong for Python.

```
   ✗ THE BOX PICTURE

   d1  ┌──────────────┐
       │  Ashok, 4.8  │      "d1 is a box containing a driver"
       └──────────────┘
```

If variables were boxes, then `d2 = d1` would mean *pour a copy into a second box*. Two boxes. Two drivers.

But we just watched that not happen.

So the box picture is wrong. Throw it away — genuinely, delete it — and let's build the right one.

---

## 4. Think

Let me ask you something that has nothing to do with code.

You write your home address on a slip of paper.

Your friend wants to visit, so you **photocopy** the slip and hand it to them.

**Question 1:** How many slips of paper now exist?

**Question 2:** How many *houses* now exist?

**Question 3:** Your friend drives to that address and paints your front door bright pink. You come home that evening. What colour is your door?

...

**A1.** Two slips.
**A2.** **One house.**
**A3.** Pink. Obviously pink. There was only ever one house.

> 💡 Now go back and read `d2 = d1` again.
> You didn't copy the driver. **You copied the address.**

---

## 5. First Principle

> 💡 **KEY IDEA**
> **A Python variable is not a box holding a value.**
> **A Python variable is a label stuck onto an object.**

```
   ✓ THE LABEL PICTURE

                 ┌──────────────────┐
   d1 ─────────► │  Driver object   │
                 │  name = "Ashok"  │
                 └──────────────────┘
```

`d1` is not the driver. `d1` is a **sticker pointing at** the driver.

Now `d2 = d1`:

```
   d1 ─────┐
           ├────► ┌──────────────────┐
   d2 ─────┘      │  Driver object   │      ONE object
                  │  name = "Ashok"  │      TWO labels
                  └──────────────────┘
```

**There was never a second driver.** Both stickers are on the same box. Reach in through either one and you're touching the same thing.

> 📖 **Definition**
> **A reference variable does not hold the object. It holds a reference to (the address of) the object.**

> 💡 **THE RULE THAT NEVER BREAKS**
> **In Python, `=` never copies an object. It only ever moves a label.**

---

## 6. Solution — Let's Prove It

Talk is cheap. Let's *see* the address.

```python
# uber/client.py

from uber.driver import Driver


def main():
    d1 = Driver(4021, "Ashok", 4.8)
    d2 = d1
    d3 = Driver(4021, "Ashok", 4.8)      # same DATA, built separately

    print("d1 address:", id(d1))
    print("d2 address:", id(d2))
    print("d3 address:", id(d3))

    print()
    print("d1 is d2 →", d1 is d2)        # same object?
    print("d1 is d3 →", d1 is d3)        # same object?


if __name__ == "__main__":
    main()
```

### Output

```
d1 address: 140234891234567
d2 address: 140234891234567
d3 address: 140234891987654

d1 is d2 → True
d1 is d3 → False
```

*(Your numbers will differ — addresses change every run. The pattern is what matters.)*

### What just happened?

- `d1` and `d2` print the **identical address**. Same object. One driver.
- `d3` has a **different address** — even though every single value inside is the same.

> 🛑 **STOP AND THINK**
> `d1` and `d3` hold identical data. Same ID, same name, same rating.
> Why are they still different objects?

Because they were **built separately**. Two houses can have identical floor plans and identical furniture and still be two different houses at two different addresses.

Data is not identity.

---

## 7. `is` vs `==` — The Two Questions

Now you can ask two genuinely different questions about objects:

| Question | Operator |
|:--|:--|
| Are these the **same object**? (identity) | `is` |
| Do these have the **same value**? (equality) | `==` |

```python
d1 is d2      # True   → one object, two labels
d1 is d3      # False  → two different objects
d1 == d3      # compares by VALUE (once the class defines how)
```

**Use `is` for one thing only, in practice:**

```python
if x is None:        # ✅ the idiomatic check
if x == None:        # ❌ works, but nobody writes this
```

> 🔁 **JAVA CORNER — and this one causes real bugs**
>
> | Purpose | Java | Python |
> |:--|:--|:--|
> | Same object? | `d1 == d2` | `d1 is d2` |
> | Same value? | `d1.equals(d2)` | `d1 == d2` |
>
> **Notice they're swapped.** Java's `==` means identity. Python's `==` means value.
> If you carry the Java habit across, every comparison you write will be subtly wrong.

---

## 8. Everything in Python Is an Object

One more piece and the picture is complete.

Some languages split the world in two: *primitives* (like `int`) that hold a value directly, and *objects* that you reach through a reference.

**Python has no primitives.**

```python
x = 10
print(type(x))      # <class 'int'>
print(id(x))        # it has an address too!
```

`10` is an object. `"Ashok"` is an object. A list is an object. A function is an object. Even a class is an object.

> 💡 **KEY IDEA**
> **Since everything is an object, every variable is always a reference.**
> **There is no other kind of variable in Python.**

That's actually *simpler* than languages with two categories — one rule, no exceptions.

### A curiosity: interning

Try this:

```python
a = "Abc"
b = "Abc"
print(a is b)        # True — really?

x = 100
y = 100
print(x is y)        # True — really?
```

Two separate lines, and Python reused **the same object**.

This is called **interning**. Python pre-creates small integers (roughly −5 to 256) and reuses short string literals, to save memory.

> 🛑 **STOP AND THINK**
> Sharing one object between many variables sounds dangerous. If I change `a`, does `b` change?
>
> Why is this actually completely safe?

Because strings and integers are **immutable** — they cannot be changed. `a.upper()` doesn't modify `"Abc"`; it builds a *new* string. Since nobody can ever modify `"Abc"`, a thousand variables can share one copy with zero risk.

> ⚠️ **But never rely on it.**
> ```python
> x = 1000
> y = int("1000")
> print(x is y)      # False!
> print(x == y)      # True  ← the answer you actually wanted
> ```
> Interning is an internal optimisation that varies between versions. **Compare values with `==`.**

> 🔁 **JAVA CORNER** — Java does the same thing and calls it the **String Pool**. `String s1 = "Abc"; String s2 = "Abc";` gives `s1 == s2 → true`, but `new String("Abc")` forces a separate object. Same idea, same reason: immutability makes sharing safe.

---

## 9. Where Do Objects Actually Live?

The classic picture — and the one your Java course draws — splits memory in two:

```
                            R A M
        ┌──────────────────┬────────────────────────────┐
        │      STACK       │           HEAP             │
        │  (fast, small)   │      (large, dynamic)      │
        ├──────────────────┼────────────────────────────┤
        │                  │   address 140234891234567: │
        │                  │     driver_id = 4021       │
        │   d1 ────────────┼──►  name      = "Ashok"    │
        │   d2 ────────────┼──►  rating    = 4.8        │
        │                  │     is_online = False      │
        └──────────────────┴────────────────────────────┘
              labels                 the real objects
```

- The **stack** holds local variables and references — small, fast, cleaned up automatically when a function returns.
- The **heap** holds the actual objects — large, dynamic, cleaned up by the garbage collector.

> 🔁 **JAVA CORNER**
> In Java, `int a = 10;` puts the value `10` **directly on the stack** — primitives are stored inline. Only objects go on the heap.
>
> In Python there are no primitives, so the picture is simpler: **everything is on the heap**, and the stack only ever holds labels pointing into it.

### Garbage collection

```python
d1 = Driver(4021, "Ashok", 4.8)
d1 = Driver(4088, "Meera", 4.9)      # the first object now has NO labels
```

> 🛑 **STOP AND THINK**
> What happens to Ashok's object? Nothing points at it any more.

Python counts how many labels point at each object. When the count hits zero, the object is unreachable and its memory is freed automatically.

You never write `free()` or `delete`. Same in Java. This is why neither language has the memory-leak class of bugs that C programmers fight.

---

## 10. Real-World Analogy — Why This Is a Feature

This isn't a quirk to be endured. In real systems, it's the whole point.

When Uber's dispatch is running, the **same** driver object is referenced from several places at once:

```python
ashok = Driver(4021, "Ashok", 4.8)

geo_index.add(ashok)          # the map service is tracking him
trip.driver = ashok           # the active trip points at him
candidates.append(ashok)      # dispatch is considering him
```

Three references. **One Ashok.**

Now he goes offline:

```python
ashok.go_offline()
```

> 🛑 **STOP AND THINK**
> How many of those three places need to be updated?

**None.** They're all looking at the same object. There is nothing to synchronise, because there's nothing to get out of sync.

> 💡 If Python had copied the object into each place, you'd have three Ashoks with three different online statuses — and dispatch would send a car that isn't coming.

**The behaviour that confused you on page one is the behaviour that makes real systems work.**

---

## 11. 🎯 Interview Questions

**Q1. What does `d2 = d1` do in Python?**

> It binds a second name to the same object. No copy is made. Both names refer to one object, so a change through either is visible through both.

**Q2. Difference between `is` and `==`?**

> `is` compares identity — are these the same object in memory? `==` compares value. Note this is the opposite of Java, where `==` is identity and `.equals()` is value.

**Q3. `a = 10; b = 10; a is b` → True. But `a = 1000; b = int("1000"); a is b` → False. Explain.**

> Small integers are pre-cached and reused by the interpreter, so both names land on the same object. Larger integers computed at runtime are separate objects. It's an internal optimisation — never write code that depends on it.

**Q4. Does Python have primitives?**

> No. Everything is an object, including integers and booleans. Consequently every variable is a reference — there's only one kind of variable.

---

## 12. ⚠️ Common Mistakes

| Mistake | Consequence |
|:--|:--|
| Believing `=` copies an object | You modify one thing and something else changes. Hours lost. |
| Using `==` to check identity (Java habit) | Wrong comparison, subtle bugs. |
| Using `is` to compare numbers or strings | Works by luck with small values, fails with large ones. |
| Thinking two objects with identical data are the same object | Data is not identity. |
| Passing an object into a function and expecting it to be safe | It isn't. **Topic 9 is entirely about this.** |

---

## 13. Summary

You predicted `Ashok`. You got `CHANGED`. That surprise was the door into the real memory model.

**A variable is a label, not a box.** `=` moves a label; it never copies an object. Two labels on one object means a change through either is visible through both.

Everything in Python is an object, so every variable is a reference. `is` asks *same object?*; `==` asks *same value?*

And the behaviour that tripped you up is exactly what lets Uber's dispatch, map and trip services all see one consistent driver.

---

## ✓ Key Takeaways

- **A Python name is a label stuck on an object**, not a box holding a value.
- **`=` never copies.** It binds another name to the same object.
- `id(obj)` shows the address. `obj1 is obj2` asks whether they're the same object.
- **`is` = identity, `==` = value.** (Opposite of Java — be careful.)
- **Everything is an object** in Python; there are no primitives.
- Objects live on the **heap**; names live on the **stack**.
- Unreferenced objects are freed automatically by **garbage collection**.

---

## ✓ Practice Questions

1. Predict, then run:
   ```python
   a = [1, 2, 3]
   b = a
   b.append(4)
   print(a)
   ```
   Explain using the label picture.

2. What does this print, and why?
   ```python
   d1 = Driver(1, "A", 5.0)
   d2 = Driver(1, "A", 5.0)
   print(d1 is d2)
   print(id(d1) == id(d2))
   ```

3. You want a *genuinely* independent copy of a driver. `d2 = d1` doesn't do it. Search for how, and explain in one sentence why Python doesn't do it by default.

4. Draw the label diagram for:
   ```python
   a = Driver(1, "X", 5.0)
   b = a
   c = b
   a = Driver(2, "Y", 4.0)
   ```
   How many objects exist? What does `b.name` print?

---

## ✓ Mini Assignment

Write `memory_demo.py` that proves all four of these with printed output:

1. `=` does not copy an object
2. Two objects with identical data are still different objects
3. Small integers are interned; large ones aren't
4. `is` and `==` give different answers for the same pair of objects

Add one comment line above each proof explaining what it demonstrates.

---

## ✓ Real-World Exercise

Take the WhatsApp group-chat idea. A `Group` object holds a list of `User` objects. The same `User` object also appears in five other groups.

On paper, draw the labels.

Now answer: when that user changes their display name, how many groups need updating?

Then answer the harder one: **what would go wrong if Python copied objects on assignment instead?**

---
---

# TOPIC 7
# Constructor and `self`

---

## 1. The Problem

Let's build a driver the long way, with no shortcuts.

```python
# uber/client.py

d1 = Driver()
d1.driver_id = 4021
d1.name = "Ashok"
d1.rating = 4.8
d1.is_online = True
```

Five lines. One driver. It works.

Now your manager says: *"Onboard the next hundred drivers."*

> 🛑 **STOP AND THINK**
> Five lines per driver × 100 drivers = how many lines?
>
> And Uber onboards thousands per week. Now what?

**500 lines** for a hundred drivers. And your class notes ask exactly the right question about this:

> *"To initialise an object with data I am writing a lot of lines. Will anyone do that at industry level?"*

**No.** Nobody does this. Ever.

But length isn't even the real problem. Let me show you the real problem.

---

## 2. Observation — The Line You Forget

Watch carefully. I'm going to make one small mistake:

```python
d1 = Driver()
d1.driver_id = 4021
d1.name = "Ashok"
d1.is_online = True          # ← notice anything missing?
```

I forgot `rating`.

Does Python complain? **No.** The program runs happily.

Then, two hours later, in a completely different file, somebody writes:

```python
print(f"Rating: {d1.rating}")
```

```
AttributeError: 'Driver' object has no attribute 'rating'
```

> 🛑 **STOP AND THINK**
> The error appeared in the *printing* file.
> But where is the actual bug?

The bug is in the **creation** file, two hours and three modules away. That's the worst kind of bug — the crash and the cause are nowhere near each other.

And notice how easy the mistake was. Four lines that look identical. Miss one. Nothing warns you.

---

## 3. Think

Let me ask about something outside code.

You're admitted to hospital. Before you become a patient in their system, you fill in an **admission form**: name, age, blood group, emergency contact.

**Question 1:** Can you skip the blood group box and still be admitted?

**Question 2:** Is it possible to be *half* admitted — in the system, but with a blank form?

...

**A1.** No. The form is checked.
**A2.** No. Either you're admitted with a complete record, or you're not admitted.

> 💡 That's the property we want.
> **There should be no way to create a driver that isn't fully set up.**

Not "please remember to set all four fields." Not "we have a checklist." Actually impossible.

> 🛑 **STOP AND THINK**
> When would be the perfect moment to force all that data to be provided?

The only moment where the class is in charge: **the moment the object is being created.**

---

## 4. First Principle

> 💡 **KEY IDEA**
> **An object should be born valid.**
> **So the class should demand everything it needs at the moment of creation — and refuse to build the object otherwise.**

Which means we need a piece of code that runs **automatically** when an object is created.

That's a constructor.

---

## 5. Solution — The Constructor

> 📖 **Definition**
> **A constructor is a special method that runs automatically when an object is created. Its job is to initialise the object's member variables.**

In Python it has a fixed name: **`__init__`**.

```python
# uber/driver.py

class Driver:
    def __init__(self, driver_id, name, rating, is_online):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online
```

And now creation is one line:

```python
d1 = Driver(4021, "Ashok", 4.8, True)
```

### Watch what happens when you forget something now

```python
d1 = Driver(4021, "Ashok")
```

```
TypeError: Driver.__init__() missing 2 required positional
arguments: 'rating' and 'is_online'
```

> 💡 **Read that error carefully. It's beautiful.**
>
> It fired **immediately**, at the line that caused it, naming exactly what's missing.
>
> Compare that to the `AttributeError` two hours later in another file. That transformation — from a distant mystery to an instant, precise complaint — **is why constructors exist.**

---

## 6. Now — What On Earth Is `self`?

You've been staring at it since Topic 4. Time to earn it.

### The problem `self` solves

WhatsApp has around **3 billion** users. There is **one** `User` class in their codebase, with one `send_message` method — one copy of that code, shared by all 3 billion.

Now somebody calls:

```python
ashok.send_message("hello")
```

> 🛑 **STOP AND THINK**
> There's one copy of the method. Three billion possible users.
> When that code runs, **how does it know whose message this is?**

Something has to tell it. That something is `self`.

### The demonstration that makes it click

These two lines do **exactly the same thing**:

```python
d1.accept_ride("R-101")             # what you write
Driver.accept_ride(d1, "R-101")     # what Python actually does
```

Look at the second line. `d1` is being passed in **as the first argument**.

> 💡 **KEY IDEA**
> **A method is just a function stored inside a class.**
> **When you call it through an object, Python quietly passes that object in as the first argument.**
> **`self` is simply the parameter that catches it.**

That's it. `self` isn't magic. It isn't a keyword. It's the parameter that receives the object you called the method on.

Try it yourself — both lines will run:

```python
d1 = Driver(4021, "Ashok", 4.8, True)

d1.accept_ride("R-101")
Driver.accept_ride(d1, "R-101")     # identical result
```

### Reading `__init__` now

```python
def __init__(self, driver_id, name, rating, is_online):
    self.name = name
```

Read that middle line as:

> **`self.name`** *(this particular driver's name)* **`=`** **`name`** *(the value just handed in)*

```
   self.name  =  name
     ▲            ▲
     │            └── the parameter (temporary, disappears)
     └── the object's own attribute (permanent, belongs to the driver)
```

---

## 7. ⚠️ The Trap That Catches Everyone

This is the number one beginner bug in Python OOP. Read it twice.

```python
class Driver:
    def rename(self, new_name):
        name = new_name          # ❌ does absolutely nothing
```

> 🛑 **STOP AND THINK**
> No error. No warning. Program runs fine.
> But the driver's name never changes. **Why?**

Because `name = new_name` creates a brand-new **local variable** called `name`, which lives for about a microsecond and then vanishes when the method ends.

It has nothing to do with the object. You never touched the object.

```python
    def rename(self, new_name):
        self.name = new_name     # ✅ this touches the object
```

> ⚠️ **THE RULE**
> **Every time you touch an attribute — reading or writing — it goes through `self.`**
> No exceptions. Not once. Ever.

Reading has the same trap, but at least it's louder:

```python
def accept_ride(self, ride_id):
    print(f"{name} took the ride")        # ❌ NameError: name is not defined
    print(f"{self.name} took the ride")   # ✅
```

> 🔁 **JAVA CORNER**
> Java's `this` is a **keyword** and it's *optional* when there's no name clash — `name = n;` works fine there.
>
> Python's `self` is **an ordinary parameter** and it is **never optional**. If you carry the Java habit over, your code will silently do nothing.
>
> This one difference causes more Java-to-Python bugs than anything else.

---

## 8. Multiple Constructors — the Java Way and the Python Way

Your class notes list three kinds of constructor:

```
   1. Default            → written by the language when you write none
   2. Non-parameterised  → you write it, takes no arguments
   3. Parameterised      → you write it, takes arguments
```

In Java, a class can have all of them at once — several constructors with the same name and different parameter lists. That's **constructor overloading**.

Now try it in Python:

```python
class Driver:
    def __init__(self):                              # version 1
        self.name = "Random"

    def __init__(self, driver_id, name):             # version 2
        self.driver_id = driver_id
        self.name = name
```

> 🛑 **STOP AND THINK**
> Two `__init__` methods. What happens?

Not an error. Something worse: **the second one silently replaces the first.** Version 1 is simply gone, as if you'd never written it.

> 💡 **Python has no method overloading. One class, one `__init__`.**

### So how does Python solve it? Default arguments.

```python
# uber/driver.py

class Driver:
    def __init__(self, driver_id=100, name="Random", rating=5.0, is_online=True):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online
```

```python
d1 = Driver()                          # no arguments      → 100, "Random", 5.0, True
d2 = Driver(4021, "Ashok", 4.8, True)  # all arguments
d3 = Driver(4021, "Ashok")             # some arguments    → rest use defaults
```

**One `__init__` does the job of all three Java constructors.**

### And Python adds something Java can't do

**Keyword arguments** — name the values as you pass them:

```python
d4 = Driver(name="Meera", driver_id=4088)     # order doesn't matter
```

Which of these two lines is clearer?

```python
Driver(4088, "Meera", 4.9, False)                 # what is False?
Driver(4088, "Meera", 4.9, is_online=False)       # oh. That.
```

> 💡 Use keyword arguments for booleans and anything ambiguous. Your future self will thank you at 2am.

---

## 9. ⚠️ The Mutable Default Trap

One more, and it's famous. Every Python programmer gets caught by it exactly once.

```python
class Driver:
    def __init__(self, name, rides=[]):     # ❌ NEVER do this
        self.name = name
        self.rides = rides
```

Looks perfectly reasonable. Watch:

```python
d1 = Driver("Ashok")
d2 = Driver("Meera")

d1.rides.append("R-101")

print(d2.rides)          # ['R-101']   😱
```

Meera has Ashok's ride.

> 🛑 **STOP AND THINK**
> Use what you learned in Topic 6. That `[]` — when is it created?

**Once.** When the `def` line is first read — not each time the method is called.

So there is exactly **one** list, and every driver created without an explicit `rides` argument gets a label pointing at that same list.

Same object, many labels. **Exactly the picture from Topic 6.**

### The fix

```python
class Driver:
    def __init__(self, name, rides=None):     # ✅
        self.name = name
        self.rides = rides if rides is not None else []
```

Now a **fresh list** is built on every call.

> 💡 **RULE: never use a mutable default argument.** Lists, dictionaries and sets as defaults are always a bug waiting to happen. Use `None` and build inside.

---

## 10. Full Working Code

### `uber/driver.py`

```python
# uber/driver.py

class Driver:
    """A driver in the Uber system."""

    def __init__(self, driver_id=100, name="Random", rating=5.0, is_online=True):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online
        self.rides = []                      # fresh list per driver

    def accept_ride(self, ride_id):
        self.rides.append(ride_id)
        print(f"{self.name} accepted ride {ride_id}")

    def change_status(self):
        self.is_online = not self.is_online
        print(f"{self.name} is online: {self.is_online}")
```

### `uber/client.py`

```python
# uber/client.py

from uber.driver import Driver


def main():
    print("--- Four ways to build a driver ---")
    d1 = Driver()
    d2 = Driver(4021, "Ashok", 4.8, True)
    d3 = Driver(4088, "Meera")
    d4 = Driver(name="Ravi", driver_id=4103)

    for d in (d1, d2, d3, d4):
        print(f"  {d.driver_id:5}  {d.name:8}  {d.rating}  {d.is_online}")

    print("\n--- self: one method, different objects ---")
    d2.accept_ride("R-101")
    d3.accept_ride("R-102")

    print("\n--- proving the rides lists are separate ---")
    print("  Ashok's rides:", d2.rides)
    print("  Meera's rides:", d3.rides)

    print("\n--- these two lines are identical ---")
    d2.change_status()
    Driver.change_status(d2)


if __name__ == "__main__":
    main()
```

### Output

```
--- Four ways to build a driver ---
    100  Random    5.0  True
   4021  Ashok     4.8  True
   4088  Meera     5.0  True
   4103  Ravi      5.0  True

--- self: one method, different objects ---
Ashok accepted ride R-101
Meera accepted ride R-102

--- proving the rides lists are separate ---
  Ashok's rides: ['R-101']
  Meera's rides: ['R-102']

--- these two lines are identical ---
Ashok is online: False
Ashok is online: True
```

---

## 11. What Just Happened?

**Four creation styles, one `__init__`.** Defaults filled the gaps; keyword arguments let us skip past the middle ones.

**`self` did its job.** `d2.accept_ride(...)` and `d3.accept_ride(...)` ran identical code and produced different output, because `self` was a different object each time.

**The rides lists are separate** — proof that moving `[]` into `__init__` fixed the mutable-default bug.

**The last two lines gave identical results**, proving `d2.change_status()` really is `Driver.change_status(d2)`.

### How Python executes `d2 = Driver(4021, "Ashok", 4.8, True)`

```
   1. Python allocates a new, empty Driver object in memory
   2. It calls __init__, passing the new object as `self`
             self       = the new object
             driver_id  = 4021
             name       = "Ashok"
   3. __init__ writes each value onto the object
   4. The finished object is handed back
   5. The label `d2` is attached to it
```

---

## 12. Real-World Analogies

### Amazon account creation

You cannot have an Amazon account with no email address. The signup form won't submit. There's no path through the interface that produces a half-account.

**That's `__init__` with required parameters.**

### The hotel room-service card

A hotel prints **one** "Room Service" card and puts an identical copy in all 200 rooms. Every card says:

> *"Dial 9 to order food to **this room**."*

The words **this room** are `self`.

**The card is identical everywhere — but it means something different depending on which room you're standing in.**

That's one method, three billion users, and `self` telling it which one.

---

## 13. 🎯 Interview Questions

**Q1. What is `__init__`?**

> The initialiser — it runs automatically when an object is created and sets up its attributes. It's the only place that can guarantee an object starts life valid.

**Q2. Is `__init__` a constructor?**

> The precise answer: *"`__init__` is technically an **initialiser** — the object already exists by the time it runs, which is why it receives `self`. The actual constructor is `__new__`, which allocates the object. In everyday code you only ever write `__init__`."*
>
> You'll rarely touch `__new__`, but knowing this distinction marks you out.

**Q3. What is `self`?**

> A reference to the object the method was called on. It's an ordinary first parameter, not a keyword — Python passes the object into it automatically. `obj.method(x)` is exactly `Class.method(obj, x)`.

**Q4. Can Python have multiple constructors?**

> No — a second `__init__` silently replaces the first. Use default arguments to cover the cases, or `@classmethod` factory methods when the *kinds* of input differ.

**Q5. What's wrong with `def __init__(self, items=[])`?**

> The default list is created once, at function-definition time, and shared by every object that doesn't pass one in. Use `None` and build the list inside.

---

## 14. ⚠️ Common Mistakes

| Mistake | Result |
|:--|:--|
| Forgetting `self` in the signature — `def go_online():` | `TypeError` on every call |
| `name = value` instead of `self.name = value` | **Silently does nothing.** The #1 bug. |
| Reading `name` instead of `self.name` | `NameError` |
| Writing two `__init__` methods | Second one wipes out the first, no warning |
| Mutable default argument | Shared state across every object |
| A default before a non-default: `def __init__(self, x=1, y)` | `SyntaxError` |
| `return` a value from `__init__` | `TypeError`. `__init__` fills in `self`; it doesn't return. |

---

## 15. Summary

Building objects field-by-field was long, and — much worse — a forgotten line became a crash in a different file hours later.

We wanted objects to be **born valid**, so we needed code that runs automatically at creation. That's `__init__`.

`self` is how one shared method knows which object it's working on: `obj.method()` is really `Class.method(obj)`.

Python has one `__init__` per class, and covers Java's multiple constructors with **default arguments** — plus keyword arguments, which Java can't do at all.

---

## ✓ Key Takeaways

- **`__init__`** runs automatically when an object is created.
- Missing arguments cause an **immediate, precise `TypeError`** — at the right line.
- **`self`** = the current object. `obj.method(x)` **is** `Class.method(obj, x)`.
- Every attribute access goes through `self.` — **reading and writing**.
- `name = x` without `self.` creates a local variable and silently does nothing.
- **One `__init__` per class.** Use **default arguments** instead of overloading.
- **Never** use a mutable default (`=[]`, `={}`). Use `None`.

---

## ✓ Practice Questions

1. What does this print, and why?
   ```python
   class Driver:
       def __init__(self, name):
           self.name = name
       def rename(self, new_name):
           name = new_name

   d = Driver("Ashok")
   d.rename("Meera")
   print(d.name)
   ```

2. Rewrite these three Java constructors as one Python `__init__`:
   ```
   Driver()
   Driver(int id, String name)
   Driver(int id, String name, double rating, boolean online)
   ```

3. Prove that `d.accept_ride("R-1")` and `Driver.accept_ride(d, "R-1")` are identical. Write the code.

4. Explain the mutable-default bug using the **label picture** from Topic 6, not just "it's shared."

---

## ✓ Mini Assignment

Build `netflix/user.py` with a `User` class:

- `__init__(self, user_id, name, plan="Basic", is_active=True)`
- `self.watch_history = []` — created correctly
- Methods: `watch(title)`, `upgrade_plan(new_plan)`, `deactivate()`

In the client, create four users using **four different calling styles** (all defaults, all explicit, partial, keyword-only).

Then prove that each user's `watch_history` is genuinely separate.

---

## ✓ Real-World Exercise

Find any signup form online — Instagram, Swiggy, your bank.

1. Note which fields are **required** (marked `*`) and which are optional.
2. Write the `__init__` signature that matches: required fields as required parameters, optional ones with defaults.
3. Now ask the design question: **why did they choose those particular fields as mandatory?**

That form *is* a constructor signature. Somebody made exactly the decision you just made.

---
---

# TOPIC 8
# The `static` Idea — Members That Belong to the Class

---

## 1. The Problem

Your manager is back.

> *"I need a number on the dashboard: how many drivers are registered on the platform. Total. Right now."*

Easy, you think. Add a counter to the `Driver` class and bump it every time a driver is created.

Let's write it.

```python
# uber/driver.py

class Driver:
    def __init__(self, name):
        self.name = name
        self.total_drivers = 0
        self.total_drivers = self.total_drivers + 1     # count this one
```

```python
# uber/client.py

d1 = Driver("Ashok")
d2 = Driver("Meera")
d3 = Driver("Ravi")

print(d1.total_drivers)
print(d2.total_drivers)
print(d3.total_drivers)
```

> 🛑 **STOP AND THINK**
> Three drivers were created. What do those three lines print?

Output:

```
1
1
1
```

Three drivers. Every one of them says **one**.

---

## 2. Observation

Let's look at what we actually built.

```
   ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
   │      d1        │   │      d2        │   │      d3        │
   │ name  = Ashok  │   │ name  = Meera  │   │ name  = Ravi   │
   │ total = 1      │   │ total = 1      │   │ total = 1      │
   └────────────────┘   └────────────────┘   └────────────────┘
```

Each driver is counting... **himself**.

Every object got its own private `total_drivers`, set it to 0, added 1, and stopped. Nobody is counting anybody else.

Your class notes put it exactly right:

> *"Will it work? No. The reason is: it is a separate copy for every object."*

> 🛑 **STOP AND THINK**
> Here's the question that unlocks the whole topic:
>
> **Whose fact is "total number of drivers"?**
>
> Is it a fact about *Ashok*? About *Meera*? About *Ravi*?

---

## 3. Think — Whose Fact Is It?

Let me ask about your college instead.

Two pieces of information:

| Piece of information | Whose fact is it? |
|:--|:--|
| Your **roll number** | Yours. Nobody else has it. 3,000 students, 3,000 different roll numbers. |
| Your **college's name** | Not yours. It belongs to the *college*. All 3,000 students share it. |

**Question:** If the college is renamed tomorrow, how many students does that affect?

**All of them. At once.** Because there was only ever one college name.

Now:

**Question:** If you change your roll number, how many students does that affect?

**One.**

> 💡 **THE TEST**
> Ask: *"If this value changes, should it change for everyone at once?"*
>
> **Yes** → it belongs to the class.
> **No** → it belongs to each object.

Apply it to the driver count:

If the total goes from 3 to 4, does Ashok's total go up? And Meera's? And Ravi's?

**Yes — all of them. Simultaneously.** Because there's only one total.

**It's not a fact about any driver. It's a fact about the class as a whole.**

---

## 4. First Principle

> 💡 **KEY IDEA**
> **Some data belongs to each object. Some data belongs to the class itself.**
> **Data that everyone shares must be stored in one place — not copied into every object.**

```
       WHAT WE BUILT (broken)              WHAT WE NEED
   ┌──────┐ ┌──────┐ ┌──────┐          ┌──────┐ ┌──────┐ ┌──────┐
   │  d1  │ │  d2  │ │  d3  │          │  d1  │ │  d2  │ │  d3  │
   │total1│ │total1│ │total1│          └───┬──┘ └───┬──┘ └───┬──┘
   └──────┘ └──────┘ └──────┘              └────────┼────────┘
     ✗ three separate copies                   ┌────▼─────┐
       nobody knows the truth                  │  Driver  │  total = 3
                                               │ (class)  │  ✓ ONE copy
                                               └──────────┘
```

---

## 5. Solution — Class Attributes

> 📖 **Definition**
> **A class attribute belongs to the class itself, not to any object. There is exactly one copy, shared by every object of that class.**

In Java this needs a keyword: `static`. In Python, **there's no keyword — the position tells you everything.**

```python
class Driver:
    total_drivers = 0                  # ← written in the CLASS BODY
                                       #   = belongs to the CLASS

    def __init__(self, name):
        self.name = name               # ← written with self.
                                       #   = belongs to the OBJECT
        Driver.total_drivers += 1      # ← note: Driver.  NOT self.
```

> 💡 **THE RULE: where you write it decides what it is.**
>
> - Directly in the class body → **class attribute** (one copy, shared)
> - With `self.` inside a method → **instance attribute** (one per object)

Let's run it:

```python
d1 = Driver("Ashok")
d2 = Driver("Meera")
d3 = Driver("Ravi")

print(Driver.total_drivers)     # 3   ✅
```

**Three.** Finally.

### Instance or class — some examples

| Belongs to each object | Belongs to the class |
|:--|:--|
| Driver's name, rating | Total driver count |
| Bank account balance | The bank's interest rate |
| Product price | The company's GST number |
| Netflix user's watch history | Maximum profiles per account |
| Student's roll number | College name |
| Swiggy order total | Platform delivery fee |

---

## 6. ⚠️ THE BIGGEST TRAP IN THIS CHAPTER

Now pay attention, because this next bit is where most students lose an afternoon.

Look at that line again:

```python
Driver.total_drivers += 1
```

Why did I write `Driver.` and not `self.`? We use `self.` everywhere else. Surely this works too?

```python
def __init__(self, name):
    self.name = name
    self.total_drivers += 1        # ← looks fine. Runs fine.
```

> 🛑 **STOP AND THINK**
> No error. It executes. What is `Driver.total_drivers` after creating three drivers?

Let's find out:

```python
d1 = Driver("Ashok")
d2 = Driver("Meera")

print("Driver.total_drivers →", Driver.total_drivers)
print("d1.total_drivers     →", d1.total_drivers)
print("d2.total_drivers     →", d2.total_drivers)
print("d1.__dict__          →", d1.__dict__)
```

```
Driver.total_drivers → 0        ← never changed!
d1.total_drivers     → 1
d2.total_drivers     → 1
d1.__dict__          → {'name': 'Ashok', 'total_drivers': 1}
```

**We're back to the original bug.** Every driver counting himself.

### Why? Split the line in half.

`self.total_drivers += 1` is shorthand for:

```python
self.total_drivers = self.total_drivers + 1
       ▲                      ▲
     WRITE                  READ
```

Those two halves behave **completely differently**:

```
   THE READ  (right-hand side)
   ───────────────────────────
   Python looks for total_drivers on the OBJECT
        → not there
   Falls back to the CLASS
        → found it: 0
   Result: 0 + 1 = 1


   THE WRITE  (left-hand side)
   ───────────────────────────
   self.total_drivers = 1
   Assignment through `self` ALWAYS writes to the OBJECT
        → creates a NEW instance attribute on this one driver
   The class attribute is never touched.
```

> 💡 **THE ASYMMETRY — memorise this**
>
> | Operation | Through `self` | Through the class name |
> |:--|:--|:--|
> | **Reading** a class attribute | ✅ works (falls back to the class) | ✅ works |
> | **Writing** a class attribute | ❌ creates an instance copy | ✅ correct |
>
> **Reading falls through to the class. Writing never does.**

And look at the evidence in `__dict__`:

```python
{'name': 'Ashok', 'total_drivers': 1}
```

`total_drivers` is sitting **inside the object**. It shouldn't be there. That's your proof.

> ✅ **THE FIX: always write class attributes through the class name.**
> ```python
> Driver.total_drivers += 1
> ```

> 🔁 **JAVA CORNER**
> In Java, `totalDrivers++` inside the constructor just works — the `static` keyword protects you, and there's no way to accidentally create an instance copy.
>
> **Python gives you no such protection.** This is genuinely on you. It's the sharpest difference between the two languages in this whole chapter.

---

## 7. Trap Number Two — Mutable Class Attributes

There's a second version of this, and it's sneakier.

```python
class Driver:
    rides = []                        # ❌ class attribute, and it's a LIST

    def __init__(self, name):
        self.name = name

    def add_ride(self, ride_id):
        self.rides.append(ride_id)
```

```python
d1 = Driver("Ashok")
d2 = Driver("Meera")

d1.add_ride("R-101")

print(d2.rides)          # ['R-101']   😱
```

> 🛑 **STOP AND THINK**
> Hang on. In the counter example, `self.x = ...` created an instance copy.
> So why didn't `self.rides.append(...)` create an instance copy here?

Because **there is no assignment.**

`append` doesn't write to `self.rides` — it *reaches into* the list that lookup found (the class's list) and modifies it in place.

Look back at Topic 6: this is mutation versus rebinding. **Only `=` writes to the instance.**

### The fix

```python
class Driver:
    def __init__(self, name):
        self.name = name
        self.rides = []           # ✅ a fresh list for every driver
```

> 💡 **RULE OF THUMB**
> **Class attributes should hold immutable values only** — `int`, `str`, `float`, `bool`, constants.
> **Anything mutable belongs in `__init__`.**

(And yes — this is the same bug as the mutable default argument from Topic 7, wearing a different hat. Same root cause: one object, many labels.)

---

## 8. Static Methods

We've handled shared *data*. Now shared *behaviour*.

Your class notes ask a question that's genuinely clever:

> *"If a driver wants to **register**, do you think his object is already created in memory?"*

> 🛑 **STOP AND THINK**
> Ashok downloads the Uber Driver app. He hasn't signed up yet.
> Is there an `Ashok` object anywhere in Uber's servers?

**No.** Of course not. He doesn't exist in the system yet.

> *"Then how will he call a method?"*

That's the problem in one sentence. A normal method needs an object to be called on:

```python
ashok.register()          # ← but there IS no ashok yet!
```

**Registration is the thing that creates the object.** So it cannot possibly require the object to already exist.

> 💡 The sign-up button has to work **before** you have an account.

### The solution

```python
class Driver:
    total_drivers = 0

    def __init__(self, name):
        self.name = name
        Driver.total_drivers += 1

    def accept_ride(self, ride_id):          # needs a SPECIFIC driver
        print(f"{self.name} took {ride_id}")

    @staticmethod
    def register():                          # needs NO driver
        print("This is Register Method")
```

```python
Driver.register()          # called on the CLASS. No object anywhere.
```

Two things to notice:

1. **`@staticmethod` is a decorator** — the `@` line modifies the function beneath it. For now, read it as a label meaning *"this method receives no `self`."*
2. **There is no `self` parameter** — because there's no object to receive.

And the rule follows automatically:

> **A static method cannot touch instance attributes.**
>
> Not because Python forbids it out of spite — because **there is no object.** There's no `self` to reach them through. `self.name` — *whose* name? There's no answer.

---

## 9. When Does the Class Body Run?

Java has a **static block** — code that runs once, when the class is first loaded, before any object exists.

Python needs no such thing, because **the class body already is one.**

```python
# uber/driver.py

class Driver:
    total_drivers = 0
    print("driver.py: the Driver class has been defined")
```

Everything written directly inside `class Driver:` — not inside a method — runs **once**, the moment Python reads the class definition.

> 🛑 **STOP AND THINK**
> When does `client.py` read `driver.py`?

At the **import** line. Which means that `print` fires *before* `main()` even starts.

Let's prove it:

```python
# uber/driver.py
class Driver:
    total_drivers = 0
    print("1. class body")

    def __init__(self, name):
        print("3. __init__")
        self.name = name
        Driver.total_drivers += 1
```

```python
# uber/client.py
from uber.driver import Driver          # ← triggers "1. class body"


def main():
    print("2. main starts")
    Driver("Ashok")
    Driver("Meera")


if __name__ == "__main__":
    main()
```

### Output

```
1. class body          ← at import time, before main() runs
2. main starts
3. __init__            ← first object
3. __init__            ← second object
```

**The class body never runs again**, no matter how many objects you create — and importing the module a second time won't re-run it either, because Python caches imported modules.

That's Java's static block, for free, with no extra syntax.

---

## 10. Full Working Code

### `uber/driver.py`

```python
# uber/driver.py

class Driver:
    """A driver in the Uber system."""

    # ---- class attribute: ONE copy, shared by everyone ----
    total_drivers = 0
    MAX_RATING = 5.0                       # a shared constant

    def __init__(self, driver_id, name, rating=5.0):
        # ---- instance attributes: one copy PER driver ----
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.rides = []                    # mutable → must be per-object

        Driver.total_drivers += 1          # class name, NOT self

    def accept_ride(self, ride_id):
        self.rides.append(ride_id)
        print(f"{self.name} accepted {ride_id}")

    @staticmethod
    def register():
        print("This is Register Method")
```

### `uber/client.py`

```python
# uber/client.py

from uber.driver import Driver


def main():
    print("--- static method, before any driver exists ---")
    Driver.register()
    print("  total so far:", Driver.total_drivers)

    print("\n--- creating three drivers ---")
    d1 = Driver(4021, "Ashok", 4.8)
    d2 = Driver(4088, "Meera", 4.9)
    d3 = Driver(4103, "Ravi", 4.7)
    print("  total now:", Driver.total_drivers)

    print("\n--- shared constant, same for everyone ---")
    print("  Driver.MAX_RATING =", Driver.MAX_RATING)
    print("  d1.MAX_RATING     =", d1.MAX_RATING, " (read falls through)")

    print("\n--- rides lists are separate ---")
    d1.accept_ride("R-101")
    d2.accept_ride("R-102")
    print("  Ashok:", d1.rides)
    print("  Meera:", d2.rides)

    print("\n--- THE TRAP, demonstrated ---")
    d1.total_drivers = 999                 # writing through self
    print("  d1.total_drivers     =", d1.total_drivers, " (instance copy!)")
    print("  d2.total_drivers     =", d2.total_drivers, " (class, untouched)")
    print("  Driver.total_drivers =", Driver.total_drivers)
    print("  d1.__dict__          =", d1.__dict__)


if __name__ == "__main__":
    main()
```

### Output

```
--- static method, before any driver exists ---
This is Register Method
  total so far: 0

--- creating three drivers ---
  total now: 3

--- shared constant, same for everyone ---
  Driver.MAX_RATING = 5.0
  d1.MAX_RATING     = 5.0  (read falls through)

--- rides lists are separate ---
Ashok accepted R-101
Meera accepted R-102
  Ashok: ['R-101']
  Meera: ['R-102']

--- THE TRAP, demonstrated ---
  d1.total_drivers     = 999  (instance copy!)
  d2.total_drivers     = 3  (class, untouched)
  Driver.total_drivers = 3
  d1.__dict__          = {'driver_id': 4021, 'name': 'Ashok', 'rating': 4.8, 'rides': ['R-101'], 'total_drivers': 999}
```

---

## 11. What Just Happened?

**`Driver.register()` ran with zero drivers in existence.** That's the whole point of a static method.

**`d1.MAX_RATING` worked** even though `MAX_RATING` isn't on the object — the read fell through to the class.

**`d1.total_drivers = 999` broke the link.** Look at that last line: `total_drivers` is now sitting inside `d1.__dict__`. Ashok has a private copy. `d2` and the class are untouched.

> 💡 **That `__dict__` output is your debugging superpower.**
> If a class attribute shows up inside an object's `__dict__`, you've hit the trap.

### The lookup rule, one last time

```
   You write:   obj.x

   1. Look in the OBJECT      (obj.__dict__)      ── found? return it
   2. Look in the CLASS       (Driver.__dict__)   ── found? return it
   3. AttributeError

   But:  obj.x = value   ALWAYS writes to step 1. Never step 2.
```

---

## 12. Real-World Analogies

### Swiggy's delivery fee

- Your **order total** → yours. Different for every order. **Instance.**
- The **platform delivery fee** → set by Swiggy. Same for everyone. **Class.**

When Swiggy raises the fee from ₹30 to ₹35, do they edit ten million order objects?

No. They change **one value**, and every order sees it instantly.

### A bank's interest rate

Ten million accounts. Each has its own **balance** (instance). All share the **interest rate** (class).

The RBI changes rates. The bank updates **one number**.

> 🛑 **STOP AND THINK**
> What would happen if the interest rate were an instance attribute, copied into ten million accounts?

You'd have to update ten million records. And if the update crashed halfway, half your customers would be on the old rate — with no way to tell which half.

**That's not a performance problem. That's a correctness disaster.**

---

## 13. 🎯 Interview Questions

**Q1. Difference between a class attribute and an instance attribute?**

> A class attribute belongs to the class — one copy, shared by every object. An instance attribute belongs to one object — one copy per object. In Python the difference is *where you write it*: the class body versus `self.` inside a method.

**Q2. Why doesn't `self.counter += 1` work for a class-level counter?**

> Because `+=` is a read and a write. The read falls back to the class, but the write always creates a new **instance** attribute — shadowing the class attribute. The class value never changes. Always write through the class name.

**Q3. Why must `register()` be a static method?**

> Because registration is what creates the driver, so no driver object exists when it's called. A normal method needs an object to be invoked on; a static method doesn't.

**Q4. Can a static method access instance attributes?**

> No. It doesn't receive `self`, and more fundamentally there may be no object at all — so there's nothing for `self.name` to refer to.

**Q5. Does Python have a static block like Java?**

> It doesn't need one. The class body itself executes exactly once, when the class definition is first read — which is at import time. Same effect, no extra syntax.

---

## 14. ⚠️ Common Mistakes

| Mistake | Result |
|:--|:--|
| `self.counter += 1` for a class attribute | **Silently broken.** Every object counts itself. |
| Mutable class attribute (`rides = []`) | All objects share one list |
| Reading `d1.total_drivers` and assuming it's the class value | It might be an instance copy shadowing it. Check `__dict__`. |
| Making everything a class attribute | Now every object shares data that should be private |
| Expecting a static method to see `self` | It has no object |
| Forgetting `@staticmethod` and omitting `self` | `TypeError` on call |

---

## 15. Summary

Our counter said "1" three times, because every driver was counting himself.

The fix came from one question: **whose fact is this?** The total isn't a fact about any driver — it's a fact about the class. So it lives on the class.

Then the trap: `self.x += 1` reads from the class but **writes to the object**, silently recreating the original bug. Always write through the class name.

Static methods exist for the mirror-image reason: some behaviour can't wait for an object, because it's the thing that *makes* the object.

And Python's class body gives you Java's static block for free.

---

## ✓ Key Takeaways

- **Class attribute** = one copy, shared. **Instance attribute** = one per object.
- **Position decides it** — class body vs `self.` inside a method. No keyword needed.
- **The test:** *"If this changes, should it change for everyone at once?"*
- ⚠️ **Reading falls through to the class. Writing never does.**
- ✅ Always write class attributes as `ClassName.attribute = ...`
- **Class attributes must be immutable.** Mutable state goes in `__init__`.
- **`@staticmethod`** = a method with no `self`, callable without any object.
- **The class body runs once, at import time** — Java's static block, for free.

---

## ✓ Practice Questions

1. Predict all three, then run:
   ```python
   class Counter:
       count = 0
       def __init__(self):
           self.count += 1

   a, b = Counter(), Counter()
   print(Counter.count, a.count, b.count)
   ```
   Then fix the class.

2. For a **Netflix `User`**, classify each as instance or class: `watch_history`, `max_profiles`, `email`, `monthly_price`, `current_plan`.

3. Why does `self.rides.append(x)` modify shared state while `self.count += 1` doesn't? Answer using *mutation vs rebinding* from Topic 6.

4. Write a `@staticmethod` on `Driver` called `is_valid_rating(value)` that returns `True` for 0–5. Explain why it doesn't need `self`.

---

## ✓ Mini Assignment

Build `bank/account.py`:

- **Class attributes:** `bank_name = "State Bank"`, `interest_rate = 0.04`, `total_accounts = 0`
- **Instance attributes:** `account_number`, `holder_name`, `balance`
- **Instance methods:** `deposit()`, `withdraw()`, `add_interest()`
- **Static method:** `bank_details()` — printable without any account existing

In the client:
1. Create three accounts, print `total_accounts`.
2. Change `Account.interest_rate` **once**, then show all three accounts using the new rate.
3. Now deliberately trigger the trap — write `acc1.interest_rate = 0.99` — and print all three plus `acc1.__dict__`. Explain what you see in two sentences.

---

## ✓ Real-World Exercise

Open **Swiggy** or **Zomato** and look at one order screen.

List every number you can see. For each one, decide: **instance or class?**

Item price · delivery fee · GST rate · restaurant rating · your order total · platform fee · packaging charge

Then find the one that's genuinely ambiguous — where you could argue either way — and write a paragraph on which you'd choose and why.

*(Hint: think about a restaurant that sets its own packaging charge.)*

---
---

# TOPIC 9
# Pass by Value — Simple Values vs Objects

---

## 1. The Problem

Two functions. Both take something, both change it. **Predict both outputs before reading on.**

```python
def add_thirty(x):
    x = x + 30


def change_name(driver):
    driver.name = "Xyz"


number = 10
add_thirty(number)
print(number)              # ← prediction?

d1 = Driver(4021, "Ashok", 4.8)
change_name(d1)
print(d1.name)             # ← prediction?
```

> 🛑 **STOP AND THINK**
> Write down both answers. Don't skip this — the surprise is the lesson.

Output:

```
10          ← unchanged
Xyz         ← changed
```

**The same idea gave opposite results.**

Both functions took something in. Both modified it. One change survived. One vanished.

If you can't explain why, you'll write this bug in production one day. So let's explain it properly.

---

## 2. Observation

Put the two functions side by side and stare at them:

```python
def add_thirty(x):
    x = x + 30              # ← there's an  =  sign here

def change_name(driver):
    driver.name = "Xyz"     # ← there's an  =  sign here too
```

They look almost identical. Both have an assignment.

But look more carefully at **what's on the left of the `=`**:

```
   x            ← the parameter ITSELF
   driver.name  ← something INSIDE the object the parameter points to
```

> 🛑 **STOP AND THINK**
> One assignment targets the parameter. The other targets something *inside* what the parameter points to.
>
> Does that difference matter?

---

## 3. Think — Back to the House

Remember the address slip from Topic 6? Bring it back. It answers this completely.

You photocopy your home address and hand the copy to a friend.

### Case A — your friend drives to the address and paints your door pink.

You come home. What colour is the door?

**Pink.** There was only one house, and they went to it.

### Case B — your friend scratches out the address on their copy and writes a different one.

You come home. What's on **your** slip? What colour is your door?

**Your slip is unchanged. Your door is unchanged.** They edited *their photocopy*, not your house.

> 💡 Two completely different actions:
>
> | Action | Name | Visible to you? |
> |:--|:--|:--|
> | Go to the house and change it | **Mutation** | ✅ Yes |
> | Change what the slip points to | **Rebinding** | ❌ No |

Now map it back:

```python
def add_thirty(x):
    x = x + 30              # REBINDING — scribbles on the photocopy

def change_name(driver):
    driver.name = "Xyz"     # MUTATION — drives there and paints the door
```

**That's the whole answer.**

---

## 4. First Principle

> 💡 **KEY IDEA**
> **When you pass something to a function, the function gets a COPY OF THE REFERENCE — not a copy of the object.**
>
> - **Change the object it points to** → the caller sees it. (mutation)
> - **Point the parameter somewhere else** → the caller sees nothing. (rebinding)

```
   add_thirty(number)                     change_name(d1)
   ────────────────────────────           ──────────────────────────────
   number (caller)   ──► [ 10 ]           d1     (caller) ──┐
   x      (function) ──► [ 10 ]                             ├──► [ Driver ]
                                          driver (function)─┘
   x      (function) ──► [ 40 ]  REBOUND        ▲
   number (caller)   ──► [ 10 ]  untouched      └── copy of the REFERENCE,
                                                    pointing at the SAME object
                                                    → the edit is visible to both
```

### Why can't `add_thirty` mutate the number?

Because integers are **immutable** — they cannot be changed. There is no way to "go inside" the number 10 and make it 40. `x + 30` doesn't modify 10; it *builds a brand-new object*, and `x =` points the local label at it.

> 📖 **Python's terminology**
> This is called **pass by object reference** or **call by sharing**.
>
> > 🔁 **JAVA CORNER** — Java calls the same behaviour **"pass by value"**, and says *everything* is pass by value: for a primitive the value is copied, for an object the **reference** is copied. Different words, identical behaviour. The line that divides things is different too:
> >
> > | Java's divide | Python's divide |
> > |:--|:--|
> > | primitive vs object | **immutable vs mutable** |

### The two categories in Python

| Immutable — behaves like `x` above | Mutable — behaves like `driver` above |
|:--|:--|
| `int`, `float`, `bool`, `str`, `tuple` | `list`, `dict`, `set`, **and every class you write** |

---

## 5. The Rule

> 💡 **MEMORISE THIS TABLE**
>
> | What the function does | Does the caller see it? |
> |:--|:--|
> | **Mutates** the object — `obj.attr = ...`, `lst.append(...)` | ✅ **YES** |
> | **Rebinds** the parameter — `obj = something_new` | ❌ **NO** |

Two things that look nearly identical:

```python
def f(nums):
    nums.append(4)          # ✅ MUTATES → caller sees [1, 2, 3, 4]

def g(nums):
    nums = nums + [4]       # ❌ REBINDS → builds a new list, caller sees nothing
```

Same intent. **Opposite result.** The only difference is whether you changed the existing object or made a new one.

---

## 6. Python Code

```python
# uber/client.py

from uber.driver import Driver


def add_thirty(x):
    """Rebinds a local name. The caller is untouched."""
    x = x + 30


def change_name(driver):
    """Mutates the object. The caller SEES this."""
    driver.name = "Xyz"


def replace_driver(driver):
    """Rebinds the parameter. The caller sees NOTHING."""
    driver = Driver(9999, "Ghost", 1.0)
    driver.name = "Zzz"


def add_ride_good(rides):
    rides.append("R-999")           # mutation


def add_ride_bad(rides):
    rides = rides + ["R-888"]       # rebinding


def main():
    print("--- 1. immutable: int ---")
    number = 10
    add_thirty(number)
    print("  number =", number)                  # 10

    print("\n--- 2. mutable: our own object ---")
    d1 = Driver(4021, "Ashok", 4.8)
    change_name(d1)
    print("  d1.name =", d1.name)                # Xyz

    print("\n--- 3. rebinding an object parameter ---")
    replace_driver(d1)
    print("  d1.name =", d1.name)                # still Xyz

    print("\n--- 4. lists: mutation vs rebinding ---")
    rides = ["R-101"]
    add_ride_good(rides)
    print("  after add_ride_good:", rides)
    add_ride_bad(rides)
    print("  after add_ride_bad: ", rides)


if __name__ == "__main__":
    main()
```

### Output

```
--- 1. immutable: int ---
  number = 10

--- 2. mutable: our own object ---
  d1.name = Xyz

--- 3. rebinding an object parameter ---
  d1.name = Xyz

--- 4. lists: mutation vs rebinding ---
  after add_ride_good: ['R-101', 'R-999']
  after add_ride_bad:  ['R-101', 'R-999']
```

---

## 7. What Just Happened?

**Case 1 — unchanged.** `int` is immutable, so `x = x + 30` had to build a new object and point the local name at it.

**Case 2 — changed.** `driver.name = "Xyz"` reached *through* the reference and edited the real object.

**Case 3 — the proof.** `replace_driver` created a whole new `Driver` and pointed its local name at it. The caller's `d1` never moved. **The function's work was completely invisible.**

**Case 4 — the pair that matters.** `add_ride_good` mutated and the caller saw it. `add_ride_bad` ran, built a new list, threw it away, and changed nothing. Notice the output is identical on both lines — because the second call did literally nothing.

> 🛑 **STOP AND THINK**
> `add_ride_bad` had no error, no warning, and no effect.
> How long would it take you to find that bug in a 40,000-line codebase?

---

## 8. Why This Matters — A Real Bug

Here's a bug that has shipped to production at real companies:

```python
def assign_trip(driver, trip):
    driver.is_online = False           # ✅ the caller's driver IS updated
    driver = find_backup_driver()      # ❌ the caller sees NOTHING
    driver.current_trip = trip         # ...and this updates the wrong object
```

Read what the author *intended*: mark this driver busy, and if there's a backup, use that one instead.

Read what actually happens:

1. The caller's driver is marked **offline**. ✅
2. The local name `driver` is pointed at a different object. The caller has no idea.
3. The trip is assigned to the backup — an object the caller never sees.

**Result:** the original driver is now offline and assigned to nothing. The passenger waits for a car that will never arrive. And there is no error message anywhere.

> 💡 This is why we spent a whole topic on it. The distinction between mutation and rebinding is not academic trivia — it's the difference between working software and a silent, expensive failure.

---

## 9. Real-World Analogies

### A shared Google Doc

You send someone a **link** to your document.

- They open it and edit a paragraph → **you see the change.** (mutation)
- They close it and create their own new document → **your doc is untouched.** (rebinding)

The link is the reference. The document is the object.

### A WhatsApp group

You add a friend to a group. Both of you now have a reference to the same group.

- They change the group photo → **everyone sees it.**
- They leave and start a brand-new group → **your group is unaffected.**

---

## 10. 🎯 Interview Questions

**Q1. Is Python pass-by-value or pass-by-reference?**

> Neither, precisely. It's **pass by object reference** (call by sharing) — the function receives a copy of the reference. Mutating the object is visible to the caller; rebinding the parameter is not.

**Q2. Why does modifying a list inside a function affect the caller, but reassigning it doesn't?**

> `append` mutates the existing object, which both names point to. `nums = nums + [4]` builds a *new* list and rebinds only the local name — the caller's name still points at the original.

**Q3. `x = 10; f(x)` where `f` does `x += 1`. Why is `x` still 10?**

> `int` is immutable. `x += 1` can't modify the object, so it creates a new one and rebinds the local name. The caller's name is untouched.

**Q4. How is this different from Java?**

> Behaviourally it isn't — Java calls it "pass by value" and copies the reference for objects, which produces identical results. The dividing line differs: Java splits primitives from objects; Python splits immutable from mutable.

---

## 11. ⚠️ Common Mistakes

| Mistake | Result |
|:--|:--|
| Reassigning a parameter and expecting the caller to see it | Silent no-op. The worst kind of bug. |
| Passing a list to a function and assuming it's safe | It isn't. The function can mutate it. |
| `nums = nums + [x]` when you meant `nums.append(x)` | Looks right, does nothing |
| Believing Python "copies" arguments | It copies the reference, never the object |
| Mutating a caller's list without documenting it | Technically works. Your teammate will not forgive you. |

---

## 12. Summary

Two functions, both with an assignment, opposite results.

The difference: one **mutated** the object (visible to the caller), one **rebound** the parameter (invisible).

Python passes a **copy of the reference**. Immutable things can only ever be rebound, so they look "safe." Mutable things can be reached into and changed.

**Mutation is visible. Rebinding is not.** That one line predicts every case.

---

## ✓ Key Takeaways

- Python uses **call by sharing** — the function gets a copy of the *reference*.
- **Mutation** (`obj.attr = ...`, `lst.append(...)`) → caller sees it ✅
- **Rebinding** (`obj = new_thing`) → caller sees nothing ❌
- **Immutable:** `int`, `float`, `bool`, `str`, `tuple`
- **Mutable:** `list`, `dict`, `set`, and every class you write
- Java calls this "pass by value" — **same behaviour, different words**.
- Rebinding a parameter and expecting the caller to notice is a **silent** bug.

---

## ✓ Practice Questions

1. Predict, then run:
   ```python
   def f(d):
       d["a"] = 99
   def g(d):
       d = {"a": 99}

   data = {"a": 1}
   f(data); print(data)
   g(data); print(data)
   ```

2. Fix `assign_trip` from Section 8 so the intent actually works. (Hint: a function can *return* something.)

3. Write a function that takes a `Driver` and safely gives you a modified version **without** touching the caller's object. What do you have to do?

4. Why can't a function ever modify an `int` the caller passed in? Answer in one sentence using the word *immutable*.

---

## ✓ Mini Assignment

Write `passing_demo.py` with **six** functions:

1. Mutates an int (prove it's impossible)
2. Rebinds an int
3. Mutates a list
4. Rebinds a list
5. Mutates a `Driver`
6. Rebinds a `Driver`

Print the caller's value before and after each. Above each function, write a one-line comment predicting the result — then check whether you were right.

---

## ✓ Real-World Exercise

Find a function in any code you've written that takes a list or dictionary.

Ask: **does it mutate the argument?**

If yes, ask: **would someone reading the function name know that?**

`sort_and_return(items)` that secretly sorts the caller's list in place is a small betrayal. Rename it, or stop mutating. This is a real code-review comment you'll receive one day — better to receive it from this page.

---
---

# TOPIC 10
# `to_string()` → `__str__`

---

## 1. The Problem

You've built your `Driver` class. Let's just print one.

```python
d1 = Driver(4021, "Ashok", 4.8)
print(d1)
```

```
<uber.driver.Driver object at 0x7f8b2c0d1a90>
```

> 🛑 **STOP AND THINK**
> Is that wrong? Is it a bug?

No. It's completely correct. It tells you: this is a `Driver`, from the `uber.driver` module, living at memory address `0x7f8b2c0d1a90`.

Every word of that is true.

**And it is completely useless to you.**

---

## 2. Observation — 2am

Let me make you feel why this matters.

It's 2am. You're on call. Dispatch is failing in one city and the alerts are going off. You open the logs:

```
ERROR  Failed to assign trip: <uber.driver.Driver object at 0x7f8b2c0d1a90>
ERROR  Failed to assign trip: <uber.driver.Driver object at 0x7f8b2c0d1b40>
ERROR  Failed to assign trip: <uber.driver.Driver object at 0x7f8b2c0d1cf0>
ERROR  Failed to assign trip: <uber.driver.Driver object at 0x7f8b2c0d1e20>
```

> 🛑 **STOP AND THINK**
> What have you learned from those four lines?

That four drivers failed. That's it. You don't know who, where, what rating, or whether they were online.

You have no idea what's wrong, and the city is still broken.

Now imagine the exact same logs, but like this:

```
ERROR  Failed to assign trip: Driver(id=4021, name='Ashok', rating=4.8, online=False)
ERROR  Failed to assign trip: Driver(id=4088, name='Meera', rating=4.9, online=False)
ERROR  Failed to assign trip: Driver(id=4103, name='Ravi',  rating=4.7, online=False)
ERROR  Failed to assign trip: Driver(id=4110, name='Priya', rating=4.6, online=False)
```

> 🛑 **STOP AND THINK**
> Read the last column. Spot it?

**`online=False`. Every single one.**

Dispatch is trying to assign trips to **offline drivers**. You found the bug in three seconds.

> 💡 That is the entire value of this topic. It isn't cosmetic. It's the difference between a system you can debug and a system you can only stare at.

---

## 3. Think

**Question:** When you call `print(d1)`, what does `print` actually need?

It needs **text**. Printing means writing characters to a screen. It cannot print an object — objects aren't made of characters.

So something must convert your object into text.

**Question:** Does Python know how *you* want a driver described?

Should it print the name? The ID? All five fields? Just the rating?

...

Python has no idea. So it falls back to the only thing it definitely knows: the class name and the address.

> 🛑 **STOP AND THINK**
> Who is the only person who knows how a `Driver` should be described in one line?

**You.** The person who wrote the class.

So Python needs to *ask you*. It needs a place where you can supply the answer.

---

## 4. First Principle

> 💡 **KEY IDEA**
> **`print()` doesn't know how to describe your object.**
> **So it asks the object to describe itself — and you get to write that answer.**

The place you write it is a method called **`__str__`**.

---

## 5. Solution — `__str__`

> 📖 **Definition**
> **`__str__` defines how an object should be represented as a human-readable string.**

```python
# uber/driver.py

class Driver:
    def __init__(self, driver_id, name, rating, is_online=True):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online

    def __str__(self):
        return (f"Driver(id={self.driver_id}, name='{self.name}', "
                f"rating={self.rating}, online={self.is_online})")
```

```python
d1 = Driver(4021, "Ashok", 4.8)
print(d1)
```

```
Driver(id=4021, name='Ashok', rating=4.8, online=True)
```

You never call `__str__` yourself. **`print()` calls it for you.**

### Where it kicks in

```python
print(d1)                       # ✅ calls __str__
text = str(d1)                  # ✅ calls __str__
print(f"Assigned to {d1}")      # ✅ f-strings call it too
```

### `__str__` is a *dunder* method

Double UNDERscore. You've already met one — `__init__`.

These are Python's hooks into built-in behaviour:

| Dunder | Hooks into |
|:--|:--|
| `__init__` | creating an object |
| `__str__` | `print()` and `str()` |

You'll meet many more later (`__len__`, `__eq__`, `__add__`). The pattern is always the same: **Python has a built-in behaviour, and a dunder method is where you customise it for your class.**

> 🔁 **JAVA CORNER**
> Java's equivalent is `toString()`, inherited from `Object` and overridden with `@Override`. Without it, `System.out.println(d1)` prints `uber.Driver@1b6d3586` — the same "class name plus address" fallback, for the same reason.

---

## 6. ⚠️ The Two Classic Mistakes

### Mistake 1: printing instead of returning

```python
def __str__(self):
    print(f"Driver {self.name}")      # ❌ WRONG
```

> 🛑 **STOP AND THINK**
> What happens when you run `print(d1)` with that?

Here's the actual result — I ran it:

```
Driver Ashok
Traceback (most recent call last):
  ...
TypeError: __str__ returned non-string (type NoneType)
```

Read that carefully, because it's a *two-part* failure:

1. The `print` **inside** `__str__` ran, so "Driver Ashok" appeared on screen.
2. Then `__str__` finished and returned **nothing** — and a method that returns `None` where Python expected a string is a `TypeError`.

The confusing part is that you *see the right text* immediately before the crash. Students often assume the text means it worked and go hunting elsewhere.

```python
def __str__(self):
    return f"Driver {self.name}"      # ✅ RIGHT
```

**`__str__` returns text. It does not print.** `print` does the printing.

### Mistake 2: returning something that isn't a string

```python
def __str__(self):
    return self.driver_id             # ❌ TypeError: __str__ returned non-string
```

Wrap it: `return str(self.driver_id)`.

---

## 7. Full Code

### `uber/driver.py`

```python
# uber/driver.py

class Driver:
    """A driver in the Uber system."""

    total_drivers = 0

    def __init__(self, driver_id, name, rating=5.0, is_online=True):
        self.driver_id = driver_id
        self.name = name
        self.rating = rating
        self.is_online = is_online
        Driver.total_drivers += 1

    def change_status(self):
        self.is_online = not self.is_online

    def __str__(self):
        status = "online" if self.is_online else "offline"
        return f"Driver #{self.driver_id} {self.name} (⭐{self.rating}, {status})"
```

### `uber/client.py`

```python
# uber/client.py

from uber.driver import Driver


def main():
    d1 = Driver(4021, "Ashok", 4.8)
    d2 = Driver(4088, "Meera", 4.9)
    d3 = Driver(4103, "Ravi", 4.7)

    print("--- printing objects directly ---")
    print(d1)
    print(d2)

    print("\n--- inside an f-string ---")
    print(f"Trip R-101 assigned to {d1}")

    print("\n--- a realistic log line ---")
    d3.change_status()
    print(f"ERROR  Failed to assign trip: {d3}")

    print("\n--- str() gives you the text ---")
    text = str(d1)
    print("  type:", type(text))
    print("  value:", text)


if __name__ == "__main__":
    main()
```

### Output

```
--- printing objects directly ---
Driver #4021 Ashok (⭐4.8, online)
Driver #4088 Meera (⭐4.9, online)

--- inside an f-string ---
Trip R-101 assigned to Driver #4021 Ashok (⭐4.8, online)

--- a realistic log line ---
ERROR  Failed to assign trip: Driver #4103 Ravi (⭐4.7, offline)

--- str() gives you the text ---
  type: <class 'str'>
  value: Driver #4021 Ashok (⭐4.8, online)
```

---

## 8. What Just Happened?

**`print(d1)`** → Python asked the object "describe yourself" → `__str__` ran → returned a string → `print` printed it.

**The f-string did the same thing.** Any place Python needs text from your object, `__str__` is where it looks.

**Look at that ERROR line.** It says `offline` right there in the message. That's the 2am scenario, solved.

**`str(d1)` returned an actual `str` object** — which you could write to a file, send over a network, or store in a log.

### How Python executes `print(d1)`

```
   print(d1)
      │
      ▼  print needs TEXT, but d1 is an object
      │
      ▼  Python asks: does Driver define __str__?
      │
      ├── YES → call it, use the returned string
      │
      └── NO  → fall back to "<module.Class object at 0x...>"
```

---

## 9. Real-World Analogy

### A conference name tag

You are a complete human being — your history, your skills, your opinions, decades of life.

At a conference you wear a badge that says:

```
   ┌─────────────────────┐
   │      ASHOK          │
   │  Backend Engineer   │
   │      Uber           │
   └─────────────────────┘
```

Three lines. Obviously not "all of you." But it's the **most useful three lines** for the situation.

`__str__` is your object's name tag. **You decide which three lines matter.**

### Netflix's "Continue Watching"

A `Video` object holds a title, duration, cast, codec, thumbnail URLs, subtitle tracks, licensing regions, and encoding profiles.

The card on your screen shows: **the title and how far you got.**

Same object. One deliberately chosen summary.

---

## 10. 🎯 Interview Questions

**Q1. What is `__str__`?**

> A dunder method defining how an object is represented as human-readable text. `print()` and `str()` call it automatically. Without it, Python falls back to the class name and memory address.

**Q2. Why does `print(obj)` show `<Class object at 0x...>` by default?**

> Because Python doesn't know which fields matter for your class. It falls back to the only universally-true description: the type and the address.

**Q3. What's the difference between `__str__` and `__repr__`?**

> `__str__` is for end users — readable. `__repr__` is for developers — unambiguous, ideally something you could paste back into code. `print()` uses `__str__`; the interactive prompt and containers use `__repr__`. If you only write one, write `__repr__`, because `__str__` falls back to it but not the other way round.

**Q4. Why does a good `__str__` matter in production?**

> Logs. When something fails at 3am, `<Driver object at 0x7f8b>` tells you nothing, while `Driver(id=4021, online=False)` can hand you the bug immediately. It's the difference between a debuggable system and an opaque one.

---

## 11. ⚠️ Common Mistakes

| Mistake | Result |
|:--|:--|
| `print(...)` inside `__str__` instead of `return` | Prints, then prints `None` |
| Returning a non-string | `TypeError` |
| Forgetting `__str__` entirely | Useless logs when you need them most |
| Dumping all 20 fields into it | Unreadable. Pick the identifying ones. |
| Putting secrets in it (passwords, tokens, card numbers) | **They end up in your log files.** Serious security bug. |

---

## 12. Summary

`print(d1)` gave you a memory address, which is true and useless.

Python can't know how *you* want your object described — so it asks the object, through `__str__`, and you supply the answer.

Write it and your logs become readable. Skip it and one day, at 2am, you'll wish you hadn't.

---

## ✓ Key Takeaways

- **`__str__`** defines your object's human-readable text form.
- **`print()`, `str()` and f-strings** call it automatically — you never call it yourself.
- It must **`return`** a string, not print one.
- Without it: `<module.Class object at 0x...>`.
- It's a **dunder method**, like `__init__` — a hook into built-in behaviour.
- Java's equivalent is **`toString()`**.
- **Never put secrets in `__str__`** — they'll leak into logs.

---

## ✓ Practice Questions

1. What's wrong here, and what's the output?
   ```python
   def __str__(self):
       print(f"Driver {self.name}")
   ```

2. Write `__str__` for a `BankAccount` that shows account number and balance — but **masks** all but the last four digits of the account number.

3. Why does `print([d1, d2])` not use your `__str__`? Search for the answer, and explain in one sentence.

4. Write a `__str__` for a Swiggy `Order` that would genuinely help you debug a failed delivery. Justify each field you include — and each one you leave out.

---

## ✓ Mini Assignment

Add `__str__` to **every** class you've written in this chapter — `Driver`, `Student`, `BankAccount`, `User`.

For each one, write a comment above the method answering: *"If I saw this line in a log at 3am, what would I need it to tell me?"*

Then deliberately write a bad one (all 15 fields) and a good one (3 fields) for the same class, print both, and write two sentences on the difference.

---

## ✓ Real-World Exercise

Find any error message from an app you use — a failed payment, a broken upload, a rejected form.

1. What information does it give you?
2. What information would have *actually* helped?
3. Rewrite it.

You have now done the exact exercise that separates engineers whose logs save the night from engineers whose logs waste it.

---
---

# TOPIC 11
# Encapsulation — Pillar 1

---

## 1. The Problem

Your `Driver` class is finished. It has data, behaviour, a constructor, a counter, a nice `__str__`.

Now let me, a careless developer on your team, write one line in a completely different file:

```python
# some_other_file.py

d1.rating = -50
```

> 🛑 **STOP AND THINK**
> A rating of minus fifty.
> Does Python stop me? Does it warn me? Does anything at all happen?

**Nothing happens.** It runs perfectly. No error, no warning.

Let me do it a few more times:

```python
d1.rating = 999            # a rating of nine hundred and ninety-nine
d1.rating = "excellent"    # a rating that is a word
d1.driver_id = -1          # a negative ID
d1.driver_id = None        # no ID at all
```

All fine. All accepted. Your object is now nonsense.

---

## 2. Observation — Follow the Damage

Let's trace what a rating of `-50` actually does to the system.

Remember Topic 3? Dispatch sorts candidate drivers before offering the trip. Suppose it sorts by rating, best first.

```
   Normal:                       With one poisoned driver:

   Meera    4.9                  Priya    4.6
   Ashok    4.8                  Ravi     4.7
   Ravi     4.7                  Ashok    4.8
   Priya    4.6                  Meera    4.9
                                 Ashok    -50    ← always last. Never gets a trip.
```

Ashok stops receiving work. He doesn't know why. He calls support. Support escalates. An engineer is assigned.

That engineer opens the **dispatch service** and starts reading the sorting code.

> 🛑 **STOP AND THINK**
> Will they find the bug in the dispatch code?

**No. The dispatch code is perfect.** It sorted exactly what it was given.

The bug is a single line in a completely different file, written three weeks ago by someone who has since moved teams.

> 💡 That's the real cost. Not the wrong value — the **distance between the cause and the symptom.**

---

## 3. Think

Two questions.

**Question 1:** Who knows that a driver's rating must be between 0 and 5?

...

The **`Driver` class** knows. It's the class's own rule. It's part of what it *means* to be a driver.

**Question 2:** Who is currently enforcing that rule?

...

**Nobody.**

The class knows the rule but has no power to apply it. Every one of the thousand files that touches a driver is free to write whatever it likes.

> 🛑 **STOP AND THINK**
> Two possible strategies:
>
> **(a)** Ask all thousand files to be careful.
> **(b)** Let the `Driver` class refuse bad values.
>
> Which one actually scales?

Strategy (a) requires a thousand developers to never make a mistake, forever. That is not an engineering strategy — it's a wish.

---

## 4. First Principle

> 💡 **KEY IDEA**
> **A class knows its own rules. So the class — and only the class — should be responsible for enforcing them.**
> **Don't ask the outside world to be careful. Make it impossible to be careless.**

To do that, you need two things:

1. **Bundle** the data together with the methods that manage it. *(You've been doing this since Topic 4.)*
2. **Restrict** direct access from outside, so all changes go through your methods.

That combination has a name.

---

## 5. Solution — Encapsulation

> 📖 **Definition**
> **Encapsulation is bundling data and the methods that operate on that data into a single unit, while restricting direct access to that data from outside.**

Both halves matter:

| Half | What it means | Have we done it? |
|:--|:--|:--|
| **Bundling** | Data and behaviour live in one class | ✅ Since Topic 4 |
| **Restricting** | Outside code can't reach in and corrupt the data | ❌ Not yet — this is today |

### Where the word comes from

A **medicine capsule**.

```
        ┌───────────────────────┐
        │  ▓▓▓▓ powder ▓▓▓▓     │   ← the data
        └───────────────────────┘
              the shell             ← the protection
```

The powder is sealed inside a shell. You can't reach in and take out half the dose, or add something else, or swap it. You take the capsule as designed.

*Encapsulate*: literally, to enclose in a capsule.

---

## 6. The Analogy That Explains Everything — The ATM

You want ₹2,000 from your bank account.

> 🛑 **STOP AND THINK**
> Is there a slot on the ATM that lets you reach into the vault and take what you want?

Obviously not. The ATM gives you exactly four operations:

```
        ┌───────────────────────────┐
        │        A T M              │
        │                           │
        │   [ Withdraw   ]          │   ← the only ways in
        │   [ Deposit    ]          │
        │   [ Balance    ]          │
        │   [ Statement  ]          │
        │                           │
        └───────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │  balance = 5000           │   ← you can NEVER touch this directly
        └───────────────────────────┘
```

And every one of those operations is **checked**. Ask for ₹5,000 with ₹200 in the account and the machine says no.

Compare that to your `Driver` class right now:

```python
d1.rating = -50           # the equivalent of reaching into the vault
```

**Your class is a bank with no walls.**

---

## 7. How Python Does It

Now here's where Python surprises people, and it's worth understanding rather than just accepting.

> **Python has no `private` keyword.**

There is no compiler standing guard. Instead, there is a **naming convention** that every Python developer on Earth understands:

| Written as | Means |
|:--|:--|
| `self.name` | **Public.** Part of the API. Use it freely. |
| `self._rating` | **Internal.** "Please don't touch this — it may change without warning." |
| `self.__secret` | **Name-mangled** to `_Driver__secret`. Mostly for avoiding clashes in inheritance. |

```python
class Driver:
    def __init__(self, driver_id, name, rating):
        self.name = name              # public
        self._rating = rating         # internal, by convention
```

### ⚠️ And now the honest part

```python
d1._rating = -50        # runs perfectly. Nothing stops you.
```

The underscore **enforces nothing**. It's a sign, not a lock.

> 🛑 **STOP AND THINK**
> A rule that isn't enforced. Is that useless?

Think about a **"Staff Only"** door in a shop.

It isn't locked. You could walk through it right now. Nothing physically prevents you.

But you don't — because the sign tells you clearly that you're not meant to, and if you do, that's on you.

> 💡 Python's philosophy is often summarised as **"we are all consenting adults here."**
>
> Access control is a *documented agreement between developers*, not a locked door.
>
> In Java, the compiler stops you. In Python, **your teammate stops you at code review.**

> 🔁 **JAVA CORNER**
> Java has real enforcement:
> ```java
> private double rating;
> ```
> `d1.rating = -50;` is a **compile error**. The program won't even build.
>
> **Trade-off:** Java gives you a guarantee. Python gives you flexibility — you can reach in during debugging, testing, or an emergency patch, without fighting the language. Neither is "better." They're different philosophies about who to trust.

---

## 8. The Controlled Path In

The naming convention says *"don't."* Now we give people something to use *instead*.

```python
# uber/driver.py

class Driver:
    """A driver in the Uber system."""

    MIN_RATING = 0.0
    MAX_RATING = 5.0

    def __init__(self, driver_id, name, rating=5.0):
        self.driver_id = driver_id
        self.name = name
        self._rating = None            # declared, then set through the setter
        self.set_rating(rating)        # ← validated even at creation!
        self.is_online = False

    def get_rating(self):
        """Controlled READ."""
        return self._rating

    def set_rating(self, value):
        """Controlled WRITE — with validation."""
        if not isinstance(value, (int, float)):
            raise TypeError("Rating must be a number")
        if not Driver.MIN_RATING <= value <= Driver.MAX_RATING:
            raise ValueError(
                f"Rating must be between {Driver.MIN_RATING} "
                f"and {Driver.MAX_RATING}, got {value}"
            )
        self._rating = value

    def __str__(self):
        return f"Driver #{self.driver_id} {self.name} (⭐{self._rating})"
```

```python
# uber/client.py

from uber.driver import Driver


def main():
    d1 = Driver(4021, "Ashok", 4.8)
    print(d1)
    print("rating:", d1.get_rating())

    print("\n--- valid update ---")
    d1.set_rating(4.5)
    print("rating:", d1.get_rating())

    print("\n--- invalid updates are now REFUSED ---")
    for bad_value in (-50, 999, "excellent"):
        try:
            d1.set_rating(bad_value)
        except (ValueError, TypeError) as e:
            print(f"  rejected {bad_value!r:12} → {type(e).__name__}: {e}")

    print("\n--- rating survived every attack ---")
    print("rating:", d1.get_rating())


if __name__ == "__main__":
    main()
```

### Output

```
Driver #4021 Ashok (⭐4.8)
rating: 4.8

--- valid update ---
rating: 4.5

--- invalid updates are now REFUSED ---
  rejected -50          → ValueError: Rating must be between 0.0 and 5.0, got -50
  rejected 999          → ValueError: Rating must be between 0.0 and 5.0, got 999
  rejected 'excellent'  → TypeError: Rating must be a number
```

---

## 9. What Just Happened?

**Three attacks. Three refusals.** The rating was 4.5 before and 4.5 after.

**Notice `__init__` calls `set_rating` too.** That's deliberate — it means you can't even *create* a driver with a bad rating. Validation at birth, not just afterwards.

**Notice where the error appeared.** Right at the line that caused it, naming the bad value.

Compare with Section 1: the bug appearing three weeks later in the dispatch service. **We moved the error from "somewhere else, much later" to "right here, right now."**

> 💡 That is what encapsulation buys you.

### The second payoff — read-only data

> 🛑 **STOP AND THINK**
> There's a `set_rating`. Where's `set_driver_id`?

There isn't one. **On purpose.**

A driver's ID should never change after creation. By providing a getter and *no* setter, you've made it **read-only** — something you cannot express at all with a plain public attribute.

### The third payoff — you can change your mind later

Right now the rating is a number stored on the object.

Suppose next year you want to compute it live from the driver's last 100 trips. Or cache it. Or fetch it from a separate ratings service.

> 🛑 **STOP AND THINK**
> If a thousand files call `d1.get_rating()`, how many have to change?

**Zero.** You rewrite the inside of `get_rating()` and every caller carries on as normal.

Now go back and read Topic 3 again. This is **exactly** the routing-engine story: *the interface stayed the same, so the implementation could be replaced.*

> 💡 **KEY IDEA**
> **Encapsulation is how you build the wall. Abstraction is what the wall gives you.**
>
> This is why abstraction is the *principle* and encapsulation is a *pillar*. You just watched one produce the other.

---

## 10. ⚠️ Important — Don't Write Java in Python

I have to warn you about something, because you're learning both languages.

The code above uses `get_rating()` and `set_rating()`. That's the **Java** style, and it's correct for Java.

In Python, writing `get_x` / `set_x` for every attribute is considered **poor style**. You'd be pulled up in a code review.

> 🛑 **STOP AND THINK**
> Which of these reads better?
> ```python
> d1.set_rating(d1.get_rating() + 0.1)
> d1.rating = d1.rating + 0.1
> ```

Python's answer is a feature called **`@property`**, which lets you keep the clean second syntax *while still running your validation behind it*:

```python
class Driver:
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not 0 <= value <= 5:
            raise ValueError("Rating must be 0-5")
        self._rating = value
```

```python
d1.rating = 4.5      # looks like a plain attribute — but runs the validation
d1.rating = -50      # ValueError!
```

> 💡 **The Pythonic rule:** start with a **plain public attribute**. Add `@property` only when you actually need validation.
>
> Because the syntax at the call site is *identical*, you can add protection later without changing a single line of calling code. Which means adding getters "just in case" gains you nothing — it's pure noise.
>
> **That's a genuine philosophical difference from Java**, and it comes directly from the fact that Python can change an attribute into a property without breaking callers. Java can't.

*(We cover `@property` fully in Chapter 2. For now, understand the concept and know the Pythonic direction of travel.)*

---

## 11. Real-World Analogies

### Instagram's private account

Your posts exist. They're real data on a server.

A stranger can't see them — not because the data is hidden, but because Instagram's code sits between them and the data, checking whether they're an approved follower.

**Same data. Controlled access.**

### Your salary in the company HR system

The number exists in a database.

- **You** can read it.
- **Your manager** can read it.
- **A colleague** cannot.
- **You** cannot write it.
- **HR** can write it — after approval.

Nobody edits the database directly. Every path goes through code that checks who's asking.

> 🛑 **STOP AND THINK**
> What would happen if any employee could run `UPDATE salary SET amount = 9999999 WHERE name = 'me'`?
>
> That's your `Driver` class without encapsulation.

---

## 12. 🎯 Interview Questions

**Q1. What is encapsulation?**

> Bundling data with the methods that operate on it, while restricting direct external access. It makes the class responsible for keeping its own state valid.

**Q2. Difference between encapsulation and abstraction?**

> Encapsulation is a **mechanism** — restrict access, expose controlled methods. Abstraction is the **outcome** — the user works with a simple idea instead of the complex reality.
>
> One-liner: *encapsulation is how you hide it; abstraction is what they see instead.*

**Q3. Python has no `private`. Is its encapsulation weaker?**

> In *enforcement*, yes — the underscore is a convention, not a lock. In *practice*, much less than you'd expect, because the convention is universal and tooling flags violations. It's a deliberate trade-off: Python favours flexibility and trusts developers; Java favours guarantees enforced by the compiler.

**Q4. What does a leading underscore mean?**

> `_name` signals "internal — not part of the public API, may change without notice." `__name` triggers name mangling to `_ClassName__name`, mainly to avoid accidental clashes in subclasses. Neither is true privacy.

**Q5. Why is encapsulation valuable beyond validation?**

> Two more reasons. It lets you make data **read-only** (getter, no setter). And it **decouples callers from storage** — you can change how a value is computed or stored without breaking any caller, which is what makes large systems maintainable.

---

## 13. ⚠️ Common Mistakes

| Mistake | Why it's wrong |
|:--|:--|
| Thinking `_name` is enforced | It's a sign, not a lock |
| Writing `get_x`/`set_x` for **every** attribute in Python | Un-Pythonic noise. Public attribute first, `@property` when needed. |
| Adding a setter that does no validation | You've added ceremony and gained nothing |
| Encapsulating everything on day one | Hide what needs protecting, not what exists |
| Validating in the setter but bypassing it in `__init__` | Then bad objects can still be born. Call the setter from `__init__`. |
| Confusing encapsulation with abstraction | Mechanism vs outcome |

---

## 14. Summary

One careless line in a distant file put `-50` into a rating, and the symptom showed up three weeks later in a different service entirely.

The `Driver` class knew the rule but had no power to enforce it. So we gave it power: mark the data internal, and make every change go through a method that checks.

Python does this by **convention** (`_name`) rather than by compiler. That's a real trade-off — flexibility over guarantees — and now you know which side each language chose, and why.

And in doing it, you built a wall. **That wall is exactly what makes abstraction possible** — which closes the loop we opened in Topic 2.

---

## ✓ Key Takeaways

- **Encapsulation** = bundle data with its methods + restrict outside access.
- The class knows its rules, so **the class should enforce them**.
- Python has **no `private`** — it uses `_name` as a convention.
- The underscore is a **sign, not a lock**. "We are all consenting adults here."
- Three payoffs: **validation**, **read-only data**, and **freedom to change the implementation**.
- ⚠️ Don't write `get_x`/`set_x` everywhere in Python — use public attributes, then `@property`.
- **Encapsulation is the mechanism. Abstraction is the outcome.**

---

## ✓ Practice Questions

1. Take the `BankAccount` from Topic 5's assignment. Add validation so the balance can never go negative. Then demonstrate that `acc._balance = -9999` still gets through — and explain why that's acceptable in Python.
2. Which attributes of a Netflix `User` should be read-only? Justify each.
3. Explain to a Java programmer why Python doesn't have `private`. Give the strongest argument *for* Python's choice, then the strongest argument *against*.
4. Why should `__init__` call the setter rather than assigning `self._rating` directly?

---

## ✓ Mini Assignment

Build `hospital/patient.py` with a `Patient` class:

- **Read-only:** `patient_id`, `blood_group` (getters only — these must never change)
- **Validated:** `age` (0–130), `weight_kg` (must be positive)
- **Public:** `name`, `phone`
- A `__str__` that would be useful in a hospital log

Then write a client that tries **five** invalid operations and catches every error.

Finish with a short paragraph: *which attributes did you leave public, and why was that the right call?*

---

## ✓ Real-World Exercise

Think about your **college's internal portal**.

Make three lists:

1. Data you can **read but not write** (attendance, marks, fee status)
2. Data you can **read and write** (phone number, address, photo)
3. Data you can **neither read nor write** (other students' marks, staff salaries)

Now: for each item in list 1, who *can* write it, and what check happens first?

**You've just described the encapsulation design of a real system.** Every one of those rules is a method somewhere with an `if` statement in it.

---
---

# 🏁 The Complete Day-1 Project

Everything from this chapter, in one working project.

## Structure

```
uber_project/
└── uber/
    ├── __init__.py
    ├── driver.py
    └── client.py
```

## `uber/__init__.py`

```python
# Empty file. Its presence makes `uber` a regular package.
```

## `uber/driver.py`

```python
# uber/driver.py
"""Defines the Driver entity for the Uber dispatch system."""


class Driver:
    """A driver in the Uber system."""

    # ---------- CLASS BODY: runs ONCE, at import time ----------
    # (This is Java's static block, for free.)
    total_drivers = 0
    MIN_RATING = 0.0
    MAX_RATING = 5.0
    print("driver.py loaded — Driver class defined")

    # ---------- CONSTRUCTOR ----------
    def __init__(self, driver_id, name, rating=5.0, is_online=False):
        self.driver_id = driver_id            # instance attributes
        self.name = name
        self._rating = None                   # internal, by convention
        self.set_rating(rating)               # validated at birth
        self.is_online = is_online
        self.rides = []                       # mutable → per object

        Driver.total_drivers += 1             # class name, NOT self

    # ---------- ENCAPSULATED ACCESS ----------
    def get_rating(self):
        return self._rating

    def set_rating(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Rating must be a number")
        if not Driver.MIN_RATING <= value <= Driver.MAX_RATING:
            raise ValueError(
                f"Rating must be between {Driver.MIN_RATING} "
                f"and {Driver.MAX_RATING}, got {value}"
            )
        self._rating = value

    # ---------- BEHAVIOUR ----------
    def go_online(self):
        self.is_online = True
        print(f"  {self.name} is now ONLINE")

    def go_offline(self):
        self.is_online = False
        print(f"  {self.name} is now OFFLINE")

    def accept_ride(self, ride_id):
        if not self.is_online:
            print(f"  {self.name} is offline — cannot accept {ride_id}")
            return
        self.rides.append(ride_id)
        print(f"  {self.name} accepted ride {ride_id}")

    # ---------- STATIC METHOD: no object needed ----------
    @staticmethod
    def register():
        print("  Registration is open for new drivers")

    # ---------- PRINTABLE FORM ----------
    def __str__(self):
        status = "online" if self.is_online else "offline"
        return (f"Driver #{self.driver_id} {self.name} "
                f"(rating {self._rating}, {status}, {len(self.rides)} rides)")
```

## `uber/client.py`

```python
# uber/client.py
"""Creates Driver objects and demonstrates every Day-1 concept."""

from uber.driver import Driver


# ---------- argument passing (Topic 9) ----------
def add_thirty(x):
    x = x + 30                        # rebinding → invisible to caller


def change_name(driver):
    driver.name = "Xyz"               # mutation → visible to caller


def replace_driver(driver):
    driver = Driver(9999, "Ghost")    # rebinding → invisible to caller
    driver.name = "Zzz"


def main():
    print("\n=== TOPIC 8: static method, before any driver exists ===")
    Driver.register()
    print("  total_drivers =", Driver.total_drivers)

    print("\n=== TOPIC 4 & 7: creating objects ===")
    d1 = Driver(4021, "Ashok", 4.8)
    d2 = Driver(4088, "Meera", 4.9)
    d3 = Driver(4103, "Ravi")             # rating uses the default
    print("  total_drivers =", Driver.total_drivers)

    print("\n=== TOPIC 10: __str__ ===")
    print(" ", d1)
    print(" ", d2)
    print(" ", d3)

    print("\n=== TOPIC 5: state changes over time ===")
    print("  before:", d1.is_online)
    d1.go_online()
    print("  after: ", d1.is_online)

    print("\n=== TOPIC 7: self — one method, different objects ===")
    d1.accept_ride("R-101")
    d2.accept_ride("R-102")               # d2 is offline — refused

    print("\n=== TOPIC 6: two labels, one object ===")
    d4 = d1
    d4.name = "CHANGED"
    print("  d1.name =", d1.name)
    print("  d1 is d4 →", d1 is d4)

    print("\n=== TOPIC 9: mutation vs rebinding ===")
    number = 10
    add_thirty(number)
    print("  number after add_thirty  =", number, "(unchanged — rebinding)")

    change_name(d2)
    print("  d2.name after change_name =", d2.name, "(changed — mutation)")

    replace_driver(d2)
    print("  d2.name after replace     =", d2.name, "(unchanged — rebinding)")

    print("\n=== TOPIC 11: encapsulation blocks bad data ===")
    for bad in (-50, 999, "excellent"):
        try:
            d1.set_rating(bad)
        except (ValueError, TypeError) as e:
            print(f"  rejected {bad!r:12} → {type(e).__name__}")
    print("  d1 rating is still", d1.get_rating())

    print("\n=== TOPIC 8: THE TRAP ===")
    d1.total_drivers = 999
    print("  d1.total_drivers     =", d1.total_drivers, "← instance copy!")
    print("  Driver.total_drivers =", Driver.total_drivers, "← unaffected")
    print("  d1.__dict__ keys     =", list(d1.__dict__.keys()))


if __name__ == "__main__":
    main()
```

## Run it

```bash
cd uber_project
python3 -m uber.client
```

## 🔍 One last puzzle before you go

Run it, and look carefully at the final `Driver.total_drivers`.

We created **three** drivers — Ashok, Meera and Ravi. But the counter says **4**.

> 🛑 **STOP AND THINK**
> Where did the fourth driver come from?

Scroll back up to `replace_driver`:

```python
def replace_driver(driver):
    driver = Driver(9999, "Ghost")     # ← a real object WAS created
    driver.name = "Zzz"
```

That function created a genuine `Driver`. `__init__` ran. `Driver.total_drivers` went up.

Then the function ended, the local name vanished, and the object became unreachable — **garbage collected**, exactly as described in Topic 6.

> 💡 The Ghost driver existed, was counted, and disappeared. Nobody kept a label on it.
>
> **The object died. Its effect on the class attribute didn't.**

That single line ties together Topic 6 (garbage collection), Topic 8 (class attributes) and Topic 9 (rebinding). If you spotted it before I pointed it out — you've genuinely understood this chapter.

---

# 📋 Chapter Summary

We started with *"build Uber"* and no idea what to type on line 1.

| Topic | The question it answered |
|:--|:--|
| 1. Entities | What are we even modelling? → **Find the things.** |
| 2. Pillars & Principle | 3 mechanisms, 1 outcome. |
| 3. Abstraction | How does a hexagonal planet-grid become one button? |
| 4. Class & Object | How do I describe a thing? → **Blueprint and building.** |
| 5. Members & State | An object has a *history*, not just values. |
| 6. References | `=` moves a label. It never copies. |
| 7. Constructor & `self` | Objects should be **born valid**. `self` is *which* object. |
| 8. Class attributes | Whose fact is it — the object's, or the class's? |
| 9. Argument passing | Mutation is visible. Rebinding isn't. |
| 10. `__str__` | Your object's name tag, written by you. |
| 11. Encapsulation | The class enforces its own rules. |

## The three sentences worth carrying forward

> 1. **A class is a blueprint. An object is memory that has actually been allocated.**
> 2. **A Python variable is a label stuck on an object — `=` never copies.**
> 3. **Encapsulation is how you build the wall; abstraction is what the wall gives you.**

## The three traps that will bite you

| Trap | Fix |
|:--|:--|
| `name = x` without `self.` | Always `self.name = x` |
| `self.counter += 1` for a class attribute | `ClassName.counter += 1` |
| Mutable default or class attribute (`= []`) | Build it inside `__init__` |

When something behaves strangely, print `obj.__dict__`. It has caught every one of these.

---

# 📅 What's Next

**Chapter 2 — Encapsulation in Depth**
`@property`, read-only attributes, computed attributes, and why "a getter and setter for every field" is not actually encapsulation.

**Chapter 3 — Inheritance (Pillar 2)**
`PremiumDriver` is-a `Driver`. `super()`, method overriding, and when *not* to use inheritance.

**Chapter 4 — Polymorphism (Pillar 3)**
One `pay()` call, five payment types, and duck typing — the most Pythonic idea you'll meet.

And when you finish those three, go back and re-read **Topic 3**. Abstraction will read completely differently once you own all three pillars.

---

# ✅ Final Chapter Challenge

Build a complete **Swiggy** mini-system in a package called `swiggy/`:

| Class | Must demonstrate |
|:--|:--|
| `Customer` | constructor with defaults, `__str__` |
| `Restaurant` | class attribute (`platform_commission`), static method |
| `Order` | state machine (`PLACED → COOKING → PICKED_UP → DELIVERED`) |
| `DeliveryPartner` | encapsulated `_rating` with validation |

Requirements:

1. Every class in its **own module** inside the package
2. A `client.py` that runs the whole flow: customer places an order, restaurant accepts, partner delivers
3. At least one **class attribute** and one **static method**
4. `__str__` on all four classes, useful enough to debug from
5. One deliberate demonstration of **mutation vs rebinding**
6. One validation that **refuses** bad data, with the error caught and printed

Then write a short `NOTES.md` answering:

- Which attributes did you encapsulate, and which did you leave public? Why?
- Where did you use a class attribute instead of an instance attribute? Why?
- Which topic from this chapter was hardest, and what finally made it click?

That last question is the most valuable one. **Answer it honestly** — the thing that finally made it click for you is exactly what you'll use to explain it to someone else, and teaching it is how you'll know you've truly got it.

---

*End of Chapter 1.*
