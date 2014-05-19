"""A module to perform the collaborative filtering."""

import numpy

def get_optimization_function(ratings, attributes):
  """ Get the function for optimization of the content based recommendation.

  Observations:
    - The returned function expects a matrix big theta, which contains a vector
      theta in each column representing a user profile.

  Args:
    ratings: the numpy.matrix with user ratings, in which restaurants are
      enconded in lines and users, in columns.
    attributes: the numpy.matrix with restaurants attributes, in which
      restaurants are encoded in lines and attributes, in columns.

  Returns:
    A functions that evaluates the optimization function.
  """
  attributes = numpy.column_stack((numpy.ones(attributes.shape[0]), attributes))
  def opt_function(big_theta):
    value = 0
    for i in range(ratings.shape[0]): # restaurant
      for j in range(ratings.shape[1]): # user
        if not ratings[i,j]:
          continue
        value += ((attributes[i] * big_theta[:,j])[0,0] - ratings[i,j]) ** 2
    for j in range(ratings.shape[1]):
      value += sum([(theta ** 2)[0,0] for theta in big_theta[:,j]])
    return value
  return opt_function
