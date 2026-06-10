# RepMind Project Plan

This is a Python-based AI fitness planning project. The goal is to build a practical workout assistant that can use user profile data, workout history, daily check-ins, and exercise knowledge to generate safe and realistic workout plans.

The project starts with a simple manual RAG prototype and later evolves into a multi-agent fitness coach.

# Current Direction

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

## Result : in progress

Add a multi-agent layer on top of the working RAG system.

The current RAG system generates a workout directly from retrieved context. In Phase 2, the system should become more modular, with different agents responsible for different decisions.

This phase is still TODO.



## Phase 2 Idea

Instead of one generation step, the future system may use several specialized agents:

```text
Check-in Analyzer Agent
        ↓
Recovery / Readiness Agent
        ↓
Exercise Selection Agent
        ↓
Workout Planning Agent
        ↓
Safety Review Agent
        ↓
Final Response Agent
```

Each agent would have a clearer responsibility.


## Phase 2 Planned Agents

### 1. Check-in Analyzer Agent

Purpose:

* read today’s check-in
* understand energy level, soreness, sleep, available time, and available equipment
* summarize today’s constraints

Status: TODO

### 2. Recovery / Readiness Agent

Purpose:

* decide whether the user should train hard, train light, or recover
* use soreness and workout history
* reduce volume or intensity when needed

Status: TODO



### 3. Knowledge Retrieval Agent

Purpose:

* decide what information should be retrieved
* build better retrieval queries
* possibly perform multiple retrieval passes

Status: TODO

Current MVP already has a simple version of this, but it is not agentic yet.


### 4. Exercise Selection Agent

Purpose:

* choose exercises based on:

  * goal
  * equipment
  * soreness
  * previous workouts
  * substitutions
* avoid exercises that are not appropriate today

Status: TODO

### 5. Workout Planning Agent

Purpose:

* assemble warm-up, main workout, cooldown, and progression
* make the plan fit the available time
* choose sets, reps, rest, and intensity

Status: TODO


### 6. Safety Review Agent

Purpose:

* inspect the generated workout before showing it to the user
* check for conflicts:

  * sore muscles overloaded
  * unavailable equipment used
  * too much volume
  * unsafe exercise choice
  * mismatch with user level

Status: TODO



### 7. Final Response Agent

Purpose:

* format the final workout plan clearly
* explain why the plan was chosen
* include safety notes
* include RAG sources used

Status: TODO



## Phase 2 Possible Orchestration

Later, this can be implemented with LangGraph or a simpler custom Python orchestration first.

Possible flow:

```text
Input state
   ↓
Analyze check-in
   ↓
Retrieve knowledge
   ↓
Assess recovery
   ↓
Select exercises
   ↓
Build workout
   ↓
Review safety
   ↓
Return final plan
   ↓
Save if accepted
```

A shared state object could hold:

```text
user_profile
workout_history
checkin
retrieved_chunks
readiness_summary
selected_exercises
draft_plan
safety_review
final_plan
```



## Phase 2 Success Criteria

Phase 2 is successful if the system can:

* separate responsibilities across agents
* make the generation process easier to debug
* revise plans when safety issues are detected
* explain which agent made which decision
* keep the RAG retriever reusable
* still support the accept/regenerate/save-to-history loop



# Later Phases

## Phase 3: Better Data Model

Possible improvements:

* structured workout history
* structured generated plans
* exercise IDs
* muscle group tags
* equipment tags
* progression tracking
* completed vs skipped exercises
* user feedback after workout


## Phase 4: Better Storage

Possible improvements:

* move from JSON files to SQLite or PostgreSQL
* store users, workouts, exercises, check-ins, and generated plans separately
* add timestamps and versioning
* track accepted, rejected, and regenerated plans



## Phase 5: Better Retrieval

Possible improvements:

* replace local JSON vector store with a real vector database
* add metadata filtering
* add stale-entry detection
* add incremental indexing
* add hybrid search
* add reranking
* track which sources were used in final answers


## Phase 6: Frontend

Possible improvements:

* simple web UI
* check-in form
* generated workout display
* accept/regenerate buttons
* workout history view
* RAG debug view for development

