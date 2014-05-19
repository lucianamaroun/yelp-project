"""Create a small dataset for test purposes."""

import heapq
import pickle

import read_json_data as data

def filter_by_category(businesses, category='Restaurants'):
  filtered = []
  for buss in businesses:
    categories = buss['categories']
    if category in categories:
      filtered.append(buss)
  return filtered


def get_top_k_businesses(businesses, k=10, attribute='review_count'):
  id_to_attribute = {b['business_id']: b[attribute] for b in businesses}
  return heapq.nlargest(k, id_to_attribute, key=lambda k: id_to_attribute[k])


def get_relevant_user_ids(reviews, buss_ids, threshold=5):
  # Get users with at least `threshold` reviews in those restaurants
  review_count = {}
  for r in reviews:
    user = r['user_id']
    business = r['business_id']
    if business not in buss_ids:
      continue
    if user in review_count:
      review_count[user] += 1
    else:
      review_count[user] = 1
  return [user for (user, count) in review_count.iteritems() if count >
      threshold]


def dump_reduced_users(users, relevant_ids):
  selected = [u for u in users if u['user_id'] in relevant_ids]
  output = open('reduced_data/user.pickle', 'w')
  pickle.dump(selected, output)


def dump_reduced_businesses(businesses, relevant_ids):
  selected = [b for b in businesses if b['business_id'] in relevant_ids]
  output = open('reduced_data/business.pickle', 'w')
  pickle.dump(selected, output)


def dump_reduced_reviews(reviews, user_ids, business_ids):
  selected = [r for r in reviews if (r['business_id'] in business_ids and r['user_id'] in user_ids)]
  output = open('reduced_data/review.pickle', 'w')
  pickle.dump(selected, output)


def main():
  """Main function."""
  businesses = data.read_businesses()
  filtered_buss = filter_by_category(businesses)
  most_reviewed = get_top_k_businesses(filtered_buss)
  reviews = data.read_reviews()
  relevant_user_ids = get_relevant_user_ids(reviews, most_reviewed)
  users = data.read_users()

  dump_reduced_users(users, relevant_user_ids)
  dump_reduced_businesses(businesses, most_reviewed)
  dump_reduced_reviews(reviews, relevant_user_ids, most_reviewed)
   

if __name__ == '__main__':
  main()
