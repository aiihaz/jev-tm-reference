# I made a transaction-monitoring judge explain itself

I started with a simple question: can a typed judgment model help rank transaction-monitoring cases without pretending to be the investigator?

The first version looked good on a small sample. It did not survive a real batch. I kept the failures in the record, rebuilt the evidence packet, split one broad score into narrow questions, and put every hard boundary back in code.

This repo is the result: a small, replaceable reference implementation of the final **Exp12 a9fix** design.

> **Read this first:** this is a clean public reference implementation built from the frozen design documents. It is not the original private experiment repository and does not claim byte-for-byte identity with the original packet builder. The frozen question text, combiner, running case and reported measurements are preserved. Fields absent from the source record stay `not recorded`.

## The whole idea in one diagram

```text
raw transactions
      |
      v
code builds a bounded episode packet
(anchor + 24h window + 30d baseline + paths + 30-180d precedents)
      |
      v
Jev returns one probability per question
      |
      v
code applies eligibility gates and max combiner
      |
      v
sealed labels open for evaluation / a human owns disposition
```

**Code owns facts and gates. Jev weighs supplied evidence. Humans own the final call.**

## What held up

On the frozen 1,000 cases, 500 planted laundering and 500 normal:

| Version | Strict point: caught | Strict point: false flags | Loose point: caught | Loose point: false flags |
|---|---:|---:|---:|---:|
| Exp9 | 430 | 192 | 481 | 302 |
| Exp10 | 105 | 19 | 341 | 130 |
| Exp10b | 135 | 27 | 436 | 156 |
| Exp11 | 160 | 0 | 383 | 133 |
| **a9fix** | **202** | **0** | **426** | **68** |

Those points compare the recorded strict and loose thresholds, not one universal threshold. a9fix beat the earlier lines at each recorded point. Across three fresh 500-case draws, the final catch-first operating point produced **681/750 caught (90.8%)** and **204/750 false flags (27.2%)**. Traditional logistic regression did better on this synthetic corpus. That is part of the result, not a footnote.

The evaluation made over **13,900 verified successful calls**, used roughly **$4 of a $5 monthly credit**, and tested **15 Exp12 wording amendments**. An independent repeat produced **0.992 rank correlation** and the same top 50, **50 for 50**.

This does not prove production AML accuracy. AMLNet is synthetic, and the remaining separation problem was mostly missing context: KYC/KYB, purpose, merchant registries and relationship history.

## Try it

Requires Python 3.10+ and your own TypeSafe API key.

```bash
git clone https://github.com/aiihaz/jev-tm-reference.git
cd jev-tm-reference
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run the included case offline through the frozen combiner:

```bash
jev-tm examples/amlnet-case-1082242.json \
  --scores examples/scores-amlnet-case-1082242.json
```

Expected result: only Q4 is eligible, the final score is `0.70`, and the case crosses the frozen `0.65` operating point.

To call Jev with your own key:

```bash
export TYPESAFE_API_KEY='your-key'
jev-tm examples/amlnet-case-1082242.json --call
```

No key is included. `.env` and result directories are ignored.

## Replace any part without touching the engine

| Change | Edit |
|---|---|
| Questions and verbatim guidance | [`config/questions.csv`](config/questions.csv) |
| Eligibility gates, threshold or max combiner | [`config/combiner.json`](config/combiner.json) |
| Windows, baseline ranges, max hops or packet sections | [`config/packet_schema.json`](config/packet_schema.json) |
| Input packet | any JSON matching your chosen schema |

The engine reads these files at runtime. Fork it, change one file, rerun, and keep the changed config with the result.

## The questions

- **Q1 pass-through** asks whether value moves onward with suspicious loss, speed, branching or hub-like endpoints. It counts only when at least one forward path exists.
- **Q2 coordination** asks whether multiple visible paths look deliberately coordinated rather than like ordinary fans, chains or settlement. It counts only with at least two paths.
- **Q4 behaviour shift** asks whether the current 24-hour window is a material, unexplained departure from the account's own history. It is always eligible.
- **QI integration** asks whether money appears to enter a legitimate-looking asset or merchant channel. It is diagnostic only and never changes the final score.

Two former standalone questions are still part of the design history. **Q5 counterparty shift** asked whether the counterparty pattern materially broke from prior history; it was folded into Q4 as counterparty continuity and novelty. **Q6 dwell shift** asked whether retention or onward-transfer behaviour departed from baseline; it was folded into Q4 as `post_credit_stasis`. **Q7 mode shift** was cut entirely because the final packet did not carry the payment-method or currency-mix data needed to answer it.

Read [the question guide](docs/questions.md) for the exact former Q5 and Q6 wording, what happened to each one, and the full six-to-three story.

## One real case

The included `amlnet-case-1082242` is a planted AMLNet positive. C3501 sent AUD 13,094.95 to C5105. No onward path was visible. That made Q1 and Q2 ineligible. Q4 scored the collection-then-silence pattern at 0.70. Code kept only Q4:

```text
max(Q4 = 0.70) = 0.70 >= 0.65
```

It was caught at the final operating point and would have been a near-miss at 0.75. Returned values for ineligible Q1, Q2 and diagnostic QI were not recorded, so this repo does not invent them.

Walk the case end to end in [`docs/architecture.md`](docs/architecture.md).

## Repository map

```text
config/                 frozen questions, gates, packet boundaries
src/jev_tm/              reference packet builder, API client, combiner, CLI
examples/                one source-grounded packet and offline score
scripts/                 batch runner
reports/                 reported measurement table, no secret raw trail
docs/                    architecture and question guide
tests/                   gate and combiner tests
```

## Limits

- Synthetic labels are generator truth, not bank adjudications.
- The reference packet builder is intentionally small and readable. It marks evidence it cannot derive as `not recorded`.
- Jev emits probabilities, not an investigation narrative.
- A high score is a ranking signal, not a disposition.
- The public reference excludes private history, secrets and internal working files.

## License

MIT. Use it, replace the battery, test it on better data, and publish what breaks.
