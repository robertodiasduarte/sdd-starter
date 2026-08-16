<!--
CANONICAL OUTPUT ASSET — SDD Brainstorm by RDD
Use this file as the structural source of truth for the final Brainstorm.
Replace placeholders in {BRACES}, remove optional sections that do not apply,
and preserve section order/titles unless the user explicitly requests otherwise.
-->

# BRAINSTORM: {Feature Name}

> Exploratory session to clarify intent and approach before requirements capture

## Metadata

| Attribute | Value |
|---|---|
| Feature | {FEATURE_NAME} |
| Date | {YYYY-MM-DD} |
| Author | brainstorm-agent |
| Status | Exploring / Approaches Identified / Handoff Ready |

## Initial Idea

**Raw Input:** {original user wording}

**Context Gathered:**
- {verified/provided context}
- {verified/provided context}

**Technical Context Observed (for Define):**

| Aspect | Observation | Implication |
|---|---|---|
| Likely Location | {path or N/A} | {impact} |
| Relevant KB Domains | {domains or N/A} | {impact} |
| IaC Patterns | {observation or N/A} | {impact} |

## Discovery Questions & Answers

| # | Question | Answer | Impact |
|---|---|---|---|
| 1 | {question} | {answer} | {impact} |
| 2 | {question} | {answer} | {impact} |
| 3 | {question} | {answer} | {impact} |

Record at least 3 discovery answers before approaches.

## Sample Data Inventory

| Type | Location | Count | Notes |
|---|---|---:|---|
| Input files | {path or N/A} | {N} | {notes} |
| Output examples | {path or N/A} | {N} | {notes} |
| Ground truth | {path or N/A} | {N} | {notes} |
| Related code | {path or N/A} | {N} | {notes} |

**How samples will be used:**
- {usage or N/A}

## Approaches Explored

### Approach A: {Name} — Recommended

**Description:** {description}

**Pros:**
- {pro}
- {pro}

**Cons:**
- {trade-off}
- {trade-off}

**Why Recommended:** {reason}

### Approach B: {Name}

**Description:** {description}

**Pros:**
- {pro}

**Cons:**
- {trade-off}

### Approach C: {Name} (Optional)

{Include only when it is meaningfully distinct.}

## Selected Approach

| Attribute | Value |
|---|---|
| Chosen | Approach {A/B/C or named hybrid} |
| User Confirmation | {date/time or conversational confirmation} |
| Reasoning | {why this direction was selected} |

## Key Decisions Made

| # | Decision | Rationale | Alternative Rejected |
|---|---|---|---|
| 1 | {decision} | {why} | {alternative} |

## Features Removed (YAGNI)

| Feature Suggested | Reason Removed/Deferred | Can Add Later? |
|---|---|---|
| {item or "None identified"} | {reason} | Yes/No/N/A |

## Incremental Validations

| Section | Presented | User Feedback | Adjusted? |
|---|---|---|---|
| {checkpoint 1} | Yes | {feedback} | Yes/No |
| {checkpoint 2} | Yes | {feedback} | Yes/No |

## Suggested Requirements for /define

### Problem Statement (Draft)

{one clear sentence supported by the conversation}

### Target Users (Draft)

| User | Pain Point |
|---|---|
| {user} | {pain} |

### Success Criteria (Draft)

- [ ] {measurable criterion if supported}
- [ ] {criterion or explicit TBD}

### Constraints Identified

- {constraint}

### Out of Scope (Confirmed)

- {excluded/deferred item}

## Session Summary

| Metric | Value |
|---|---:|
| Questions Asked | {N} |
| Approaches Explored | {N} |
| Features Removed (YAGNI) | {N} |
| Validations Completed | {N} |

## Next Step

Execute o **SDD Define by RDD**.
