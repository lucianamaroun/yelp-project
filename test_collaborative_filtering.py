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


class SimpleTestCase(unittest.TestCase):

  def setUp(self):
    self.ratings = np.matrix((
      '5 5 5 3 0 2 1 0 0 0;'
      '0 4 5 2 3 3 0 0 1 1;'
      '5 5 5 0 3 3 1 1 0 0;'
      '0 0 1 0 0 0 3 5 5 5;'
      '0 1 1 0 3 0 0 5 5 4;'
      '1 0 0 3 0 1 2 5 0 5'))
    self.initial_guess = np.array(
      # users
      [5., 0., 5., 0., 5., 0., # first attribute positive
       3., 3., 3., 3., 3., 1., 1., 3., # mid-term
       0., 5., 0., 5., 0., 5., # second attribute positive
      # restaurants
       1., 0., 1., 0., 1., 0., # one attribute positive
       0., 1., 0., 1., 0., 1.]) # second attribute positive
    self.n_user = 10
    self.n_rest = 6
    self.n_attrs = 2

  def test_mean_normalize(self):
    norm_matrix, mean = cf.mean_normalize(self.ratings)
    self.maxDiff = None
    true_matrix = [[1.5, 1.5, 1.5, -0.5, 0.0, -1.5, -2.5, 0.0, 0.0, 0.0],
         [0.0, 1.28571429, 2.28571429, -0.71428571, 0.28571429, 0.28571429, 0.0, 0.0,
          -1.71428571, -1.71428571],
         [1.71428571, 1.71428571, 1.71428571, 0.0, -0.28571428, -0.28571428,
          -2.28571428, -2.28571428, 0.0, 0.0],
         [0.0, 0.0, -2.8, 0.0, 0.0, 0.0, -0.8, 1.2, 1.2, 1.2],
         [0.0, -2.16666667, -2.16666667, 0.0, -0.16666667, 0.0, 0.0, 1.83333333,
           1.83333333, 0.83333333],
         [-1.83333333, 0.0, 0.0, 0.16666667, 0.0, -1.83333333, -0.83333333,
           2.16666667, 0.0, 2.166666667]]
    for i in range(self.n_rest):
      for j in range(self.n_user):
        self.assertAlmostEqual(norm_matrix[i,j], true_matrix[i][j])
    
    true_mean = [3.5, 2.71428571, 3.28571428, 3.8, 3.16666667, 2.83333333]
    for i in range(self.n_rest):
      self.assertAlmostEqual(mean[i], true_mean[i])

  def test_optimization(self):
    opt_function = cf.get_optimization_function(self.ratings, self.n_attrs)
    result = sp.optimize.minimize(opt_function, self.initial_guess).x
    self.assertTrue(opt_function(result) <= opt_function(self.initial_guess))

  def test_predict(self):
    norm_matrix, mean = cf.mean_normalize(self.ratings)
    opt_function = cf.get_optimization_function(norm_matrix, self.n_attrs)
    result = sp.optimize.minimize(opt_function, self.initial_guess).x
    big_theta, big_attrs = cf.decode_big_vector(result, self.n_rest, 
        self.n_user, self.n_attrs)
    predict = cf.predict(big_theta, big_attrs, mean)
    print predict
    for i in range(self.n_rest):
      for j in range(self.n_user):
        if norm_matrix[i,j]:
          self.assertAlmostEqual(predict[i,j], self.ratings[i,j], 0)

if __name__ == '__main__':
  unittest.main()
