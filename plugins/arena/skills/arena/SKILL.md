---
name: arena
description: >-
  Orchestrates multi-expert debates with real-world personas who argue directly
  with each other until convergence. Use when the user wants multiple opposing
  viewpoints, expert panel discussion, or structured debate on a complex
  question. Don't use for quick questions, single-expert analysis,
  implementation planning, or structured thinking without debate.
allowed-tools:
  - TeamCreate
  - TeamDelete
  - SendMessage
  - TaskCreate
  - TaskGet
  - TaskUpdate
  - TaskList
  - Task
  - Read
  - Glob
  - Grep
  - Bash
argument-hint: "<debate question>"
model: opus
---

# Expert Arena — Organic Debate Moderator

The **Moderator** orchestrates an expert arena. The goal: select experts, provide context, and **let them argue among themselves**. The Moderator observes and intervenes only when necessary.

**Key principle:** Experts communicate DIRECTLY with each other via SendMessage. The Moderator does NOT relay messages. The Moderator does NOT manage rounds. Experts argue until they reach common ground themselves.

Works for ANY domain: development, product, strategy, business, science, philosophy.

---

## PHASE 0: Question Analysis and Expert Selection

### Step 1: Understand the Question

Determine:
- **Domain(s):** What field does the question belong to? (may span multiple)
- **Decision type:** Technical, strategic, architectural, product, ethical?
- **Stakes:** What are the consequences of a wrong decision?

### Step 2: Select 3-5 Experts

**Aim for 5.** Fewer only if the domain is narrow.

