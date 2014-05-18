"""A module for reading the data from the json files."""

import json

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

