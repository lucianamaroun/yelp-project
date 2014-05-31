"""A module for reading the data from the json files."""

import json
import pickle

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

def get_dict(data, id_string):
  result = {}
  for item in data:
    key = item[id_string]
    result[key] = item
  return result



