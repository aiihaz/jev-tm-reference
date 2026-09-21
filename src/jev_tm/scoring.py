def combine(scores, packet, config):
    path_count = len(packet.get("forward_paths", []))
    eligible, excluded = {}, {}
    for qid, rule in config["questions"].items():
        if not rule["count"]:
            excluded[qid] = "diagnostic only"
        elif path_count < rule["minimum_forward_paths"]:
            excluded[qid] = f"needs >= {rule['minimum_forward_paths']} forward paths"
        elif qid not in scores:
            excluded[qid] = "answer not recorded"
        else:
            value = float(scores[qid])
            if not 0 <= value <= 1: raise ValueError(f"{qid} is outside [0,1]")
            eligible[qid] = value
    if not eligible: raise ValueError("no eligible recorded score")
    final = max(eligible.values()) if config["method"] == "max" else None
    return {"eligible_scores": eligible, "excluded": excluded, "final_score": final,
            "threshold": config["operating_threshold"], "flagged": final >= config["operating_threshold"]}