See `references/expert-selection-guide.md` for the full selection criteria (diversity requirements, angle types, Devil's Advocate) and arena presentation template.

### Step 3: Present the Arena to the User

Show the user: Arena Question, Expert Panel table, Devil's Advocate designation. See the template in `references/expert-selection-guide.md`.

---

## PHASE 1: Research (one-shot agents)

> "The Arena is preparing. Gathering context for the debates... 🏟️"

Launch 2-4 `arena:researcher` agents **IN PARALLEL** in a single message. These are one-shot agents — they are NOT part of the team.

### For code/development questions:

```
Researcher 1: "Study the project architecture, stack, and existing patterns.
QUESTION CONTEXT: [question]
FOCUS: Code structure, key modules, dependencies."

Researcher 2: "Find current best practices and expert opinions.
QUESTION CONTEXT: [question]
FOCUS: Via WebSearch — recent articles, discussions, approach comparisons."

Researcher 3: "Analyze constraints and tech debt.
QUESTION CONTEXT: [question]
FOCUS: Existing solutions, dependencies, potential conflicts."
```

### For non-technical questions:

```
Researcher 1: "Find current data, statistics, and trends."
Researcher 2: "Find expert positions and notable debates on the topic."
Researcher 3: "Find case studies, precedents, and real-world examples."
```

### For mixed questions: combine both sets, 3-4 agents.

---

## PHASE 2: Launching the Arena

### Step 1: Compile the Briefing

Once the researchers return, compile findings into a unified briefing package:

```
## Arena Briefing

### Project Context (if applicable)
[From Researcher 1]

### Current Data and Practices
[From Researcher 2]

### Constraints and Precedents
[From Researcher 3]
```

### Step 2: Create the Team

```
TeamCreate(team_name="arena-<topic-slug>")
```

### Step 3: Launch ALL Experts IN PARALLEL

> "Context gathered. Releasing the experts into the arena ⚔️"

Launch all experts **in a single message** — each receives a full init prompt:

```
Task(
  subagent_type="arena:expert",
  team_name="arena-<topic-slug>",
  name="<expert-slug>",
  prompt="# You are [Full Name]

## Your Persona
[Description: books, principles, characteristic style. 3-5 sentences]
[If Devil's Advocate — specify the special role and VETO right]

## Debate Question
[Full question statement]

## Briefing
[Compiled briefing package — IN FULL]

## Other Participants
- **[slug-1]** — [Name 1] ([angle]): [expected position]
- **[slug-2]** — [Name 2] ([angle]): [expected position]
...

## Begin!
1. Broadcast your position to ALL participants
2. Then argue directly with those you disagree with
3. When you believe common ground has been reached — notify team-lead"
)
```

**Names (slug):** lowercase Latin with hyphens: `martin-fowler`, `dhh`, `nassim-taleb`

---

## PHASE 3: Observing the Debates

### What happens automatically:

Experts on their own:
1. **Broadcast** initial positions
2. **Challenge** specific experts via direct messages
3. **Respond** to received challenges
4. **Shift positions** when persuaded
5. **Signal** convergence (send final position to team-lead)

### What the Moderator sees:

- **Direct messages to the Moderator** — positions, convergence signals
- **Peer DM summaries** — idle notifications briefly showing who wrote what to whom
- **Idle notifications** — when an expert goes silent

### When to INTERVENE:

| Situation | Action |
|-----------|--------|
| Expert silent for too long | `SendMessage(recipient="slug", content="You haven't weighed in on [X] yet. What do you think?")` |
| Argument drifted off-topic | `SendMessage(type="broadcast", content="Let's return to the question: [X]")` |
| Two experts stuck in a loop | `SendMessage(recipient="third-slug", content="Arbitrate the dispute between A and B on [X]")` |
| No progress toward convergence | `SendMessage(type="broadcast", content="Provide an interim summary. Where do you agree? Where do you disagree?")` |
| More than 15 minutes elapsed | `SendMessage(type="broadcast", content="Time's up. Send your final positions to team-lead")` |

### When NOT to intervene:

- Experts are actively debating — **do not intervene**
- Someone shifted their position — that is progress
- The argument got heated — that is normal and productive
- One expert dominates — others will respond on their own

### Live Commentary — Make the Debates Spectacular

When significant debate events occur, provide real-time commentary for the user.

See `references/live-commentary-rules.md` for the full commentary protocol (sources, event types, format, tone).

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Researcher fails in Phase 1 | Proceed with reduced briefing. Experts receive less context but can still debate. |
| Expert agent fails to spawn | Proceed with N-1 experts. Minimum 2 experts required for meaningful debate. If fewer than 2, report failure. |
| Expert goes silent after spawning | Send nudge via SendMessage. If no response after 2 nudges, proceed without that expert. |
| No convergence after 20 minutes | Broadcast timeout. Request final positions. Compile synthesis from available positions. |
| SendMessage fails | Retry once. If still fails, note communication gap and proceed with available data. |

---

## PHASE 4: Convergence

### Convergence decision tree:

```mermaid
flowchart TD
    FP{"3+ of N experts<br/>submitted final positions?"}
    FP -->|YES| VETO{"VETO active?"}
    FP -->|NO| IDLE{"All experts idle?"}
    IDLE -->|YES| BCAST["Broadcast: Submit final positions"]
    BCAST --> WAIT5["Wait 5 min"] --> SYNTH
    IDLE -->|NO| TIMEOUT{">20 min of active debate?"}
    TIMEOUT -->|YES| TO_BCAST["Broadcast timeout<br/>Request final positions"] --> SYNTH
    TIMEOUT -->|NO| MON["Continue monitoring"]

    VETO -->|NO| SYNTH["Proceed to Synthesis"]
    VETO -->|YES| V_BCAST["Broadcast VETO to all<br/>Wait for responses"]
    V_BCAST --> V_CHECK{"VETO withdrawn?"}
    V_CHECK -->|YES| SYNTH
    V_CHECK -->|NO| DISAGREE["Record disagreement<br/>in synthesis"] --> SYNTH
```

---

## PHASE 5: Synthesis

When the debates are concluded:

### Step 1: Create the Final Document

Compile the synthesis document using the template from `references/synthesis-template.md`.

Save the document to `docs/arena/YYYY-MM-DD-[topic-brief].md`

### Step 2: Shut Down the Team

```
SendMessage(type="shutdown_request", recipient="<slug-1>", content="Arena concluded!")
SendMessage(type="shutdown_request", recipient="<slug-2>", content="Arena concluded!")
...
```

Wait for confirmations, then: `TeamDelete()`

### Step 3: Report the Result

> "Arena concluded. Results saved to `docs/arena/...`.
> Would you like to dive deeper into any aspect, or shall we move to action?"
