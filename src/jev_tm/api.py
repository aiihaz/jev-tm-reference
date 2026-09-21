import json, os, urllib.request

def request_body(packet, questions, model="jev-1.13.0"):
    return {"model": model, "state": json.dumps(packet, separators=(",", ":")),
            "questions": {q["question_id"]: {"answer_type": q["answer_type"], "question": q["question_text_verbatim"]} for q in questions}}

def call_jev(body, api_key=None, endpoint="https://api.typesafe.ai/v1/systemone"):
    key = api_key or os.environ.get("TYPESAFE_API_KEY")
    if not key: raise RuntimeError("Set TYPESAFE_API_KEY. Never commit it.")
    req = urllib.request.Request(endpoint, data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as response:
        return json.load(response)
