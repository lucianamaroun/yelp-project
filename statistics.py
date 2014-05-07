""" Script with basic statistics of the dataset """

import json

# Number of businesses
old_busin_str = open('old_data/yelp_academic_dataset_business.json', 'r').read()
old_busin = json.loads(old_busin_str)
print '# old business: %d' % len(old_busin)

new_busin_str = open('data/yelp_academic_dataset_business.json', 'r').read()
new_busin = json.loads(new_busin_str)
print '# new business: %d' % len(new_busin)

old_busin_ids = set([busin['business_id'] for busin in old_busin])
new_busin_ids = set([busin['business_id'] for busin in new_busin])

only_old_busin = old_busin_ids.difference(new_busin_ids)
print '# only old business: %d' % len(only_old_busin)

only_new_busin = new_busin_ids.difference(old_busin_ids)
print '# only new business: %d' % len(only_new_busin)

# Number of cities
old_cities = set([busin['city'].title().strip() for busin in old_busin])
print '# old cities: %d ' % len(old_cities)
print old_cities

new_cities = set([busin['city'].title().strip() for busin in new_busin])
print '# new cities: %d ' % len(new_cities)
print new_cities

city_file = open('city.sql', 'w')
print >> city_file, 'create table city (name varchar);'
for city in new_cities:
  print >> city_file, 'insert into city values (\'%s\');' % city

intersection = new_cities.intersection(old_cities)
print 'intersection: ' + str(intersection)

only_old_cities = old_cities.difference(new_cities)
print 'only old: ' + str(only_old_cities)

only_new_cities = new_cities.difference(old_cities)
print 'only new: ' + str(only_new_cities)

# Number of users
old_user_str = open('old_data/yelp_academic_dataset_user.json', 'r').read()
old_user = json.loads(old_user_str)
print '# old users: %d' % len(old_user)

new_user_str = open('data/yelp_academic_dataset_user.json', 'r').read()
new_user = json.loads(new_user_str)
print '# new users: %d' % len(new_user)

old_user_ids = set([user['user_id'] for user in old_user])
new_user_ids = set([user['user_id'] for user in new_user])

only_old_user = old_user_ids.difference(new_user_ids)
print '# only old user: %d' % len(only_old_user)

only_new_user = new_user_ids.difference(old_user_ids)
print '# only new user: %d' % len(only_new_user)

