# Python AI Dev — Applied AI Engineer
## Complete 24-Week Syllabus (Tech Stack)

> **What this document is:** The full technical curriculum for the Applied AI Engineer program. Day-wise breakdown of all tech content across 24 weeks, split into two phases of 12 weeks each.
>
> **What it isn't:** DSA / interview prep is handled separately and not included here.

---

## Program Structure

| Phase | Weeks | Focus | Daily Pattern |
|---|---|---|---|
| **Phase 1** | 1–12 | Foundations + Full-Stack Engineering | 4 tech days/week |
| **Phase 2** | 13–24 | AI Engineering + Capstone | 4 tech days + 1 project day/week |

**Every session = 90 min Learn + 90 min Practice (3 hours total)**

---

## Module Map

### Phase 1 — Foundations + Engineering (Weeks 1–12)

| Weeks | Module |
|---|---|
| 1–2 | Python OOP + Async |
| 3 | SQL + Networking |
| 4 | Mini Project — Async API Client |
| 5–6 | FastAPI |
| 7 | React + Tailwind |
| 8 | Full-Stack Project (Deployed) |
| 9 | LLD (Low Level Design) |
| 10 | HLD (High Level Design) |
| 11 | ML Conceptual (Light) |
| 12 | Prompt Engineering + AI Mini Project |

### Phase 2 — AI Engineering + Capstone (Weeks 13–24)

| Weeks | Module |
|---|---|
| 13–15 | RAG Systems (learn + build) |
| 16–18 | AI Agents + Multi-Agent Systems |
| 19 | Production AI (Streaming, Security, Cost) |
| 20–23 | Capstone — AI Interview Coach |
| 24 | Portfolio Finalization + Launch |

---

# PHASE 1 — FOUNDATIONS + ENGINEERING

## Week 1 — Python OOP Foundation

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | OOP Basics | Classes, instances, `__init__`, instance vs class vs static methods | Build `BankAccount` class with deposit, withdraw, balance |
| 2 | Inheritance | Single & multiple inheritance, `super()`, MRO, polymorphism | Build `Vehicle → Car / Bike` hierarchy with method overriding |
| 3 | Abstraction & Encapsulation | `abc` module, abstract methods, properties, private attributes | Convert Vehicle to abstract; add `@property` for read-only fields |
| 4 | Composition + Dunder Methods | Composition over inheritance, `__str__`, `__eq__`, `__len__`, `__add__` | Build `Library` class composed of `Book` objects with dunder methods |

---

## Week 2 — Python Advanced (Decorators, Generators, Async)

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | Decorators | Function decorators, decorators with args, `functools.wraps` | Write `@timer`, `@retry`, `@cache` decorators |
| 2 | Generators & Iterators | Generator functions, `yield`, iterators, generator expressions | Build a file line-reader generator + Fibonacci generator |
| 3 | Context Managers + Type Hints | `with` statement, `__enter__`/`__exit__`, custom context managers, type hints | Write a `Timer` context manager + add type hints to all Week 1 code |
| 4 | Async/Await | Event loop, coroutines, `async/await`, `asyncio.gather` | Build async function calling 3 APIs concurrently |

---

## Week 3 — SQL + Networking

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | SQL Basics | SELECT, WHERE, ORDER BY, LIMIT, INSERT/UPDATE/DELETE | 15 queries on a sample dataset (employees / orders) |
| 2 | SQL Joins & Aggregations | INNER/LEFT/RIGHT JOIN, GROUP BY, HAVING, aggregate functions | 10 multi-table queries |
| 3 | SQL Indexes + Transactions | Indexes (why & when), ACID, basic transactions | Add indexes to your sample DB; measure speed difference |
| 4 | Networking Concepts | HTTP methods, status codes, REST principles, WebSockets vs HTTP, TLS basics | Use Postman: hit 5 public APIs (GET/POST/PUT/DELETE); document responses |

---

## Week 4 — Mini Project: Async API Client

> **Goal:** Lock in Python OOP + Async + SQL in one project. Build something that hits 3+ APIs concurrently and stores results in SQLite.

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | Project setup | Project structure, `uv` package manager, `aiohttp`/`httpx` basics | Set up repo with `uv init`, install deps, scaffold OOP structure |
| 2 | Build async fetcher | Concurrent API calls with asyncio.gather, error handling | Implement async client class with 3 API integrations |
| 3 | DB integration | SQLAlchemy basics, schema design | Add models + save fetched data to SQLite |
| 4 | Polish & ship | Logging, README writing, git workflow | Push to GitHub with clean README + screenshots. **🏆 Portfolio Piece #1** |

