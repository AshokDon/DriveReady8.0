# Python AI Dev — Applied AI Engineer

## Complete 24-Week Syllabus (v3 — Scaler-Merged, System Design Heavy)

> **What changed in v3:** Merged the strongest parts of the Scaler upskilling track (SQL module + LLD modules) into the DriveReady syllabus, translated from Java to **Python**. Nothing was rebuilt — five weeks were upgraded (W2, W3, W5, W8, W9) and one deepened (W19). NoSQL stays **out** of the SQL week on purpose — it is taught later in the HLD weeks, matching how Scaler teaches it in system design.
>
> **What changed in v2 (retained):** LLD and HLD heavily expanded for placement interviews (now 35 total system design sessions across both phases). Capstone tightened to 2 weeks. Filler topics removed to make room for interview-critical content.
>
> **Why:** For B.Tech 3rd-year students, system design is the difference between a ₹6 LPA service company offer and a ₹15–25 LPA product company offer. Same DSA, same projects, different system design depth.

---

## Program Structure

| Phase       | Weeks | Focus                                              | Domain Pattern                   | DSA Track                    |
| ----------- | ----- | -------------------------------------------------- | -------------------------------- | ---------------------------- |
| **Phase 1** | 1–12  | Foundations + Engineering + LLD/HLD                | 4 tech days/week                 | +2 self-paced days/week      |
| **Phase 2** | 13–24 | AI Engineering + Advanced System Design + Capstone | 4 tech + 1 project day/week      | +2 self-paced days/week      |

**Every session = 90 min Learn + 90 min Practice (3 hours total)**

> **Weekly rhythm:** 6-day week = **4 domain days (in this doc)** + **2 DSA days (separate track, self-paced)**. DSA content is owned and paced by the instructor and is not detailed here. In Phase 2, the extra Project day makes the domain load heavier — see the open note in the changelog for how to balance that against the DSA days.

---

## What's Inside (Headline Numbers)

| Metric                            | Count                                                                                                                                              |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Total weeks                       | 24                                                                                                                                                 |
| Total tech sessions               | 108                                                                                                                                                |
| **SQL depth**                     | **Full 12-topic relational module** (CRUD → joins → indexing → ACID → window functions → schema design) — *Scaler-merged*                          |
| **LLD problems solved**           | **8** (Library Management, Parking Lot, Tic-Tac-Toe, Splitwise, BookMyShow, LRU/LFU Cache, Notification System, Chess, Logging Framework)          |
| **Design patterns mastered**      | **12** (Strategy, Factory, Observer, Singleton, Builder, Prototype, Registry, Decorator, Adapter, Facade, Flyweight, State, Chain of Responsibility) — *taught the Python way* |
| **HLD case studies**              | **10** (URL Shortener, Rate Limiter, WhatsApp, Twitter Feed, Uber, YouTube/Netflix, Distributed Cache, Search Autocomplete, RAG-at-scale, ChatGPT) |
| **Assessments (contests)**        | **3** (Python/OOP/Concurrency, Design Patterns, Machine Coding) — *Scaler-merged*                                                                  |
| **Mock system design interviews** | **3** (LLD mock, HLD mock, AI System Design mock)                                                                                                  |
| **Deployed portfolio projects**   | **6** (Async client, Full-stack app, AI Resume Reviewer, RAG Chatbot, Multi-Agent Assistant, AI Interview Coach capstone)                          |

---

## Module Map

### Phase 1 — Foundations + Engineering + System Design (Weeks 1–12)

| Week   | Module                                    |
| ------ | ----------------------------------------- |
| 1      | Python OOP & Object-Oriented Programming  |
| 2      | Advanced Python, Async & Concurrency      |
| 3      | Databases & SQL                           |
| 4      | Async API Mini Project                    |
| 5      | FastAPI Backend Development               |
| 6      | React Frontend Development                |
| 7      | Full-Stack Application (Deployed)         |
| **8**  | **LLD — Foundations (SOLID + UML)**       |
| **9**  | **LLD — Patterns & Problems**             |
| **10** | **HLD — Building Blocks**                 |
| **11** | **HLD — System Design Cases**             |
| 12     | ML + Prompt Engineering + AI Mini Project |

### Phase 2 — AI Engineering + Advanced System Design + Capstone (Weeks 13–24)

| Week   | Module                                |
| ------ | ------------------------------------- |
| 13     | RAG Foundations                       |
| 14     | RAG Retrieval Quality                 |
| 15     | RAG Production & Shipping             |
| 16     | AI Agents Foundations                 |
| 17     | LangGraph Orchestration               |
| 18     | Multi-Agent Systems                   |
| **19** | **Advanced LLD for Interviews**       |
| **20** | **Advanced HLD — Real System Design** |
| **21** | **HLD for AI Systems**                |
| 22     | Capstone — Planning & Backend         |
| 23     | Capstone — Frontend & Deployment      |
| 24     | Portfolio Finalization & Launch       |

