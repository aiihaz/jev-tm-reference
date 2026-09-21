"""Config-driven reference packet builder.

The original Exp12 code is not published here. This clean implementation makes the
recorded packet boundaries executable without claiming byte-for-byte identity.
"""
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from statistics import median

TS = "%Y-%m-%dT%H:%M:%S"

def dt(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def amount(row):
    return float(row.get("amount", 0) or 0)

def summarize(rows, subject):
    values = [amount(r) for r in rows]
    inbound = sum(amount(r) for r in rows if r.get("receiver_id") == subject)
    outbound = sum(amount(r) for r in rows if r.get("sender_id") == subject)
    parties = {r.get("sender_id") if r.get("receiver_id") == subject else r.get("receiver_id") for r in rows}
    return {"transaction_count": len(rows), "value": sum(values), "inbound_value": inbound,
            "outbound_value": outbound, "onward_ratio": outbound / inbound if inbound else None,
            "counterparty_count": len(parties),
            "payment_mix": dict(Counter(r.get("payment_type", "not recorded") for r in rows)),
            "category_mix": dict(Counter(r.get("category", "not recorded") for r in rows))}

def forward_paths(rows, receiver, anchor_time, end_time, hops=2):
    later = sorted((r for r in rows if anchor_time <= dt(r["timestamp"]) <= end_time), key=lambda r: dt(r["timestamp"]))
    paths = []
    def walk(node, after, path, depth):
        if depth == 0: return
        for r in later:
            t = dt(r["timestamp"])
            if r.get("sender_id") == node and t >= after and r not in path:
                new = path + [r]
                paths.append(new)
                walk(r.get("receiver_id"), t, new, depth - 1)
    walk(receiver, anchor_time, [], hops)
    return [[r.get("transaction_id", r.get("source_row_id")) for r in p] for p in paths]

def build_packet(anchor, transactions, cfg):
    at = dt(anchor["timestamp"]); subject = anchor["sender_id"]; receiver = anchor["receiver_id"]
    window_start = at - timedelta(hours=cfg["anchor_window_hours"])
    baseline_start = at - timedelta(days=cfg["baseline_days"])
    extended_start = at - timedelta(days=cfg["extended_baseline_end_days"])
    extended_end = at - timedelta(days=cfg["extended_baseline_start_days"])
    current_rows = [r for r in transactions if window_start <= dt(r["timestamp"]) <= at and subject in (r.get("sender_id"), r.get("receiver_id"))]
    baseline_rows = [r for r in transactions if baseline_start <= dt(r["timestamp"]) < window_start and subject in (r.get("sender_id"), r.get("receiver_id"))]
    extended_rows = [r for r in transactions if extended_start <= dt(r["timestamp"]) < extended_end and subject in (r.get("sender_id"), r.get("receiver_id"))]
    paths = forward_paths(transactions, receiver, at, at + timedelta(days=cfg["baseline_days"]), cfg["max_forward_hops"])
    daily = defaultdict(float)
    for r in baseline_rows: daily[dt(r["timestamp"]).date().isoformat()] += amount(r)
    base = summarize(baseline_rows, subject)
    base.update({"coverage_days": cfg["baseline_days"], "daily_median_value": median(daily.values()) if daily else None})
    categories = defaultdict(list)
    for r in extended_rows: categories[r.get("category", "not recorded")].append(r)
    ext = {k: {"precedent_count": len(v), "max_value": max(map(amount, v)), "most_recent_date": max(dt(r["timestamp"]).date().isoformat() for r in v)} for k,v in categories.items()}
    return {"schema_version": cfg["schema_version"], "anchor_transaction": anchor,
            "current": summarize(current_rows, subject), "baseline": base, "forward_paths": paths,
            "chain_dissipation": {"longest_chain_value_retention": None},
            "endpoint_network": {"status": "not recorded by this reference input"},
            "receiver_network": {"status": "not recorded by this reference input"},
            "extended_baseline": {"window_days_available": cfg["extended_baseline_end_days"], "per_category": ext},
            "ordinary_explanations": {"recurring_timing": [], "category_established": False,
                "counterparty_continuity": None, "payroll_like": None, "precedent_strength": "not recorded"},
            "post_credit_stasis": {"status": "not recorded by this reference input"},
            "baseline_sufficiency": "adequate" if len(baseline_rows) >= 20 else "thin"}
