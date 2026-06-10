# RepMind Project Plan

This is a Python-based AI fitness planning project. The goal is to build a practical workout assistant that can use user profile data, workout history, daily check-ins, and exercise knowledge to generate safe and realistic workout plans.

The project starts with a simple manual RAG prototype and later evolves into a multi-agent fitness coach.

# Current Direction

RAG is knowledge. Memory is personalization. Agents are workflow. State is the temporary working document passed through that workflow.

RAG knowledge:
"General training rules, recovery rules, exercise substitutions, warm-up advice"

Memory:
"This specific user tends to get sore after lower body, prefers dumbbells, pull-ups are hard, rows feel good at 20 kg"

Agents:
"Separate steps that analyze, retrieve, plan, validate, and format"

State:
"The current request being processed, plus everything agents discovered along the way"

```text
                  ┌────────────────────┐
                  │ User check-in       │
                  │ time, energy, sore  │
                  │ equipment, notes    │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ LangGraph State     │
                  │ temporary dict      │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Memory Agent        │
                  │ loads profile,      │
                  │ history, summary    │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ RAG Agent           │
                  │ retrieves knowledge │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Planner Agent       │
                  │ generates workout   │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Final workout plan  │
                  └─────────┬──────────┘
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
      User accepts                    User rejects
             │                             │
             ▼                             ▼
 ┌────────────────────┐          ┌────────────────────┐
 │ Save workout        │          │ Regenerate or quit  │
 │ to history          │          │ for now no memory    │
 └─────────┬──────────┘          └────────────────────┘
           │
           ▼
 ┌────────────────────┐
 │ Update memory       │
 │ summary with LLM    │
 └────────────────────┘
 ```

The first version is intentionally simple.

Instead of starting with a full production vector database or complex orchestration, the MVP focuses on proving that the core loop works:

```text
User profile + workout history + daily check-in
        ↓
Retrieve relevant fitness knowledge
        ↓
Generate workout plan
        ↓
User accepts or regenerates
        ↓
Accepted plan is saved to workout history
```

Chroma was originally considered for the vector database, but it did not work on the current macOS setup because of dependency/platform issues. For the MVP, the project uses a very manual local vector store instead.

This means:

* embeddings are generated with Gemini
* vectors are stored in a local JSON file
* retrieval is done with NumPy cosine similarity
* no optimized vector database indexing is used yet
* this is acceptable for a small MVP knowledge base



# Phase 1: Manual RAG MVP

## Goal

Build a working prototype that can generate a workout plan using:

* demo user profile
* workout history
* daily check-in
* local exercise/programming knowledge
* Gemini embeddings
* Gemini generation model
* local JSON-based vector store

This phase is not about perfect architecture. It is about proving that the system can retrieve useful context and generate a reasonable workout.

## Result : Done

## Phase 1 Data

The current knowledge base includes pre-generated markdown files such as:

```text
01_recovery_rules.md
02_training_goals.md
03_dumbbell_exercises.md
04_bodyweight_exercises.md
05_warmup_cooldown.md
06_exercise_substitutions.md
```

The app also uses demo user data:

```text
demo_user.json
workout_history.json
```

The workout history contains previous workouts, exercises, loads, and notes. This helps the generator avoid creating plans in isolation.


## Phase 1 Workflow

```text
Markdown knowledge files
        ↓
Chunk by headings
        ↓
Generate embeddings with Gemini
        ↓
Save local vector store as JSON
        ↓

Daily check-in + user profile + recent workout history
        ↓
Build retrieval query
        ↓
Embed retrieval query
        ↓
Compare query vector with stored chunk vectors
        ↓
Retrieve top-k most similar chunks
        ↓
Build generation prompt
        ↓
Generate workout plan with Gemini
        ↓
Save generated workout candidate
        ↓
User accepts or regenerates
        ↓
If accepted, append workout to workout_history.json
```


## Phase 1 Implemented

The following parts are already done or currently being implemented:

* Python project setup with `uv`
* local project structure
* markdown-based exercise knowledge files
* demo user profile
* demo workout history
* Gemini API integration
* embedding generation
* local JSON vector store
* heading-based chunking
* retrieval query construction
* query embedding
* NumPy cosine similarity search
* top-k chunk retrieval
* Gemini-based workout generation
* RAG debug printing
* saving generated workout plans as markdown
* saving RAG debug output separately
* user choice flow:

  * accept workout
  * regenerate workout
  * quit without saving