---
---

# PHASE 1 — FOUNDATIONS + ENGINEERING + SYSTEM DESIGN

## Week 1 — Python OOP Foundation

> Covers Scaler Module-1's full OOP list (abstraction, classes, encapsulation, inheritance, polymorphism, abstract classes, interfaces) — kept as ours, since we already teach it in Python. Scaler's *Interfaces* are taught the Python way = `abc.ABC` + `typing.Protocol` (structural typing; Python has no `interface` keyword).

| Day | Topic                        | 90 min Learn                                                            | 90 min Practice                                                      |
| --- | ---------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------- |
| 1   | OOP Basics                   | Classes, instances, `__init__`, instance vs class vs static methods     | Build `BankAccount` class with deposit, withdraw, balance            |
| 2   | Inheritance                  | Single & multiple inheritance, `super()`, MRO, polymorphism             | Build `Vehicle → Car / Bike` hierarchy with method overriding        |
| 3   | Abstraction & Encapsulation  | `abc` module, abstract methods, properties, private/protected/public attributes, `Protocol` vs ABC | Convert Vehicle to abstract; add `@property` for read-only fields    |
| 4   | Composition + Dunder Methods | Composition over inheritance, `__str__`, `__eq__`, `__len__`, `__add__` | Build `Library` class composed of `Book` objects with dunder methods |

---

## Week 2 — Advanced Python, Async & Concurrency

> **Scaler-merged.** Absorbs Scaler Module-1's *Concurrency* section (threads, executors/callables, synchronization, semaphores) and *Advanced Java* equivalents (Streams → generators, Lambdas, Generics, Exceptions), all in Python. The key Python-specific teaching point: the **GIL** — threads give concurrency but not CPU-bound parallelism; use `multiprocessing` for that.

| Day | Topic                             | 90 min Learn                                                                                       | 90 min Practice                                                       |
| --- | --------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| 1   | Decorators & functools            | Function decorators, decorators with args, `functools.wraps`, `lambda` *(Scaler: Lambdas)*         | Write `@timer`, `@retry`, `@cache` decorators                        |
| 2   | Generators, Iterators & Typing    | `yield`, generators, `itertools` *(Scaler: Streams)*, context managers, type hints, generics (`TypeVar`, `Generic`) *(Scaler: Generics)*, exceptions & custom errors *(Scaler: Exception Handling)* | Build a Timer context manager + file line-reader generator; add type hints to Week 1 code |
| 3   | Concurrency *(Scaler)*            | Processes vs threads, `threading`, `concurrent.futures` (Executors & Callables), the **GIL caveat**, `multiprocessing` for CPU-bound work | Build a thread pool that fetches 10 URLs concurrently; measure vs sequential |
| 4   | Synchronization + asyncio         | Locks, `Semaphore`, race conditions *(Scaler: Synchronization)* → `asyncio`, event loop, `asyncio.gather`, httpx | Fix a race condition with a lock/semaphore; build an async function calling 3 APIs concurrently |

> **Assessment:** *Contest 1 — Python, OOP & Concurrency* (Scaler-merged, adapted to Python).

---

## Week 3 — Databases & SQL

> **Scaler-merged (rebuilt week).** Replaces the old "Databases & Networking" week with Scaler's full **12-topic relational SQL module**, taught on **PostgreSQL** and threaded to the QuickBite domain. **Networking (HTTP/REST/status codes/WebSockets/TLS) relocated to Week 5**, where it's taught in the context of building an API. **NoSQL is deliberately excluded here** — it is introduced in the HLD weeks (W10, W20), matching how Scaler sequences it in system design.

| Day | Topic                              | 90 min Learn                                                                          | 90 min Practice                                                    |
| --- | ---------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 1   | DB Foundations + CRUD *(Scaler)*   | Intro to databases, relational fundamentals (tables, keys, relationships), SELECT/WHERE/ORDER BY, INSERT/UPDATE/DELETE | 15 CRUD queries on a QuickBite dataset (users / orders / restaurants) |
| 2   | Joins + Aggregation *(Scaler)*     | All join types (inner/left/right/full/self), GROUP BY, HAVING, aggregate functions     | 10 multi-table join + aggregation queries; joins & aggregation practice set |
| 3   | Subqueries, Indexing & ACID *(Scaler)* | Subqueries & views, indexing & query optimization (when/how, EXPLAIN), transactions & ACID | Add indexes to a slow query and measure speedup; write a transaction with rollback |
| 4   | Window Functions + Schema Design *(Scaler)* | Window functions (ROW_NUMBER, RANK, running totals), Database Schema Design I & II (normalization, ER modeling) | Write 5 window-function queries; design a normalized schema for QuickBite from scratch |

