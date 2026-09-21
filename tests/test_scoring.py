import json, unittest
from pathlib import Path
from jev_tm.scoring import combine
class TestCombiner(unittest.TestCase):
 def setUp(self): self.c=json.loads(Path('config/combiner.json').read_text())
 def test_zero_path_case(self):
  r=combine({'Q1_pass_through':.99,'Q2_coordination':.98,'Q4_velocity_shift':.70,'QI_integration':1}, {'forward_paths':[]}, self.c)
  self.assertEqual(r['eligible_scores'], {'Q4_velocity_shift':.70}); self.assertTrue(r['flagged'])
 def test_two_paths_max(self):
  r=combine({'Q1_pass_through':.2,'Q2_coordination':.8,'Q4_velocity_shift':.4}, {'forward_paths':[1,2]}, self.c)
  self.assertEqual(r['final_score'], .8)
if __name__=='__main__': unittest.main()
