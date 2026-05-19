# Applied AI Engineer — Phase 1 Day-Wise Plan (12 Weeks)

## Structure
- **6 days/week** (Sunday = rest)
- **Mon–Thu:** Tech sessions (4 days)
- **Fri–Sat:** DSA Placement sessions (2 days)
- **Each session:** 90 min Learn + 90 min Practice = 3 hours/day
- **Weekly total:** 18 hours

## Phase 1 Module Map
| Weeks | Module |
|---|---|
| 1–2 | Python OOP + Async |
| 3 | SQL + Networking Basics |
| 4 | Mini Project (Async API Client) |
| 5–6 | FastAPI |
| 7 | React + Tailwind |
| 8 | Full-Stack Project (Deployed) |
| 9 | LLD (Low Level Design) |
| 10 | HLD (High Level Design) |
| 11 | ML Conceptual (Light) |
| 12 | Prompt Engineering + AI Mini Project |

---

## Week 1 — Python OOP Foundation

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| Mon | OOP Basics | Classes, instances, `__init__`, instance vs class vs static methods | Build `BankAccount` class with deposit, withdraw, balance |
| Tue | Inheritance | Single & multiple inheritance, `super()`, MRO, polymorphism | Build `Vehicle → Car / Bike` hierarchy with method overriding |
| Wed | Abstraction & Encapsulation | `abc` module, abstract methods, properties, private attributes | Convert Vehicle to abstract; add `@property` for read-only fields |
| Thu | Composition + Dunder Methods | Composition over inheritance, `__str__`, `__eq__`, `__len__`, `__add__` | Build `Library` class composed of `Book` objects with dunder methods |
| Fri | DSA: Arrays | Prefix sums, basic array manipulation patterns | 4 array problems (3 easy + 1 medium) |
| Sat | DSA: Two Pointers | Two pointer pattern in sorted arrays | 4 two-pointer problems |

---

## Week 2 — Python Advanced (Decorators, Generators, Async)

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| Mon | Decorators | Function decorators, decorators with args, `functools.wraps` | Write `@timer`, `@retry`, `@cache` decorators |
| Tue | Generators & Iterators | Generator functions, `yield`, iterators, generator expressions | Build a file line-reader generator + Fibonacci generator |
| Wed | Context Managers + Type Hints | `with` statement, `__enter__`/`__exit__`, custom context managers, type hints | Write a `Timer` context manager + add type hints to all Week 1 code |
| Thu | Async/Await | Event loop, coroutines, `async/await`, `asyncio.gather` | Build async function calling 3 APIs concurrently |
| Fri | DSA: Strings | Common string patterns, anagrams, palindromes | 4 string problems |
| Sat | DSA: Sliding Window | Fixed and variable window techniques | 4 sliding window problems |

---

## Week 3 — SQL + Networking

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| Mon | SQL Basics | SELECT, WHERE, ORDER BY, LIMIT, INSERT/UPDATE/DELETE | 15 queries on a sample dataset (employees / orders) |
| Tue | SQL Joins & Aggregations | INNER/LEFT/RIGHT JOIN, GROUP BY, HAVING, aggregate functions | 10 multi-table queries |
| Wed | SQL Indexes + Transactions | Indexes (why & when), ACID, basic transactions | Add indexes to your sample DB; measure speed difference |
| Thu | Networking Concepts | HTTP methods, status codes, REST principles, WebSockets vs HTTP, TLS basics | Use Postman: hit 5 public APIs (GET/POST/PUT/DELETE); document responses |
| Fri | DSA: Hash Maps | When to use hash maps, frequency counters | 4 hash map problems |
| Sat | DSA: Hash Map Patterns | Two-sum variations, anagram grouping | 4 problems |

---

## Week 4 — Mini Project: Async API Client

