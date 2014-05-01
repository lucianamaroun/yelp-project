""" Script which selects a fraction of reviewers for training. """

import json
import random


_TRAINING_SIZE = 200


def users_sample():
  users_str = open('data/yelp_academic_dataset_user.json', 'r').read()
  users = json.loads(users_str)
  selected_users = random.sample(users, _TRAINING_SIZE)
  return selected_users


def dump_selected_users(selected_users):
  selected_users_str = ',\n'.join([json.dumps(selected_user) for selected_user
    in selected_users])
  open('selected/users.json', 'w').write(selected_users_str)


def get_reviews():
  reviews_str = open('data/yelp_academic_dataset_review.json', 'r').read()
  reviews = json.loads(reviews_str)
  return reviews


def get_user_reviews(user, reviews):
  return [review for review in reviews if review['user_id'] ==
      user['user_id']]


def dump_selected_reviews(user, reviews):
  selected_reviews_str = ',\n'.join([json.dumps(review) for review in reviews])
  open('selected/reviews-' + user['user_id'] + '.json', 'w') \
      .write(selected_reviews_str)


if __name__ == '__main__':
  selected_users = users_sample()
  dump_selected_users(selected_users)
  reviews = get_reviews()
  for user in selected_users:
    dump_selected_reviews(user, get_user_reviews(user, reviews))
