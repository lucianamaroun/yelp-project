""" Unit testing for the collaborative filtering module. """

import unittest
import numpy

import collaborative_filtering as cf


class SimpleTestCase(unittest.TestCase):

  def setUp(self):
    self.ratings = numpy.matrix('1 5;5 1')
    self.attributes = numpy.matrix('1 0; 0 1')
    self.bigtheta = numpy.matrix('1 1;0 4;4 0')

  def test_perfect_prediction(self):
    self.assertEqual(cf.get_optimization_function(self.ratings, 
        self.attributes)(self.bigtheta), 34.0)

  def test_imperfect_prediction(self):
    bigtheta = self.bigtheta.copy()
    bigtheta[1,0] = 1
    self.assertEqual(cf.get_optimization_function(self.ratings, 
        self.attributes)(bigtheta), 36.0)
  
  def test_missing_value(self):
    ratings = self.ratings.copy()
    ratings[0,0] = 0
    self.assertEqual(cf.get_optimization_function(ratings, 
        self.attributes)(self.bigtheta), 34.0)

if __name__ == '__main__':
  unittest.main()