---

## Week 5 — FastAPI Part 1

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | FastAPI Intro | Setup, routing, Pydantic models, automatic docs | Build basic CRUD API with in-memory store (5 endpoints) |
| 2 | Request Handling | Path params, query params, request body, response models | Add validation + custom response models to your API |
| 3 | SQLAlchemy Async | Async engine, sessions, models, `select()` | Set up Postgres locally (Docker), define models, write first async query |
| 4 | CRUD with DB | Connect API to DB, async CRUD endpoints | Full CRUD endpoints backed by Postgres |

---

## Week 6 — FastAPI Part 2

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | Authentication | JWT basics, password hashing, OAuth2 password flow | Add login/register endpoints with JWT |
| 2 | Dependency Injection | FastAPI's DI system, `Depends`, current-user dependency | Protect routes with auth dependency; add user-scoped resources |
| 3 | Middleware + Error Handling | Middleware (CORS, logging), exception handlers, validation errors | Add CORS middleware + custom exception handler |
| 4 | Docker for FastAPI | Dockerfile, docker-compose with Postgres, env vars | Dockerize your full API + Postgres with docker-compose |

---

## Week 7 — React + Tailwind

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | React Fundamentals | JSX, components, props, conditional rendering | Build a static landing page with 3–4 components |
| 2 | State + Effects | `useState`, `useEffect`, event handlers, controlled inputs | Build a counter + a fetch-from-API component |
| 3 | Routing + Context | React Router, `useContext`, custom hooks | Build a 3-page app with shared state via context |
| 4 | Forms + Tailwind | Forms with validation, axios for API calls, Tailwind utility classes | Build a styled login + signup form that posts to your FastAPI |

---

## Week 8 — Full-Stack Project

> **Goal:** Wire React + FastAPI from Weeks 5–7 into a real deployed app. Pick: URL shortener, notes app, or expense tracker.

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | Plan + scaffold | API contract design, folder structure | Create both repos; define endpoints; build initial UI shells |
| 2 | Wire auth end-to-end | Token storage, protected routes (frontend), refresh patterns | Login + signup flow working end-to-end |
| 3 | Core features + polish | CRUD on frontend, error handling, loading states | Implement core CRUD on UI + backend |
| 4 | Deploy + document | Render.com (backend), Vercel (frontend), env vars, custom domain | Deploy live, write README with architecture, record 1-min demo. **🏆 Portfolio Piece #2** |

---

## Week 9 — LLD (Low Level Design)

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | SOLID Principles | All 5 principles with Python examples | Refactor your Week 4 project to follow SOLID; document changes |
| 2 | Strategy + Factory | Strategy pattern, simple factory, factory method | Implement Strategy for payment methods + Factory for vehicles |
| 3 | Observer + Singleton + Builder | When to use each, Python implementations | Implement event-based notification system using Observer |
| 4 | LLD Problem Solving | Approach: requirements → classes → interactions → code | Solve Parking Lot (or Splitwise) in Python with class diagrams |

---

## Week 10 — HLD (High Level Design)

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | Scalability Basics | Vertical vs horizontal, load balancers, CAP theorem | Sketch architecture for "design Instagram feed" on paper |
| 2 | Caching + CDN | Redis basics, cache strategies (write-through, cache-aside), CDN | Add Redis caching to one endpoint in your Week 8 project |
| 3 | Queues + Sharding | Message queues (Kafka/RabbitMQ conceptual), sharding, replication, read replicas | Sketch architecture for "design a notification system" |
| 4 | System Design Case Study | Walkthrough: design URL shortener (you built it!) | Solve: design a rate limiter, with class + sequence diagrams |

---

## Week 11 — ML Conceptual (Light, Goal: Build Intuition)

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | What is ML? | ML vs traditional programming, supervised/unsupervised, train/val/test split | Watch Andrew Ng ML Week 1; take notes |
| 2 | Regression + Classification | Linear regression, logistic regression, cost functions intuition | Train a linear regression model on a toy dataset with scikit-learn |
| 3 | Trees + Ensembles | Decision trees, random forests, XGBoost overview | Train a Random Forest classifier on Titanic dataset |
| 4 | Neural Net Intuition + Embeddings | What's a neural net, backprop intuition, what are embeddings | Read about word embeddings; play with sentence-transformers in Colab |

