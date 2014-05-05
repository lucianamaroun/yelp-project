from matplotlib import pyplot
from numpy import arange

import json
import numpy

def scatterplot(x, y):
    pyplot.plot(x, y, 'b.')
    pyplot.xlim(min(x)-1, max(x)+1)
    pyplot.ylim(min(y)-1, max(y)+1)
    pyplot.show()

def barplot(labels, data):
    pos = arange(len(data))
    pyplot.xticks(pos+1.4, labels)
    pyplot.bar(pos, data)
    pyplot.show()


# Number of reviews
users_str = open('data/yelp_academic_dataset_user.json', 'r').read()
users_list = json.loads(users_str)
print len(users_list)
print users_list[0]

users = {}

for user in users_list:
    users[user['user_id']] = user

avg_stars = []
votes = []

for user in users_list:
    if user['review_count'] > 0:
        votes.append(user['votes']['useful'])
        avg_stars.append(user['average_stars'])

scatterplot(avg_stars, votes)