> **Note:** This week feeds directly into Week 4 (persistence) and Week 5 (SQLAlchemy async on Postgres), so the same schema carries forward.

---

## Week 4 — Mini Project: Async API Client

> **Goal:** Lock in Python OOP + Async + SQL in one project. Build something that hits 3+ APIs concurrently and stores results in SQLite.

| Day | Topic          | 90 min Learn                                             | 90 min Practice                                                  |
| --- | -------------- | -------------------------------------------------------- | ---------------------------------------------------------------- |
| 1   | Project setup  | Structure, `uv` package manager, `pyproject.toml`, httpx | Set up repo with `uv init`, install deps, scaffold OOP structure |
| 2   | Async fetcher  | Concurrent API calls, error handling, retries            | Implement async client class with 3 API integrations             |
| 3   | DB integration | SQLAlchemy basics, schema design, persistence            | Add models + save fetched data to SQLite                         |
| 4   | Polish & ship  | Logging, README, git workflow                            | Push to GitHub with clean README. **🏆 Portfolio Piece #1**       |

---

## Week 5 — FastAPI Backend Development (Condensed)

> **Updated:** Networking essentials (relocated from old Week 3) are now folded into Day 1, where HTTP methods, status codes, and REST principles are taught in the natural context of building routes.

| Day | Topic               | 90 min Learn                                                            | 90 min Practice                                          |
| --- | ------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------- |
| 1   | Networking + FastAPI + Pydantic | **HTTP methods, status codes, REST principles, WebSockets vs HTTP, TLS** *(relocated networking)* → FastAPI setup, routing, Pydantic models, request/response validation, auto-docs | Hit 5 public APIs and document responses; build basic CRUD API with in-memory store (5 endpoints) |
| 2   | DB Integration      | SQLAlchemy 2.0 async, Postgres setup, async sessions, CRUD with DB      | Full CRUD endpoints backed by Postgres in Docker         |
| 3   | Authentication      | JWT, password hashing, dependency injection (`Depends`), current-user   | Add login/register + protect routes with auth dependency |
| 4   | Middleware + Docker | CORS, exception handlers, Docker basics for FastAPI                     | Add CORS + error handler; Dockerize your API             |

---

## Week 6 — React + Tailwind

| Day | Topic              | 90 min Learn                                                         | 90 min Practice                                               |
| --- | ------------------ | -------------------------------------------------------------------- | ------------------------------------------------------------- |
| 1   | React Fundamentals | JSX, components, props, conditional rendering                        | Build a static landing page with 3–4 components               |
| 2   | State + Effects    | `useState`, `useEffect`, event handlers, controlled inputs           | Build a counter + a fetch-from-API component                  |
| 3   | Routing + Context  | React Router, `useContext`, custom hooks                             | Build a 3-page app with shared state via context              |
| 4   | Forms + Tailwind   | Forms with validation, axios for API calls, Tailwind utility classes | Build a styled login + signup form that posts to your FastAPI |

---

## Week 7 — Full-Stack Project

> **Goal:** Wire React + FastAPI from Weeks 5–6 into a real deployed app.

| Day | Topic             | 90 min Learn                                                 | 90 min Practice                                              |
| --- | ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1   | Plan + scaffold   | API contract design, folder structure, CORS                  | Create both repos; define endpoints; build initial UI shells |
| 2   | Auth end-to-end   | Token storage, protected routes (frontend), refresh patterns | Login + signup flow working end-to-end                       |
| 3   | Core features     | CRUD on frontend, error handling, loading states             | Implement core CRUD on UI + backend                          |
| 4   | Deploy + document | Render.com (backend), Vercel (frontend), env vars            | Deploy live, write README. **🏆 Portfolio Piece #2**          |

---

## 🎯 Week 8 — LLD Foundations (SOLID + UML)

> **The placement-critical week #1.** Most freshers know SOLID by name but can't apply it. This week makes you actually apply it.
>
> **Scaler-merged:** adds the *machine-coding approach method* and the *Library Management System* as the first hands-on design problem, plus the *AI-integrations* framing for extensible design. Interfaces are taught as ABC + `Protocol`.