---

## Week 12 — Prompt Engineering + AI Mini Project

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | LLM API Basics | System/user/assistant messages, temperature, max tokens, API calling (Claude/OpenAI) | Make 10 API calls to an LLM; experiment with temperature and system prompts |
| 2 | Prompt Patterns | Few-shot, chain-of-thought, structured output (JSON mode) | Build prompts that return strictly typed JSON for 3 use cases |
| 3 | Prompt Chaining + Context Mgmt | Multi-step prompts, context window limits, token counting | Build a 3-step prompt chain (extract → classify → summarize) |
| 4 | Build: AI Resume Reviewer | Apply everything: FastAPI backend + LLM call + simple React UI | Ship a deployed AI resume reviewer. **🏆 Portfolio Piece #3** |

---

## ✅ End of Phase 1 — What You'll Have

**Skills:**
- Strong Python (OOP + async + standard library)
- SQL fluency + networking conceptual base
- FastAPI + React intermediate full-stack
- LLD + HLD interview-ready (intermediate)
- ML conceptual base
- Prompt engineering fundamentals

**Portfolio (3 deployed projects):**
1. Async API Client (Week 4)
2. Full-Stack Web App (Week 8)
3. AI Resume Reviewer (Week 12)

---

---

# PHASE 2 — AI ENGINEERING + CAPSTONE

> **Pattern change:** Phase 2 adds a dedicated **Project Build Day** each week (Day 5). The 4 tech days teach concepts; the project day applies them to a real shipping project that compounds week over week.

---

## Week 13 — RAG Foundations

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | What is RAG | When to use RAG vs fine-tuning, the full RAG pipeline | Read DeepLearning.AI RAG module 1; sketch a RAG architecture |
| 2 | Document Parsing | Loading PDFs, websites, markdown with LangChain loaders | Parse 10 PDFs into clean text chunks |
| 3 | Chunking Strategies | Fixed-size, recursive, semantic chunking, overlap tuning | Compare 3 chunking strategies on same document; measure retrieval quality |
| 4 | Embeddings | Embeddings basics, OpenAI / BGE / Cohere models, similarity | Generate embeddings for your chunks; explore in 2D with t-SNE |
| **5 (Project)** | **RAG MVP** | — | **Build:** Bare-bones RAG over your own notes (ChromaDB + OpenAI/Claude). Single-file Python script. Working end-to-end |

---

## Week 14 — RAG: Retrieval Quality

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | Vector Databases | ChromaDB deep dive: collections, metadata filtering, persistence | Migrate Week 13 MVP to persistent ChromaDB; add metadata |
| 2 | Hybrid Search | BM25 + semantic search combined, reciprocal rank fusion | Implement hybrid search; compare to pure semantic on 10 queries |
| 3 | Re-ranking | Cross-encoder rerankers (cohere, bge-reranker), when to use | Add re-ranker to your pipeline; measure quality improvement |
| 4 | Query Transformation | HyDE, multi-query, query decomposition | Implement multi-query retrieval; test on complex questions |
| **5 (Project)** | **RAG with FastAPI** | — | **Build:** Wrap your RAG in a FastAPI endpoint. POST `/ask`, returns answer + sources. Deploy to Render |

---

## Week 15 — RAG: Production

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | Source Citations | Returning sources, page numbers, confidence scores | Add citation rendering to API response |
| 2 | Evaluation: RAGAs | Faithfulness, context precision, answer relevancy | Set up RAGAs; evaluate your RAG on 20 test questions |
| 3 | Cloud Vector DBs | Pinecone setup, when to move off ChromaDB | Migrate one collection to Pinecone; compare latency |
| 4 | RAG Patterns | Agentic RAG, parent-document retrieval, hierarchical | Pick one advanced pattern; integrate into your project |
| **5 (Project)** | **Ship RAG Chatbot** | — | **Build:** Full React UI for your RAG. Streaming responses. Deploy. Write blog post. **🏆 Portfolio Piece #4** |

---

