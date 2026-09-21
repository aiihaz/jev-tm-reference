import argparse, json
from pathlib import Path
from .api import call_jev, request_body
from .config import ROOT, load_json, load_questions
from .scoring import combine

def main():
    p=argparse.ArgumentParser(prog="jev-tm", description="Run the public reference harness")
    p.add_argument("packet", type=Path); p.add_argument("--scores", type=Path); p.add_argument("--call", action="store_true")
    p.add_argument("--questions", default=ROOT/"config/questions.csv"); p.add_argument("--combiner", default=ROOT/"config/combiner.json")
    a=p.parse_args(); packet=json.loads(a.packet.read_text()); questions=load_questions(a.questions)
    if a.call:
        print(json.dumps(call_jev(request_body(packet, questions)), indent=2)); return
    if not a.scores: p.error("use --scores for an offline combine, or --call")
    print(json.dumps(combine(json.loads(a.scores.read_text()), packet, load_json(a.combiner)), indent=2))
if __name__ == "__main__": main()