| Day | Topic                     | 90 min Learn                                                           | 90 min Practice                                                           |
| --- | ------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| 1   | SRP + OCP + Code Smells   | Single Responsibility & Open/Closed with Python examples; identifying duplicate code, long methods, large classes | Refactor Week 4 project — find SRP violations and 5 code smells, fix them |
| 2   | LSP + ISP + DIP           | Liskov Substitution, Interface Segregation, Dependency Inversion; interfaces the Python way (ABC + `Protocol`) | Spot LSP violations in inheritance trees; design ISP-compliant interfaces |
| 3   | UML + Extensible/AI Design *(Scaler)* | Class diagrams (attributes, methods, relationships), sequence diagrams; designing extensible systems + AI-integration seams | Draw UML class diagrams for Week 4 + Week 7 projects                      |
| 4   | Machine Coding: Approach + Library *(Scaler)* | How to approach design problems (requirements → entities → classes → interactions → code) | Design & code a **Library Management System** in Python end-to-end (with UML) |

> **Assessment:** *Contest 2 — Design Principles* (Scaler-merged; runs with Week 9).

---

## 🎯 Week 9 — LLD Patterns & Problems

> **The placement-critical week #2.** Solve classic LLD problems used in Indian product company interviews.
>
> **Scaler-merged:** design patterns are re-taught **the Python way** (Singleton via module/metaclass/decorator, not Java's private constructor; Builder often via `@dataclass`; Prototype via `copy.deepcopy`; Decorator contrasted against Python's *native* decorators). Adds Prototype, Registry, Flyweight, State. **Tic-Tac-Toe** added as the gentle first machine-coding problem; **Chess** moved to Week 19 (harder tier).

| Day | Topic                          | 90 min Learn                                                                          | 90 min Practice                                                                       |
| --- | ------------------------------ | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| 1   | Creational Patterns (Python way) | Strategy, Factory, Singleton (module/metaclass), Builder (`@dataclass`), Prototype (`deepcopy`), Registry | Implement Strategy for payment methods + Factory for vehicles + Builder for a complex query |
| 2   | Structural + Behavioral        | Decorator (native vs GoF pattern), Adapter, Facade, Flyweight, Observer, State        | Build an event-based notification system using Observer; State for an order workflow   |
| 3   | LLD Problem Pair 1 *(Scaler approach)* | Approach method applied: requirements → entities → classes → interactions → code | Solve: **Parking Lot** + **Tic-Tac-Toe** in Python (with UML diagrams)                |
| 4   | LLD Problem Pair 2             | Same approach, harder multi-entity problems                                           | Solve: **Splitwise** (balances, simplify-debts) + **BookMyShow** (seat-locking)       |

> **Assessment:** *Contest 3 — Machine Coding* (Scaler-merged).

---

## 🎯 Week 10 — HLD Building Blocks

> **The placement-critical week #3.** Without these building blocks, every HLD interview is just guessing. **NoSQL is introduced here** (deferred from the SQL week by design).

| Day | Topic                        | 90 min Learn                                                                                   | 90 min Practice                                             |
| --- | ---------------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| 1   | Scalability + Load Balancers | CAP theorem, vertical vs horizontal, L4 vs L7 load balancers, algorithms                       | Sketch how to scale a single-server app to handle 1M users  |
| 2   | Caching + CDN                | Cache-aside, write-through, write-back patterns, Redis usage, CDN basics                       | Add Redis caching to a Week 7 endpoint; measure speedup     |
| 3   | SQL vs NoSQL + Message Queues | **When to use NoSQL (document/KV/wide-column) vs SQL**; Kafka vs RabbitMQ, pub/sub model       | Sketch architecture for a notification system using a queue; pick DB type per use case |
| 4   | Sharding + Microservices     | Database sharding strategies, replication (master-slave), microservices vs monolith trade-offs | Sketch when to split a monolith into microservices          |

---

## 🎯 Week 11 — HLD System Design Cases

> **The placement-critical week #4.** Solve real interview cases. By end of week, students can attempt any standard HLD question.

| Day | Topic                            | 90 min Learn                                                                                                  | 90 min Practice                                                |
| --- | -------------------------------- | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| 1   | API Gateway + Rate Limiting + HA | Gateway responsibilities, rate limiting strategies (token bucket, sliding window), high availability patterns | Design a rate limiter on paper + write pseudocode              |
| 2   | Case Studies Pair 1              | Walk through: **URL Shortener** (TinyURL), **Rate Limiter** design                                            | Solve from scratch on whiteboard, time-boxed 45 min each       |
| 3   | Case Studies Pair 2              | Walk through: **WhatsApp messaging**, **Twitter feed**                                                        | Solve from scratch, focus on data model + architecture         |
| 4   | Case Study + Mock                | Walk through: **Uber ride-matching** + Mock system design interview practice                                  | Pair up + take turns being interviewer/candidate (45 min each) |

