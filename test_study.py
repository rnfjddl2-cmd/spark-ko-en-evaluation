import unittest
from fractions import Fraction
from study import cases, extract

class StudyTests(unittest.TestCase):
    def test_all_hand_checked_answers(self):
        expected=[29150,38780,73990,58170,86800,74100,10500,10600,26,22,130,123]
        data=cases()
        self.assertEqual(len(data),24)
        self.assertEqual([Fraction(x['expected']) for x in data[::2]],list(map(Fraction,expected)))
        for en,ko in zip(data[::2],data[1::2]):
            self.assertEqual(en['pair'],ko['pair']); self.assertEqual(en['expected'],ko['expected'])
    def test_exact_equivalence(self):
        self.assertEqual(extract('Work\nFINAL: 3/2'),Fraction('1.5'))
        self.assertEqual(extract('FINAL: -0.5'),Fraction('-1/2'))
    def test_no_last_number_fallback(self):
        self.assertIsNone(extract('The answer is 26.'))
    def test_reject_conflicting_markers(self):
        self.assertIsNone(extract('FINAL: 12\nFINAL: 26'))
    def test_reject_unfinished_or_ambiguous(self):
        for text in ['FINAL: 1/0','FINAL: 3/','FINAL: 26 won','FINAL: 26\nActually 12','FINAL: NaN','FINAL: 1,000']:
            self.assertIsNone(extract(text))

if __name__=='__main__': unittest.main()