* appending accepted workout plans to `workout_history.json`



## Phase 1 Current Limitations

This MVP is intentionally manual and simple.

Current limitations:

* no production vector database
* no optimized indexing
* no metadata filtering
* no stale-entry detection
* no automatic detection that knowledge files changed
* embeddings must be regenerated manually after knowledge changes
* generated workouts are mostly saved as text, not fully structured exercise objects
* no frontend yet
* no database yet
* no user authentication
* no real multi-user support
* no agent orchestration yet

Important note:

When new knowledge is added or existing markdown knowledge changes, the vector store must be rebuilt manually.

For now:

```text
Change knowledge file
        ↓
Rerun embedding/vector store builder
        ↓
New vector_store.json is created
```

There is currently no label or flag showing that a vector store entry is stale.



# Phase 2: Multi-Agent Orchestration

## Goal

**Status: in progress**

Add a simple LangGraph-based agent workflow on top of the existing RAG system.

The goal of this phase is not to build a complex agent system immediately.
The goal is to separate the current logic into clear steps:

```text
Memory → RAG → Planner
```

This gives the project a clean foundation for adding more agents later.

---

## Core Idea

The current RAG system already works.

Phase 2 keeps that logic, but organizes it into agents connected by LangGraph.

```text
RAG      = general fitness knowledge
Memory   = user-specific personalization
Agents   = workflow steps
State    = temporary object passed between agents
```

Agents read from state, add their result, and pass the updated state to the next agent.

---

## Current Phase 2 Workflow

```text
User check-in
   ↓
LangGraph state
   ↓
Memory Agent
   ↓
RAG Agent
   ↓
Planner Agent
   ↓
Generated workout plan
   ↓
User accepts / regenerates / quits
   ↓
If accepted:
   - save workout to workout_history.json
   - update memory_summary.md
```

---

## Workflow Diagram

```text
┌────────────────────┐
│ User check-in       │
│ time, energy, sore  │
│ equipment, notes    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ WorkoutState        │
│ temporary state     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Memory Agent        │
│ loads profile,      │
│ history, memory     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ RAG Agent           │
│ builds query and    │
│ retrieves chunks    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Planner Agent       │
│ calls Gemini and    │
│ creates workout     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Workout candidate   │
│ saved as markdown   │
│ + RAG debug files   │
└─────────┬──────────┘
          │
          ▼
┌──────────────────────────────┐
│ User choice                  │
│ y = accept / save             │
│ r = regenerate                │
│ q = quit                      │
└─────────┬────────────────────┘
          │
          ▼
┌────────────────────┐
│ If accepted:        │
│ save to history     │
│ update memory       │
└────────────────────┘
```

---

## Phase 2.1 Shared State

Current minimal state:

```python
class WorkoutState(TypedDict, total=False):
    checkin: Dict[str, Any]

    user_profile: Dict[str, Any]
    workout_history: List[Dict[str, Any]]
    memory_summary: str

    retrieval_query: str
    retrieved_knowledge: List[Dict[str, Any]]

    workout_plan: str
```

### Current fields

| Field                 | Purpose                        |
| --------------------- | ------------------------------ |
| `checkin`             | Today’s workout context        |
| `user_profile`        | Goal, level, preferences       |
| `workout_history`     | Recent completed workouts      |
| `memory_summary`      | Long-term user personalization |
| `retrieval_query`     | Query sent to the retriever    |
| `retrieved_knowledge` | RAG chunks used for planning   |
| `workout_plan`        | Generated workout output       |

### Later fields

| Field                 | Use later                   |
| --------------------- | --------------------------- |
| `run_id`              | Better file/debug tracking  |
| `user_id`             | Multi-user support          |
| `readiness_summary`   | Recovery/readiness decision |
| `draft_plan`          | Structured internal plan    |
| `validation_feedback` | Safety review results       |
| `is_valid`            | Validator result            |
| `should_regenerate`   | Conditional graph routing   |
| `errors` / `warnings` | Debugging and observability |

---

## Phase 2.2 Current Agents

### 1. Memory Agent

**Status: implemented / in progress**

Purpose:

* load `demo_user.json`
* load `workout_history.json`
* load `memory_summary.md`
* write them into `WorkoutState`

The Memory Agent does not update memory.
It only loads existing user context before planning.