---

## Week 12 — ML + Prompt Engineering + AI Mini Project

> **Combined module:** Light ML conceptual + practical prompt engineering. ML is intuition-only; prompt engineering is where you actually build.

| Day | Topic                     | 90 min Learn                                                                          | 90 min Practice                                                                          |
| --- | ------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 1   | ML Fundamentals           | Supervised/unsupervised, train/val/test split, regression vs classification intuition | Watch Andrew Ng ML Week 1; train a simple linear regression with scikit-learn            |
| 2   | NN Intuition + Embeddings | Neural networks intuition (3Blue1Brown), embeddings concept                           | Train a Random Forest classifier; explore sentence-transformers in Colab                 |
| 3   | Prompt Engineering Basics | LLM message format, temperature, few-shot, Chain-of-Thought, structured output (JSON) | Make 10 API calls; build prompt for structured JSON output                               |
| 4   | Build AI Mini Project     | Prompt chaining + context management + integration patterns                           | Ship a deployed AI Resume Reviewer (FastAPI + simple React UI). **🏆 Portfolio Piece #3** |

---

## ✅ End of Phase 1 — What You'll Have

**Skills:**

- Strong Python (OOP + async + **concurrency with the GIL understood**)
- **SQL fluency to interview depth** (joins, indexing, ACID, window functions, schema design) + networking base
- FastAPI + React intermediate full-stack
- **LLD: SOLID applied + patterns the Python way + 4 classic problems solved (incl. Library Management)**
- **HLD: Building blocks + 5 case studies + 1 mock interview**
- ML conceptual base + Prompt engineering fundamentals

**Portfolio (3 deployed projects):**

1. Async API Client (Week 4)
2. Full-Stack Web App (Week 7)
3. AI Resume Reviewer (Week 12)

**Placement Readiness:** Students can attempt any standard LLD problem + 70% of standard HLD cases.

---
---

# PHASE 2 — AI ENGINEERING + ADVANCED SYSTEM DESIGN + CAPSTONE

> **Pattern:** 4 tech days + 1 dedicated Project Build day per week (plus the separate 2-day DSA track).

---

## Week 13 — RAG Foundations

| Day             | Topic                 | 90 min Learn                                                                | 90 min Practice                                                                              |
| --------------- | --------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 1               | What is RAG           | RAG vs Fine-tuning, full RAG pipeline, document parsing (PDFs, websites)    | Sketch a RAG architecture; parse 10 PDFs into clean text                                     |
| 2               | Chunking              | Fixed, recursive, semantic chunking, overlap tuning                         | Compare 3 chunking strategies on same document                                               |
| 3               | Embeddings            | OpenAI / BGE embeddings, similarity, distance metrics (cosine, dot product) | Generate embeddings for chunks; visualize in 2D                                              |
| 4               | Vector DBs + ChromaDB | ChromaDB setup, collections, persistence basics                             | Set up ChromaDB; ingest your chunks; run similarity search                                   |
| **5 (Project)** | **RAG MVP**           | —                                                                           | **Build:** Bare-bones RAG over your own notes. Single-file Python script. Working end-to-end |

---

## Week 14 — RAG Retrieval Quality

| Day             | Topic                  | 90 min Learn                                                       | 90 min Practice                                                                        |
| --------------- | ---------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| 1               | ChromaDB Deep Dive     | Collections, metadata filtering, persistence, advanced queries     | Migrate Week 13 MVP to persistent ChromaDB; add metadata filters                       |
| 2               | Hybrid Search          | BM25 + semantic combined, reciprocal rank fusion                   | Implement hybrid search; compare to pure semantic on 10 queries                        |
| 3               | Re-ranking             | Cross-encoder rerankers (Cohere, bge-reranker), when to use        | Add re-ranker to your pipeline; measure quality improvement                            |
| 4               | Citations + Evaluation | Source citations, RAGAs framework, faithfulness, context precision | Add citation rendering; evaluate RAG on 20 test questions                              |
| **5 (Project)** | **RAG + FastAPI**      | —                                                                  | **Build:** Wrap RAG in FastAPI endpoint. POST `/ask`, returns answer + sources. Deploy |

---

## Week 15 — RAG Production & Shipping

