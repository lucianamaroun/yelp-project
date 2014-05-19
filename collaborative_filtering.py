"""A module to perform the collaborative filtering."""

import numpy as np
import read_json_data as data
import scipy.optimize as opt


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
  attributes = np.column_stack((np.ones(attributes.shape[0]), attributes))
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

def create_index_dict(my_list, id_string):
  return {x[id_string]:ind for ind, x in enumerate(my_list)}


def create_rating_matrix(reviews, users_dict, buss_dict):
  matrix = np.matrix(np.zeros((len(buss_dict), len(users_dict))))
  for r in reviews:
    user_id = r['user_id']
    buss_id = r['business_id']
    user_index = users_dict[user_id]
    buss_index = buss_dict[buss_id]
    matrix[buss_index, user_index] = r['stars']
  return matrix

def create_attrs_matrix(businesses, buss_dict):
  matrix = np.matrix(np.zeros((len(businesses), 4)))
  for b in businesses:
    b_index = buss_dict[b['business_id']]
    matrix[b_index, 0] = b['attributes']['Price Range']
    matrix[b_index, 1] = b['attributes']['Good For']['lunch']
    matrix[b_index, 2] = b['attributes']['Good For']['dinner']
    matrix[b_index, 3] = b['attributes']['Good For']['latenight']
  return matrix
 

def main():
  users = data.read_users_reduced()
  businesses = data.read_businesses_reduced()
  reviews = data.read_reviews_reduced()

  users_dict = create_index_dict(users, 'user_id')
  buss_dict = create_index_dict(businesses, 'business_id')

  rating_matrix = create_rating_matrix(reviews, users_dict, buss_dict)
  attrs_matrix = create_attrs_matrix(businesses, buss_dict)

  opt_function = get_optimization_function(rating_matrix, attrs_matrix)

  initial_guess = np.ndarray(shape=(5, len(users)), buffer=np.zeros(5*len(users)))
  initial_guess[0] = 1
  #print initial_guess

  opt.minimize(opt_function, initial_guess)



if __name__ == '__main__':
  main()