> **Goal:** Lock in Python OOP + Async + SQL in one project. Build something that hits 3+ APIs concurrently and stores results in SQLite.

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| Mon | Project setup | Project structure, `uv`/`poetry`, `aiohttp`/`httpx` basics | Set up repo, install deps, scaffold OOP structure |
| Tue | Build async fetcher | Concurrent API calls with asyncio.gather, error handling | Implement async client class with 3 API integrations |
| Wed | DB integration | SQLAlchemy basics (sync first), schema design | Add models + save fetched data to SQLite |
| Thu | Polish & ship | Logging, README writing, git workflow | Push to GitHub with clean README + screenshots. **Portfolio piece #1** |
| Fri | DSA: Linked Lists | Singly linked list operations, traversal | 4 LL problems (reverse, middle, merge) |
| Sat | DSA: LL Patterns | Fast/slow pointer (Floyd's), cycle detection | 4 problems |

---

## Week 5 — FastAPI Part 1

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| Mon | FastAPI Intro | Setup, routing, Pydantic models, automatic docs | Build basic CRUD API with in-memory store (5 endpoints) |
| Tue | Request Handling | Path params, query params, request body, response models | Add validation + custom response models to your API |
| Wed | SQLAlchemy Async | Async engine, sessions, models, `select()` | Set up Postgres locally (Docker), define models, write first async query |
| Thu | CRUD with DB | Connect API to DB, async CRUD endpoints | Full CRUD endpoints backed by Postgres |
| Fri | DSA: Stacks | Stack patterns, parentheses problems | 4 stack problems |
| Sat | DSA: Monotonic Stack | Next greater element pattern | 4 problems |

---

## Week 6 — FastAPI Part 2

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| Mon | Authentication | JWT basics, password hashing, OAuth2 password flow | Add login/register endpoints with JWT |
| Tue | Dependency Injection | FastAPI's DI system, `Depends`, current-user dependency | Protect routes with auth dependency; add user-scoped resources |
| Wed | Middleware + Error Handling | Middleware (CORS, logging), exception handlers, validation errors | Add CORS middleware + custom exception handler |
| Thu | Docker for FastAPI | Dockerfile, docker-compose with Postgres, env vars | Dockerize your full API + Postgres with docker-compose |
| Fri | DSA: Recursion | Recursion fundamentals, base/recursive cases | 4 recursion problems |
| Sat | DSA: Backtracking | Backtracking template, permutations, subsets | 4 backtracking problems |

---

## Week 7 — React + Tailwind

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| Mon | React Fundamentals | JSX, components, props, conditional rendering | Build a static landing page with 3–4 components |
| Tue | State + Effects | `useState`, `useEffect`, event handlers, controlled inputs | Build a counter + a fetch-from-API component |
| Wed | Routing + Context | React Router, `useContext`, custom hooks | Build a 3-page app with shared state via context |
| Thu | Forms + Tailwind | Forms with validation, axios for API calls, Tailwind utility classes | Build a styled login + signup form that posts to your FastAPI |
| Fri | DSA: Binary Trees | Tree representation, recursion on trees | 4 binary tree problems |
| Sat | DSA: Tree Traversals | BFS (level-order), DFS (pre/in/post-order) | 4 traversal problems |

---

## Week 8 — Full-Stack Project

> **Goal:** Wire React + FastAPI from Weeks 5–7 into a real deployed app. Pick: URL shortener, notes app, or expense tracker.

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| Mon | Plan + scaffold | API contract design, folder structure | Create both repos; define endpoints; build initial UI shells |
| Tue | Wire auth end-to-end | Token storage, protected routes (frontend), refresh patterns | Login + signup flow working end-to-end |
| Wed | Core features + polish | CRUD on frontend, error handling, loading states | Implement core CRUD on UI + backend |
| Thu | Deploy + document | Render.com (backend), Vercel (frontend), env vars, custom domain | Deploy live, write README with architecture, record 1-min demo. **Portfolio piece #2** |
| Fri | DSA: BSTs | BST properties, search/insert/delete | 4 BST problems |
| Sat | DSA: BST Patterns | Validate BST, kth smallest, LCA | 4 problems |

---

## Week 9 — LLD (Low Level Design)

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| Mon | SOLID Principles | All 5 principles with Python examples | Refactor your Week 4 project to follow SOLID; document changes |
| Tue | Strategy + Factory | Strategy pattern, simple factory, factory method | Implement Strategy for payment methods + Factory for vehicles |
| Wed | Observer + Singleton + Builder | When to use each, Python implementations | Implement event-based notification system using Observer |
| Thu | LLD Problem Solving | Approach: requirements → classes → interactions → code | Solve Parking Lot (or Splitwise) in Python with class diagrams |
| Fri | DSA: Heaps | Min/max heap, `heapq` module | 4 heap problems |
| Sat | DSA: Priority Queue | Top-K patterns, merge-K-sorted | 4 problems |

---

## Week 10 — HLD (High Level Design)

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| Mon | Scalability Basics | Vertical vs horizontal, load balancers, CAP theorem | Sketch architecture for "design Instagram feed" on paper |
| Tue | Caching + CDN | Redis basics, cache strategies (write-through, cache-aside), CDN | Add Redis caching to one endpoint in your Week 8 project |
| Wed | Queues + Sharding | Message queues (Kafka/RabbitMQ conceptual), sharding, replication, read replicas | Sketch architecture for "design a notification system" |
| Thu | System Design Case Study | Walkthrough: design URL shortener (you built it!) | Solve: design a rate limiter, with class + sequence diagrams |
| Fri | DSA: Graphs Part 1 | Adjacency list/matrix, BFS | 4 graph problems |
| Sat | DSA: Graphs Part 2 | DFS, connected components | 4 problems |

---

## Week 11 — ML Conceptual (Light, Goal: Build Intuition)

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| Mon | What is ML? | ML vs traditional programming, supervised/unsupervised, train/val/test split | Watch Andrew Ng ML Week 1; take notes |
| Tue | Regression + Classification | Linear regression, logistic regression, cost functions intuition | Train a linear regression model on a toy dataset with scikit-learn |
| Wed | Trees + Ensembles | Decision trees, random forests, XGBoost overview | Train a Random Forest classifier on Titanic dataset |
| Thu | Neural Net Intuition + Embeddings | What's a neural net, backprop intuition, what are embeddings | Read about word embeddings; play with sentence-transformers in Colab |
| Fri | DSA: DP Part 1 | DP intuition, memoization, tabulation, Fibonacci pattern | 4 DP problems (climbing stairs, house robber, etc.) |
| Sat | DSA: DP Part 2 | 1D DP continued (decode ways, word break) | 4 problems |

---

## Week 12 — Prompt Engineering + AI Mini Project

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| Mon | LLM API Basics | System/user/assistant messages, temperature, max tokens, API calling (Claude/OpenAI) | Make 10 API calls to an LLM; experiment with temperature and system prompts |
| Tue | Prompt Patterns | Few-shot, chain-of-thought, structured output (JSON mode) | Build prompts that return strictly typed JSON for 3 use cases |
| Wed | Prompt Chaining + Context Mgmt | Multi-step prompts, context window limits, token counting | Build a 3-step prompt chain (extract → classify → summarize) |
| Thu | Build: AI Resume Reviewer | Apply everything: FastAPI backend + LLM call + simple React UI | Ship a deployed AI resume reviewer. **Portfolio piece #3** |
| Fri | DSA: DP Part 3 (2D) | 2D DP patterns (grid problems, LCS) | 4 problems |
| Sat | DSA: Binary Search | Binary search variants, search on answer | 4 binary search problems |

---

## End of Phase 1 — What You'll Have

**Skills:**
- Strong Python (OOP + async + standard library)
- SQL fluency + networking conceptual base
- FastAPI + React intermediate full-stack
- LLD + HLD interview-ready (intermediate)
- ML conceptual base (enough to talk about it)
- Prompt engineering fundamentals
- DSA refreshed across 12 patterns

**Portfolio (3 projects, all on GitHub, 2 deployed live):**
1. Async API client + SQLite (Week 4)
2. Full-stack web app — auth + CRUD, deployed (Week 8)
3. AI Resume Reviewer — LLM-powered, deployed (Week 12)

**DSA Patterns Covered (24 sessions, ~96 problems):**
Arrays, Two Pointers, Strings, Sliding Window, Hash Maps, Linked Lists, Stacks, Monotonic Stack, Recursion, Backtracking, Binary Trees, Tree Traversals, BSTs, Heaps, Priority Queues, Graphs (BFS/DFS), DP (1D + 2D), Binary Search

---

## Rules to Survive Phase 1

1. **Ship every project rough.** Don't polish into perfection. Move on.
2. **If you fall behind on a day:** don't try to catch up by skipping the practice. Skip the *next* day's learn, do practice instead. Practice > theory.
3. **Sunday is sacred.** Use it. Burnout breaks the plan more than missed days.
4. **Block the time on a calendar.** "3 hrs after work" is not a plan. "7–10 PM, Mon–Sat" is.
5. **CP-style debugging when stuck:** when something doesn't work, isolate the specific concept that's missing, learn just that, fix, continue. Don't open a new course.
6. **Every Saturday evening (5 min):** check off the week, note what you skipped, plan tweaks for next week.

---

*End of Phase 1 plan. Phase 2 day-wise will be built at the end of Week 12 based on actual pace and gaps.*