| Day             | Topic                | 90 min Learn                                                                | 90 min Practice                                                                                |
| --------------- | -------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| 1               | Streaming            | Server-Sent Events (SSE) with FastAPI's `StreamingResponse`                 | Add streaming to your RAG endpoint; verify token-by-token                                      |
| 2               | Security             | Prompt injection (direct/indirect), defensive prompts, PII filtering basics | Test prompt injection attacks; add guards                                                       |
| 3               | Cost + Tokens        | Token counting, cost-per-request, model routing                             | Add cost tracking; route easy queries to cheap models                                          |
| 4               | Observability        | LangSmith or Helicone setup, tracing, debugging                             | Wire LangSmith into your RAG; track 100 requests                                               |
| **5 (Project)** | **Ship RAG Chatbot** | —                                                                           | **Build:** Full React UI for your RAG. Streaming responses. Deployed. **🏆 Portfolio Piece #4** |

---

## Week 16 — AI Agents Foundations

| Day             | Topic                    | 90 min Learn                                                 | 90 min Practice                                                                                                         |
| --------------- | ------------------------ | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| 1               | What is an Agent         | Agents vs RAG vs LLM calls, when to use each                 | Read Anthropic's "Building effective agents"; take notes                                                                |
| 2               | Tool Use                 | LLM function calling, tool schemas, structured outputs       | Build a single-tool agent: calculator that LLM can call                                                                 |
| 3               | ReAct Loop               | Reasoning + Acting pattern, observation-thought-action cycle | Trace through 3 ReAct examples on paper before coding                                                                   |
| 4               | Build ReAct from Scratch | Hand-rolled ReAct loop (no framework yet)                    | Build a from-scratch ReAct agent with 3 tools: search, calculator, time                                                 |
| **5 (Project)** | **Tool-Calling Demo**    | —                                                            | **Build:** A "personal assistant" agent with 5 tools (weather, web search, calculator, calendar mock, notes). Local CLI |

---

## Week 17 — LangGraph Orchestration

| Day             | Topic                       | 90 min Learn                                                    | 90 min Practice                                                                                      |
| --------------- | --------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 1               | LangGraph Basics            | State, nodes, edges, the StateGraph                             | Rebuild Week 16 ReAct agent in LangGraph; compare code                                               |
| 2               | Conditional Edges + Cycles  | Branching logic, loops, when to terminate                       | Build a 3-node graph with conditional routing                                                        |
| 3               | Tools in LangGraph          | ToolNode, tool integration, error handling                      | Add 5 tools to your graph with proper error handling                                                 |
| 4               | Memory + RAG Integration    | Checkpointing, conversation memory, giving agents access to RAG | Add persistent memory + connect Week 15 RAG as a tool                                                |
| **5 (Project)** | **Stateful Research Agent** | —                                                               | **Build:** A research assistant that remembers prior conversations + uses your RAG. FastAPI endpoint |

---

## Week 18 — Multi-Agent Systems

| Day             | Topic                              | 90 min Learn                                              | 90 min Practice                                                                                                            |
| --------------- | ---------------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 1               | Multi-Agent Patterns               | Supervisor pattern, when multi-agent beats single-agent   | Sketch architecture for a multi-agent customer support system                                                              |
| 2               | Supervisor + Specialists           | Build a supervisor that routes to specialist agents       | Implement supervisor + 2 specialists in LangGraph                                                                          |
| 3               | Inter-Agent State Passing          | How agents share state, message protocols                 | Build a 3-agent pipeline passing state between them                                                                        |
| 4               | Debugging + Use Cases              | Common failure modes, real-world multi-agent applications | Inject deliberate bugs into your multi-agent system; debug them                                                            |
| **5 (Project)** | **Multi-Agent Research Assistant** | —                                                         | **Build:** Researcher (RAG) + Analyst (reasoning) + Writer (output) multi-agent system. Deployed. **🏆 Portfolio Piece #5** |

---

## 🎯 Week 19 — Advanced LLD for Interviews

> **The placement-critical week #5.** Goes beyond basic patterns into the LLD problems that separate good candidates from great ones. **Chess** now lives here (moved from Week 9) as a top-tier hard problem, alongside Scaler's harder machine-coding set.

| Day             | Topic                           | 90 min Learn                                       | 90 min Practice                                                                                   |
| --------------- | ------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| 1               | Chain of Responsibility + State | Two patterns frequently asked in senior interviews | Implement CoR for request validation; State for order workflow                                    |
| 2               | Adapter + Facade                | Integration patterns essential for system design   | Build Adapter for legacy API; Facade for complex subsystem                                        |
| 3               | LLD Problem Pair 1              | Same approach as Week 9 but harder                 | Solve: **LRU/LFU Cache** + **Notification System**                                                |
| 4               | LLD Problem Pair 2              | More complex multi-class interactions              | Solve: **Chess** + **Logging Framework**                                                          |
| **5 (Project)** | **Mock LLD Interview**          | —                                                  | **Practice:** Live mock LLD interview (60 min) with another student or instructor — design + code |

---

## 🎯 Week 20 — Advanced HLD — Real System Design

