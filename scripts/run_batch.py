#!/usr/bin/env python3
import argparse, json, time
from pathlib import Path
from jev_tm.api import call_jev, request_body
from jev_tm.config import load_questions
p=argparse.ArgumentParser(); p.add_argument('packets',type=Path); p.add_argument('output',type=Path); p.add_argument('--batch-size',type=int,default=100); a=p.parse_args()
qs=load_questions(); done=set()
if a.output.exists():
 for line in a.output.read_text().splitlines():
  try: done.add(json.loads(line)['case_id'])
  except Exception: pass
rows=[json.loads(x) for x in a.packets.read_text().splitlines() if x.strip()]
a.output.parent.mkdir(parents=True,exist_ok=True)
with a.output.open('a') as out:
 for packet in [x for x in rows if x['case_id'] not in done][:a.batch_size]:
  response=call_jev(request_body(packet,qs)); out.write(json.dumps({'case_id':packet['case_id'],'response':response})+'\n'); out.flush(); time.sleep(.25)
