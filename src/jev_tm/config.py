import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load_json(path):
    return json.loads(Path(path).read_text())

def load_questions(path=ROOT / "config/questions.csv"):
    with Path(path).open(newline="") as f:
        rows = list(csv.DictReader(f))
    required = {"question_id", "answer_type", "question_text_verbatim"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("question config is missing required columns")
    return rows
