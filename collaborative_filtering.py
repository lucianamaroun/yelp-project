""" A module to perform the collaborative filtering. """

import numpy as np
import read_json_data as data
import scipy.optimize as opt

_LAMBDA = 0.01 # what value to use?


def get_optimization_function(ratings, n_attrs):
  """ Provides the function for optimization in collaborative filtering.

  Observations:
    - The returned function expects two matrices: big theta, which contains a 
      vector theta transposed in each row representing a user profile; and X,
      which contains a vector x transposed in each row representing the
      restaurants attributes.
    - Only one vector of variables is received by the function, being the first
      n(u)*n_attrs corresponding to big_theta and the last n(r)*n_attrs
      correspoding to X (big_attrs), where n(u) is the number of users and n(r),
      of restaurants.

  Args:
    ratings: the numpy.matrix with user ratings, in which restaurants are
      encoded in lines and users, in columns.
    n_attrs: the number of attributes to fit.

  Returns:
    A function that evaluates the optimization function.
  """
  def opt_function(big_vector):
    n_rest = ratings.shape[0]
    n_user = ratings.shape[1]
    big_theta, big_attrs = decode_big_vector(big_vector, n_rest, n_user, 
        n_attrs) 
    evaluation = 0
    for rest in range(n_rest):
      for user in range(n_user):
        if not ratings[rest,user]:
          continue
        evaluation += ((big_theta[user,:] * big_attrs[rest,:].T)[0,0] -
            ratings[rest,user]) ** 2
    for user in range(n_user):
      evaluation += _LAMBDA * sum([(theta ** 2) for theta in
          big_theta[user,:].tolist()[0]])
    for rest in range(n_rest):
      evaluation += _LAMBDA * sum([(attr ** 2) for attr in
          big_attrs[rest,:].tolist()[0]])
    return evaluation
  return opt_function


def create_index_dict(my_list, id_string):
  return {x[id_string]:ind for ind, x in enumerate(my_list)}


def create_rating_matrix(reviews, users_dict, buss_dict):
  matrix = np.matrix(np.zeros((len(buss_dict), len(users_dict))))
  for r in reviews:
    user_id = r['user_id']
    buss_id = r['business_id']
    if user_id not in users_dict:
      continue
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
  return matrix


def simple_example():
  """ Small example matrix with very well defined users for each of two
      attributes, as well as mid-term users. """
  n_attrs = 2
  rating_matrix = np.matrix((
      '5 5 5 3 0 2 1 0 0 0;'
      '0 4 5 2 3 3 0 0 1 1;'
      '5 5 5 0 3 3 1 1 0 0;'
      '0 0 1 0 0 0 3 5 5 5;'
      '0 1 1 0 3 0 0 5 5 4;'
      '1 0 0 3 0 1 2 5 0 5'))
  initial_guess = np.array(
      # users
      [5., 0., 5., 0., 5., 0.,
       3., 2., 3., 2., 3., 2., 3., 2.,
       0., 5., 0., 5., 0., 5.,
      # restaurants
       1., 0., 1., 0., 1., 0.,
       0., 1., 0., 1., 0., 1.])
  return rating_matrix, initial_guess, n_attrs


def sample_example():
  """ Sample from Yelp's dataset with 10 most popular restaurants, 77 most
      interactive users for those and 2 attributes. """
  users = data.read_users_reduced()
  businesses = data.read_businesses_reduced()
  reviews = data.read_reviews_reduced()
  n_attrs = 2

  users_dict = create_index_dict(users, 'user_id')
  buss_dict = create_index_dict(businesses, 'business_id')

  rating_matrix = create_rating_matrix(reviews, users_dict, buss_dict)
  #attrs_matrix = create_attrs_matrix(businesses, buss_dict)
  initial_guess = np.ones(len(users) * n_attrs + len(businesses) * n_attrs)
  return rating_matrix, initial_guess, n_attrs


def complete_data():
  users = data.read_users()
  businesses = data.read_businesses()
  reviews = data.read_reviews()
  n_attrs = 2

  users_dict = create_index_dict(users, 'user_id')
  buss_dict = create_index_dict(businesses, 'business_id')

  rating_matrix = create_rating_matrix(reviews, users_dict, buss_dict)
  #attrs_matrix = create_attrs_matrix(businesses, buss_dict)
  print len(businesses)
  initial_guess = np.ones(len(users) * n_attrs + len(businesses) * n_attrs)
  return rating_matrix, initial_guess, n_attrs


def mean_normalize(matrix):
  """ Normalizes the matrix by row averages """
  n_row = matrix.shape[0]
  n_col = matrix.shape[1]
  mean = np.array(np.zeros(n_row))
  norm_matrix = np.matrix([[0.] * n_col for row in range(n_row)])
  for i in range(n_row):
    grades = [g for g in matrix[i,:].tolist()[0] if g]
    mean[i] = float(sum(grades)) / len(grades) if grades else 0.
    for j in range(n_col):
      if matrix[i, j]:
        norm_matrix[i,j] = matrix[i,j] - mean[i]
  return norm_matrix, mean


def predict(big_theta, big_attrs, mean_vector):
  # are the bounds supposed to be respected?
  nrow = big_theta.shape[0]
  mean_matrix = np.matrix([mean_vector] * nrow).T
  return big_attrs * big_theta.T + mean_matrix


def decode_big_vector(big_vector, n_rest, n_user, n_attrs):
  """ Decodes the linear vector of variables theta and x (attributes) into two
      matrices big theta and big attrs.

  Observations:
    - Both matrices have a individual transpose vector in each row.
  """
  big_theta = np.asmatrix(big_vector[:n_user*n_attrs]).reshape(n_user, n_attrs)
  big_attrs = np.asmatrix(big_vector[n_user*n_attrs:]).reshape(n_rest, n_attrs)
  return big_theta, big_attrs


def main():
  rating_matrix, initial_guess, n_attrs = complete_data() 
  n_rest = rating_matrix.shape[0]
  n_user = rating_matrix.shape[1]
  norm_rating_matrix, mean_vector = mean_normalize(rating_matrix)
  opt_function = get_optimization_function(norm_rating_matrix, n_attrs)
  final_guess = opt.minimize(opt_function, initial_guess) 
  print final_guess
  big_theta, big_attrs = decode_big_vector(final_guess.x, n_rest, n_user,
    n_attrs)

  out_pred = open('pred_ratings.txt', 'w')
  print >> out_pred, predict(big_theta, big_attrs, mean_vector)
  out_pred.close()

  out_theta = open('theta.txt', 'w')
  for i in range(n_user):
    point_str = ''
    for j in range(n_attrs):
      point_str += str(big_theta[i,j]) + ','
    print >> out_theta, point_str[:-1]
  out_theta.close()

  out_attrs = open('attrs.txt', 'w')
  for i in range(n_rest):
    point_str = ''
    for j in range(n_attrs):
      point_str += str(big_attrs[i,j]) + ','
    print >> out_attrs, point_str[:-1]
  out_attrs.close()

if __name__ == '__main__':
  main()
