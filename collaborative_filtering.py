""" A module to perform the collaborative filtering. """

import numpy as np
import read_json_data as data
import scipy.optimize as opt

_LAMBDA = 1 # which value to use?

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
    big_theta = np.asmatrix(big_vector[:n_user*n_attrs].reshape(n_user,
        n_attrs))
    big_attrs = np.asmatrix(big_vector[n_user*n_attrs:].reshape(n_rest,
        n_attrs))
    evaluation = 0
    for rest in range(n_rest):
      for user in range(n_user):
        if not ratings[rest,user]:
          continue
        rating = ratings[rest,user]
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
  return rating_matrix, initial_guess


def sample_example():
  users = data.read_users_reduced()
  businesses = data.read_businesses_reduced()
  reviews = data.read_reviews_reduced()

  users_dict = create_index_dict(users, 'user_id')
  buss_dict = create_index_dict(businesses, 'business_id')

  rating_matrix = create_rating_matrix(reviews, users_dict, buss_dict)
  #attrs_matrix = create_attrs_matrix(businesses, buss_dict)
  initial_guess = np.zeros(shape=(5, len(users)))
  return rating_matrix, initial_guess


def mean_normalize(matrix):
  """ Normalizes the matrix by row averages """
  n_row = matrix.shape[0]
  n_col = matrix.shape[1]
  mean = np.array(np.zeros(n_row))
  norm_matrix = np.matrix([[0.] * n_col for row in range(n_row)])
  for i in range(n_row):
    grades = [g for g in matrix[i,:].tolist()[0] if g]
    mean[i] = float(sum(grades)) / len(grades)
    for j in range(n_col):
      norm_matrix[i,j] = matrix[i,j] - mean[i]
  return norm_matrix, mean


def predict(big_theta, big_attrs, mean_vector):
  # are the bounds supposed to be respected?
  nrow = big_theta.shape[0]
  mean_matrix = np.matrix([mean_vector] * nrow).T
  print mean_matrix
  return big_attrs * big_theta.T + mean_matrix

# TODO: Tests
# TODO: Refactor main()
def main():
  rating_matrix, initial_guess = simple_example()
  norm_rating_matrix, mean_vector = mean_normalize(rating_matrix)
  opt_function = get_optimization_function(norm_rating_matrix, 2)

  #initial_guess = np.zeros(shape=(5, len(users)))
  #initial_guess = np.ndarray(shape=(5, len(users)), buffer=np.zeros(5*len(users)))
  #initial_guess[0] = 1
  #print initial_guess

  n_rest = rating_matrix.shape[0]
  n_user = rating_matrix.shape[1]
  n_attrs = 2
  final_guess = opt.minimize(opt_function, initial_guess) 
  big_theta = np.asmatrix(final_guess.x[:n_user*n_attrs].reshape(n_user,
      n_attrs))
  big_attrs = np.asmatrix(final_guess.x[n_user*n_attrs:].reshape(n_rest,
      n_attrs))

  print predict(big_theta, big_attrs, mean_vector)

  output = open('theta.txt', 'w')
  for i in range(n_user):
    point_str = ''
    for j in range(n_attrs):
      point_str += str(big_theta[i,j]) + ','
    print >> output, point_str[:-1]


if __name__ == '__main__':
  main()
