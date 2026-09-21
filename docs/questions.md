# The a9fix question battery

The API had no system prompt. Guidance lived in the question text, so the battery was versioned like code. The exact text is in [`config/questions.csv`](../config/questions.csv). This page translates it without replacing it.

## Q1 - pass-through

**Plain language:** did the receiver move the value onward in a pattern that looks like pass-through layering rather than ordinary payment or settlement?

**Eligible when:** at least one forward path exists from the anchor.

**Evidence weighed:** longest-chain retention, elapsed time, branching, endpoint sender history, receiver collection activity and onward settlement. Value loss below 0.5 retention is strong evidence. Intact movement is usually weaker unless the endpoint itself looks like a collection hub.

**Why the gate exists:** with no onward path, the packet cannot establish pass-through. A model score cannot create a missing path.

## Q2 - coordination

**Plain language:** do at least two paths show parties splitting or gathering value together, beyond the account's own ordinary fan-shaped activity?

**Eligible when:** at least two forward paths exist.

**Evidence weighed:** correlated timing, similar split amounts, matching branch structure, retention, endpoint structure, the account's own base rate, 30-180 day precedents and ordinary explanations. A fan or chain alone is weak evidence.

## Q4 - behaviour shift

**Plain language:** is this 24-hour window materially different from the account's own history in a way that history does not explain?

**Eligible when:** always.

**Evidence weighed:** 30-day recurring timing, 30-180 day comparable precedents, history coverage, value retention, speed, branches, destination, counterparty continuity, post-credit dwell and receiver-network behaviour. Size is judged first, character second. Holding funds is not suspicious by itself.

Q4 absorbed two earlier jobs:

- **Q5 counterparty shift** moved into Q4 as counterparty continuity and novelty. First-seen counterparties alone did not separate the classes reliably.
- **Q6 dwell shift** moved into Q4 as post-credit stasis. Dwell alone had flagged 26 innocent savers. It matters only when the credit's source is otherwise unexplained.

## QI - integration

**Plain language:** does the episode look like money entering a legitimate-looking asset or merchant channel?

**Eligibility:** diagnostic only. It never counts.

AMLNet did not provide merchant registry, purpose or source-of-funds evidence. The question explicitly forbids inventing those facts. It stayed available for diagnosis but could not override the narrower mechanisms.

## What happened to Q7?

Q7 asked whether payment-method or currency mix materially shifted. The final packet did not carry enough method or currency-mix evidence to answer it. It was cut instead of being simulated with prose.

## Why the numbering skips

The earlier battery had six scored questions across two families: Q1, Q2, Q4, Q5, Q6 and Q7. No Q3 existed. Fifteen Exp12 amendments merged overlapping jobs and removed the unanswerable one. The final battery has three counting questions plus QI as a diagnostic.

## Frozen combination

```text
final = max(
  Q1 if forward_paths >= 1,
  Q2 if forward_paths >= 2,
  Q4 always
)
QI never counts.
```
