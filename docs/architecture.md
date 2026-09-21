# Architecture: one transaction through the system

This follows `amlnet-case-1082242` from source row to audit. Facts unavailable in the preserved source are called out rather than filled in.

## 1. Anchor

Recorded anchor: `amlnet-row-1082242`, 5 August 2025 at 13:20:46, C3501 to C5105, AUD 13,094.95, transfer. The source print cut the category off mid-value, so the exact anchor category is not recorded.

## 2. Packet

The private experiment builder did not send the row alone. It assembled:

1. anchor transaction;
2. 24-hour current window;
3. 30-day baseline;
4. forward paths up to two hops;
5. 30-180 day extended baseline;
6. ordinary-explanation precedents;
7. network, retention, stasis and sufficiency facts where available.

For this case the current window had two transactions, AUD 13,591.27 in total, and no forward path from C5105. The baseline covered 185 days in the preserved packet excerpt. The exact complete baseline and extended baseline were truncated in the source print and remain marked that way in the sample.

## 3. Request

```json
{
  "model": "jev-1.13.0",
  "state": "...complete episode packet as text...",
  "questions": {
    "Q1_pass_through": {"answer_type": "noul", "question": "..."},
    "Q2_coordination": {"answer_type": "noul", "question": "..."},
    "Q4_velocity_shift": {"answer_type": "noul", "question": "..."},
    "QI_integration": {"answer_type": "noul", "question": "..."}
  }
}
```

There was no system prompt. Jev was stateless and returned one unit-interval probability per question. Observed latency was usually about 100-350 ms per case.

## 4. Gates

- Zero paths means Q1 is ineligible.
- Zero paths means Q2 is ineligible.
- Q4 is always eligible.
- QI never counts.

The raw result records Q1 at 0.18, Q2 at 0.13, Q4 at 0.70 and QI at 0.11. Code excluded Q1 and Q2 as ineligible because the case had zero paths. QI was returned but remained diagnostic-only. Only Q4 counted.

## 5. Combiner

```text
eligible = {Q4: 0.70}
final = max(eligible) = 0.70
0.70 >= 0.65 => caught
```

At 0.75 it is a near-miss. The evidence does not change when the threshold changes.

## 6. Sealed-label audit

The evaluation order was: select case with a fixed salt, build packet, send frozen questions, store answers, apply gates and combiner, then open the label. The opened label was a planted AMLNet laundering positive, described in the preserved walkthrough as a collection account / zero-path dormant receiver.

## 7. Ownership

| Layer | Owns |
|---|---|
| Code | case selection, hashes, windows, paths, counts, ratios, missingness, gates, combination |
| Jev | one probability per supplied question |
| Human | investigation, external context, explanation, disposition and action |

The model does not browse, fetch KYC, remember cases or decide whether a customer is guilty.
