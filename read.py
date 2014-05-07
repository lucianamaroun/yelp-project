""" Reading json into variables. """

import json


def get_reviews():
  reviews_str = open('data/yelp_academic_dataset_review.json', 'r').read()
  reviews = json.loads(reviews_str)
  return reviews


def get_users():
  users_str = open('data/yelp_academic_dataset_user.json', 'r').read()
  users = json.loads(users_str)
  return users