> **The placement-critical week #6.** Real interview HLD questions, with the advanced concepts that come up in product company interviews.

| Day             | Topic                              | 90 min Learn                                                                        | 90 min Practice                                                                |
| --------------- | ---------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| 1               | Database Design at Scale           | SQL vs NoSQL trade-offs, when to use each, data modeling for scale                  | Design data layer for "design Instagram" — choose DBs with justification       |
| 2               | Consistent Hashing + Bloom Filters | How distributed systems route + check existence efficiently                         | Implement consistent hashing in Python; build a Bloom filter                   |
| 3               | Event-Driven Architecture          | Event sourcing, CQRS, when to use, trade-offs                                       | Sketch an event-driven order processing system                                 |
| 4               | Case Studies                       | Walk through: **YouTube/Netflix** + **Distributed Cache** + **Search Autocomplete** | Solve from scratch on whiteboard, 30 min each                                  |
| **5 (Project)** | **Mock HLD Interview**             | —                                                                                   | **Practice:** Live mock HLD interview (60 min) — full whiteboard system design |

---

## 🎯 Week 21 — HLD for AI Systems (The Hidden Weapon)

> **The placement-critical week #7.** AI companies are now asking "design ChatGPT" and "design a RAG system" in interviews. This module gives you the answer.

| Day             | Topic                               | 90 min Learn                                                            | 90 min Practice                                                                    |
| --------------- | ----------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| 1               | Designing a RAG System at Scale     | Ingestion pipeline, vector DB sharding, retrieval optimization, caching | Sketch architecture for RAG serving 1M queries/day                                 |
| 2               | Designing ChatGPT Architecture      | LLM serving, request routing, session management, streaming             | Walk through full ChatGPT architecture, identify all bottlenecks                   |
| 3               | Designing a Recommendation System   | Candidate generation, ranking, personalization, real-time updates       | Design YouTube's recommendation pipeline                                           |
| 4               | LLM Inference at Scale              | Caching, batching, model routing (cheap → expensive), token streaming   | Calculate cost vs latency trade-offs for a RAG system                              |
| **5 (Project)** | **Mock AI System Design Interview** | —                                                                       | **Practice:** Live mock AI system design interview — design from scratch in 60 min |

---

## Week 22 — Capstone — Planning & Backend

> **Project: AI Interview Coach** — Multi-agent system that conducts mock interviews, evaluates answers, and provides coaching.

| Day             | Topic                          | 90 min Learn                                                          | 90 min Practice                                                                      |
| --------------- | ------------------------------ | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| 1               | Capstone Planning              | PRD writing, architecture diagrams, user flows                        | Write 1-page PRD; draw system architecture; create GitHub repo                       |
| 2               | Database + Auth Setup          | Schema design, user accounts, interview sessions                      | Set up FastAPI + Postgres + JWT auth                                                 |
| 3               | RAG: Question Bank             | Ingesting interview questions across DSA + System Design + Behavioral | Ingest curated question bank into ChromaDB                                           |
| 4               | Interviewer + Evaluator Agents | Build the first two agents using LangGraph                            | Build Interviewer (asks questions) + Evaluator (scores answers)                      |
| **5 (Project)** | **Backend Wired**              | —                                                                     | **Build:** Auth + question bank + interviewer + evaluator working end-to-end via CLI |

---

## Week 23 — Capstone — Frontend & Deployment

| Day             | Topic                 | 90 min Learn                                                      | 90 min Practice                                                                                 |
| --------------- | --------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| 1               | React UI Setup        | Vite + React + Tailwind, design system                            | Build login + dashboard shell                                                                   |
| 2               | Interview Interface   | Real-time interview UI with streaming responses                   | Build the interview screen with streaming                                                       |
| 3               | Feedback + Dashboard  | Render evaluator scores, coach feedback, progress charts          | Build post-interview review + user dashboard with recharts                                      |
| 4               | Production Deployment | Docker, Render (backend), Vercel (frontend), env vars, monitoring | Deploy to production URLs; test end-to-end                                                      |
| **5 (Project)** | **Capstone Ship**     | —                                                                 | **Build:** Production-grade capstone deployed and demoable. **🏆 Portfolio Piece #6 — Capstone** |

---

## Week 24 — Portfolio Finalization & Launch

