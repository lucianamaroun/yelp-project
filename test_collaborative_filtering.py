""" Unit testing for the collaborative filtering module. """

import unittest
import numpy as np
import scipy as sp

import collaborative_filtering as cf

class VerySimpleTestCase(unittest.TestCase):

  def setUp(self):
    self.ratings = np.matrix('5 1;1 5')
    self.n_user = 2
    self.n_rest = 2
    self.n_attrs = 2
    self.big_vector = np.array([5., 1., 1., 5., 1., 0., 0., 1.])

  def test_opt_perfect_prediction(self):
    self.assertAlmostEqual(cf.get_optimization_function(self.ratings, self.n_attrs)
        (self.big_vector), cf._LAMBDA * sum(self.big_vector ** 2))

  def test_opt_imperfect_prediction(self):
    big_vector = self.big_vector.copy()
    big_vector[0] = 1.
    self.assertAlmostEqual(cf.get_optimization_function(self.ratings, self.n_attrs)
        (big_vector), cf._LAMBDA * sum(big_vector ** 2) + 16)
  
  def test_missing_value(self):
    ratings = self.ratings.copy()
    ratings[0,0] = 0
    big_vector = self.big_vector.copy()
    big_vector[0] = 1.
    self.assertAlmostEqual(cf.get_optimization_function(ratings, 
        self.n_attrs)(big_vector), cf._LAMBDA * sum(big_vector ** 2))

  def test_mean_normalize(self):
    norm_matrix, mean = cf.mean_normalize(self.ratings)
    self.assertEqual(norm_matrix.tolist(), [[2, -2], [-2, 2]])
    self.assertEqual(mean.tolist(), [3, 3])

  def test_optimization(self):
    opt_function = cf.get_optimization_function(self.ratings, self.n_attrs)
    result = sp.optimize.minimize(opt_function, self.big_vector).x
    self.assertTrue(opt_function(result) <= cf._LAMBDA * sum(self.big_vector ** 
        2))

  def test_predict(self):
    norm_matrix, mean = cf.mean_normalize(self.ratings)
    opt_function = cf.get_optimization_function(norm_matrix, self.n_attrs)
    result = sp.optimize.minimize(opt_function, np.ones(self.n_user * 
      self.n_attrs + self.n_rest * self.n_attrs)).x
    big_theta, big_attrs = cf.decode_big_vector(result, self.n_rest, 
        self.n_user, self.n_attrs)
    predict = cf.predict(big_theta, big_attrs, mean)
    for i in range(self.n_rest):
      for j in range(self.n_user):
        self.assertAlmostEqual(predict[i,j], self.ratings[i,j], 1)

if __name__ == '__main__':
  unittest.main()