## Week 16 — AI Agents: Foundations

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | What is an Agent | Agents vs RAG vs simple LLM calls, when to use each | Read Anthropic's "Building effective agents" article; take notes |
| 2 | Tool Use / Function Calling | LLM function calling, structured outputs, tool schemas | Build a single-tool agent: calculator that LLM can call |
| 3 | ReAct Loop | Reasoning + Acting pattern, observation-thought-action cycle | Trace through 3 ReAct examples on paper before coding |
| 4 | Build ReAct from Scratch | Hand-rolled ReAct loop (no framework yet) | Build a from-scratch ReAct agent with 3 tools: search, calculator, time |
| **5 (Project)** | **Tool-Calling Demo** | — | **Build:** A "personal assistant" agent with 5 tools (weather, web search, calculator, calendar mock, notes). Local CLI |

---

## Week 17 — LangGraph

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | LangGraph Basics | State, nodes, edges, the StateGraph | Rebuild Week 16 ReAct agent in LangGraph; compare code |
| 2 | Conditional Edges + Cycles | Branching logic, loops, when to terminate | Build a 3-node graph with conditional routing |
| 3 | Tools in LangGraph | ToolNode, tool integration, error handling | Add 5 tools to your graph with proper error handling |
| 4 | Memory + Persistence | Checkpointing, conversation memory, thread management | Add persistent memory; agent remembers across runs |
| **5 (Project)** | **Stateful Agent** | — | **Build:** A research assistant that remembers prior conversations. FastAPI endpoint. Test with 5-turn conversation |

---

## Week 18 — Multi-Agent Systems

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | Multi-Agent Patterns | Supervisor, hierarchical, network patterns; when to use multi-agent | Sketch architecture for a multi-agent customer support system |
| 2 | Supervisor Pattern | Build supervisor that routes to specialist agents | Implement supervisor + 2 specialists in LangGraph |
| 3 | Agent + RAG Integration | Giving agents access to your RAG as a tool | Combine Week 15 RAG and Week 17 agent — agent uses RAG to answer questions |
| 4 | MCP Basics | Model Context Protocol, why it matters, basic server | Read MCP spec; explore one open-source MCP server |
| **5 (Project)** | **Multi-Agent Research Assistant** | — | **Build:** Researcher (RAG) + Analyst (reasoning) + Writer (output) multi-agent system. Deployed with React UI. **🏆 Portfolio Piece #5** |

---

## Week 19 — Production AI

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | Streaming Responses | SSE (Server-Sent Events) with FastAPI's `StreamingResponse` | Add streaming to one existing project's chat endpoint |
| 2 | WebSocket Streaming | When to use WebSockets vs SSE, bidirectional streams | Build a WebSocket chat with token-by-token streaming |
| 3 | Security: Prompt Injection + PII | Direct/indirect prompt injection, defensive prompts, PII filtering (Presidio) | Test prompt injection attacks on your projects; add guards |
| 4 | Cost + Observability | Token tracking, model routing, LangSmith/Helicone setup | Wire LangSmith into your RAG chatbot; track 100 requests |
| **5 (Project)** | **Production Retrofit** | — | **Build:** Add streaming + guards + cost monitoring to Portfolio Pieces #4 and #5. Document changes in READMEs |

---

## Week 20 — Capstone: Planning + Backend Foundation

> **Project: AI Interview Coach** — A multi-agent system that conducts mock technical interviews, evaluates answers, and provides personalized coaching.

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | Capstone Planning | Requirements gathering, user flows, architecture diagrams | Write 1-page PRD; draw system architecture; create GitHub repo |
| 2 | Database + Auth | User accounts, interview sessions schema, auth flow | Set up FastAPI + Postgres + JWT auth (reuse Week 6 patterns) |
| 3 | RAG: Question Bank | Building a RAG over 1000+ interview questions across topics | Ingest curated question bank (DSA + System Design + Behavioral) |
| 4 | Interviewer Agent | First agent: picks questions, asks them, manages flow | Build the Interviewer agent with LangGraph |
| **5 (Project)** | **Major Build Day** | — | **Build:** Wire auth + question bank + interviewer agent end-to-end. CLI demo working |

---

## Week 21 — Capstone: Agent Architecture

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | Evaluator Agent | LLM-as-judge patterns, rubric-based evaluation | Build Evaluator agent that scores answers on 5 dimensions |
| 2 | Coach Agent | Personalized feedback generation, weakness identification | Build Coach agent that uses Evaluator output |
| 3 | Multi-Agent Orchestration | Supervisor orchestrating Interviewer → Evaluator → Coach | Wire all 3 agents into one LangGraph |
| 4 | Memory + Progress Tracking | Per-user progress, topics covered, weakness trends | Add persistent memory; track user across sessions |
| **5 (Project)** | **Major Build Day** | — | **Build:** Multi-agent system fully operational. Run 3 full mock interviews end-to-end |