| Day             | Topic                     | 90 min Learn                                                  | 90 min Practice                                                                           |
| --------------- | ------------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 1               | README Mastery            | Architecture diagrams, demo GIFs, clear setup instructions    | Polish READMEs for all 6 portfolio projects                                               |
| 2               | Demo Videos               | 60-second product demos, Loom/Riverside basics                | Record 1-min demo videos for all 6 projects                                               |
| 3               | GitHub Profile            | Profile README, pinned repos, contribution graph              | Polish GitHub profile; pin top 6 projects                                                 |
| 4               | LinkedIn + Portfolio Site | LinkedIn rewrite for AI engineer roles, simple portfolio site | Update LinkedIn; deploy a simple portfolio site (Vercel)                                  |
| **5 (Project)** | **Public Launch**         | —                                                             | **Build:** LinkedIn post, X/Twitter thread, share in AI communities. Capstone goes public |

---

## ✅ End of Phase 2 — What You'll Have

**Skills:**

- Production RAG systems (chunking, hybrid search, re-ranking, evaluation)
- AI agents from scratch + LangGraph orchestration
- Multi-agent systems
- Streaming, security, cost optimization
- **Advanced LLD: 12 patterns (Python way), 8 problems solved**
- **Advanced HLD: 10 case studies, 3 mock interviews including AI system design**
- Full deployed capstone

**Portfolio (3 new + capstone, total 6):**
4. **RAG Chatbot** (Week 15)
5. **Multi-Agent Research Assistant** (Week 18)
6. **AI Interview Coach Capstone** (Week 23)

---

## Why This v3 Curriculum Wins Placements

The single biggest change from v1 to v2 was **system design depth**. v3 keeps that and adds **interview-grade SQL** and **Python-native LLD** from the Scaler track. Here's the math on why this matters:

|                               | Typical Course | This Course (v3)             |
| ----------------------------- | -------------- | ---------------------------- |
| SQL depth                     | 2-3 topics     | **12-topic module**          |
| LLD sessions                  | 4              | **20** (Weeks 8-9 + 19)      |
| HLD sessions                  | 4              | **15** (Weeks 10-11 + 20-21) |
| LLD problems solved           | 1-2            | **8**                        |
| HLD case studies              | 2-3            | **10**                       |
| Assessments (contests)        | 0              | **3**                        |
| Mock system design interviews | 0              | **3**                        |

**Interview reality:**

- Service companies test mostly DSA → ₹4-8 LPA range
- Product companies test DSA + LLD → ₹8-15 LPA range
- Top product companies + AI startups test DSA + LLD + HLD → **₹15-25+ LPA range**

Your students will be ready for the third tier — not just AI roles, but any product company AI/backend role.

---

## Master Rules for Both Phases

1. **Ship rough, ship fast.** A working ugly project beats a beautiful unfinished one.
2. **One topic at a time.** No tutorial hopping. Finish the day's learn → do the day's practice → close everything → next day.
3. **System design = whiteboard or paper FIRST.** Don't code until you've drawn the design.
4. **Stuck protocol:** Isolate the specific concept that's blocking → 30 min of focused search/read → unblock → continue.
5. **Weekend reflection (5 min, Saturday):** Check off the week. Note what slipped. Plan adjustments for next week.
6. **Public is better than private.** GitHub from Week 1. Blog from Week 4. LinkedIn from Week 12.

---

## v3 Merge Log (Scaler → DriveReady)

| Week | Change | Type |
| ---- | ------ | ---- |
| W2   | Added Concurrency (threading, `concurrent.futures`, GIL, semaphores) + folded in Streams→generators, Lambdas, Generics, Exceptions | **Add** |
| W3   | Rebuilt as "Databases & SQL" using Scaler's 12-topic module on PostgreSQL; NoSQL deferred to HLD | **Replace** |
| W5   | Networking essentials (HTTP/REST/status/TLS) relocated here into Day 1 | **Move** |
| W8   | Added machine-coding approach + Library Management System; Interfaces = ABC/`Protocol`; AI-integration framing | **Add** |
| W9   | Patterns re-taught the Python way; added Prototype/Registry/Flyweight/State; Tic-Tac-Toe added; Chess → W19 | **Replace + Add** |
| W19  | Absorbed Chess as a top-tier hard problem | **Move** |
| All  | Adopted Scaler's 3 contests as assessments (Python/OOP/Concurrency, Design Patterns, Machine Coding) | **Add** |

**Open item for instructor:** Phase 2 runs 4 tech + 1 project day. With the separate 2-day DSA track that's a 7-day footprint. Decide whether Phase 2 DSA drops to 1 day/week, or the project day rotates biweekly, so the week stays sustainable.

**Deliberately NOT merged:** Java-specific plumbing (Java Collections internals, checked exceptions, JVM concurrency details) — replaced by Python equivalents. NoSQL kept out of the SQL week by design (taught in HLD, matching Scaler's own sequencing).

---

*End of 24-week consolidated syllabus v3. DSA and other placement preparation are handled separately per the student's own pacing.*
