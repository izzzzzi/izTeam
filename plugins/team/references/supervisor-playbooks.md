# Supervisor Event Handling Playbooks

> Detailed playbooks for each event type the Supervisor handles.

## 1) Idle / No-response

Trigger: no activity beyond role SLA, missed review response window.

1. Send gentle ping.
2. If still silent, send progress nudge with one concrete next step.
3. Escalate to Lead with evidence (`who`, `task`, `elapsed`, `stage`).
4. Propose replacement/reassignment when threshold is reached.

## 2) Review Loop

Trigger: same major issue repeated across 3+ rounds, `IN_PROGRESS ↔ IN_REVIEW` churn.

1. Mark task `LOOP_SUSPECTED` in state.
2. Quarantine operationally (do not freeze unrelated tasks).
3. Summarize repeated blocker pattern for Lead.
4. Recommend: clarify acceptance criteria, swap owner, or schedule Tech Lead checkpoint.

## 3) Duplicate / Overlap Work

Trigger: double-claim on same task, overlapping file scope across active coders.

1. Mark `DUPLICATE_TASK_KEY` or `OVERLAP_SCOPE`.
2. Freeze conflicting claims in state.
3. Notify Lead with canonical owner recommendation.
4. Resume only one owner path after arbitration.

## 4) Reassignment Readiness

Trigger: `STUCK` after 2 attempts, repeated no-response, capability mismatch.

1. Collect concise evidence from state and recent messages.
2. Suggest reassignment strategy (same role replacement, split task, specialist routing).
3. Update state after Lead decision and publish new ownership map.

## 5) Tool Unavailability

Trigger: agent reports MCP tool not found/erroring, researcher fails on unavailable tool, coder reports missing dependency.

1. Record `TOOL_UNAVAILABLE` in state.md with: tool name, agent name, task ID, timestamp.
2. Route to Lead with decision request: skip / retry / proceed with caveat.
3. If same tool fails for 3+ agents → escalate as systemic issue.
4. Track resolution for post-mortem health summary.

## 6) Teardown Readiness

FSM: `TEARDOWN_INIT` → `SHUTDOWN_REQUESTED` → `WAITING_ACKS` → `RETRYING` → `READY_TO_DELETE`
Terminal: `TEAM_DELETED` or `TEARDOWN_FAILED_SAFE`

Retry constants: `ACK_RETRY_ROUNDS=3`, `ACK_RETRY_TIMEOUT_SEC=60`.

**Normal path:** Verify preconditions (no active non-terminal tasks, state.md consistent, summaries persisted, full roster ACK) → `READY_TO_DELETE`.

**Forced-finalize path:** Run `ACK_RETRY_ROUNDS` retries → verify forced-finalize preconditions → emit `FORCED_FINALIZE_CANDIDATE` → require Lead `FORCED_FINALIZE_ACK` → freeze writes, persist teardown report, mark unresolved ACKs → `READY_TO_DELETE`. No ACK → `TEARDOWN_FAILED_SAFE`.

## Secret Hygiene

Never ask for, copy, or store secrets. Redact as `[REDACTED_SECRET]` immediately. Operational reports include only minimal orchestration metadata.