---

## Week 22 — Capstone: Frontend + UX

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | React UI Setup | Vite + React + Tailwind, design system, component library | Build login + dashboard shell |
| 2 | Interview Interface | Real-time interview UI, question display, answer input | Build the interview screen with streaming responses |
| 3 | Feedback + Coaching Display | Render evaluator scores + coach feedback nicely | Build the post-interview review screen |
| 4 | Dashboard + Progress | User dashboard showing history, strengths, gaps | Build dashboard with charts (recharts) |
| **5 (Project)** | **Major Build Day** | — | **Build:** Full frontend wired to backend. End-to-end demo recordable |

---

## Week 23 — Capstone: Production + Polish

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | Production Deployment | Docker, Render (backend), Vercel (frontend), env vars | Deploy capstone to production URLs |
| 2 | Cost Monitoring Dashboard | Token tracking per user, cost-per-session, model routing | Build admin dashboard showing usage + costs |
| 3 | Security Hardening | Prompt injection defenses, PII handling, rate limiting | Run security audit; fix any vulnerabilities |
| 4 | Performance | Caching responses, model routing (cheap → expensive), latency | Optimize: target sub-3-sec first-token latency |
| **5 (Project)** | **Major Build Day** | — | **Build:** Production-grade capstone deployed and stress-tested |

---

## Week 24 — Portfolio Finalization + Launch

| Day | Topic | 90 min Learn | 90 min Practice |
|---|---|---|---|
| 1 | README Mastery | Architecture diagrams, demo GIFs, clear setup instructions | Polish READMEs for all 5 portfolio projects |
| 2 | Demo Videos | 60-second product demos, Loom/Riverside basics | Record 1-min demo videos for all 5 projects |
| 3 | GitHub Profile | Profile README, pinned repos, contribution graph optimization | Polish GitHub profile; pin 5 best projects |
| 4 | LinkedIn + Portfolio Site | LinkedIn rewrite for AI engineer roles, simple portfolio site | Update LinkedIn; deploy a simple portfolio site (Vercel) |
| **5 (Project)** | **Capstone Launch** | — | **Build:** Public launch — LinkedIn post, X/Twitter thread, share in AI communities. **🏆 Portfolio Piece #6 — Capstone** |

---

## ✅ End of Phase 2 — What You'll Have

**Skills:**
- Production RAG systems (chunking, hybrid search, re-ranking, evaluation)
- AI agents from scratch + LangGraph orchestration
- Multi-agent systems with real coordination
- Streaming, security, cost optimization
- Full capstone deployed and shippable

**Portfolio (3 new deployed AI projects + 1 capstone):**
4. **RAG Chatbot** (Week 15) — RAG over personal docs with citations
5. **Multi-Agent Research Assistant** (Week 18) — Researcher + Analyst + Writer
6. **Capstone: AI Interview Coach** (Week 24) — Full production multi-agent system

**By end of Week 24, total portfolio:** 6 deployed projects across the full stack — from async clients to production multi-agent systems.

---

## Phase 2 Project Day Philosophy

Every Phase 2 project day directly applies what was just learned. This compounds:

- Week 13 RAG MVP → Week 14 adds production → Week 15 adds UI → **Portfolio Piece #4**
- Week 16 tool agent → Week 17 LangGraph version → Week 18 multi-agent → **Portfolio Piece #5**
- Weeks 20-24 capstone builds incrementally → **Portfolio Piece #6**

No "throwaway practice" — every line of code goes toward shippable work.

---

## Master Rules for Both Phases

1. **Ship rough, ship fast.** A working ugly project beats a beautiful unfinished one. Always.
2. **One topic at a time.** No tutorial hopping. Finish the day's learn → do the day's practice → close everything → next day.
3. **Stuck protocol:** Isolate the specific concept that's blocking → 30 min of focused search/read on JUST that concept → unblock → continue. Don't open a new course.
4. **Weekend reflection (5 min, Saturday):** Check off the week. Note what slipped. Plan adjustments for next week.
5. **Public is better than private.** GitHub from Week 1. Blog from Week 4. LinkedIn from Week 12.

---

*End of complete 24-week tech stack syllabus. DSA and placement preparation are handled separately on Day 5 and Day 6 of each week per your own pacing.*