---

### 2. RAG Agent

**Status: implemented / in progress**

Purpose:

* build a retrieval query from:

  * check-in
  * user profile
  * workout history
  * memory summary
* retrieve top relevant knowledge chunks
* write `retrieval_query` and `retrieved_knowledge` into state

This reuses the current local JSON + NumPy retriever.

---

### 3. Planner Agent

**Status: implemented / in progress**

Purpose:

* receive:

  * check-in
  * user profile
  * recent workout history
  * memory summary
  * retrieved RAG chunks
* call Gemini
* generate the workout plan
* write `workout_plan` into state

---

## Phase 2.3 LangGraph Workflow

Current graph:

```text
START
  ↓
memory
  ↓
rag
  ↓
planner
  ↓
END
```

Implemented in:

```text
app/workflows/workout_graph.py
```

The CLI runner lives in:

```text
app/workflows/run_workout.py
```

The CLI runner handles:

```text
generate → show plan → ask y/r/q
```

LangGraph handles only the generation flow for now.

---

## Phase 2.4 Memory Update

Memory update happens after the graph finishes.

It is not part of the graph yet.

```text
Workout generated
   ↓
User accepts
   ↓
Append workout to workout_history.json
   ↓
Call Gemini to update memory_summary.md
```

The memory updater receives:

```text
old memory summary
new accepted workout log
user feedback
```

It returns an updated compact memory summary.

Memory should contain only useful long-term information:

* stable preferences
* disliked exercises
* useful working weights
* recurring soreness patterns
* recovery patterns
* constraints that affect future planning

It should not store every detail from every workout.

---

## Phase 2.5 Current File Structure

```text
app/
  agents/
    state.py
    memory_agent.py
    rag_agent.py
    planner_agent.py

  workflows/
    workout_graph.py
    run_workout.py

  memory/
    memory_store.py
    memory_updater.py

  rag/
    retriever.py
    build_vector_store.py

  data/
    demo_user.json
    workout_history.json
    memory_summary.md
    vector_store.json
    generated_workouts/
```

---

## Phase 2.6 Current User Loop

```text
Generate workout candidate
   ↓
Save candidate files:
- workout_plan.md
- rag_debug.md
- rag_debug.json
- checkin.json
   ↓
Ask user:
- y = accept
- r = regenerate
- q = quit
   ↓
If y:
- append to workout_history.json
- update memory_summary.md
- mark candidate folder as accepted
```

Rejected or regenerated workouts are kept only as generated artifacts for now.
They are not used for future planning yet.

Later, rejected workouts can be stored with rejection reasons and used as feedback.

---

## Planned Future Agents

These are not implemented yet.

### Intake Agent

Purpose:

* normalize today’s check-in
* summarize constraints

Status: TODO

---

### Readiness Agent

Purpose:

* decide training intensity for today
* use soreness, history, and memory
* produce a readiness summary

Status: TODO

---

### Exercise Selection Agent

Purpose:

* choose exercises based on goal, soreness, equipment, and history
* avoid inappropriate exercises

Status: TODO

---

### Safety Validator Agent

Purpose:

* check if the plan violates constraints
* detect sore-muscle overload
* detect unavailable equipment
* detect unrealistic volume

Status: TODO

---

### Coach Response Agent

Purpose:

* format the final response
* explain reasoning
* include safety notes and sources

Status: TODO

---

## Future Graph Direction

Later graph:

```text
START
  ↓
intake
  ↓
memory
  ↓
rag
  ↓
readiness
  ↓
planner
  ↓
safety_validator
  ↓
coach_response
  ↓
END
```

Later conditional routing:

```text
planner
   ↓
safety_validator
   ↓
if valid: coach_response
if invalid: planner again
```

---

## Phase 2 Success Criteria

Phase 2 is successful when:

* the generation flow runs through LangGraph
* memory, RAG, and planning are separate agents
* the shared state is easy to inspect
* generated candidates are saved
* accepted workouts are saved to history
* memory summary is updated after acceptance
* the system is ready for readiness and safety agents later

---

## Current Summary

Current implemented direction:

```text
check-in
   ↓
memory_agent
   ↓
rag_agent
   ↓
planner_agent
   ↓
workout plan
   ↓
accept / regenerate / quit
   ↓
if accepted: save history + update memory
```

This is the first simple multi-agent version.
