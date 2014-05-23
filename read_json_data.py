"""A module for reading the data from the json files."""

import json
import pickle
import os

USER_JSON = 'data/yelp_academic_dataset_user.json'
USER_PKL = 'user_graph.pkl'


def read_reviews():
  """Load reviews from json file."""
  reviews_str = open('data/yelp_academic_dataset_review.json', 'r').read()
  reviews = json.loads(reviews_str)
  return reviews


def read_businesses():
  """Load business from json file."""
  businesses_str = open('data/yelp_academic_dataset_business.json', 'r').read()
  businesses = json.loads(businesses_str)
  return businesses  


def read_users():
  """Load users from json file."""
  users_str = open('data/yelp_academic_dataset_user.json', 'r').read()
  users = json.loads(users_str)
  return users

def read_reviews_reduced():
  """Load reduced set of reviews from json file."""
  input_file = open('reduced_data/review.pickle', 'r')
  return pickle.load(input_file)


def read_businesses_reduced():
  """Load reduced set of businesses from json file."""
  input_file = open('reduced_data/business.pickle', 'r')
  return pickle.load(input_file)


def read_users_reduced():
  """Load reduced set of users from json file."""
  input_file = open('reduced_data/user.pickle', 'r')
  return pickle.load(input_file)

def read_graph():
  """ Reads the users friendship graph from the users' json file.

  Observations:
    - The users json file is a static parameter of the algorithm, defined in the
      top of this file.
    - The nodes' id are interpreted as strings.

  Args:
    None.

  Returns:
    A networkx.Graph() object.
  """
  user_str = open(USER_JSON, 'r').read()
  users = json.loads(user_str)

  if os.path.exists(USER_PKL):
    pkl_file = open(USER_PKL, 'r')
    graph = pickle.load(pkl_file)
    pkl_file.close()
  else:
    graph = nx.Graph()
    for user in users:
      graph.add_node(user['user_id'])
      for friend in user['friends']:
        graph.add_edge(user['user_id'], friend)
    pkl_file = open(USER_PKL, 'w')
    pickle.dump(graph, pkl_file)
    pkl_file.close()

  return graph


