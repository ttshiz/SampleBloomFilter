# @Author Tesia Shizume

import unittest
from bloom import *

class TestBloomFilter(unittest.TestCase):
    def setUp(self):
        self.fsize = 2**20
        self.k = 5
        self.bf = BloomFilter(self.fsize, self.k, hashfunc=hash, verbose=False)
        self.new_string = "xdxdx"
        self.new_string_loc = self.bf.bhash(self.new_string)%self.bf.fsize
        # if using larger dataset consider moving this IO to a single call for all tests
        with open("words.txt") as fp: 
            self.words = [i.strip() for i in fp]

    def test_init(self):
        self.assertEqual(self.bf.filter.count(1), 0)
        self.assertEqual(self.bf.filter.count(0), self.bf.fsize)

    def test_enter_datum(self):
        self.assertEqual(self.bf.filter[self.new_string_loc], 0)
        self.bf.enter_datum(self.new_string)
        self.assertEqual(self.bf.filter[self.new_string_loc], 1)
        
        onesafter = self.bf.filter.count(1)
        zerosafter = self.bf.filter.count(0)
        self.assertLessEqual(onesafter, self.k)
        self.assertGreaterEqual(zerosafter, self.fsize-self.k)
        
    def test_populate_filter(self):
        onesbefore = self.bf.filter.count(1)
        zerosbefore = self.bf.filter.count(0)

        self.bf.populate_filter(self.words)
        onesafter = self.bf.filter.count(1)
        zerosafter = self.bf.filter.count(0)
        self.assertLess(onesbefore, onesafter)
        self.assertLess(zerosafter, zerosbefore)
        
    def test_is_new_data(self):
        string_from_data = "arctic"        
        self.assertTrue(self.bf.is_new_data(string_from_data))
        self.assertTrue(self.bf.is_new_data(self.new_string))

        self.bf.populate_filter(self.words)
        self.assertFalse(self.bf.is_new_data(string_from_data))
       
    def test_filter(self):
        self.bf.populate_filter(self.words)
        for w in self.words:
            self.assertFalse(self.bf.is_new_data(w))
            
    def test_prob_fp(self):
        self.assertAlmostEqual(self.bf.prob_fp(2**17), 0.0217, places=4)
        self.assertAlmostEqual(self.bf.prob_fp(2**16), 0.00139, places=5)
        self.assertAlmostEqual(self.bf.prob_fp(2**15), 6.33e-05, places=7)

        probbf = BloomFilter(32, 1)
        self.assertAlmostEqual(probbf.prob_fp(1), 0.0308, places=4)
        self.assertAlmostEqual(probbf.prob_fp(2), 0.0606, places=4)
        self.assertAlmostEqual(probbf.prob_fp(4), 0.118, places=3)
        self.assertAlmostEqual(probbf.prob_fp(8), 0.221, places=3)
        self.assertAlmostEqual(probbf.prob_fp(16), 0.393, places=3)
     

        
        
if __name__ == '__main__':
    unittest.main()
